import requests
import defusedxml.ElementTree as ET
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import time
import os

class PubMedClient:
    """Client for interacting with PubMed E-utilities API"""
    
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.api_key = os.getenv("NCBI_API_KEY", "")
        self.email = os.getenv("NCBI_EMAIL", "research@example.com")
        
        # Rate limiting (NCBI allows 3 requests/second without API key, 10/second with key)
        self.last_request_time = 0
        self.request_delay = 0.1 if self.api_key else 0.34  # Be conservative
        
        # Tool identification for NCBI
        self.tool = "synthetic_ehr_generator"
    
    def search_papers(self, query: str, max_results: int = 20, 
                     date_range: Optional[Tuple[str, str]] = None) -> List[str]:
        """
        Search PubMed for paper IDs matching the query
        
        Args:
            query: Search terms
            max_results: Maximum number of results to return
            date_range: Optional tuple of (start_date, end_date) in YYYY/MM/DD format
            
        Returns:
            List of PMIDs
        """
        self._rate_limit()
        
        search_url = f"{self.base_url}esearch.fcgi"
        
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "xml",
            "sort": "relevance",
            "tool": self.tool,
            "email": self.email
        }
        
        # Add date range if specified
        if date_range:
            start_date, end_date = date_range
            params["datetype"] = "pdat"
            params["mindate"] = start_date
            params["maxdate"] = end_date
        else:
            # Default to last 10 years
            params["reldate"] = 3650
            params["datetype"] = "pdat"
        
        # Add API key if available
        if self.api_key:
            params["api_key"] = self.api_key
        
        try:
            response = requests.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)
            
            # Extract PMIDs
            pmids = []
            for id_elem in root.findall(".//Id"):
                pmids.append(id_elem.text)
            
            return pmids
            
        except requests.RequestException as e:
            print(f"Error searching PubMed: {e}")
            return []
        except ET.ParseError as e:
            print(f"Error parsing PubMed search response: {e}")
            return []
    
    def fetch_paper_details(self, pmids: List[str]) -> List[Dict]:
        """
        Fetch detailed information for a list of PMIDs
        
        Args:
            pmids: List of PubMed IDs
            
        Returns:
            List of paper dictionaries with details
        """
        if not pmids:
            return []
        
        self._rate_limit()
        
        fetch_url = f"{self.base_url}efetch.fcgi"
        
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "tool": self.tool,
            "email": self.email
        }
        
        if self.api_key:
            params["api_key"] = self.api_key
        
        try:
            response = requests.get(fetch_url, params=params, timeout=60)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)
            
            papers = []
            for article in root.findall(".//PubmedArticle"):
                paper_data = self._parse_article(article)
                if paper_data:
                    papers.append(paper_data)
            
            return papers
            
        except requests.RequestException as e:
            print(f"Error fetching PubMed details: {e}")
            return []
        except ET.ParseError as e:
            print(f"Error parsing PubMed fetch response: {e}")
            return []
    
    def _parse_article(self, article_elem) -> Optional[Dict]:
        """Parse a single PubMed article XML element"""
        try:
            # Initialize paper data
            paper = {}
            
            # Get PMID
            pmid_elem = article_elem.find(".//PMID")
            paper['pmid'] = pmid_elem.text if pmid_elem is not None else ""
            
            # Get title
            title_elem = article_elem.find(".//ArticleTitle")
            paper['title'] = self._clean_text(title_elem.text) if title_elem is not None else ""
            
            # Get abstract
            abstract_parts = []
            for abstract_elem in article_elem.findall(".//AbstractText"):
                if abstract_elem.text:
                    label = abstract_elem.get("Label", "")
                    text = self._clean_text(abstract_elem.text)
                    if label and label.lower() not in ['background', 'objective']:
                        abstract_parts.append(f"{label}: {text}")
                    else:
                        abstract_parts.append(text)
            
            paper['abstract'] = " ".join(abstract_parts)
            
            # Get authors
            authors = []
            for author_elem in article_elem.findall(".//Author"):
                last_name_elem = author_elem.find("LastName")
                first_name_elem = author_elem.find("ForeName")
                
                if last_name_elem is not None:
                    last_name = last_name_elem.text
                    first_name = first_name_elem.text if first_name_elem is not None else ""
                    
                    if first_name:
                        authors.append(f"{first_name} {last_name}")
                    else:
                        authors.append(last_name)
            
            paper['authors'] = ", ".join(authors[:10])  # Limit to first 10 authors
            
            # Get publication date
            paper['publication_date'] = self._parse_publication_date(article_elem)
            
            # Get journal information
            journal_elem = article_elem.find(".//Journal/Title")
            paper['journal'] = journal_elem.text if journal_elem is not None else ""
            
            # Get DOI
            doi_elem = article_elem.find(".//ArticleId[@IdType='doi']")
            paper['doi'] = doi_elem.text if doi_elem is not None else ""
            
            # Create PubMed URL
            paper['url'] = f"https://pubmed.ncbi.nlm.nih.gov/{paper['pmid']}/"
            
            # Get keywords
            keywords = []
            for keyword_elem in article_elem.findall(".//Keyword"):
                if keyword_elem.text:
                    keywords.append(keyword_elem.text)
            paper['keywords'] = keywords
            
            # Get MeSH terms
            mesh_terms = []
            for descriptor_elem in article_elem.findall(".//DescriptorName"):
                if descriptor_elem.text:
                    mesh_terms.append(descriptor_elem.text)
            paper['mesh_terms'] = mesh_terms
            
            return paper
            
        except Exception as e:
            print(f"Error parsing article: {e}")
            return None
    
    def _parse_publication_date(self, article_elem) -> Optional[datetime]:
        """Parse publication date from article XML"""
        try:
            # Try different date elements
            date_elem = article_elem.find(".//PubDate")
            if date_elem is None:
                date_elem = article_elem.find(".//ArticleDate")
            
            if date_elem is None:
                return None
            
            year_elem = date_elem.find("Year")
            month_elem = date_elem.find("Month")
            day_elem = date_elem.find("Day")
            
            if year_elem is None:
                return None
            
            year = int(year_elem.text)
            month = 1
            day = 1
            
            if month_elem is not None:
                month_text = month_elem.text
                if month_text.isdigit():
                    month = int(month_text)
                else:
                    # Handle month names
                    month_map = {
                        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
                    }
                    month = month_map.get(month_text[:3], 1)
            
            if day_elem is not None and day_elem.text.isdigit():
                day = int(day_elem.text)
            
            return datetime(year, month, day)
            
        except (ValueError, AttributeError) as e:
            print(f"Error parsing date: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove XML tags if any remain
        import re
        text = re.sub(r'<[^>]+>', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _rate_limit(self):
        """Implement rate limiting for API requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def get_paper_links(self, pmid: str) -> Dict[str, str]:
        """Get available links for a paper (full text, PDF, etc.)"""
        links = {
            'pubmed': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            'pmc': None,
            'doi': None
        }
        
        try:
            # Use elink to find associated resources
            self._rate_limit()
            
            elink_url = f"{self.base_url}elink.fcgi"
            params = {
                "dbfrom": "pubmed",
                "db": "pmc",
                "id": pmid,
                "retmode": "xml",
                "tool": self.tool,
                "email": self.email
            }
            
            if self.api_key:
                params["api_key"] = self.api_key
            
            response = requests.get(elink_url, params=params, timeout=30)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            
            # Check for PMC links
            for link_elem in root.findall(".//Link/Id"):
                pmc_id = link_elem.text
                if pmc_id:
                    links['pmc'] = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/"
                    break
            
        except Exception as e:
            print(f"Error getting paper links: {e}")
        
        return links
    
    def search_and_fetch(self, query: str, max_results: int = 20) -> List[Dict]:
        """Convenience method to search and fetch papers in one call"""
        pmids = self.search_papers(query, max_results)
        
        if not pmids:
            return []
        
        papers = self.fetch_paper_details(pmids)
        
        # Add relevance scores based on search order
        for i, paper in enumerate(papers):
            paper['search_rank'] = i + 1
            paper['relevance_score'] = 1.0 - (i / len(papers))  # Higher for earlier results
        
        return papers
    
    def validate_connection(self) -> bool:
        """Test connection to PubMed API"""
        try:
            # Simple test search
            test_pmids = self.search_papers("cancer", max_results=1)
            return len(test_pmids) > 0
        except Exception as e:
            print(f"PubMed connection validation failed: {e}")
            return False
