"""
Biomedical Research Dashboard for Synthetic Ascension
Comprehensive interface for biomedical database search and analysis
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import asyncio

# Page configuration
st.set_page_config(
    page_title="Biomedical Research - Synthetic Ascension",
    page_icon="🔬",
    layout="wide"
)

def display_header():
    """Display the page header with branding"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #0A1F44; margin-bottom: 0.5rem;">🔬 Biomedical Research Hub</h1>
        <p style="color: #6B4EFF; font-size: 1.2rem; margin: 0;">
            Access 5+ medical databases with AI-powered analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

def comprehensive_search_interface():
    """Interface for comprehensive biomedical database search"""
    st.header("🌐 Comprehensive Database Search")
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            query = st.text_input(
                "Research Query",
                placeholder="e.g., diabetes type 2, breast cancer immunotherapy, COVID-19 vaccines",
                help="Enter your research topic to search across multiple biomedical databases"
            )
        
        with col2:
            max_results = st.slider("Results per database", 5, 50, 20)
        
        # Database selection
        st.subheader("📚 Select Databases")
        database_options = {
            "PubMed": "pubmed",
            "ClinicalTrials.gov": "clinicaltrials", 
            "FDA Drug Labels": "fda_drugs",
            "NIH Reporter": "nih_reporter",
            "UniProt Proteins": "uniprot"
        }
        
        selected_databases = []
        cols = st.columns(len(database_options))
        
        for i, (display_name, db_code) in enumerate(database_options.items()):
            with cols[i]:
                if st.checkbox(display_name, value=True, key=f"db_{db_code}"):
                    selected_databases.append(db_code)
        
        if st.button("🔍 Search All Databases", type="primary"):
            if query and selected_databases:
                with st.spinner("Searching biomedical databases..."):
                    try:
                        # API call to comprehensive search endpoint
                        api_url = "http://localhost:8000/biomedical/comprehensive-search"
                        payload = {
                            "query": query,
                            "databases": selected_databases,
                            "max_results_per_db": max_results
                        }
                        
                        response = requests.post(api_url, json=payload)
                        
                        if response.status_code == 200:
                            results = response.json()
                            display_comprehensive_results(results)
                        else:
                            st.error(f"Search failed: {response.text}")
                            
                    except requests.exceptions.ConnectionError:
                        st.error("⚠️ Could not connect to API server. Please ensure the API server is running on port 8000.")
                    except Exception as e:
                        st.error(f"Search error: {str(e)}")
            else:
                st.warning("Please enter a query and select at least one database.")

