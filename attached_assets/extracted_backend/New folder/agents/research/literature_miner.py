from .base_agent import BaseAgent
from datetime import datetime
import logging
from typing import Dict, Any, List
import requests

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

class LiteratureMiner(BaseAgent):
    def __init__(self, llm=None):
        super().__init__()
        self.llm = llm  # Pass in your callable LLM, e.g. BioGPT, Meditron, OpenAI, etc.

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"[{self.agent_name}] Mining evidence from PubMed/Semantic Scholar...")

        query = input_data.get("research_query") or " ".join(input_data.get("conditions", []))
        max_results = input_data.get("max_results", 3)
        evidence_items: List[Dict[str, Any]] = []

        # --- 1. Retrieve papers from Semantic Scholar ---
        papers = self.semantic_scholar_search(query, max_results)
        # --- 2. Retrieve papers from PubMed (optional, uncomment if needed) ---
        papers += self.pubmed_search(query, max_results)
        papers = self.dedupe_papers(papers)

        # --- 3. Summarize abstracts using the LLM (if available) ---
        for paper in papers:
            if self.llm and paper.get("abstract"):
                summary = self.llm(
                    f"Summarize this paper for a clinical researcher:\nTitle: {paper['title']}\nAbstract: {paper['abstract']}\n"
                )
            else:
                summary = paper.get("abstract", "")

            evidence_items.append({
                "source_id": paper.get("url", "unknown"),
                "confidence_score": 0.9,  # Placeholder; later use LLM scoring/confidence
                "timestamp": datetime.utcnow().isoformat(),
                "agent": self.agent_name,
                "type": "literature_summary",
                "content": {
                    "title": paper["title"],
                    "summary": summary,
                    "source_url": paper["url"],
                }
            })

        input_data["literature_evidence"] = evidence_items
        log_msg = f"[{self.agent_name}] Retrieved {len(evidence_items)} paper(s) for query: '{query}'."

        return self.standard_response(output=input_data, log=log_msg)

    def semantic_scholar_search(self, query: str, max_results: int) -> List[Dict[str, str]]:
        params = {
            "query": query,
            "fields": "title,abstract,url",
            "limit": max_results
        }
        try:
            resp = requests.get(SEMANTIC_SCHOLAR_API, params=params, timeout=10)
            if resp.status_code == 200:
                return [
                    {
                        "title": p.get("title", ""),
                        "abstract": p.get("abstract", ""),
                        "url": p.get("url", "")
                    }
                    for p in resp.json().get("data", [])
                ]
        except Exception as e:
            logging.warning(f"[{self.agent_name}] Semantic Scholar error: {e}")
        return []

    def pubmed_search(self, query: str, max_results: int) -> List[Dict[str, str]]:
        # Step 1: eSearch
        esearch_params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json"
        }
        try:
            esearch = requests.get(PUBMED_ESEARCH, params=esearch_params, timeout=10)
            idlist = esearch.json().get("esearchresult", {}).get("idlist", [])
            if not idlist:
                return []
            # Step 2: eSummary
            esummary_params = {
                "db": "pubmed",
                "id": ",".join(idlist),
                "retmode": "json"
            }
            esummary = requests.get(PUBMED_ESUMMARY, params=esummary_params, timeout=10)
            papers = []
            if esummary.status_code == 200:
                result = esummary.json().get("result", {})
                for pmid in idlist:
                    entry = result.get(pmid, {})
                    papers.append({
                        "title": entry.get("title", ""),
                        "abstract": entry.get("elocationid", ""),  # PubMed eSummary doesn't return abstract; fetch w/ eFetch for full text
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    })
            return papers
        except Exception as e:
            logging.warning(f"[{self.agent_name}] PubMed error: {e}")
            return []

    def dedupe_papers(self, papers: List[Dict[str, str]]) -> List[Dict[str, str]]:
        seen = set()
        unique = []
        for p in papers:
            key = (p["title"], p["url"])
            if key not in seen and p["title"]:
                seen.add(key)
                unique.append(p)
        return unique
