import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from agents.rag_orchestrator import RAGOrchestrator
from models.patient_data import PatientCohort
from models.literature_data import LiteratureResult

# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = RAGOrchestrator()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_cohort' not in st.session_state:
    st.session_state.current_cohort = None
if 'current_literature' not in st.session_state:
    st.session_state.current_literature = None

def main():
    st.title("🧬 Synthetic Ascension")
    st.markdown("### Literature-backed synthetic patient cohorts for AI research")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model settings
        st.subheader("Model Settings")
        model_name = st.selectbox(
            "LLM Model",
            ["mistral:latest", "llama2:latest", "codellama:latest"],
            help="Select the Ollama model for text generation"
        )
        
        # Cohort settings
        st.subheader("Cohort Settings")
        cohort_size = st.slider("Cohort Size", 10, 1000, 100)
        include_notes = st.checkbox("Include Clinical Notes", True)
        include_labs = st.checkbox("Include Lab Results", True)
        
        # Literature settings
        st.subheader("Literature Settings")
        max_papers = st.slider("Max Papers to Retrieve", 5, 50, 20)
        include_preprints = st.checkbox("Include Preprints (bioRxiv)", True)
        
        # Update orchestrator settings
        st.session_state.orchestrator.update_settings({
            'model_name': model_name,
            'cohort_size': cohort_size,
            'include_notes': include_notes,
            'include_labs': include_labs,
            'max_papers': max_papers,
            'include_preprints': include_preprints
        })
    
    # Main chat interface
    st.header("💬 Research Query")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Enter your research query (e.g., 'How does drug X affect women with hypertension and diabetes?')"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process the query
        with st.chat_message("assistant"):
            with st.spinner("Processing your query..."):
                try:
                    # Create progress container
                    progress_container = st.container()
                    
                    # Process query through RAG orchestrator
                    result = st.session_state.orchestrator.process_query(
                        prompt, 
                        progress_callback=lambda msg: progress_container.info(msg)
                    )
                    
                    # Clear progress container
                    progress_container.empty()
                    
                    # Display results
                    st.markdown("### 📊 Analysis Complete")
                    
                    # Summary
                    if result.get('summary'):
                        st.markdown("**Summary:**")
                        st.markdown(result['summary'])
                    
                    # Literature findings
                    if result.get('literature'):
                        st.session_state.current_literature = result['literature']
                        st.markdown(f"**Literature Review:** Found {len(result['literature'].papers)} relevant papers")
                    
                    # Synthetic cohort
                    if result.get('cohort'):
                        st.session_state.current_cohort = result['cohort']
                        st.markdown(f"**Synthetic Cohort:** Generated {len(result['cohort'].patients)} patients")
                    
                    # Critique
                    if result.get('critique'):
                        st.markdown("**Validation:**")
                        st.markdown(result['critique'])
                    
                    # Store assistant response
                    response_content = f"Analysis complete! Generated {len(result['cohort'].patients) if result.get('cohort') else 0} synthetic patients based on {len(result['literature'].papers) if result.get('literature') else 0} literature sources."
                    st.session_state.messages.append({"role": "assistant", "content": response_content})
                    
                except Exception as e:
                    error_msg = f"Error processing query: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Results tabs
    if st.session_state.current_cohort or st.session_state.current_literature:
        st.header("📋 Results")
        
        tabs = []
        if st.session_state.current_literature:
            tabs.append("Literature")
        if st.session_state.current_cohort:
            tabs.extend(["Cohort Overview", "Patient Details"])
        
        if tabs:
            tab_objects = st.tabs(tabs)
            tab_idx = 0
            
            # Literature tab
            if st.session_state.current_literature:
                with tab_objects[tab_idx]:
                    display_literature_results(st.session_state.current_literature)
                tab_idx += 1
            
            # Cohort tabs
            if st.session_state.current_cohort:
                with tab_objects[tab_idx]:
                    display_cohort_overview(st.session_state.current_cohort)
                tab_idx += 1
                
                with tab_objects[tab_idx]:
                    display_patient_details(st.session_state.current_cohort)

def display_literature_results(literature_result):
    """Display literature search results"""
    st.subheader(f"📚 Literature Review ({len(literature_result.papers)} papers)")
    
    # Summary stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Papers", len(literature_result.papers))
    with col2:
        pubmed_count = sum(1 for p in literature_result.papers if p.source == "pubmed")
        st.metric("PubMed", pubmed_count)
    with col3:
        biorxiv_count = sum(1 for p in literature_result.papers if p.source == "biorxiv")
        st.metric("bioRxiv", biorxiv_count)
    
    # Papers table
    if literature_result.papers:
        papers_data = []
        for paper in literature_result.papers:
            papers_data.append({
                "Title": paper.title,
                "Authors": paper.authors,
                "Year": paper.publication_date.year if paper.publication_date else "N/A",
                "Source": paper.source.upper(),
                "Relevance": f"{paper.relevance_score:.2f}",
                "URL": paper.url
            })
        
        papers_df = pd.DataFrame(papers_data)
        st.dataframe(papers_df, use_container_width=True)
        
        # Export button
        if st.button("📥 Export Literature Summary"):
            export_literature(literature_result)