def display_comprehensive_results(results):
    """Display comprehensive search results with visualizations"""
    st.success("✅ Search completed successfully!")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    query_meta = results.get('query_metadata', {})
    search_results = results.get('results', {}).get('results', {})
    summary = results.get('results', {}).get('summary', {})
    
    with col1:
        st.metric("Total Results", summary.get('total_results_found', 0))
    
    with col2:
        st.metric("Databases Searched", len(query_meta.get('databases_searched', [])))
    
    with col3:
        databases_with_results = summary.get('databases_with_results', [])
        st.metric("Databases with Results", len(databases_with_results))
    
    with col4:
        most_productive = summary.get('most_productive_database', 'N/A')
        st.metric("Most Productive DB", most_productive.replace('_', ' ').title() if most_productive != 'N/A' else 'N/A')
    
    # Results breakdown chart
    if search_results:
        st.subheader("📊 Results Distribution")
        
        db_counts = {}
        for db_name, db_data in search_results.items():
            db_counts[db_name.replace('_', ' ').title()] = db_data.get('total_count', 0)
        
        if any(count > 0 for count in db_counts.values()):
            fig = px.bar(
                x=list(db_counts.keys()),
                y=list(db_counts.values()),
                title="Results by Database",
                color=list(db_counts.values()),
                color_continuous_scale="Viridis"
            )
            fig.update_layout(
                xaxis_title="Database",
                yaxis_title="Number of Results",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Detailed results by database
    st.subheader("📋 Detailed Results")
    
    for db_name, db_data in search_results.items():
        if db_data.get('total_count', 0) > 0:
            with st.expander(f"{db_name.replace('_', ' ').title()} - {db_data.get('total_count', 0)} results"):
                display_database_specific_results(db_name, db_data)

def display_database_specific_results(db_name, db_data):
    """Display results specific to each database"""
    
    if db_name == 'pubmed':
        articles = db_data.get('articles', [])
        if articles:
            for i, article in enumerate(articles[:5]):  # Show first 5
                st.markdown(f"**{i+1}. {article.get('title', 'No title')}**")
                st.markdown(f"*Authors:* {', '.join(article.get('authors', [])[:3])}")
                st.markdown(f"*Journal:* {article.get('journal', 'Unknown')} ({article.get('year', 'Unknown')})")
                if article.get('abstract'):
                    st.markdown(f"*Abstract:* {article['abstract'][:200]}...")
                if article.get('url'):
                    st.markdown(f"[View on PubMed]({article['url']})")
                st.divider()
    
    elif db_name == 'clinicaltrials':
        studies = db_data.get('studies', [])
        if studies:
            for i, study in enumerate(studies[:5]):  # Show first 5
                st.markdown(f"**{i+1}. {study.get('brief_title', 'No title')}**")
                st.markdown(f"*NCT ID:* {study.get('nct_id', 'Unknown')}")
                st.markdown(f"*Status:* {study.get('status', 'Unknown')}")
                st.markdown(f"*Phase:* {study.get('phase', 'Unknown')}")
                if study.get('summary'):
                    st.markdown(f"*Summary:* {study['summary'][:200]}...")
                if study.get('url'):
                    st.markdown(f"[View on ClinicalTrials.gov]({study['url']})")
                st.divider()
    
    elif db_name == 'fda_drugs':
        drugs = db_data.get('drugs', [])
        if drugs:
            for i, drug in enumerate(drugs[:5]):  # Show first 5
                brand_names = ', '.join(drug.get('brand_name', ['Unknown']))
                generic_names = ', '.join(drug.get('generic_name', ['Unknown']))
                st.markdown(f"**{i+1}. {brand_names}**")
                st.markdown(f"*Generic Name:* {generic_names}")
                manufacturers = ', '.join(drug.get('manufacturer_name', ['Unknown']))
                st.markdown(f"*Manufacturer:* {manufacturers}")
                routes = ', '.join(drug.get('route', ['Unknown']))
                st.markdown(f"*Route:* {routes}")
                st.divider()
    
    elif db_name == 'nih_reporter':
        projects = db_data.get('projects', [])
        if projects:
            for i, project in enumerate(projects[:5]):  # Show first 5
                st.markdown(f"**{i+1}. {project.get('title', 'No title')}**")
                st.markdown(f"*Project Number:* {project.get('project_number', 'Unknown')}")
                st.markdown(f"*Organization:* {project.get('organization', 'Unknown')}")
                st.markdown(f"*Fiscal Year:* {project.get('fiscal_year', 'Unknown')}")
                if project.get('award_amount'):
                    st.markdown(f"*Award Amount:* ${project['award_amount']:,}")
                if project.get('abstract'):
                    st.markdown(f"*Abstract:* {project['abstract'][:200]}...")
                st.divider()
    
    elif db_name == 'uniprot':
        proteins = db_data.get('proteins', [])
        if proteins:
            for i, protein in enumerate(proteins[:5]):  # Show first 5
                st.markdown(f"**{i+1}. {protein.get('protein_name', 'No name')}**")
                st.markdown(f"*Accession:* {protein.get('accession', 'Unknown')}")
                st.markdown(f"*Organism:* {protein.get('organism', 'Unknown')}")
                if protein.get('gene_names'):
                    st.markdown(f"*Gene Names:* {', '.join(protein['gene_names'])}")
                if protein.get('length'):
                    st.markdown(f"*Length:* {protein['length']} amino acids")
                if protein.get('url'):
                    st.markdown(f"[View on UniProt]({protein['url']})")
                st.divider()

def enhanced_literature_interface():
    """Interface for enhanced literature search with AI analysis"""
    st.header("🤖 Enhanced Literature Analysis")
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            query = st.text_input(
                "Research Topic",
                placeholder="e.g., Alzheimer disease treatment, cancer immunotherapy",
                help="Enter a research topic for AI-powered literature analysis",
                key="enhanced_query"
            )
        
        with col2:
            max_results = st.slider("Results per source", 10, 50, 25, key="enhanced_results")
        
        # Analysis options
        st.subheader("🎯 Analysis Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_trials = st.checkbox("Include Clinical Trials", value=True)
        with col2:
            include_drugs = st.checkbox("Include Drug Data", value=True)
        with col3:
            include_proteins = st.checkbox("Include Protein Data", value=False)
        
        if st.button("🧠 Analyze Literature", type="primary", key="enhanced_search"):
            if query:
                with st.spinner("Performing AI-powered literature analysis..."):
                    try:
                        api_url = "http://localhost:8000/biomedical/enhanced-literature-search"
                        payload = {
                            "query": query,
                            "max_results_per_source": max_results,
                            "include_clinical_trials": include_trials,
                            "include_drug_data": include_drugs,
                            "include_protein_data": include_proteins
                        }
                        
                        response = requests.post(api_url, json=payload)
                        
                        if response.status_code == 200:
                            results = response.json()
                            display_enhanced_analysis(results)
                        else:
                            st.error(f"Analysis failed: {response.text}")
                            
                    except requests.exceptions.ConnectionError:
                        st.error("⚠️ Could not connect to API server. Please ensure the API server is running on port 8000.")
                    except Exception as e:
                        st.error(f"Analysis error: {str(e)}")
            else:
                st.warning("Please enter a research topic.")

def display_enhanced_analysis(results):
    """Display enhanced literature analysis results"""
    st.success("✅ AI analysis completed!")
    
    analysis_summary = results.get('analysis_summary', {})
    enhanced_results = results.get('enhanced_results', {})
    
    # Analysis summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Sources Analyzed", analysis_summary.get('total_sources', 0))
    
    with col2:
        st.metric("Research Themes", analysis_summary.get('research_themes_found', 0))
    
    with col3:
        evidence_strength = analysis_summary.get('evidence_strength', 'unknown')
        st.metric("Evidence Strength", evidence_strength.title())
    
    with col4:
        clinical_maturity = analysis_summary.get('clinical_maturity', 'unknown')
        st.metric("Clinical Maturity", clinical_maturity.split(' - ')[0] if ' - ' in clinical_maturity else clinical_maturity)
    
    # Research themes visualization
    research_themes = enhanced_results.get('research_themes', {})
    if research_themes.get('top_research_themes'):
        st.subheader("🎯 Key Research Themes")
        
        themes_data = research_themes['top_research_themes']
        if len(themes_data) > 0:
            themes_df = pd.DataFrame(themes_data)
            
            fig = px.bar(
                themes_df.head(10),
                x='frequency',
                y='theme',
                orientation='h',
                title="Top Research Themes by Frequency",
                color='frequency',
                color_continuous_scale="Blues"
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
    
    # Cross-database insights
    cross_insights = enhanced_results.get('cross_database_insights', {})
    if cross_insights:
        st.subheader("🔗 Cross-Database Insights")
        
        # Research to clinical translation
        translation_gap = cross_insights.get('research_to_clinical_gap', {})
        if translation_gap:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Research-to-Clinical Translation**")
                research_articles = translation_gap.get('research_articles', 0)
                clinical_trials = translation_gap.get('clinical_trials', 0)
                translation_ratio = translation_gap.get('translation_ratio', 0)
                assessment = translation_gap.get('translation_assessment', 'Unknown')
                
                st.metric("Research Articles", research_articles)
                st.metric("Clinical Trials", clinical_trials)
                st.metric("Translation Ratio", f"{translation_ratio:.3f}")
                st.info(f"Assessment: {assessment}")
            
            with col2:
                # Create a simple gauge chart for translation ratio
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = translation_ratio * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Translation %"},
                    gauge = {
                        'axis': {'range': [None, 50]},
                        'bar': {'color': "#6B4EFF"},
                        'steps': [
                            {'range': [0, 10], 'color': "#ffebee"},
                            {'range': [10, 20], 'color': "#e3f2fd"},
                            {'range': [20, 50], 'color': "#e8f5e8"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
    
    # Evidence quality assessment
    evidence_quality = enhanced_results.get('evidence_quality', {})
    if evidence_quality.get('quality_distribution'):
        st.subheader("📊 Evidence Quality Assessment")
        
        quality_dist = evidence_quality['quality_distribution']
        quality_df = pd.DataFrame([
            {'Quality Level': 'High Quality', 'Count': quality_dist.get('high', 0)},
            {'Quality Level': 'Medium Quality', 'Count': quality_dist.get('medium', 0)},
            {'Quality Level': 'Standard', 'Count': quality_dist.get('standard', 0)}
        ])
        
        fig = px.pie(
            quality_df,
            values='Count',
            names='Quality Level',
            title="Evidence Quality Distribution",
            color_discrete_map={
                'High Quality': '#34C759',
                'Medium Quality': '#6B4EFF',
                'Standard': '#0A1F44'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

def disease_profile_interface():
    """Interface for comprehensive disease profiling"""
    st.header("🏥 Disease Research Profile")
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            disease = st.text_input(
                "Disease Name",
                placeholder="e.g., Alzheimer disease, Type 2 diabetes, Breast cancer",
                help="Enter a disease name for comprehensive research profiling",
                key="disease_query"
            )
        
        with col2:
            st.write("") # Spacer
        
        # Profile options
        col1, col2 = st.columns(2)
        with col1:
            include_genetics = st.checkbox("Include Genetics Research", value=True)
        with col2:
            include_treatments = st.checkbox("Include Treatment Research", value=True)
        
        if st.button("🔬 Generate Disease Profile", type="primary", key="disease_profile"):
            if disease:
                with st.spinner("Generating comprehensive disease profile..."):
                    try:
                        api_url = "http://localhost:8000/biomedical/disease-profile"
                        payload = {
                            "disease": disease,
                            "include_genetics": include_genetics,
                            "include_treatments": include_treatments
                        }
                        
                        response = requests.post(api_url, json=payload)
                        
                        if response.status_code == 200:
                            results = response.json()
                            display_disease_profile(results)
                        else:
                            st.error(f"Profile generation failed: {response.text}")
                            
                    except requests.exceptions.ConnectionError:
                        st.error("⚠️ Could not connect to API server. Please ensure the API server is running on port 8000.")
                    except Exception as e:
                        st.error(f"Profile error: {str(e)}")
            else:
                st.warning("Please enter a disease name.")

def display_disease_profile(results):
    """Display comprehensive disease profile"""
    disease_profile = results.get('disease_profile', {})
    profile_summary = results.get('profile_summary', {})
    
    st.success(f"✅ Disease profile generated for: {disease_profile.get('disease', 'Unknown')}")
    
    # Profile summary cards
    st.subheader("📋 Disease Profile Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Research Maturity**")
        research_maturity = profile_summary.get('research_maturity', 'Unknown')
        st.info(research_maturity)
        
        st.markdown("**Genetic Understanding**")
        genetic_understanding = profile_summary.get('genetic_understanding', 'Unknown')
        st.info(genetic_understanding)
    
    with col2:
        st.markdown("**Clinical Pipeline Strength**")
        clinical_pipeline = profile_summary.get('clinical_pipeline_strength', 'Unknown')
        st.info(clinical_pipeline)
        
        st.markdown("**Treatment Landscape**")
        treatment_landscape = profile_summary.get('treatment_landscape', 'Unknown')
        st.info(treatment_landscape)
    
    # Comprehensive overview metrics
    comprehensive_overview = disease_profile.get('comprehensive_overview', {})
    if comprehensive_overview:
        search_meta = comprehensive_overview.get('search_metadata', {})
        st.subheader("🔍 Research Overview")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Results Found", search_meta.get('total_results', 0))
        with col2:
            databases_searched = len(search_meta.get('databases_searched', []))
            st.metric("Databases Searched", databases_searched)
        with col3:
            timestamp = search_meta.get('search_timestamp', '')
            if timestamp:
                st.metric("Generated", timestamp.split('T')[0])

def database_status_interface():
    """Interface for checking database connectivity status"""
    st.header("🌐 Database Status Monitor")
    
    if st.button("🔄 Check Database Status", type="primary"):
        with st.spinner("Checking database connectivity..."):
            try:
                api_url = "http://localhost:8000/biomedical/databases/status"
                response = requests.get(api_url)
                
                if response.status_code == 200:
                    status_data = response.json()
                    display_database_status(status_data)
                else:
                    st.error(f"Status check failed: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("⚠️ Could not connect to API server. Please ensure the API server is running on port 8000.")
            except Exception as e:
                st.error(f"Status check error: {str(e)}")

def display_database_status(status_data):
    """Display database connectivity status"""
    overall_status = status_data.get('overall_status', 'unknown')
    individual_dbs = status_data.get('individual_databases', {})
    available_dbs = status_data.get('available_databases', [])
    
    # Overall status
    if overall_status == 'healthy':
        st.success(f"✅ All databases are healthy ({len(available_dbs)}/{len(individual_dbs)} connected)")
    else:
        st.warning(f"⚠️ Some databases are experiencing issues ({len(available_dbs)}/{len(individual_dbs)} connected)")
    
    # Individual database status
    st.subheader("Database Status Details")
    
    for db_name, db_status in individual_dbs.items():
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            display_name = db_name.replace('_', ' ').title()
            st.write(f"**{display_name}**")
        
        with col2:
            if db_status['status'] == 'connected':
                st.success("✅ Connected")
            else:
                st.error("❌ Error")
        
        with col3:
            if db_status['status'] == 'connected':
                test_results = db_status.get('test_results', 0)
                st.write(f"Test query returned {test_results} results")
            else:
                error_msg = db_status.get('message', 'Unknown error')
                st.write(f"Error: {error_msg}")

def main():
    """Main dashboard function"""
    display_header()
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌐 Multi-Database Search",
        "🤖 AI Literature Analysis", 
        "🏥 Disease Profiling",
        "🔧 Database Status"
    ])
    
    with tab1:
        comprehensive_search_interface()
    
    with tab2:
        enhanced_literature_interface()
    
    with tab3:
        disease_profile_interface()
    
    with tab4:
        database_status_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #666;">
        <p>Synthetic Ascension Biomedical Research Hub | Powered by 5+ Medical Databases</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()