"""
Biomedical Database Connector for Synthetic Ascension
Integrates multiple research repositories and medical databases
"""

import requests
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
import time
import logging
from datetime import datetime, timedelta
import pandas as pd

class BiomedicalDatabaseConnector:
    """
    Comprehensive connector for biomedical databases and research repositories
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Synthetic-Ascension/1.0 (Research Platform)'
        })
        
        # Rate limiting trackers
        self.last_request_times = {}
        self.request_delays = {
            'pubmed': 0.5,  # 2 requests per second max
            'clinicaltrials': 1.0,  # 1 request per second max
            'fda': 0.3,  # Conservative rate limit
            'nih_reporter': 1.0,
            'opentargets': 0.5,
            'ebi_chembl': 0.5,
            'uniprot': 0.3
        }
        
        # API endpoints
        self.endpoints = {
            'pubmed_search': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
            'pubmed_fetch': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi',
            'pubmed_summary': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi',
            'clinicaltrials': 'https://clinicaltrials.gov/api/query/study_fields',
            'fda_drugs': 'https://api.fda.gov/drug/label.json',
            'fda_adverse': 'https://api.fda.gov/drug/event.json',
            'nih_reporter': 'https://api.reporter.nih.gov/v2/projects/search',
            'opentargets_disease': 'https://api.platform.opentargets.org/api/v4/graphql',
            'chembl_compound': 'https://www.ebi.ac.uk/chembl/api/data/molecule',
            'uniprot_proteins': 'https://rest.uniprot.org/uniprotkb/search'
        }

    def _rate_limit(self, source: str):
        """Implement rate limiting for API calls"""
        if source in self.last_request_times:
            elapsed = time.time() - self.last_request_times[source]
            min_delay = self.request_delays.get(source, 1.0)
            if elapsed < min_delay:
                time.sleep(min_delay - elapsed)
        
        self.last_request_times[source] = time.time()

    def search_pubmed_enhanced(self, query: str, max_results: int = 50, 
                             publication_types: List[str] = None,
                             date_range: tuple = None) -> Dict[str, Any]:
        """
        Enhanced PubMed search with advanced filtering
        """
        self._rate_limit('pubmed')
        
        # Build advanced query
        search_terms = [query]
        
        if publication_types:
            pub_filters = [f'"{pt}"[Publication Type]' for pt in publication_types]
            search_terms.append(f"({' OR '.join(pub_filters)})")
        
        if date_range:
            start_date, end_date = date_range
            date_filter = f'("{start_date}"[Date - Publication] : "{end_date}"[Date - Publication])'
            search_terms.append(date_filter)
        
        final_query = ' AND '.join(search_terms)
        
        # Search for PMIDs
        search_params = {
            'db': 'pubmed',
            'term': final_query,
            'retmax': max_results,
            'retmode': 'json',
            'sort': 'relevance'
        }
        
        try:
            response = self.session.get(self.endpoints['pubmed_search'], params=search_params)
            response.raise_for_status()
            search_data = response.json()
            
            pmids = search_data.get('esearchresult', {}).get('idlist', [])
            
            if not pmids:
                return {'articles': [], 'total_count': 0, 'query': final_query}
            
            # Fetch detailed article information
            articles = self._fetch_pubmed_details(pmids[:max_results])
            
            return {
                'articles': articles,
                'total_count': len(pmids),
                'query': final_query,
                'retrieved_count': len(articles)
            }
            
        except Exception as e:
            logging.error(f"PubMed search error: {e}")
            return {'articles': [], 'total_count': 0, 'error': str(e)}

    def _fetch_pubmed_details(self, pmids: List[str]) -> List[Dict[str, Any]]:
        """Fetch detailed article information from PubMed"""
        self._rate_limit('pubmed')
        
        # Batch fetch article details
        fetch_params = {
            'db': 'pubmed',
            'id': ','.join(pmids),
            'retmode': 'xml'
        }
        
        try:
            response = self.session.get(self.endpoints['pubmed_fetch'], params=fetch_params)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)
            articles = []
            
            for article in root.findall('.//PubmedArticle'):
                try:
                    article_data = self._parse_pubmed_article(article)
                    if article_data:
                        articles.append(article_data)
                except Exception as e:
                    logging.warning(f"Error parsing article: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            logging.error(f"Error fetching PubMed details: {e}")
            return []

    def _parse_pubmed_article(self, article_xml) -> Optional[Dict[str, Any]]:
        """Parse individual PubMed article XML"""
        try:
            # Extract PMID
            pmid_elem = article_xml.find('.//PMID')
            pmid = pmid_elem.text if pmid_elem is not None else None
            
            # Extract article details
            medline_citation = article_xml.find('.//MedlineCitation')
            if medline_citation is None:
                return None
            
            article_elem = medline_citation.find('.//Article')
            if article_elem is None:
                return None
            
            # Title
            title_elem = article_elem.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else "No title available"
            
            # Abstract
            abstract_elems = article_elem.findall('.//AbstractText')
            abstract_parts = []
            for abs_elem in abstract_elems:
                label = abs_elem.get('Label', '')
                text = abs_elem.text or ''
                if label:
                    abstract_parts.append(f"{label}: {text}")
                else:
                    abstract_parts.append(text)
            abstract = '\n'.join(abstract_parts) if abstract_parts else "No abstract available"
            
            # Authors
            authors = []
            author_list = article_elem.find('.//AuthorList')
            if author_list is not None:
                for author in author_list.findall('.//Author'):
                    last_name = author.find('.//LastName')
                    first_name = author.find('.//ForeName')
                    if last_name is not None and first_name is not None:
                        authors.append(f"{first_name.text} {last_name.text}")
            
            # Journal
            journal_elem = article_elem.find('.//Journal/Title')
            journal = journal_elem.text if journal_elem is not None else "Unknown journal"
            
            # Publication date
            pub_date = article_elem.find('.//PubDate')
            year_elem = pub_date.find('.//Year') if pub_date is not None else None
            year = year_elem.text if year_elem is not None else "Unknown"
            
            # Keywords/MeSH terms
            keywords = []
            mesh_list = medline_citation.find('.//MeshHeadingList')
            if mesh_list is not None:
                for mesh in mesh_list.findall('.//MeshHeading'):
                    descriptor = mesh.find('.//DescriptorName')
                    if descriptor is not None:
                        keywords.append(descriptor.text)
            
            return {
                'pmid': pmid,
                'title': title,
                'abstract': abstract,
                'authors': authors,
                'journal': journal,
                'year': year,
                'keywords': keywords,
                'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None
            }
            
        except Exception as e:
            logging.error(f"Error parsing article XML: {e}")
            return None

    def search_clinical_trials(self, condition: str, max_results: int = 50,
                             status: List[str] = None, phase: List[str] = None) -> Dict[str, Any]:
        """
        Search ClinicalTrials.gov database
        """
        self._rate_limit('clinicaltrials')
        
        # Build search parameters
        fields = [
            'NCTId', 'BriefTitle', 'OfficialTitle', 'Condition', 'InterventionName',
            'Phase', 'OverallStatus', 'StudyType', 'PrimaryCompletionDate',
            'EnrollmentCount', 'BriefSummary', 'DetailedDescription'
        ]
        
        params = {
            'expr': condition,
            'fields': ','.join(fields),
            'min_rnk': 1,
            'max_rnk': max_results,
            'fmt': 'json'
        }
        
        # Add filters
        if status:
            status_filter = ' OR '.join([f'AREA[OverallStatus]{s}' for s in status])
            params['expr'] += f' AND ({status_filter})'
        
        if phase:
            phase_filter = ' OR '.join([f'AREA[Phase]{p}' for p in phase])
            params['expr'] += f' AND ({phase_filter})'
        
        try:
            response = self.session.get(self.endpoints['clinicaltrials'], params=params)
            response.raise_for_status()
            data = response.json()
            
            studies = []
            if 'StudyFieldsResponse' in data and 'StudyFields' in data['StudyFieldsResponse']:
                for study in data['StudyFieldsResponse']['StudyFields']:
                    study_data = {
                        'nct_id': study.get('NCTId', [None])[0],
                        'brief_title': study.get('BriefTitle', [None])[0],
                        'official_title': study.get('OfficialTitle', [None])[0],
                        'condition': study.get('Condition', []),
                        'intervention': study.get('InterventionName', []),
                        'phase': study.get('Phase', [None])[0],
                        'status': study.get('OverallStatus', [None])[0],
                        'study_type': study.get('StudyType', [None])[0],
                        'completion_date': study.get('PrimaryCompletionDate', [None])[0],
                        'enrollment': study.get('EnrollmentCount', [None])[0],
                        'summary': study.get('BriefSummary', [None])[0],
                        'description': study.get('DetailedDescription', [None])[0],
                        'url': f"https://clinicaltrials.gov/ct2/show/{study.get('NCTId', [None])[0]}" if study.get('NCTId') else None
                    }
                    studies.append(study_data)
            
            return {
                'studies': studies,
                'total_count': len(studies),
                'query': condition
            }
            
        except Exception as e:
            logging.error(f"ClinicalTrials.gov search error: {e}")
            return {'studies': [], 'total_count': 0, 'error': str(e)}

    def search_fda_drugs(self, drug_name: str, max_results: int = 20) -> Dict[str, Any]:
        """
        Search FDA drug labels and adverse events
        """
        self._rate_limit('fda')
        
        # Search drug labels
        label_params = {
            'search': f'openfda.brand_name:"{drug_name}" OR openfda.generic_name:"{drug_name}"',
            'limit': max_results
        }
        
        try:
            # Get drug labels
            response = self.session.get(self.endpoints['fda_drugs'], params=label_params)
            response.raise_for_status()
            label_data = response.json()
            
            drugs = []
            if 'results' in label_data:
                for result in label_data['results']:
                    openfda = result.get('openfda', {})
                    drug_info = {
                        'brand_name': openfda.get('brand_name', []),
                        'generic_name': openfda.get('generic_name', []),
                        'manufacturer_name': openfda.get('manufacturer_name', []),
                        'product_type': openfda.get('product_type', []),
                        'route': openfda.get('route', []),
                        'substance_name': openfda.get('substance_name', []),
                        'indications_and_usage': result.get('indications_and_usage', ['Not available']),
                        'dosage_and_administration': result.get('dosage_and_administration', ['Not available']),
                        'contraindications': result.get('contraindications', ['Not available']),
                        'warnings': result.get('warnings', ['Not available']),
                        'adverse_reactions': result.get('adverse_reactions', ['Not available'])
                    }
                    drugs.append(drug_info)
            
            return {
                'drugs': drugs,
                'total_count': len(drugs),
                'query': drug_name
            }
            
        except Exception as e:
            logging.error(f"FDA drug search error: {e}")
            return {'drugs': [], 'total_count': 0, 'error': str(e)}

    def search_nih_reporter(self, project_terms: str, max_results: int = 50,
                           fiscal_year: int = None) -> Dict[str, Any]:
        """
        Search NIH Research Portfolio Online Reporting Tools (RePORTER)
        """
        self._rate_limit('nih_reporter')
        
        # Build search criteria
        criteria = {
            'use_relevance': True,
            'include_active_projects': True,
            'include_historical_projects': True,
            'project_nums': [],
            'text_search': {
                'search_text': project_terms,
                'search_field': 'terms'
            }
        }
        
        if fiscal_year:
            criteria['fiscal_years'] = [fiscal_year]
        
        payload = {
            'criteria': criteria,
            'include_fields': [
                'ProjectNum', 'ProjectTitle', 'AbstractText', 'PrincipalInvestigators',
                'Organization', 'FiscalYear', 'AwardAmount', 'ActivityCode',
                'StudySection', 'FundingMechanism', 'FullStudySection'
            ],
            'offset': 0,
            'limit': max_results
        }
        
        try:
            response = self.session.post(self.endpoints['nih_reporter'], json=payload)
            response.raise_for_status()
            data = response.json()
            
            projects = []
            if 'results' in data:
                for project in data['results']:
                    project_data = {
                        'project_number': project.get('project_num'),
                        'title': project.get('project_title'),
                        'abstract': project.get('abstract_text'),
                        'principal_investigators': [pi.get('full_name') for pi in project.get('principal_investigators', [])],
                        'organization': project.get('organization', {}).get('org_name'),
                        'fiscal_year': project.get('fiscal_year'),
                        'award_amount': project.get('award_amount'),
                        'activity_code': project.get('activity_code'),
                        'study_section': project.get('study_section'),
                        'funding_mechanism': project.get('funding_mechanism')
                    }
                    projects.append(project_data)
            
            return {
                'projects': projects,
                'total_count': data.get('meta', {}).get('total', 0),
                'query': project_terms
            }
            
        except Exception as e:
            logging.error(f"NIH Reporter search error: {e}")
            return {'projects': [], 'total_count': 0, 'error': str(e)}

    def search_uniprot_proteins(self, protein_query: str, max_results: int = 50) -> Dict[str, Any]:
        """
        Search UniProt protein database
        """
        self._rate_limit('uniprot')
        
        params = {
            'query': protein_query,
            'format': 'json',
            'size': max_results,
            'fields': 'accession,id,protein_name,gene_names,organism_name,length,sequence,function_cc,pathway,disease'
        }
        
        try:
            response = self.session.get(self.endpoints['uniprot_proteins'], params=params)
            response.raise_for_status()
            data = response.json()
            
            proteins = []
            if 'results' in data:
                for result in data['results']:
                    protein_data = {
                        'accession': result.get('primaryAccession'),
                        'entry_name': result.get('uniProtkbId'),
                        'protein_name': result.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value'),
                        'gene_names': [gene.get('geneName', {}).get('value') for gene in result.get('genes', []) if gene.get('geneName')],
                        'organism': result.get('organism', {}).get('scientificName'),
                        'length': result.get('sequence', {}).get('length'),
                        'function': [comment.get('texts', [{}])[0].get('value') for comment in result.get('comments', []) if comment.get('commentType') == 'FUNCTION'],
                        'pathways': [comment.get('reaction', {}).get('name') for comment in result.get('comments', []) if comment.get('commentType') == 'CATALYTIC_ACTIVITY'],
                        'diseases': [disease.get('diseaseId') for disease in result.get('features', []) if disease.get('type') == 'VARIANT'],
                        'url': f"https://www.uniprot.org/uniprot/{result.get('primaryAccession')}" if result.get('primaryAccession') else None
                    }
                    proteins.append(protein_data)
            
            return {
                'proteins': proteins,
                'total_count': len(proteins),
                'query': protein_query
            }
            
        except Exception as e:
            logging.error(f"UniProt search error: {e}")
            return {'proteins': [], 'total_count': 0, 'error': str(e)}

    def comprehensive_biomedical_search(self, query: str, databases: List[str] = None,
                                      max_results_per_db: int = 20) -> Dict[str, Any]:
        """
        Perform comprehensive search across multiple biomedical databases
        """
        if databases is None:
            databases = ['pubmed', 'clinicaltrials', 'fda_drugs', 'nih_reporter', 'uniprot']
        
        results = {
            'query': query,
            'search_timestamp': datetime.now().isoformat(),
            'databases_searched': databases,
            'results': {}
        }
        
        # Search each database
        if 'pubmed' in databases:
            results['results']['pubmed'] = self.search_pubmed_enhanced(
                query, max_results_per_db,
                publication_types=['Clinical Trial', 'Randomized Controlled Trial', 'Meta-Analysis']
            )
        
        if 'clinicaltrials' in databases:
            results['results']['clinicaltrials'] = self.search_clinical_trials(
                query, max_results_per_db,
                status=['Recruiting', 'Active, not recruiting', 'Completed']
            )
        
        if 'fda_drugs' in databases:
            results['results']['fda_drugs'] = self.search_fda_drugs(query, max_results_per_db)
        
        if 'nih_reporter' in databases:
            results['results']['nih_reporter'] = self.search_nih_reporter(query, max_results_per_db)
        
        if 'uniprot' in databases:
            results['results']['uniprot'] = self.search_uniprot_proteins(query, max_results_per_db)
        
        # Calculate summary statistics
        total_results = sum([
            results['results'].get(db, {}).get('total_count', 0) 
            for db in databases
        ])
        
        results['summary'] = {
            'total_results_found': total_results,
            'databases_with_results': [
                db for db in databases 
                if results['results'].get(db, {}).get('total_count', 0) > 0
            ],
            'most_productive_database': max(
                databases,
                key=lambda db: results['results'].get(db, {}).get('total_count', 0)
            ) if total_results > 0 else None
        }
        
        return results

    def get_research_trends(self, topic: str, years: List[int] = None) -> Dict[str, Any]:
        """
        Analyze research trends for a specific topic across years
        """
        if years is None:
            current_year = datetime.now().year
            years = list(range(current_year - 5, current_year + 1))
        
        trends = {
            'topic': topic,
            'years_analyzed': years,
            'publication_trends': {},
            'clinical_trial_trends': {},
            'funding_trends': {}
        }
        
        # Analyze publication trends by year
        for year in years:
            pubmed_results = self.search_pubmed_enhanced(
                topic, max_results=100,
                date_range=(f"{year}/01/01", f"{year}/12/31")
            )
            trends['publication_trends'][year] = pubmed_results.get('total_count', 0)
            
            # Add small delay between requests
            time.sleep(0.5)
        
        return trends

# Usage example and testing functions
def test_biomedical_connector():
    """Test the biomedical database connector"""
    connector = BiomedicalDatabaseConnector()
    
    # Test comprehensive search
    test_query = "diabetes"
    results = connector.comprehensive_biomedical_search(
        test_query, 
        databases=['pubmed', 'clinicaltrials'],
        max_results_per_db=5
    )
    
    print(f"Search results for '{test_query}':")
    print(f"Total results: {results['summary']['total_results_found']}")
    print(f"Databases with results: {results['summary']['databases_with_results']}")
    
    return results

if __name__ == "__main__":
    test_biomedical_connector()