def display_cohort_overview(cohort):
    """Display synthetic cohort overview"""
    st.subheader(f"👥 Synthetic Cohort Overview ({len(cohort.patients)} patients)")
    
    # Basic demographics
    ages = [p.age for p in cohort.patients if p.age]
    genders = [p.gender for p in cohort.patients if p.gender]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Patients", len(cohort.patients))
    with col2:
        avg_age = sum(ages) / len(ages) if ages else 0
        st.metric("Average Age", f"{avg_age:.1f}")
    with col3:
        female_count = sum(1 for g in genders if g.lower() == 'female')
        st.metric("Female", female_count)
    with col4:
        male_count = sum(1 for g in genders if g.lower() == 'male')
        st.metric("Male", male_count)
    
    # Age distribution
    if ages:
        st.subheader("Age Distribution")
        age_df = pd.DataFrame({'Age': ages})
        st.bar_chart(age_df['Age'].value_counts().sort_index())
    
    # Conditions summary
    all_conditions = []
    for patient in cohort.patients:
        all_conditions.extend(patient.conditions)
    
    if all_conditions:
        st.subheader("Most Common Conditions")
        condition_counts = pd.Series(all_conditions).value_counts().head(10)
        st.bar_chart(condition_counts)
    
    # Export button
    if st.button("📥 Export Cohort Data"):
        export_cohort(cohort)

def display_patient_details(cohort):
    """Display detailed patient information"""
    st.subheader("🔍 Patient Details")
    
    # Patient selector
    patient_options = [f"Patient {i+1} - {p.patient_id}" for i, p in enumerate(cohort.patients)]
    selected_patient_idx = st.selectbox("Select Patient", range(len(patient_options)), format_func=lambda x: patient_options[x])
    
    if selected_patient_idx is not None:
        patient = cohort.patients[selected_patient_idx]
        
        # Basic info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**ID:** {patient.patient_id}")
            st.write(f"**Age:** {patient.age}")
        with col2:
            st.write(f"**Gender:** {patient.gender}")
            st.write(f"**Ethnicity:** {patient.ethnicity}")
        with col3:
            st.write(f"**Created:** {patient.created_at.strftime('%Y-%m-%d')}")
        
        # Conditions
        if patient.conditions:
            st.subheader("Medical Conditions")
            for condition in patient.conditions:
                st.write(f"• {condition}")
        
        # Medications
        if patient.medications:
            st.subheader("Medications")
            for medication in patient.medications:
                st.write(f"• {medication}")
        
        # Lab results
        if patient.lab_results:
            st.subheader("Lab Results")
            lab_df = pd.DataFrame([
                {"Test": test, "Value": value, "Unit": unit}
                for test, (value, unit) in patient.lab_results.items()
            ])
            st.dataframe(lab_df, use_container_width=True)
        
        # Clinical notes
        if patient.clinical_notes:
            st.subheader("Clinical Notes")
            for i, note in enumerate(patient.clinical_notes):
                with st.expander(f"Note {i+1} - {note['date']}"):
                    st.write(f"**Type:** {note['type']}")
                    st.write(f"**Provider:** {note['provider']}")
                    st.write(note['content'])

def export_literature(literature_result):
    """Export literature results to JSON"""
    export_data = {
        "export_timestamp": datetime.now().isoformat(),
        "total_papers": len(literature_result.papers),
        "papers": [
            {
                "title": paper.title,
                "authors": paper.authors,
                "abstract": paper.abstract,
                "publication_date": paper.publication_date.isoformat() if paper.publication_date else None,
                "source": paper.source,
                "url": paper.url,
                "relevance_score": paper.relevance_score,
                "key_findings": paper.key_findings
            }
            for paper in literature_result.papers
        ]
    }
    
    filename = f"literature_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    st.download_button(
        label="Download Literature JSON",
        data=json.dumps(export_data, indent=2),
        file_name=filename,
        mime="application/json"
    )

def export_cohort(cohort):
    """Export cohort data to CSV and JSON"""
    # CSV export for tabular data
    csv_data = []
    for patient in cohort.patients:
        row = {
            "patient_id": patient.patient_id,
            "age": patient.age,
            "gender": patient.gender,
            "ethnicity": patient.ethnicity,
            "conditions": "; ".join(patient.conditions),
            "medications": "; ".join(patient.medications),
            "created_at": patient.created_at.isoformat()
        }
        
        # Add lab results as separate columns
        for test, (value, unit) in patient.lab_results.items():
            row[f"lab_{test}"] = f"{value} {unit}"
        
        csv_data.append(row)
    
    csv_df = pd.DataFrame(csv_data)
    
    # JSON export for complete data
    json_data = {
        "export_timestamp": datetime.now().isoformat(),
        "cohort_size": len(cohort.patients),
        "generation_parameters": cohort.generation_parameters,
        "patients": [patient.to_dict() for patient in cohort.patients]
    }
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download CSV",
            data=csv_df.to_csv(index=False),
            file_name=f"cohort_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        st.download_button(
            label="Download JSON",
            data=json.dumps(json_data, indent=2),
            file_name=f"cohort_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()
