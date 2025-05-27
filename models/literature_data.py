from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

@dataclass
class Paper:
    """Represents a scientific paper from literature search"""
    
    title: str
    authors: str
    abstract: str
    publication_date: Optional[datetime] = None
    source: str = "unknown"  # e.g., "pubmed", "biorxiv"
    url: str = ""
    paper_id: str = ""  # PMID, DOI, etc.
    journal: str = ""
    doi: str = ""
    keywords: List[str] = None
    mesh_terms: List[str] = None
    relevance_score: float = 0.0
    key_findings: List[str] = None
    study_type: str = ""
    sample_size: Optional[int] = None
    population: str = ""
    
    def __post_init__(self):
        """Initialize default values for mutable fields"""
        if self.keywords is None:
            self.keywords = []
        if self.mesh_terms is None:
            self.mesh_terms = []
        if self.key_findings is None:
            self.key_findings = []
    
    def add_keyword(self, keyword: str):
        """Add a keyword to the paper"""
        if keyword and keyword not in self.keywords:
            self.keywords.append(keyword)
    
    def add_mesh_term(self, mesh_term: str):
        """Add a MeSH term to the paper"""
        if mesh_term and mesh_term not in self.mesh_terms:
            self.mesh_terms.append(mesh_term)
    
    def add_key_finding(self, finding: str):
        """Add a key finding to the paper"""
        if finding and finding not in self.key_findings:
            self.key_findings.append(finding)
    
    def get_publication_year(self) -> Optional[int]:
        """Get the publication year"""
        if self.publication_date:
            return self.publication_date.year
        return None
    
    def get_age_in_years(self) -> Optional[float]:
        """Get the age of the paper in years"""
        if self.publication_date:
            age_delta = datetime.now() - self.publication_date
            return age_delta.days / 365.25
        return None
    
    def is_recent(self, years: int = 5) -> bool:
        """Check if paper is recent (within specified years)"""
        age = self.get_age_in_years()
        return age is not None and age <= years
    
    def is_preprint(self) -> bool:
        """Check if this is a preprint paper"""
        return self.source.lower() in ["biorxiv", "medrxiv", "arxiv", "preprint"]
    
    def get_citation_format(self, style: str = "apa") -> str:
        """Generate citation in specified format"""
        if style.lower() == "apa":
            citation = f"{self.authors}"
            if self.publication_date:
                citation += f" ({self.get_publication_year()})"
            citation += f". {self.title}"
            if self.journal:
                citation += f". {self.journal}"
            if self.doi:
                citation += f". https://doi.org/{self.doi}"
            elif self.url:
                citation += f". Retrieved from {self.url}"
            return citation
        else:
            # Basic citation format
            return f"{self.authors}. {self.title}. {self.journal}. {self.get_publication_year() or 'n.d.'}"
    
    def extract_abstract_sections(self) -> Dict[str, str]:
        """Extract structured sections from abstract"""
        sections = {}
        
        if not self.abstract:
            return sections
        
        # Common abstract section headers
        section_headers = [
            "background", "objective", "objectives", "purpose", "aim", "aims",
            "methods", "methodology", "design", "participants", "setting",
            "results", "findings", "outcomes", "conclusion", "conclusions",
            "implications", "significance"
        ]
        
        abstract_lower = self.abstract.lower()
        
        # Simple section extraction
        for header in section_headers:
            patterns = [f"{header}:", f"{header}.", f"{header} -"]
            for pattern in patterns:
                if pattern in abstract_lower:
                    start_idx = abstract_lower.find(pattern)
                    if start_idx != -1:
                        # Find the end of this section (next section or end)
                        section_text = self.abstract[start_idx + len(pattern):].strip()
                        
                        # Find next section
                        min_next_idx = len(section_text)
                        for next_header in section_headers:
                            for next_pattern in [f"{next_header}:", f"{next_header}.", f"{next_header} -"]:
                                next_idx = section_text.lower().find(next_pattern)
                                if next_idx != -1 and next_idx < min_next_idx:
                                    min_next_idx = next_idx
                        
                        sections[header] = section_text[:min_next_idx].strip()
                        break
        
        return sections
    
    def get_study_population_info(self) -> Dict[str, Any]:
        """Extract study population information from abstract"""
        population_info = {
            "sample_size": self.sample_size,
            "population_description": self.population,
            "demographics": [],
            "inclusion_criteria": [],
            "exclusion_criteria": []
        }
        
        if not self.abstract:
            return population_info
        
        abstract_lower = self.abstract.lower()
        
        # Extract sample size if not already set
        if not self.sample_size:
            import re
            # Look for patterns like "n=123", "N=123", "123 patients", "123 participants"
            size_patterns = [
                r'n\s*=\s*(\d+)',
                r'n\s*(\d+)',
                r'(\d+)\s+patients',
                r'(\d+)\s+participants',
                r'(\d+)\s+subjects',
                r'sample\s+of\s+(\d+)'
            ]
            
            for pattern in size_patterns:
                match = re.search(pattern, abstract_lower)
                if match:
                    population_info["sample_size"] = int(match.group(1))
                    break
        
        # Extract demographic keywords
        demographic_keywords = [
            "male", "female", "men", "women", "adults", "children", "elderly",
            "pediatric", "geriatric", "adolescent", "young", "old"
        ]
        
        for keyword in demographic_keywords:
            if keyword in abstract_lower:
                population_info["demographics"].append(keyword)
        
        return population_info
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert paper to dictionary representation"""
        return {
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "publication_date": self.publication_date.isoformat() if self.publication_date else None,
            "source": self.source,
            "url": self.url,
            "paper_id": self.paper_id,
            "journal": self.journal,
            "doi": self.doi,
            "keywords": self.keywords,
            "mesh_terms": self.mesh_terms,
            "relevance_score": self.relevance_score,
            "key_findings": self.key_findings,
            "study_type": self.study_type,
            "sample_size": self.sample_size,
            "population": self.population,
            "publication_year": self.get_publication_year(),
            "age_in_years": self.get_age_in_years(),
            "is_recent": self.is_recent(),
            "is_preprint": self.is_preprint()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Paper':
        """Create paper from dictionary representation"""
        # Handle publication_date conversion
        publication_date = None
        if "publication_date" in data and data["publication_date"]:
            if isinstance(data["publication_date"], str):
                try:
                    publication_date = datetime.fromisoformat(data["publication_date"])
                except ValueError:
                    # Try parsing other common formats
                    for fmt in ["%Y-%m-%d", "%Y-%m", "%Y"]:
                        try:
                            publication_date = datetime.strptime(data["publication_date"], fmt)
                            break
                        except ValueError:
                            continue
            elif isinstance(data["publication_date"], datetime):
                publication_date = data["publication_date"]
        
        return cls(
            title=data.get("title", ""),
            authors=data.get("authors", ""),
            abstract=data.get("abstract", ""),
            publication_date=publication_date,
            source=data.get("source", "unknown"),
            url=data.get("url", ""),
            paper_id=data.get("paper_id", ""),
            journal=data.get("journal", ""),
            doi=data.get("doi", ""),
            keywords=data.get("keywords", []),
            mesh_terms=data.get("mesh_terms", []),
            relevance_score=data.get("relevance_score", 0.0),
            key_findings=data.get("key_findings", []),
            study_type=data.get("study_type", ""),
            sample_size=data.get("sample_size"),
            population=data.get("population", "")
        )
    
    def to_bibtex(self) -> str:
        """Generate BibTeX entry for the paper"""
        # Determine entry type
        entry_type = "article"
        if self.is_preprint():
            entry_type = "misc"
        
        # Create BibTeX key
        first_author = self.authors.split(",")[0].strip() if self.authors else "Unknown"
        year = self.get_publication_year() or "n.d."
        title_words = self.title.split()[:3] if self.title else ["Unknown"]
        key = f"{first_author.replace(' ', '')}{year}{''.join(title_words)}"
        
        bibtex = f"@{entry_type}{{{key},\n"
        bibtex += f"  title={{{self.title}}},\n"
        bibtex += f"  author={{{self.authors}}},\n"
        
        if self.journal:
            bibtex += f"  journal={{{self.journal}}},\n"
        
        if self.get_publication_year():
            bibtex += f"  year={{{self.get_publication_year()}}},\n"
        
        if self.doi:
            bibtex += f"  doi={{{self.doi}}},\n"
        
        if self.url:
            bibtex += f"  url={{{self.url}}},\n"
        
        bibtex += "}\n"
        
        return bibtex
    
    def __str__(self) -> str:
        """String representation of paper"""
        return f"Paper('{self.title[:50]}...', {self.source}, {self.get_publication_year()})"
    
    def __repr__(self) -> str:
        """Detailed representation of paper"""
        return (f"Paper(title='{self.title[:30]}...', authors='{self.authors[:30]}...', "
                f"source='{self.source}', year={self.get_publication_year()})")


@dataclass
class LiteratureResult:
    """Represents the result of a literature search"""
    
    query: str
    papers: List[Paper]
    summary: str = ""
    search_timestamp: datetime = None
    total_found: int = 0
    sources_searched: List[str] = None
    search_parameters: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values"""
        if self.search_timestamp is None:
            self.search_timestamp = datetime.now()
        if self.sources_searched is None:
            self.sources_searched = []
        if self.search_parameters is None:
            self.search_parameters = {}
        if self.total_found == 0:
            self.total_found = len(self.papers)
    
    def get_paper_count(self) -> int:
        """Get the number of papers found"""
        return len(self.papers)
    
    def get_papers_by_source(self, source: str) -> List[Paper]:
        """Get papers from a specific source"""
        return [paper for paper in self.papers if paper.source.lower() == source.lower()]
    
    def get_recent_papers(self, years: int = 5) -> List[Paper]:
        """Get papers published within the last N years"""
        return [paper for paper in self.papers if paper.is_recent(years)]
    
    def get_papers_by_year(self) -> Dict[int, List[Paper]]:
        """Group papers by publication year"""
        by_year = {}
        for paper in self.papers:
            year = paper.get_publication_year()
            if year:
                if year not in by_year:
                    by_year[year] = []
                by_year[year].append(paper)
        return by_year
    
    def get_top_papers(self, n: int = 10) -> List[Paper]:
        """Get top N papers by relevance score"""
        sorted_papers = sorted(self.papers, key=lambda p: p.relevance_score, reverse=True)
        return sorted_papers[:n]
    
    def get_authors_frequency(self) -> Dict[str, int]:
        """Get frequency of authors across papers"""
        author_freq = {}
        for paper in self.papers:
            if paper.authors:
                # Split authors and count each
                authors = [author.strip() for author in paper.authors.split(",")]
                for author in authors:
                    author_freq[author] = author_freq.get(author, 0) + 1
        return author_freq
    
    def get_journal_distribution(self) -> Dict[str, int]:
        """Get distribution of papers by journal"""
        journal_dist = {}
        for paper in self.papers:
            if paper.journal:
                journal_dist[paper.journal] = journal_dist.get(paper.journal, 0) + 1
        return journal_dist
    
    def get_keywords_frequency(self) -> Dict[str, int]:
        """Get frequency of keywords across papers"""
        keyword_freq = {}
        for paper in self.papers:
            for keyword in paper.keywords:
                keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
        return keyword_freq
    
    def get_mesh_terms_frequency(self) -> Dict[str, int]:
        """Get frequency of MeSH terms across papers"""
        mesh_freq = {}
        for paper in self.papers:
            for mesh_term in paper.mesh_terms:
                mesh_freq[mesh_term] = mesh_freq.get(mesh_term, 0) + 1
        return mesh_freq
    
    def filter_by_study_type(self, study_type: str) -> 'LiteratureResult':
        """Create a new result filtered by study type"""
        filtered_papers = [p for p in self.papers if study_type.lower() in p.study_type.lower()]
        
        return LiteratureResult(
            query=f"{self.query} (filtered by {study_type})",
            papers=filtered_papers,
            summary=f"Filtered results for {study_type} studies",
            search_timestamp=self.search_timestamp,
            sources_searched=self.sources_searched.copy(),
            search_parameters=self.search_parameters.copy()
        )
    
    def filter_by_sample_size(self, min_size: int) -> 'LiteratureResult':
        """Create a new result filtered by minimum sample size"""
        filtered_papers = [p for p in self.papers if p.sample_size and p.sample_size >= min_size]
        
        return LiteratureResult(
            query=f"{self.query} (min sample size: {min_size})",
            papers=filtered_papers,
            summary=f"Filtered results with sample size >= {min_size}",
            search_timestamp=self.search_timestamp,
            sources_searched=self.sources_searched.copy(),
            search_parameters=self.search_parameters.copy()
        )
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """Get comprehensive search statistics"""
        stats = {
            "query": self.query,
            "total_papers": self.get_paper_count(),
            "search_timestamp": self.search_timestamp.isoformat() if self.search_timestamp else None,
            "sources_searched": self.sources_searched,
            "papers_by_source": {},
            "papers_by_year": {},
            "recent_papers": len(self.get_recent_papers()),
            "preprints": len([p for p in self.papers if p.is_preprint()]),
            "with_sample_size": len([p for p in self.papers if p.sample_size]),
            "average_relevance_score": 0.0
        }
        
        # Papers by source
        for source in set(p.source for p in self.papers):
            stats["papers_by_source"][source] = len(self.get_papers_by_source(source))
        
        # Papers by year
        by_year = self.get_papers_by_year()
        for year, papers in by_year.items():
            stats["papers_by_year"][year] = len(papers)
        
        # Average relevance score
        if self.papers:
            scores = [p.relevance_score for p in self.papers if p.relevance_score > 0]
            if scores:
                stats["average_relevance_score"] = sum(scores) / len(scores)
        
        return stats
    
    def export_citations(self, format: str = "apa") -> List[str]:
        """Export citations in specified format"""
        citations = []
        for paper in self.papers:
            if format.lower() == "bibtex":
                citations.append(paper.to_bibtex())
            else:
                citations.append(paper.get_citation_format(format))
        return citations
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary representation"""
        return {
            "query": self.query,
            "papers": [paper.to_dict() for paper in self.papers],
            "summary": self.summary,
            "search_timestamp": self.search_timestamp.isoformat() if self.search_timestamp else None,
            "total_found": self.total_found,
            "sources_searched": self.sources_searched,
            "search_parameters": self.search_parameters,
            "statistics": self.get_search_statistics()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LiteratureResult':
        """Create result from dictionary representation"""
        # Convert papers
        papers = []
        for paper_data in data.get("papers", []):
            papers.append(Paper.from_dict(paper_data))
        
        # Handle search_timestamp conversion
        search_timestamp = None
        if "search_timestamp" in data and data["search_timestamp"]:
            if isinstance(data["search_timestamp"], str):
                try:
                    search_timestamp = datetime.fromisoformat(data["search_timestamp"])
                except ValueError:
                    search_timestamp = datetime.now()
            elif isinstance(data["search_timestamp"], datetime):
                search_timestamp = data["search_timestamp"]
        
        return cls(
            query=data.get("query", ""),
            papers=papers,
            summary=data.get("summary", ""),
            search_timestamp=search_timestamp,
            total_found=data.get("total_found", len(papers)),
            sources_searched=data.get("sources_searched", []),
            search_parameters=data.get("search_parameters", {})
        )
    
    def save_to_file(self, filepath: str, format: str = "json"):
        """Save literature result to file"""
        if format.lower() == "json":
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        elif format.lower() == "csv":
            import csv
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                if self.papers:
                    writer = csv.DictWriter(f, fieldnames=self.papers[0].to_dict().keys())
                    writer.writeheader()
                    for paper in self.papers:
                        writer.writerow(paper.to_dict())
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'LiteratureResult':
        """Load literature result from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def merge_with(self, other: 'LiteratureResult') -> 'LiteratureResult':
        """Merge with another literature result"""
        merged_papers = self.papers.copy()
        
        # Add papers from other result, avoiding duplicates
        existing_ids = {p.paper_id for p in self.papers if p.paper_id}
        for paper in other.papers:
            if not paper.paper_id or paper.paper_id not in existing_ids:
                merged_papers.append(paper)
                if paper.paper_id:
                    existing_ids.add(paper.paper_id)
        
        # Combine sources searched
        merged_sources = list(set(self.sources_searched + other.sources_searched))
        
        # Combine search parameters
        merged_params = self.search_parameters.copy()
        merged_params.update(other.search_parameters)
        
        return LiteratureResult(
            query=f"{self.query} + {other.query}",
            papers=merged_papers,
            summary=f"Merged results: {self.summary} | {other.summary}",
            search_timestamp=max(self.search_timestamp, other.search_timestamp),
            sources_searched=merged_sources,
            search_parameters=merged_params
        )
    
    def __len__(self) -> int:
        """Return the number of papers"""
        return len(self.papers)
    
    def __iter__(self):
        """Allow iteration over papers"""
        return iter(self.papers)
    
    def __getitem__(self, index):
        """Allow indexing into the papers list"""
        return self.papers[index]
    
    def __str__(self) -> str:
        """String representation of result"""
        return f"LiteratureResult('{self.query}', {len(self.papers)} papers)"
    
    def __repr__(self) -> str:
        """Detailed representation of result"""
        return (f"LiteratureResult(query='{self.query}', papers={len(self.papers)}, "
                f"timestamp='{self.search_timestamp}')")
