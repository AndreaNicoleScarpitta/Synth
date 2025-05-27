import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import time
import os
import trafilatura
from models.literature_data import Paper, LiteratureResult
from utils.vector_store import VectorStore
from utils.ollama_client import OllamaClient

class LiteratureAgent:
    """Agent responsible for retrieving and processing biomedical literature"""
    
    def __init__(self, vector_store: VectorStore, ollama_client: OllamaClient):
        self.vector_store = vector_store
        self.ollama_client = ollama_client
        self.pubmed_base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.biorxiv_base_url = "https://api.biorxiv.org/details/biorxiv/"
        
        # Get API keys from environment
        self.ncbi_api_key = os.getenv("NCBI_API_KEY", "")
        
        # Rate limiting
        self.last_pubmed_request = 0
        self.pubmed_delay = 0.34  # ~3 requests per second for NCBI
        
    def search_literature(self, query: str, max_papers: int = 20, include_preprints: bool = True) -> LiteratureResult:
        """Search literature from multiple sources"""
        papers = []
        
        # Search PubMed
        pubmed_papers = self._search_pubmed(query, max_papers // 2)
        papers.extend(pubmed_papers)
        
        # Search bioRxiv if enabled
        if include_preprints:
            biorxiv_papers = self._search_biorxiv(query, max_papers // 2)
            papers.extend(biorxiv_papers)
        
        # Score relevance and rank papers
        scored_papers = self._score_relevance(papers, query)
        
        # Take top papers up to max_papers
        final_papers = scored_papers[:max_papers]
        
        # Generate summary
        summary = self._generate_literature_summary(final_papers, query)
        
        return LiteratureResult(
            query=query,
            papers=final_papers,
            summary=summary,
            search_timestamp=datetime.now()
        )
    
    def _search_pubmed(self, query: str, max_results: int) -> List[Paper]:
        """Search PubMed using E-utilities API"""
        papers = []
        
        try:
            # Step 1: Search for PMIDs
            pmids = self._search_pubmed_ids(query, max_results)
            
            if not pmids:
                return papers
            
            # Step 2: Fetch paper details
            papers = self._fetch_pubmed_details(pmids)
            
        except Exception as e:
            print(f"Error searching PubMed: {e}")
        
        return papers
    
    def _search_pubmed_ids(self, query: str, max_results: int) -> List[str]:
        """Search PubMed for paper IDs"""
        self._rate_limit_pubmed()
        
        search_url = f"{self.pubmed_base_url}esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "xml",
            "sort": "relevance",
            "datetype": "pdat",
            "reldate": 3650  # Last 10 years
        }
        
        if self.ncbi_api_key:
            params["api_key"] = self.ncbi_api_key
        
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(response.content)
        pmids = [id_elem.text for id_elem in root.findall(".//Id")]
        
        return pmids
    
    def _fetch_pubmed_details(self, pmids: List[str]) -> List[Paper]:
        """Fetch detailed information for PubMed papers"""
        papers = []
        
        if not pmids:
            return papers
        
        self._rate_limit_pubmed()
        
        fetch_url = f"{self.pubmed_base_url}efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml"
        }
        
        if self.ncbi_api_key:
            params["api_key"] = self.ncbi_api_key
        
        response = requests.get(fetch_url, params=params)
        response.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(response.content)
        
        for article in root.findall(".//PubmedArticle"):
            try:
                paper = self._parse_pubmed_article(article)
                if paper:
                    papers.append(paper)
            except Exception as e:
                print(f"Error parsing PubMed article: {e}")
                continue
        
        return papers
    
    def _parse_pubmed_article(self, article_elem) -> Optional[Paper]:
        """Parse a single PubMed article XML element"""
        try:
            # Get PMID
            pmid_elem = article_elem.find(".//PMID")
            pmid = pmid_elem.text if pmid_elem is not None else ""
            
            # Get title
            title_elem = article_elem.find(".//ArticleTitle")
            title = title_elem.text if title_elem is not None else ""
            
            # Get abstract
            abstract_parts = []
            for abstract_elem in article_elem.findall(".//AbstractText"):
                if abstract_elem.text:
                    label = abstract_elem.get("Label", "")
                    text = abstract_elem.text
                    if label:
                        abstract_parts.append(f"{label}: {text}")
                    else:
                        abstract_parts.append(text)
            abstract = " ".join(abstract_parts)
            
            # Get authors
            authors = []
            for author_elem in article_elem.findall(".//Author"):
                last_name = author_elem.find("LastName")
                first_name = author_elem.find("ForeName")
                if last_name is not None and first_name is not None:
                    authors.append(f"{first_name.text} {last_name.text}")
            authors_str = ", ".join(authors)
            
            # Get publication date
            pub_date = None
            date_elem = article_elem.find(".//PubDate")
            if date_elem is not None:
                year_elem = date_elem.find("Year")
                month_elem = date_elem.find("Month")
                day_elem = date_elem.find("Day")
                
                if year_elem is not None:
                    year = int(year_elem.text)
                    month = 1
                    day = 1
                    
                    if month_elem is not None:
                        try:
                            month = int(month_elem.text)
                        except ValueError:
                            # Handle month names
                            month_names = {
                                "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
                                "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
                                "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
                            }
                            month = month_names.get(month_elem.text, 1)
                    
                    if day_elem is not None:
                        try:
                            day = int(day_elem.text)
                        except ValueError:
                            day = 1
                    
                    pub_date = datetime(year, month, day)
            
            # Create URL
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            
            return Paper(
                title=title,
                authors=authors_str,
                abstract=abstract,
                publication_date=pub_date,
                source="pubmed",
                url=url,
                paper_id=pmid
            )
            
        except Exception as e:
            print(f"Error parsing PubMed article: {e}")
            return None
    
    def _search_biorxiv(self, query: str, max_results: int) -> List[Paper]:
        """Search bioRxiv preprints"""
        papers = []
        
        try:
            # bioRxiv API search
            search_url = "https://api.biorxiv.org/details/biorxiv/"
            
            # Get papers from last 2 years
            end_date = datetime.now()
            start_date = end_date - timedelta(days=730)
            
            date_range = f"{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
            full_url = f"{search_url}{date_range}"
            
            response = requests.get(full_url)
            response.raise_for_status()
            
            data = response.json()
            
            if "collection" in data:
                # Filter papers by query relevance
                relevant_papers = []
                query_lower = query.lower()
                
                for paper_data in data["collection"]:
                    title = paper_data.get("title", "").lower()
                    abstract = paper_data.get("abstract", "").lower()
                    
                    # Simple relevance check
                    if any(term in title or term in abstract for term in query_lower.split()):
                        paper = self._parse_biorxiv_paper(paper_data)
                        if paper:
                            relevant_papers.append(paper)
                
                # Sort by date and take most recent
                relevant_papers.sort(key=lambda x: x.publication_date or datetime.min, reverse=True)
                papers = relevant_papers[:max_results]
        
        except Exception as e:
            print(f"Error searching bioRxiv: {e}")
        
        return papers
    
    def _parse_biorxiv_paper(self, paper_data: Dict) -> Optional[Paper]:
        """Parse a bioRxiv paper from API response"""
        try:
            title = paper_data.get("title", "")
            authors = paper_data.get("authors", "")
            abstract = paper_data.get("abstract", "")
            
            # Parse date
            pub_date = None
            date_str = paper_data.get("date")
            if date_str:
                try:
                    pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    pass
            
            # Create URL
            doi = paper_data.get("doi", "")
            url = f"https://www.biorxiv.org/content/{doi}v1" if doi else ""
            
            return Paper(
                title=title,
                authors=authors,
                abstract=abstract,
                publication_date=pub_date,
                source="biorxiv",
                url=url,
                paper_id=doi
            )
            
        except Exception as e:
            print(f"Error parsing bioRxiv paper: {e}")
            return None
    
    def _score_relevance(self, papers: List[Paper], query: str) -> List[Paper]:
        """Score papers by relevance to query and sort"""
        query_terms = query.lower().split()
        
        for paper in papers:
            score = 0
            text_to_search = f"{paper.title} {paper.abstract}".lower()
            
            # Simple term matching
            for term in query_terms:
                if term in text_to_search:
                    score += 1
            
            # Boost recent papers
            if paper.publication_date:
                years_old = (datetime.now() - paper.publication_date).days / 365
                if years_old < 2:
                    score += 2
                elif years_old < 5:
                    score += 1
            
            paper.relevance_score = score / len(query_terms) if query_terms else 0
        
        # Sort by relevance score
        return sorted(papers, key=lambda x: x.relevance_score, reverse=True)
    
    def _generate_literature_summary(self, papers: List[Paper], query: str) -> str:
        """Generate a summary of literature findings using LLM"""
        if not papers:
            return "No relevant literature found for the given query."
        
        # Prepare prompt
        papers_text = ""
        for i, paper in enumerate(papers[:10], 1):  # Limit to top 10 for summary
            papers_text += f"{i}. {paper.title}\n"
            papers_text += f"   Authors: {paper.authors}\n"
            papers_text += f"   Abstract: {paper.abstract[:500]}...\n\n"
        
        prompt = f"""
        Based on the following research papers related to the query "{query}", provide a comprehensive literature summary:

        {papers_text}

        Please provide:
        1. Key findings and patterns across studies
        2. Main methodologies used
        3. Patient populations studied
        4. Gaps or limitations identified
        5. Implications for synthetic data generation

        Keep the summary concise but informative (3-4 paragraphs).
        """
        
        try:
            summary = self.ollama_client.generate_text(prompt)
            return summary
        except Exception as e:
            print(f"Error generating literature summary: {e}")
            return f"Found {len(papers)} relevant papers. Summary generation failed."
    
    def extract_key_findings(self, paper: Paper) -> List[str]:
        """Extract key findings from a paper using LLM"""
        prompt = f"""
        Extract the key findings from this research paper:

        Title: {paper.title}
        Abstract: {paper.abstract}

        Provide 3-5 key findings as bullet points. Focus on:
        - Main results and outcomes
        - Statistical significance
        - Clinical implications
        - Population characteristics

        Format as a simple list.
        """
        
        try:
            findings_text = self.ollama_client.generate_text(prompt)
            # Parse findings into list
            findings = [line.strip().lstrip('•-*').strip() 
                       for line in findings_text.split('\n') 
                       if line.strip() and not line.strip().startswith('Key')]
            return findings[:5]  # Limit to 5 findings
        except Exception as e:
            print(f"Error extracting key findings: {e}")
            return []
    
    def _rate_limit_pubmed(self):
        """Implement rate limiting for PubMed API"""
        current_time = time.time()
        time_since_last = current_time - self.last_pubmed_request
        
        if time_since_last < self.pubmed_delay:
            time.sleep(self.pubmed_delay - time_since_last)
        
        self.last_pubmed_request = time.time()
