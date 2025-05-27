import requests
import time
import schedule
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin
import validators
from fake_useragent import UserAgent
import feedparser
from bs4 import BeautifulSoup
import newspaper
from newspaper import Article
import json
import hashlib
from dataclasses import dataclass
from utils.vector_store import VectorStore
from utils.ollama_client import OllamaClient

@dataclass
class WebSource:
    """Represents a web source to monitor"""
    name: str
    url: str
    source_type: str  # "rss", "website", "news", "journal"
    trustworthiness_score: float = 0.5
    last_checked: Optional[datetime] = None
    active: bool = True
    check_frequency: int = 60  # minutes
    keywords: List[str] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []

@dataclass
class ScrapedContent:
    """Represents scraped content from the web"""
    title: str
    content: str
    url: str
    source_name: str
    scraped_at: datetime
    content_hash: str
    trustworthiness_score: float = 0.0
    keywords: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.metadata is None:
            self.metadata = {}
        if not self.content_hash:
            self.content_hash = hashlib.md5(self.content.encode()).hexdigest()

class WebMonitorAgent:
    """Agent responsible for monitoring web sources and curating data"""
    
    def __init__(self, vector_store: VectorStore, ollama_client: OllamaClient):
        self.vector_store = vector_store
        self.ollama_client = ollama_client
        self.ua = UserAgent()
        
        # Content storage
        self.scraped_content = []
        self.content_hashes = set()
        
        # Monitoring sources
        self.sources = []
        self.is_monitoring = False
        
        # Default medical/health sources
        self.default_sources = [
            WebSource(
                name="PubMed RSS", 
                url="https://pubmed.ncbi.nlm.nih.gov/rss/", 
                source_type="rss",
                trustworthiness_score=0.95,
                keywords=["medical", "health", "clinical", "research"]
            ),
            WebSource(
                name="Nature Medicine",
                url="https://www.nature.com/nm.rss",
                source_type="rss", 
                trustworthiness_score=0.9,
                keywords=["medicine", "research", "clinical"]
            ),
            WebSource(
                name="BMJ",
                url="https://www.bmj.com/rss",
                source_type="rss",
                trustworthiness_score=0.9,
                keywords=["medical", "bmj", "clinical"]
            ),
            WebSource(
                name="The Lancet",
                url="https://www.thelancet.com/rssfeed/lancet_current.xml",
                source_type="rss",
                trustworthiness_score=0.95,
                keywords=["medicine", "lancet", "research"]
            )
        ]
        
        # Initialize with default sources
        self.sources.extend(self.default_sources)
    
    def add_source(self, source: WebSource):
        """Add a new source to monitor"""
        if not any(s.url == source.url for s in self.sources):
            self.sources.append(source)
            print(f"Added source: {source.name}")
    
    def remove_source(self, url: str):
        """Remove a source from monitoring"""
        self.sources = [s for s in self.sources if s.url != url]
        print(f"Removed source: {url}")
    
    def assess_trustworthiness(self, content: ScrapedContent) -> float:
        """Assess the trustworthiness of scraped content using LLM"""
        prompt = f"""
        Assess the trustworthiness of this medical/health content on a scale of 0.0 to 1.0:

        Title: {content.title}
        Source: {content.source_name}
        URL: {content.url}
        Content Preview: {content.content[:500]}...

        Consider these factors:
        1. Source credibility and reputation
        2. Content quality and scientific rigor
        3. Presence of citations or references
        4. Author credentials (if available)
        5. Publication date and relevance
        6. Potential bias or commercial interests

        Respond with only a decimal number between 0.0 and 1.0, where:
        - 0.9-1.0: Highly trustworthy (peer-reviewed journals, established medical institutions)
        - 0.7-0.89: Generally trustworthy (reputable news sources, medical organizations)
        - 0.5-0.69: Moderately trustworthy (general websites with some credibility)
        - 0.3-0.49: Low trustworthiness (blogs, unverified sources)
        - 0.0-0.29: Not trustworthy (questionable or harmful content)
        """
        
        try:
            response = self.ollama_client.generate_text(prompt)
            # Extract numeric score from response
            import re
            score_match = re.search(r'0\.\d+|1\.0|0\.0', response)
            if score_match:
                score = float(score_match.group())
                return max(0.0, min(1.0, score))
            else:
                return 0.5  # Default moderate score
        except Exception as e:
            print(f"Error assessing trustworthiness: {e}")
            return 0.5
    
    def extract_keywords(self, content: ScrapedContent) -> List[str]:
        """Extract relevant keywords from content using LLM"""
        prompt = f"""
        Extract 5-10 relevant medical/health keywords from this content:

        Title: {content.title}
        Content: {content.content[:1000]}...

        Focus on:
        - Medical conditions and diseases
        - Treatments and medications
        - Medical procedures
        - Health topics
        - Research areas

        Return as a comma-separated list of keywords.
        """
        
        try:
            response = self.ollama_client.generate_text(prompt)
            # Parse keywords from response
            keywords = [kw.strip() for kw in response.split(',')]
            # Clean and filter keywords
            keywords = [kw for kw in keywords if kw and len(kw) > 2 and len(kw) < 50]
            return keywords[:10]  # Limit to 10 keywords
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []
    
    def scrape_rss_feed(self, source: WebSource) -> List[ScrapedContent]:
        """Scrape content from RSS feed"""
        content_list = []
        
        try:
            # Parse RSS feed
            feed = feedparser.parse(source.url)
            
            for entry in feed.entries[:10]:  # Limit to 10 recent entries
                try:
                    # Extract basic info
                    title = entry.get('title', '')
                    link = entry.get('link', '')
                    summary = entry.get('summary', '')
                    
                    # Try to get full content
                    full_content = self._get_full_article_content(link)
                    content = full_content if full_content else summary
                    
                    if content and title:
                        scraped_content = ScrapedContent(
                            title=title,
                            content=content,
                            url=link,
                            source_name=source.name,
                            scraped_at=datetime.now(),
                            content_hash="",
                            metadata={
                                'published': entry.get('published', ''),
                                'author': entry.get('author', ''),
                                'tags': entry.get('tags', [])
                            }
                        )
                        
                        # Check for duplicates
                        if scraped_content.content_hash not in self.content_hashes:
                            content_list.append(scraped_content)
                            self.content_hashes.add(scraped_content.content_hash)
                
                except Exception as e:
                    print(f"Error processing RSS entry: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping RSS feed {source.url}: {e}")
        
        return content_list
    
    def scrape_website(self, source: WebSource) -> List[ScrapedContent]:
        """Scrape content from a regular website"""
        content_list = []
        
        try:
            headers = {'User-Agent': self.ua.random}
            response = requests.get(source.url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract articles or main content
            articles = soup.find_all(['article', 'div'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['article', 'post', 'content', 'news']
            ))
            
            if not articles:
                # Fallback to main content areas
                articles = soup.find_all(['main', 'div'], class_=lambda x: x and 'main' in x.lower())
            
            for article in articles[:5]:  # Limit to 5 articles
                try:
                    title_elem = article.find(['h1', 'h2', 'h3'])
                    title = title_elem.get_text().strip() if title_elem else ''
                    
                    # Get article text
                    content = article.get_text().strip()
                    
                    # Get article link
                    link_elem = article.find('a', href=True)
                    link = urljoin(source.url, link_elem['href']) if link_elem else source.url
                    
                    if content and title and len(content) > 100:
                        scraped_content = ScrapedContent(
                            title=title,
                            content=content,
                            url=link,
                            source_name=source.name,
                            scraped_at=datetime.now(),
                            content_hash=""
                        )
                        
                        if scraped_content.content_hash not in self.content_hashes:
                            content_list.append(scraped_content)
                            self.content_hashes.add(scraped_content.content_hash)
                
                except Exception as e:
                    print(f"Error processing article: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping website {source.url}: {e}")
        
        return content_list
    
    def _get_full_article_content(self, url: str) -> Optional[str]:
        """Get full article content using newspaper3k"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception:
            return None
    
    def scrape_source(self, source: WebSource) -> List[ScrapedContent]:
        """Scrape content from a source based on its type"""
        if not source.active:
            return []
        
        print(f"Scraping {source.name} ({source.source_type})")
        
        try:
            if source.source_type == "rss":
                content_list = self.scrape_rss_feed(source)
            else:
                content_list = self.scrape_website(source)
            
            # Process each piece of content
            processed_content = []
            for content in content_list:
                # Assess trustworthiness
                content.trustworthiness_score = self.assess_trustworthiness(content)
                
                # Extract keywords
                content.keywords = self.extract_keywords(content)
                
                # Only keep content above minimum trustworthiness threshold
                if content.trustworthiness_score >= 0.3:
                    processed_content.append(content)
                    self.scraped_content.append(content)
            
            # Update last checked time
            source.last_checked = datetime.now()
            
            print(f"Scraped {len(processed_content)} pieces of content from {source.name}")
            return processed_content
            
        except Exception as e:
            print(f"Error scraping source {source.name}: {e}")
            return []
    
    def scrape_all_sources(self) -> List[ScrapedContent]:
        """Scrape content from all active sources"""
        all_content = []
        
        for source in self.sources:
            if source.active:
                # Check if it's time to scrape this source
                if (source.last_checked is None or 
                    datetime.now() - source.last_checked > timedelta(minutes=source.check_frequency)):
                    
                    content = self.scrape_source(source)
                    all_content.extend(content)
                    
                    # Small delay between sources to be respectful
                    time.sleep(2)
        
        return all_content
    
    def curate_content(self, content_list: List[ScrapedContent], query: str = "") -> List[ScrapedContent]:
        """Curate content based on relevance and quality"""
        if not content_list:
            return []
        
        # Filter by trustworthiness
        trusted_content = [c for c in content_list if c.trustworthiness_score >= 0.5]
        
        # If query provided, filter by relevance
        if query:
            relevant_content = []
            query_lower = query.lower()
            
            for content in trusted_content:
                # Check if query terms appear in title, content, or keywords
                content_text = f"{content.title} {content.content}".lower()
                keyword_text = " ".join(content.keywords).lower()
                
                if (any(term in content_text for term in query_lower.split()) or
                    any(term in keyword_text for term in query_lower.split())):
                    relevant_content.append(content)
            
            return relevant_content
        
        return trusted_content
    
    def add_to_rag(self, content_list: List[ScrapedContent]):
        """Add curated content to the RAG vector store"""
        if not content_list:
            return
        
        documents = []
        for content in content_list:
            # Create document for vector store
            doc_content = f"Title: {content.title}\n"
            doc_content += f"Source: {content.source_name}\n"
            doc_content += f"URL: {content.url}\n"
            doc_content += f"Content: {content.content}\n"
            doc_content += f"Keywords: {', '.join(content.keywords)}"
            
            metadata = {
                'title': content.title,
                'source': content.source_name,
                'url': content.url,
                'scraped_at': content.scraped_at.isoformat(),
                'trustworthiness_score': content.trustworthiness_score,
                'keywords': content.keywords,
                'content_type': 'web_scraped'
            }
            
            documents.append({
                'content': doc_content,
                'metadata': metadata
            })
        
        # Add to vector store
        self.vector_store.add_documents(documents)
        print(f"Added {len(documents)} documents to RAG vector store")
    
    def start_monitoring(self, interval_minutes: int = 30):
        """Start automated monitoring of sources"""
        if self.is_monitoring:
            print("Monitoring is already running")
            return
        
        self.is_monitoring = True
        
        # Schedule monitoring job
        schedule.every(interval_minutes).minutes.do(self._monitoring_job)
        
        print(f"Started monitoring {len(self.sources)} sources every {interval_minutes} minutes")
        
        # Run the monitoring loop
        while self.is_monitoring:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def stop_monitoring(self):
        """Stop automated monitoring"""
        self.is_monitoring = False
        schedule.clear()
        print("Stopped monitoring")
    
    def _monitoring_job(self):
        """Job function for scheduled monitoring"""
        print(f"Running monitoring job at {datetime.now()}")
        
        # Scrape all sources
        new_content = self.scrape_all_sources()
        
        if new_content:
            # Curate content
            curated_content = self.curate_content(new_content)
            
            # Add to RAG
            self.add_to_rag(curated_content)
            
            print(f"Monitoring cycle complete: {len(new_content)} scraped, {len(curated_content)} curated")
    
    def manual_scrape_and_update(self, query: str = "") -> Dict[str, Any]:
        """Manually trigger scraping and RAG update"""
        print("Starting manual scrape and update...")
        
        # Scrape all sources
        new_content = self.scrape_all_sources()
        
        # Curate content
        curated_content = self.curate_content(new_content, query)
        
        # Add to RAG
        self.add_to_rag(curated_content)
        
        # Return summary
        return {
            'total_scraped': len(new_content),
            'curated_content': len(curated_content),
            'sources_checked': len([s for s in self.sources if s.active]),
            'timestamp': datetime.now().isoformat(),
            'query_used': query
        }
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        return {
            'is_monitoring': self.is_monitoring,
            'total_sources': len(self.sources),
            'active_sources': len([s for s in self.sources if s.active]),
            'total_content_scraped': len(self.scraped_content),
            'unique_content_hashes': len(self.content_hashes),
            'sources': [
                {
                    'name': s.name,
                    'url': s.url,
                    'type': s.source_type,
                    'trustworthiness': s.trustworthiness_score,
                    'last_checked': s.last_checked.isoformat() if s.last_checked else None,
                    'active': s.active
                }
                for s in self.sources
            ]
        }
    
    def search_scraped_content(self, query: str, limit: int = 10) -> List[ScrapedContent]:
        """Search through scraped content"""
        query_lower = query.lower()
        matching_content = []
        
        for content in self.scraped_content:
            # Calculate relevance score
            score = 0
            content_text = f"{content.title} {content.content}".lower()
            
            for term in query_lower.split():
                if term in content_text:
                    score += 1
                if term in " ".join(content.keywords).lower():
                    score += 0.5
            
            if score > 0:
                matching_content.append((content, score))
        
        # Sort by relevance and trustworthiness
        matching_content.sort(key=lambda x: (x[1], x[0].trustworthiness_score), reverse=True)
        
        return [content for content, score in matching_content[:limit]]