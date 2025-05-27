from typing import Dict, Any, Optional, Callable
from agents.literature_agent import LiteratureAgent
from agents.synthetic_cohort_agent import SyntheticCohortAgent
from agents.critique_agent import CritiqueAgent
from agents.web_monitor_agent import WebMonitorAgent
from agents.statistical_validation_agent import StatisticalValidationAgent
from agents.medical_terminology_agent import MedicalTerminologyAgent
from utils.vector_store import VectorStore
from utils.ollama_client import OllamaClient
from models.literature_data import LiteratureResult
from models.patient_data import PatientCohort

class RAGOrchestrator:
    """Main orchestrator that coordinates all agents for the RAG workflow"""
    
    def __init__(self):
        # Initialize core components
        self.vector_store = VectorStore()
        self.ollama_client = OllamaClient()
        
        # Initialize agents
        self.literature_agent = LiteratureAgent(self.vector_store, self.ollama_client)
        self.cohort_agent = SyntheticCohortAgent(self.ollama_client)
        self.critique_agent = CritiqueAgent(self.ollama_client)
        self.web_monitor_agent = WebMonitorAgent(self.vector_store, self.ollama_client)
        self.statistical_validation_agent = StatisticalValidationAgent(self.ollama_client)
        self.medical_terminology_agent = MedicalTerminologyAgent(self.ollama_client)
        
        # Default settings
        self.settings = {
            'model_name': 'mistral:latest',
            'cohort_size': 100,
            'include_notes': True,
            'include_labs': True,
            'max_papers': 20,
            'include_preprints': True
        }
    
    def update_settings(self, new_settings: Dict[str, Any]):
        """Update orchestrator settings"""
        self.settings.update(new_settings)
        self.ollama_client.model_name = self.settings.get('model_name', 'mistral:latest')
    
    def process_query(self, query: str, progress_callback: Optional[Callable[[str], None]] = None) -> Dict[str, Any]:
        """Process a research query through the complete RAG pipeline"""
        
        if progress_callback:
            progress_callback("🔍 Starting literature search...")
        
        try:
            # Step 1: Literature Retrieval
            literature_result = self.literature_agent.search_literature(
                query=query,
                max_papers=self.settings['max_papers'],
                include_preprints=self.settings['include_preprints']
            )
            
            if progress_callback:
                progress_callback(f"📚 Found {len(literature_result.papers)} relevant papers")
            
            # Step 2: Extract key findings from literature
            if progress_callback:
                progress_callback("🔬 Extracting key findings from literature...")
            
            for paper in literature_result.papers:
                paper.key_findings = self.literature_agent.extract_key_findings(paper)
            
            # Step 3: Store literature in vector store for RAG
            if progress_callback:
                progress_callback("💾 Indexing literature for RAG...")
            
            self._index_literature(literature_result)
            
            # Step 4: Generate synthetic cohort
            if progress_callback:
                progress_callback("👥 Generating synthetic patient cohort...")
            
            cohort = self.cohort_agent.generate_cohort(
                query=query,
                literature_context=literature_result.summary,
                cohort_size=self.settings['cohort_size'],
                include_notes=self.settings['include_notes'],
                include_labs=self.settings['include_labs']
            )
            
            if progress_callback:
                progress_callback(f"✅ Generated {len(cohort.patients)} synthetic patients")
            
            # Step 5: Statistical validation and medical terminology check
            if progress_callback:
                progress_callback("📊 Performing statistical validation...")
            
            statistical_validation = self.statistical_validation_agent.comprehensive_validation(
                cohort=cohort,
                literature=literature_result
            )
            
            if progress_callback:
                progress_callback("🩺 Validating medical terminology...")
            
            # Validate medical terminology in the query and results
            terminology_validation = self.medical_terminology_agent.validate_medical_terminology(query)
            
            # Step 6: Critique and validate
            if progress_callback:
                progress_callback("🔍 Validating cohort against literature...")
            
            critique = self.critique_agent.critique_cohort(
                cohort=cohort,
                literature=literature_result,
                query=query
            )
            
            # Step 6: Generate final summary
            if progress_callback:
                progress_callback("📝 Generating final analysis summary...")
            
            final_summary = self._generate_final_summary(
                query, literature_result, cohort, critique
            )
            
            if progress_callback:
                progress_callback("✨ Analysis complete!")
            
            return {
                'query': query,
                'literature': literature_result,
                'cohort': cohort,
                'critique': critique['overall_assessment'],
                'critique_detailed': critique,
                'summary': final_summary
            }
            
        except Exception as e:
            error_msg = f"Error in RAG pipeline: {str(e)}"
            if progress_callback:
                progress_callback(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def _index_literature(self, literature_result: LiteratureResult):
        """Index literature in vector store for RAG retrieval"""
        documents = []
        
        for paper in literature_result.papers:
            # Create document content
            content = f"Title: {paper.title}\n"
            content += f"Authors: {paper.authors}\n"
            content += f"Abstract: {paper.abstract}\n"
            
            if paper.key_findings:
                content += f"Key Findings: {'; '.join(paper.key_findings)}\n"
            
            # Add metadata
            metadata = {
                'paper_id': paper.paper_id,
                'source': paper.source,
                'title': paper.title,
                'authors': paper.authors,
                'publication_date': paper.publication_date.isoformat() if paper.publication_date else None,
                'relevance_score': paper.relevance_score,
                'url': paper.url
            }
            
            documents.append({
                'content': content,
                'metadata': metadata
            })
        
        # Add documents to vector store
        self.vector_store.add_documents(documents)
    
    def query_literature_context(self, query: str, top_k: int = 5) -> str:
        """Query the vector store for relevant literature context"""
        try:
            results = self.vector_store.similarity_search(query, top_k=top_k)
            
            if not results:
                return "No relevant literature context found."
            
            context = "Relevant Literature Context:\n\n"
            for i, result in enumerate(results, 1):
                context += f"{i}. {result['metadata']['title']}\n"
                context += f"   Source: {result['metadata']['source']}\n"
                context += f"   Content: {result['content'][:300]}...\n\n"
            
            return context
            
        except Exception as e:
            print(f"Error querying literature context: {e}")
            return "Error retrieving literature context."
    
    def _generate_final_summary(self, query: str, literature: LiteratureResult, 
                               cohort: PatientCohort, critique: Dict[str, Any]) -> str:
        """Generate a comprehensive final summary"""
        
        prompt = f"""
        Generate a comprehensive research summary based on the following analysis:

        Original Query: {query}

        Literature Analysis:
        - Papers Found: {len(literature.papers)}
        - Literature Summary: {literature.summary}

        Synthetic Cohort:
        - Patients Generated: {len(cohort.patients)}
        - Average Age: {sum(p.age for p in cohort.patients if p.age) / len([p for p in cohort.patients if p.age]):.1f} years
        - Key Conditions: {self._get_top_conditions(cohort)}

        Validation Results:
        - Realism Score: {critique.get('realism_score', 0):.2f}/1.0
        - Literature Alignment: {critique.get('literature_alignment', {}).get('overall_alignment', 0):.2f}/1.0

        Provide a structured summary that includes:
        1. Key insights from literature review
        2. Characteristics of the generated synthetic cohort
        3. Validation assessment and confidence level
        4. Practical implications for AI/ML model development
        5. Recommendations for data usage

        Keep it professional and actionable (4-5 paragraphs).
        """
        
        try:
            summary = self.ollama_client.generate_text(prompt)
            return summary
        except Exception as e:
            print(f"Error generating final summary: {e}")
            return self._create_fallback_summary(query, literature, cohort, critique)
    
    def _get_top_conditions(self, cohort: PatientCohort, top_n: int = 5) -> str:
        """Get top N conditions from cohort"""
        all_conditions = []
        for patient in cohort.patients:
            all_conditions.extend(patient.conditions)
        
        if not all_conditions:
            return "No conditions recorded"
        
        # Count conditions
        condition_counts = {}
        for condition in all_conditions:
            condition_counts[condition] = condition_counts.get(condition, 0) + 1
        
        # Get top conditions
        sorted_conditions = sorted(condition_counts.items(), key=lambda x: x[1], reverse=True)
        top_conditions = [condition for condition, count in sorted_conditions[:top_n]]
        
        return ", ".join(top_conditions)
    
    def _create_fallback_summary(self, query: str, literature: LiteratureResult, 
                                cohort: PatientCohort, critique: Dict[str, Any]) -> str:
        """Create a fallback summary when LLM generation fails"""
        summary = f"Research Analysis Summary for: {query}\n\n"
        
        summary += f"Literature Review: Retrieved {len(literature.papers)} relevant papers "
        summary += f"from PubMed and bioRxiv. "
        
        if literature.papers:
            pubmed_count = sum(1 for p in literature.papers if p.source == "pubmed")
            biorxiv_count = sum(1 for p in literature.papers if p.source == "biorxiv")
            summary += f"Sources include {pubmed_count} PubMed articles and {biorxiv_count} bioRxiv preprints.\n\n"
        
        summary += f"Synthetic Cohort: Generated {len(cohort.patients)} synthetic patients "
        
        if cohort.patients:
            ages = [p.age for p in cohort.patients if p.age]
            if ages:
                avg_age = sum(ages) / len(ages)
                summary += f"with an average age of {avg_age:.1f} years. "
            
            top_conditions = self._get_top_conditions(cohort, 3)
            summary += f"Most common conditions include: {top_conditions}.\n\n"
        
        realism_score = critique.get('realism_score', 0)
        summary += f"Validation: The synthetic cohort achieved a realism score of {realism_score:.2f}/1.0. "
        
        if realism_score >= 0.8:
            summary += "This indicates high quality synthetic data suitable for AI model training."
        elif realism_score >= 0.6:
            summary += "This indicates acceptable quality with some areas for improvement."
        else:
            summary += "This indicates the cohort may need refinement before use."
        
        return summary
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents and components"""
        return {
            'literature_agent': {
                'status': 'ready',
                'vector_store_size': self.vector_store.get_collection_size()
            },
            'cohort_agent': {
                'status': 'ready',
                'model': self.settings.get('model_name', 'mistral:latest')
            },
            'critique_agent': {
                'status': 'ready'
            },
            'ollama_client': {
                'status': 'ready' if self.ollama_client.check_connection() else 'disconnected',
                'model': self.ollama_client.model_name
            },
            'settings': self.settings
        }
    
    def reset_session(self):
        """Reset session state and clear vector store"""
        try:
            self.vector_store.clear_collection()
            print("Session reset successfully")
        except Exception as e:
            print(f"Error resetting session: {e}")
