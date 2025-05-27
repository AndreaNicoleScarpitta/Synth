"""
Enhanced Literature Agent for Synthetic Ascension
Integrates comprehensive biomedical database search with AI-powered analysis
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

from .biomedical_database_connector import BiomedicalDatabaseConnector

class EnhancedLiteratureAgent:
    """
    Advanced literature search and analysis agent using multiple biomedical databases
    """
    
    def __init__(self):
        self.db_connector = BiomedicalDatabaseConnector()
        self.search_history = []
        
    async def comprehensive_literature_search(self, 
                                            query: str, 
                                            max_results_per_source: int = 25,
                                            include_clinical_trials: bool = True,
                                            include_drug_data: bool = True,
                                            include_protein_data: bool = False,
                                            date_filter: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Perform comprehensive literature search across multiple databases
        """
        
        # Determine databases to search based on query and preferences
        databases = ['pubmed']
        
        if include_clinical_trials:
            databases.append('clinicaltrials')
            
        if include_drug_data:
            databases.append('fda_drugs')
            
        if include_protein_data:
            databases.append('uniprot')
        
        # Add NIH Reporter for funding/research context
        databases.append('nih_reporter')
        
        # Log search initiation
        search_record = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'databases': databases,
            'parameters': {
                'max_results_per_source': max_results_per_source,
                'date_filter': date_filter
            }
        }
        self.search_history.append(search_record)
        
        # Perform comprehensive search
        results = self.db_connector.comprehensive_biomedical_search(
            query=query,
            databases=databases,
            max_results_per_db=max_results_per_source
        )
        
        # Enhance results with analysis
        enhanced_results = await self._analyze_search_results(results)
        
        return enhanced_results
    
    async def _analyze_search_results(self, raw_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze and enhance raw search results with metadata and insights
        """
        
        analysis = {
            'search_metadata': {
                'query': raw_results.get('query'),
                'timestamp': raw_results.get('search_timestamp'),
                'databases_searched': raw_results.get('databases_searched', []),
                'total_results': raw_results.get('summary', {}).get('total_results_found', 0)
            },
            'database_results': raw_results.get('results', {}),
            'cross_database_insights': {},
            'research_themes': {},
            'clinical_relevance': {},
            'evidence_quality': {}
        }
        
        # Analyze PubMed results for research themes
        if 'pubmed' in analysis['database_results']:
            pubmed_data = analysis['database_results']['pubmed']
            analysis['research_themes'] = self._extract_research_themes(pubmed_data)
            analysis['evidence_quality']['pubmed'] = self._assess_evidence_quality(pubmed_data)
        
        # Analyze clinical trials for clinical relevance
        if 'clinicaltrials' in analysis['database_results']:
            ct_data = analysis['database_results']['clinicaltrials']
            analysis['clinical_relevance'] = self._analyze_clinical_trials(ct_data)
        
        # Cross-database insights
        analysis['cross_database_insights'] = self._generate_cross_database_insights(
            analysis['database_results']
        )
        
        return analysis
    
    def _extract_research_themes(self, pubmed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract key research themes from PubMed articles
        """
        articles = pubmed_data.get('articles', [])
        
        # Extract keywords and MeSH terms
        all_keywords = []
        publication_years = []
        journal_distribution = {}
        
        for article in articles:
            keywords = article.get('keywords', [])
            all_keywords.extend(keywords)
            
            year = article.get('year', 'Unknown')
            if year != 'Unknown':
                try:
                    publication_years.append(int(year))
                except ValueError:
                    pass
            
            journal = article.get('journal', 'Unknown')
            journal_distribution[journal] = journal_distribution.get(journal, 0) + 1
        
        # Analyze keyword frequency
        keyword_frequency = {}
        for keyword in all_keywords:
            keyword_frequency[keyword] = keyword_frequency.get(keyword, 0) + 1
        
        # Get top themes
        top_keywords = sorted(keyword_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Analyze publication timeline
        year_range = {
            'earliest': min(publication_years) if publication_years else None,
            'latest': max(publication_years) if publication_years else None,
            'span_years': max(publication_years) - min(publication_years) if len(publication_years) > 1 else 0
        }
        
        # Top journals
        top_journals = sorted(journal_distribution.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'top_research_themes': [{'theme': keyword, 'frequency': freq} for keyword, freq in top_keywords],
            'publication_timeline': year_range,
            'leading_journals': [{'journal': journal, 'article_count': count} for journal, count in top_journals],
            'total_articles_analyzed': len(articles)
        }
    
    def _assess_evidence_quality(self, pubmed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess the quality of evidence from PubMed search results
        """
        articles = pubmed_data.get('articles', [])
        
        # Keywords that indicate high-quality study types
        high_quality_indicators = [
            'randomized controlled trial', 'meta-analysis', 'systematic review',
            'clinical trial', 'double-blind', 'placebo-controlled'
        ]
        
        medium_quality_indicators = [
            'cohort study', 'case-control study', 'prospective study',
            'multicenter', 'longitudinal'
        ]
        
        quality_scores = {'high': 0, 'medium': 0, 'standard': 0}
        
        for article in articles:
            article_text = f"{article.get('title', '')} {article.get('abstract', '')}".lower()
            keywords = [kw.lower() for kw in article.get('keywords', [])]
            
            # Check for quality indicators
            has_high_quality = any(
                indicator in article_text or indicator in ' '.join(keywords)
                for indicator in high_quality_indicators
            )
            
            has_medium_quality = any(
                indicator in article_text or indicator in ' '.join(keywords)
                for indicator in medium_quality_indicators
            )
            
            if has_high_quality:
                quality_scores['high'] += 1
            elif has_medium_quality:
                quality_scores['medium'] += 1
            else:
                quality_scores['standard'] += 1
        
        total_articles = len(articles)
        quality_percentages = {
            level: (count / total_articles * 100) if total_articles > 0 else 0
            for level, count in quality_scores.items()
        }
        
        return {
            'quality_distribution': quality_scores,
            'quality_percentages': quality_percentages,
            'high_quality_ratio': quality_percentages['high'],
            'evidence_strength': 'strong' if quality_percentages['high'] > 30 else 
                               'moderate' if quality_percentages['high'] > 15 else 'emerging'
        }
    
    def _analyze_clinical_trials(self, ct_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze clinical trials data for clinical relevance insights
        """
        studies = ct_data.get('studies', [])
        
        # Analyze study phases
        phase_distribution = {}
        status_distribution = {}
        study_types = {}
        enrollment_data = []
        
        for study in studies:
            phase = study.get('phase', 'Not Applicable')
            phase_distribution[phase] = phase_distribution.get(phase, 0) + 1
            
            status = study.get('status', 'Unknown')
            status_distribution[status] = status_distribution.get(status, 0) + 1
            
            study_type = study.get('study_type', 'Unknown')
            study_types[study_type] = study_types.get(study_type, 0) + 1
            
            enrollment = study.get('enrollment')
            if enrollment and enrollment.isdigit():
                enrollment_data.append(int(enrollment))
        
        # Calculate enrollment statistics
        enrollment_stats = {}
        if enrollment_data:
            enrollment_stats = {
                'total_participants': sum(enrollment_data),
                'average_enrollment': sum(enrollment_data) / len(enrollment_data),
                'median_enrollment': sorted(enrollment_data)[len(enrollment_data) // 2],
                'largest_study': max(enrollment_data),
                'smallest_study': min(enrollment_data)
            }
        
        return {
            'total_studies': len(studies),
            'phase_distribution': phase_distribution,
            'status_distribution': status_distribution,
            'study_type_distribution': study_types,
            'enrollment_statistics': enrollment_stats,
            'clinical_maturity': self._assess_clinical_maturity(phase_distribution, status_distribution)
        }
    
    def _assess_clinical_maturity(self, phase_dist: Dict[str, int], status_dist: Dict[str, int]) -> str:
        """
        Assess the clinical maturity of research based on trial phases and status
        """
        total_studies = sum(phase_dist.values())
        if total_studies == 0:
            return 'No clinical data'
        
        # Count advanced phase studies
        advanced_phases = phase_dist.get('Phase 3', 0) + phase_dist.get('Phase 4', 0)
        early_phases = phase_dist.get('Phase 1', 0) + phase_dist.get('Phase 2', 0)
        
        completed_studies = status_dist.get('Completed', 0)
        
        advanced_ratio = advanced_phases / total_studies
        completion_ratio = completed_studies / total_studies
        
        if advanced_ratio > 0.3 and completion_ratio > 0.4:
            return 'Mature - Ready for clinical application'
        elif advanced_ratio > 0.1 or completion_ratio > 0.3:
            return 'Developing - Active clinical research'
        elif early_phases > 0:
            return 'Early stage - Proof-of-concept research'
        else:
            return 'Preclinical - Limited clinical evidence'
    
    def _generate_cross_database_insights(self, database_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate insights by correlating data across multiple databases
        """
        insights = {
            'research_to_clinical_gap': {},
            'drug_development_pipeline': {},
            'funding_research_correlation': {},
            'translational_potential': {}
        }
        
        # Analyze research-to-clinical translation
        pubmed_count = database_results.get('pubmed', {}).get('total_count', 0)
        ct_count = database_results.get('clinicaltrials', {}).get('total_count', 0)
        
        if pubmed_count > 0:
            clinical_translation_ratio = ct_count / pubmed_count
            insights['research_to_clinical_gap'] = {
                'research_articles': pubmed_count,
                'clinical_trials': ct_count,
                'translation_ratio': clinical_translation_ratio,
                'translation_assessment': (
                    'Strong translation' if clinical_translation_ratio > 0.2 else
                    'Moderate translation' if clinical_translation_ratio > 0.1 else
                    'Limited translation'
                )
            }
        
        # Assess drug development pipeline
        fda_count = database_results.get('fda_drugs', {}).get('total_count', 0)
        if ct_count > 0 and fda_count > 0:
            insights['drug_development_pipeline'] = {
                'clinical_trials': ct_count,
                'approved_drugs': fda_count,
                'development_maturity': 'Established' if fda_count > 0 else 'In development'
            }
        
        # Analyze funding correlation
        nih_count = database_results.get('nih_reporter', {}).get('total_count', 0)
        if nih_count > 0 and pubmed_count > 0:
            funding_research_ratio = nih_count / pubmed_count
            insights['funding_research_correlation'] = {
                'funded_projects': nih_count,
                'research_publications': pubmed_count,
                'funding_efficiency': funding_research_ratio,
                'funding_assessment': (
                    'Well-funded area' if funding_research_ratio > 0.05 else
                    'Moderately funded' if funding_research_ratio > 0.02 else
                    'Limited funding'
                )
            }
        
        return insights
    
    async def get_research_trends(self, topic: str, years: List[int] = None) -> Dict[str, Any]:
        """
        Get comprehensive research trends across multiple databases
        """
        trends = self.db_connector.get_research_trends(topic, years)
        
        # Enhance with additional trend analysis
        enhanced_trends = {
            **trends,
            'trend_analysis': self._analyze_publication_trends(trends.get('publication_trends', {})),
            'research_momentum': self._assess_research_momentum(trends.get('publication_trends', {}))
        }
        
        return enhanced_trends
    
    def _analyze_publication_trends(self, yearly_counts: Dict[int, int]) -> Dict[str, Any]:
        """
        Analyze publication trends over time
        """
        if not yearly_counts:
            return {}
        
        years = sorted(yearly_counts.keys())
        counts = [yearly_counts[year] for year in years]
        
        # Calculate growth rate
        growth_rates = []
        for i in range(1, len(counts)):
            if counts[i-1] > 0:
                growth_rate = (counts[i] - counts[i-1]) / counts[i-1] * 100
                growth_rates.append(growth_rate)
        
        avg_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0
        
        # Identify trend direction
        recent_trend = 'stable'
        if len(counts) >= 3:
            recent_counts = counts[-3:]
            if all(recent_counts[i] >= recent_counts[i-1] for i in range(1, len(recent_counts))):
                recent_trend = 'increasing'
            elif all(recent_counts[i] <= recent_counts[i-1] for i in range(1, len(recent_counts))):
                recent_trend = 'decreasing'
        
        return {
            'average_growth_rate': avg_growth_rate,
            'recent_trend': recent_trend,
            'peak_year': max(yearly_counts, key=yearly_counts.get),
            'peak_publications': max(yearly_counts.values()),
            'total_publications': sum(yearly_counts.values())
        }
    
    def _assess_research_momentum(self, yearly_counts: Dict[int, int]) -> str:
        """
        Assess the current research momentum in the field
        """
        if not yearly_counts:
            return 'No data available'
        
        years = sorted(yearly_counts.keys())
        if len(years) < 2:
            return 'Insufficient data'
        
        recent_years = years[-2:]
        recent_total = sum(yearly_counts[year] for year in recent_years)
        earlier_years = years[:-2] if len(years) > 2 else years[:1]
        earlier_avg = sum(yearly_counts[year] for year in earlier_years) / len(earlier_years) if earlier_years else 0
        
        if recent_total / 2 > earlier_avg * 1.5:
            return 'High momentum - Rapidly growing field'
        elif recent_total / 2 > earlier_avg * 1.1:
            return 'Moderate momentum - Steady growth'
        elif recent_total / 2 > earlier_avg * 0.9:
            return 'Stable momentum - Consistent activity'
        else:
            return 'Declining momentum - Decreasing activity'
    
    def get_search_history(self) -> List[Dict[str, Any]]:
        """
        Get the search history for this session
        """
        return self.search_history
    
    async def focused_disease_research(self, disease: str, 
                                     include_genetics: bool = True,
                                     include_treatments: bool = True) -> Dict[str, Any]:
        """
        Perform focused research on a specific disease
        """
        
        # Base search for the disease
        base_results = await self.comprehensive_literature_search(
            query=disease,
            max_results_per_source=30,
            include_clinical_trials=True,
            include_drug_data=include_treatments
        )
        
        # Additional targeted searches
        additional_searches = {}
        
        if include_genetics:
            genetics_query = f"{disease} genetics genomics mutations"
            additional_searches['genetics'] = await self.comprehensive_literature_search(
                query=genetics_query,
                max_results_per_source=15,
                include_protein_data=True
            )
        
        if include_treatments:
            treatment_query = f"{disease} treatment therapy intervention"
            additional_searches['treatments'] = await self.comprehensive_literature_search(
                query=treatment_query,
                max_results_per_source=20,
                include_clinical_trials=True,
                include_drug_data=True
            )
        
        return {
            'disease': disease,
            'comprehensive_overview': base_results,
            'specialized_research': additional_searches,
            'disease_profile': self._generate_disease_profile(base_results, additional_searches)
        }
    
    def _generate_disease_profile(self, base_results: Dict[str, Any], 
                                additional_searches: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive disease profile from search results
        """
        
        profile = {
            'research_maturity': 'Unknown',
            'clinical_pipeline_strength': 'Unknown',
            'genetic_understanding': 'Unknown',
            'treatment_landscape': 'Unknown'
        }
        
        # Assess research maturity from base results
        pubmed_results = base_results.get('database_results', {}).get('pubmed', {})
        total_publications = pubmed_results.get('total_count', 0)
        
        if total_publications > 1000:
            profile['research_maturity'] = 'Well-established research field'
        elif total_publications > 100:
            profile['research_maturity'] = 'Active research area'
        elif total_publications > 10:
            profile['research_maturity'] = 'Emerging research field'
        else:
            profile['research_maturity'] = 'Limited research available'
        
        # Assess clinical pipeline
        clinical_relevance = base_results.get('clinical_relevance', {})
        clinical_maturity = clinical_relevance.get('clinical_maturity', '')
        profile['clinical_pipeline_strength'] = clinical_maturity
        
        # Assess genetic understanding
        if 'genetics' in additional_searches:
            genetics_results = additional_searches['genetics']
            genetics_publications = genetics_results.get('database_results', {}).get('pubmed', {}).get('total_count', 0)
            protein_data = genetics_results.get('database_results', {}).get('uniprot', {}).get('total_count', 0)
            
            if genetics_publications > 50 and protein_data > 5:
                profile['genetic_understanding'] = 'Strong genetic characterization'
            elif genetics_publications > 10:
                profile['genetic_understanding'] = 'Moderate genetic understanding'
            else:
                profile['genetic_understanding'] = 'Limited genetic data'
        
        # Assess treatment landscape
        if 'treatments' in additional_searches:
            treatment_results = additional_searches['treatments']
            fda_drugs = treatment_results.get('database_results', {}).get('fda_drugs', {}).get('total_count', 0)
            clinical_trials = treatment_results.get('database_results', {}).get('clinicaltrials', {}).get('total_count', 0)
            
            if fda_drugs > 0:
                profile['treatment_landscape'] = 'FDA-approved treatments available'
            elif clinical_trials > 10:
                profile['treatment_landscape'] = 'Active treatment development'
            elif clinical_trials > 0:
                profile['treatment_landscape'] = 'Early treatment research'
            else:
                profile['treatment_landscape'] = 'Limited treatment options'
        
        return profile

# Example usage
async def main():
    """Example usage of the Enhanced Literature Agent"""
    agent = EnhancedLiteratureAgent()
    
    # Comprehensive search
    results = await agent.comprehensive_literature_search(
        query="diabetes mellitus type 2",
        max_results_per_source=10,
        include_clinical_trials=True,
        include_drug_data=True
    )
    
    print("Search completed!")
    print(f"Total results: {results['search_metadata']['total_results']}")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())