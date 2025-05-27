"""
Authentic PubMed Literature Retrieval Agent
Connects to real NCBI PubMed database for genuine medical research
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
from datetime import datetime
import time
import trafilatura
from urllib.parse import quote

class PubMedConnector:
    """Real PubMed API connector for authentic medical literature"""
    
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.email = "research@syntheticascension.com"  # Required by NCBI
        
    def search_pubmed(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """Search PubMed for authentic medical literature"""
        
        # Step 1: Search for PMIDs
        search_url = f"{self.base_url}/esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "email": self.email,
            "tool": "SyntheticAscension"
        }
        
        try:
            search_response = requests.get(search_url, params=search_params, timeout=10)
            search_response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(search_response.content)
            pmids = [id_elem.text for id_elem in root.findall(".//Id")]
            
            if not pmids:
                return []
            
            # Step 2: Fetch article details
            return self._fetch_article_details(pmids)
            
        except requests.RequestException as e:
            print(f"PubMed search failed: {e}")
            return []
    
    def _fetch_article_details(self, pmids: List[str]) -> List[Dict[str, Any]]:
        """Fetch detailed article information from PubMed"""
        
        pmid_str = ",".join(pmids)
        fetch_url = f"{self.base_url}/efetch.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": pmid_str,
            "rettype": "abstract",
            "retmode": "xml",
            "email": self.email,
            "tool": "SyntheticAscension"
        }
        
        try:
            # Be respectful to NCBI servers
            time.sleep(0.34)  # NCBI rate limit: 3 requests per second max
            
            fetch_response = requests.get(fetch_url, params=fetch_params, timeout=15)
            fetch_response.raise_for_status()
            
            return self._parse_pubmed_xml(fetch_response.content)
            
        except requests.RequestException as e:
            print(f"PubMed fetch failed: {e}")
            return []
    
    def _parse_pubmed_xml(self, xml_content: bytes) -> List[Dict[str, Any]]:
        """Parse PubMed XML response into structured data"""
        
        articles = []
        root = ET.fromstring(xml_content)
        
        for article in root.findall(".//PubmedArticle"):
            try:
                # Extract basic article information
                pmid = article.find(".//PMID").text if article.find(".//PMID") is not None else "Unknown"
                
                # Title
                title_elem = article.find(".//ArticleTitle")
                title = title_elem.text if title_elem is not None else "No title available"
                
                # Authors
                authors = []
                for author in article.findall(".//Author"):
                    lastname = author.find("LastName")
                    forename = author.find("ForeName")
                    if lastname is not None and forename is not None:
                        authors.append(f"{forename.text} {lastname.text}")
                
                # Abstract
                abstract_elem = article.find(".//Abstract/AbstractText")
                abstract = abstract_elem.text if abstract_elem is not None else "No abstract available"
                
                # Journal
                journal_elem = article.find(".//Journal/Title")
                journal = journal_elem.text if journal_elem is not None else "Unknown journal"
                
                # Publication date
                pub_date_year = article.find(".//PubDate/Year")
                pub_date_month = article.find(".//PubDate/Month")
                pub_date = f"{pub_date_year.text if pub_date_year is not None else 'Unknown'}"
                if pub_date_month is not None:
                    pub_date += f" {pub_date_month.text}"
                
                # DOI
                doi_elem = article.find(".//ArticleId[@IdType='doi']")
                doi = doi_elem.text if doi_elem is not None else None
                
                # Keywords/MeSH terms
                mesh_terms = []
                for mesh in article.findall(".//MeshHeading/DescriptorName"):
                    mesh_terms.append(mesh.text)
                
                articles.append({
                    "pmid": pmid,
                    "title": title,
                    "authors": authors,
                    "abstract": abstract,
                    "journal": journal,
                    "publication_date": pub_date,
                    "doi": doi,
                    "mesh_terms": mesh_terms,
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    "retrieved_at": datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
        
        return articles
    
    def get_clinical_trials(self, condition: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Retrieve clinical trials from ClinicalTrials.gov"""
        
        search_url = "https://clinicaltrials.gov/api/query/study_fields"
        params = {
            "expr": condition,
            "fields": "NCTId,BriefTitle,Condition,Phase,StudyType,PrimaryCompletionDate,LeadSponsorName",
            "min_rnk": 1,
            "max_rnk": max_results,
            "fmt": "json"
        }
        
        try:
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            trials = []
            
            if "StudyFieldsResponse" in data and "StudyFields" in data["StudyFieldsResponse"]:
                for study in data["StudyFieldsResponse"]["StudyFields"]:
                    trial_data = {
                        "nct_id": study.get("NCTId", ["Unknown"])[0],
                        "title": study.get("BriefTitle", ["Unknown"])[0],
                        "condition": study.get("Condition", ["Unknown"])[0],
                        "phase": study.get("Phase", ["Unknown"])[0],
                        "study_type": study.get("StudyType", ["Unknown"])[0],
                        "completion_date": study.get("PrimaryCompletionDate", ["Unknown"])[0],
                        "sponsor": study.get("LeadSponsorName", ["Unknown"])[0],
                        "url": f"https://clinicaltrials.gov/ct2/show/{study.get('NCTId', [''])[0]}",
                        "retrieved_at": datetime.now().isoformat()
                    }
                    trials.append(trial_data)
            
            return trials
            
        except requests.RequestException as e:
            print(f"ClinicalTrials.gov search failed: {e}")
            return []
    
    def get_fda_guidance(self, topic: str) -> List[Dict[str, Any]]:
        """Retrieve FDA guidance documents (web scraping approach)"""
        
        search_url = f"https://www.fda.gov/search?query={quote(topic)}"
        
        try:
            # Fetch the search results page
            response = requests.get(search_url, timeout=10)
            response.raise_for_status()
            
            # Extract text content using trafilatura
            extracted_text = trafilatura.extract(response.text)
            
            if extracted_text:
                return [{
                    "source": "FDA.gov",
                    "topic": topic,
                    "content": extracted_text[:2000],  # Limit content length
                    "url": search_url,
                    "retrieved_at": datetime.now().isoformat()
                }]
            else:
                return []
                
        except requests.RequestException as e:
            print(f"FDA guidance search failed: {e}")
            return []
    
    def get_who_reports(self, topic: str) -> List[Dict[str, Any]]:
        """Retrieve WHO health reports and guidelines"""
        
        search_url = f"https://www.who.int/search?query={quote(topic)}"
        
        try:
            response = requests.get(search_url, timeout=10)
            response.raise_for_status()
            
            extracted_text = trafilatura.extract(response.text)
            
            if extracted_text:
                return [{
                    "source": "WHO.int",
                    "topic": topic,
                    "content": extracted_text[:2000],
                    "url": search_url,
                    "retrieved_at": datetime.now().isoformat()
                }]
            else:
                return []
                
        except requests.RequestException as e:
            print(f"WHO search failed: {e}")
            return []

# Global instance
pubmed_connector = PubMedConnector()