"""
Researcher-Facing Dashboard for Synthetic EHR Platform
Provides comprehensive interface for data access, filtering, and validation insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np

from agents.rag_orchestrator import RAGOrchestrator
from agents.adversarial_validation_agent import AdversarialValidationOrchestrator
from agents.multimodal_ehr_agent import MultimodalEHRAgent

def main():
    
    # Initialize session state
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = RAGOrchestrator()
    
    if 'validation_orchestrator' not in st.session_state:
        st.session_state.validation_orchestrator = AdversarialValidationOrchestrator(
            st.session_state.orchestrator.ollama_client
        )
    
    if 'multimodal_agent' not in st.session_state:
        st.session_state.multimodal_agent = MultimodalEHRAgent(
            st.session_state.orchestrator.ollama_client
        )
    
    if 'generated_cohorts' not in st.session_state:
        st.session_state.generated_cohorts = []
    
    if 'validation_results' not in st.session_state:
        st.session_state.validation_results = []
    
    # Main header
    st.title("🏥 Synthetic Ascension Research Dashboard")
    st.markdown("**Advanced Synthetic EHR Generation with Adversarial Validation**")
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        [
            "🚀 Generate Cohorts",
            "📊 Data Explorer", 
            "🔍 Validation Center",
            "⚙️ Agent Configuration",
            "📈 Analytics & Insights",
            "📋 Audit & Transparency"
        ]
    )
    
    # Route to appropriate page
    if page == "🚀 Generate Cohorts":
        show_generation_page()
    elif page == "📊 Data Explorer":
        show_data_explorer()
    elif page == "🔍 Validation Center":
        show_validation_center()
    elif page == "⚙️ Agent Configuration":
        show_agent_configuration()
    elif page == "📈 Analytics & Insights":
        show_analytics_page()
    elif page == "📋 Audit & Transparency":
        show_audit_page()

def show_generation_page():
    """Main cohort generation interface"""
    st.header("🚀 Generate Synthetic Patient Cohorts")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Clinical Research Context")
        
        # Predefined research contexts
        example_contexts = [
            "Simulate late-stage renal failure in Type 2 diabetics with comorbid hypertension",
            "Generate elderly patients with multiple cardiovascular risk factors",
            "Create pediatric cohort with autoimmune conditions requiring immunosuppression",
            "Model patients with treatment-resistant depression and anxiety comorbidities",
            "Simulate acute respiratory failure in COPD patients during exacerbation"
        ]
        
        selected_example = st.selectbox(
            "Quick Start - Select Example Context:",
            [""] + example_contexts
        )
        
        clinical_context = st.text_area(
            "Clinical Research Question/Context:",
            value=selected_example,
            height=100,
            help="Describe the clinical scenario, patient population, or research question you want to simulate"
        )
        
        # Generation parameters
        st.subheader("Generation Parameters")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            cohort_size = st.number_input(
                "Cohort Size",
                min_value=1,
                max_value=100,
                value=10,
                help="Number of synthetic patients to generate"
            )
        
        with col_b:
            include_multimodal = st.checkbox(
                "Include Multimodal Data",
                value=True,
                help="Generate imaging, procedures, and time-series data"
            )
        
        with col_c:
            validation_level = st.selectbox(
                "Validation Strictness",
                ["Lenient", "Standard", "Strict"],
                index=1,
                help="How rigorous should the validation agents be?"
            )
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            include_time_series = st.checkbox("Time-series vitals and labs", value=True)
            include_imaging = st.checkbox("Imaging studies and reports", value=True)
            include_procedures = st.checkbox("Procedures and interventions", value=True)
            
            # Validation agent configuration
            st.subheader("Validation Agent Settings")
            
            skepticism_mapping = {"Lenient": 0.3, "Standard": 0.5, "Strict": 0.8}
            skepticism_level = skepticism_mapping[validation_level]
            
            realism_skepticism = st.slider(
                "Realism Agent Skepticism",
                0.0, 1.0, skepticism_level,
                help="0.0 = Very lenient, 1.0 = Very strict"
            )
            
            relevance_skepticism = st.slider(
                "Relevance Agent Skepticism", 
                0.0, 1.0, skepticism_level,
                help="0.0 = Very lenient, 1.0 = Very strict"
            )
        
        # Generation button
        if st.button("🎯 Generate Synthetic Cohort", type="primary"):
            if not clinical_context.strip():
                st.error("Please provide a clinical context or research question.")
                return
            
            # Configure validation agents
            st.session_state.validation_orchestrator.configure_agent_skepticism(
                'realism', realism_skepticism
            )
            st.session_state.validation_orchestrator.configure_agent_skepticism(
                'relevance', relevance_skepticism
            )
            
            # Progress tracking
            progress_container = st.container()
            progress_bar = progress_container.progress(0)
            status_text = progress_container.empty()
            
            try:
                # Generate cohort
                status_text.text("🔍 Analyzing clinical context and retrieving literature...")
                progress_bar.progress(20)
                
                result = st.session_state.orchestrator.process_query(clinical_context)
                
                status_text.text("👥 Generating synthetic patients...")
                progress_bar.progress(60)
                
                # Generate multimodal data if requested
                if include_multimodal:
                    status_text.text("🏥 Generating multimodal EHR data...")
                    progress_bar.progress(80)
                    
                    enhanced_patients = []
                    for patient in result['synthetic_cohort'].patients:
                        multimodal_data = st.session_state.multimodal_agent.generate_comprehensive_ehr(
                            patient, clinical_context,
                            include_time_series=include_time_series,
                            include_imaging=include_imaging,
                            include_procedures=include_procedures
                        )
                        patient.multimodal_data = multimodal_data
                        enhanced_patients.append(patient)
                    
                    result['synthetic_cohort'].patients = enhanced_patients
                
                # Run validation
                status_text.text("✅ Running adversarial validation...")
                progress_bar.progress(90)
                
                validation_result = st.session_state.validation_orchestrator.validate_cohort(
                    result['synthetic_cohort'], clinical_context
                )
                
                # Store results
                cohort_data = {
                    'id': len(st.session_state.generated_cohorts),
                    'timestamp': datetime.now(),
                    'context': clinical_context,
                    'cohort': result['synthetic_cohort'],
                    'validation': validation_result,
                    'literature': result.get('literature_result'),
                    'parameters': {
                        'size': cohort_size,
                        'multimodal': include_multimodal,
                        'realism_skepticism': realism_skepticism,
                        'relevance_skepticism': relevance_skepticism
                    }
                }
                
                st.session_state.generated_cohorts.append(cohort_data)
                st.session_state.validation_results.append(validation_result)
                
                progress_bar.progress(100)
                status_text.text("🎉 Generation complete!")
                
                # Show results summary
                st.success(f"✅ Successfully generated {len(result['synthetic_cohort'].patients)} synthetic patients!")
                
                # Validation summary
                passed_patients = validation_result['summary']['passed_patients']
                total_patients = validation_result['summary']['total_patients']
                avg_score = validation_result['summary']['average_score']
                
                col_summary1, col_summary2, col_summary3 = st.columns(3)
                
                with col_summary1:
                    st.metric("Validation Pass Rate", f"{passed_patients}/{total_patients}", f"{(passed_patients/total_patients)*100:.1f}%")
                
                with col_summary2:
                    st.metric("Average Quality Score", f"{avg_score:.2f}", "Out of 1.0")
                
                with col_summary3:
                    st.metric("Data Types Generated", len(cohort_data['cohort'].patients[0].multimodal_data) if include_multimodal else 3)
                
                st.info("💡 Navigate to the Data Explorer to examine the generated cohort in detail.")
                
            except Exception as e:
                st.error(f"❌ Generation failed: {str(e)}")
                status_text.text("Generation failed.")
                progress_bar.progress(0)
    
    with col2:
        st.subheader("🎯 Generation Queue")
        
        if st.session_state.generated_cohorts:
            for i, cohort in enumerate(st.session_state.generated_cohorts[-5:]):  # Show last 5
                with st.expander(f"Cohort {cohort['id']} - {cohort['timestamp'].strftime('%H:%M')}"):
                    st.write(f"**Context:** {cohort['context'][:100]}...")
                    st.write(f"**Size:** {len(cohort['cohort'].patients)} patients")
                    st.write(f"**Validation Score:** {cohort['validation']['summary']['average_score']:.2f}")
                    
                    if st.button(f"View Details", key=f"view_{cohort['id']}"):
                        st.session_state.selected_cohort = cohort['id']
                        st.experimental_rerun()
        else:
            st.info("No cohorts generated yet. Create your first synthetic cohort above!")
        
        # Quick stats
        if st.session_state.generated_cohorts:
            st.subheader("📊 Quick Stats")
            total_patients = sum(len(c['cohort'].patients) for c in st.session_state.generated_cohorts)
            avg_validation = np.mean([c['validation']['summary']['average_score'] for c in st.session_state.generated_cohorts])
            
            st.metric("Total Patients Generated", total_patients)
            st.metric("Average Validation Score", f"{avg_validation:.2f}")

def show_data_explorer():
    """Data exploration and filtering interface"""
    st.header("📊 Synthetic EHR Data Explorer")
    
    if not st.session_state.generated_cohorts:
        st.warning("No cohorts available. Generate some data first!")
        return
    
    # Cohort selection
    cohort_options = [f"Cohort {c['id']}: {c['context'][:50]}..." for c in st.session_state.generated_cohorts]
    selected_idx = st.selectbox("Select Cohort to Explore:", range(len(cohort_options)), format_func=lambda x: cohort_options[x])
    
    selected_cohort = st.session_state.generated_cohorts[selected_idx]
    patients = selected_cohort['cohort'].patients
    
    # Filtering controls
    st.subheader("🔍 Filters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        age_range = st.slider(
            "Age Range",
            min_value=0,
            max_value=100,
            value=(0, 100)
        )
    
    with col2:
        gender_filter = st.multiselect(
            "Gender",
            options=list(set(p.gender for p in patients if p.gender)),
            default=list(set(p.gender for p in patients if p.gender))
        )
    
    with col3:
        # Get all unique conditions
        all_conditions = set()
        for p in patients:
            all_conditions.update(p.conditions)
        
        condition_filter = st.multiselect(
            "Conditions",
            options=list(all_conditions),
            default=[]
        )
    
    with col4:
        validation_status = st.selectbox(
            "Validation Status",
            ["All", "Passed Only", "Failed Only"]
        )
    
    # Apply filters
    filtered_patients = []
    validation_data = selected_cohort['validation']['patient_validations']
    
    for patient in patients:
        # Age filter
        if not (age_range[0] <= (patient.age or 0) <= age_range[1]):
            continue
        
        # Gender filter
        if patient.gender not in gender_filter:
            continue
        
        # Condition filter
        if condition_filter and not any(cond in patient.conditions for cond in condition_filter):
            continue
        
        # Validation filter
        if validation_status != "All":
            patient_validation = validation_data.get(patient.patient_id, {})
            passed = patient_validation.get('overall_result', {}).get('passed', True)
            
            if validation_status == "Passed Only" and not passed:
                continue
            elif validation_status == "Failed Only" and passed:
                continue
        
        filtered_patients.append(patient)
    
    st.write(f"**Showing {len(filtered_patients)} of {len(patients)} patients**")
    
    if not filtered_patients:
        st.warning("No patients match the current filters.")
        return
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Patient List", "📊 Demographics", "🔬 Clinical Data", "🏥 Multimodal"])
    
    with tab1:
        show_patient_list(filtered_patients, validation_data)
    
    with tab2:
        show_demographics_analysis(filtered_patients)
    
    with tab3:
        show_clinical_analysis(filtered_patients)
    
    with tab4:
        show_multimodal_data(filtered_patients)

def show_patient_list(patients: List, validation_data: Dict):
    """Show detailed patient list with validation status"""
    
    for i, patient in enumerate(patients):
        with st.expander(f"👤 Patient {patient.patient_id} - {patient.age}yo {patient.gender}"):
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("**Demographics:**")
                st.write(f"Age: {patient.age}, Gender: {patient.gender}, Ethnicity: {patient.ethnicity}")
                
                st.write("**Conditions:**")
                st.write(", ".join(patient.conditions))
                
                st.write("**Medications:**")
                st.write(", ".join(patient.medications))
                
                if patient.lab_results:
                    st.write("**Key Lab Results:**")
                    for lab, (value, unit) in list(patient.lab_results.items())[:5]:
                        st.write(f"• {lab}: {value} {unit}")
            
            with col2:
                # Validation status
                patient_val = validation_data.get(patient.patient_id, {})
                overall_result = patient_val.get('overall_result', {})
                
                if overall_result.get('passed', True):
                    st.success("✅ Validation Passed")
                else:
                    st.error("❌ Validation Failed")
                
                score = overall_result.get('overall_score', 0)
                st.metric("Quality Score", f"{score:.2f}")
                
                # Show validation issues if any
                if 'critical_failures' in overall_result and overall_result['critical_failures']:
                    st.warning("⚠️ Critical Issues:")
                    for issue in overall_result['critical_failures'][:3]:
                        st.write(f"• {issue}")
                
                # Multimodal data indicator
                if hasattr(patient, 'multimodal_data'):
                    st.info("🏥 Multimodal Data Available")
                    
                    if st.button(f"View Multimodal", key=f"multimodal_{patient.patient_id}"):
                        show_patient_multimodal_detail(patient)

def show_demographics_analysis(patients: List):
    """Show demographic analysis charts"""
    
    # Age distribution
    ages = [p.age for p in patients if p.age]
    if ages:
        fig_age = px.histogram(
            x=ages,
            nbins=20,
            title="Age Distribution",
            labels={'x': 'Age', 'y': 'Count'}
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender distribution
        genders = [p.gender for p in patients if p.gender]
        if genders:
            gender_counts = pd.Series(genders).value_counts()
            fig_gender = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                title="Gender Distribution"
            )
            st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # Ethnicity distribution
        ethnicities = [p.ethnicity for p in patients if p.ethnicity]
        if ethnicities:
            ethnicity_counts = pd.Series(ethnicities).value_counts()
            fig_ethnicity = px.bar(
                x=ethnicity_counts.values,
                y=ethnicity_counts.index,
                orientation='h',
                title="Ethnicity Distribution"
            )
            st.plotly_chart(fig_ethnicity, use_container_width=True)

def show_clinical_analysis(patients: List):
    """Show clinical data analysis"""
    
    # Condition prevalence
    all_conditions = []
    for p in patients:
        all_conditions.extend(p.conditions)
    
    if all_conditions:
        condition_counts = pd.Series(all_conditions).value_counts().head(10)
        fig_conditions = px.bar(
            x=condition_counts.values,
            y=condition_counts.index,
            orientation='h',
            title="Most Common Conditions"
        )
        st.plotly_chart(fig_conditions, use_container_width=True)
    
    # Lab value distributions
    st.subheader("🔬 Lab Value Distributions")
    
    # Get all lab types
    all_lab_types = set()
    for p in patients:
        all_lab_types.update(p.lab_results.keys())
    
    if all_lab_types:
        selected_lab = st.selectbox("Select Lab Test:", list(all_lab_types))
        
        lab_values = []
        for p in patients:
            if selected_lab in p.lab_results:
                value, unit = p.lab_results[selected_lab]
                lab_values.append(value)
        
        if lab_values:
            fig_lab = px.histogram(
                x=lab_values,
                nbins=20,
                title=f"{selected_lab} Distribution",
                labels={'x': f'{selected_lab} Value', 'y': 'Count'}
            )
            st.plotly_chart(fig_lab, use_container_width=True)
            
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Mean", f"{np.mean(lab_values):.2f}")
            with col2:
                st.metric("Median", f"{np.median(lab_values):.2f}")
            with col3:
                st.metric("Min", f"{np.min(lab_values):.2f}")
            with col4:
                st.metric("Max", f"{np.max(lab_values):.2f}")

def show_multimodal_data(patients: List):
    """Show multimodal data analysis"""
    
    multimodal_patients = [p for p in patients if hasattr(p, 'multimodal_data')]
    
    if not multimodal_patients:
        st.warning("No multimodal data available for the selected patients.")
        return
    
    st.write(f"**{len(multimodal_patients)} patients have multimodal data**")
    
    # Data type availability
    data_types = {}
    for patient in multimodal_patients:
        if hasattr(patient, 'multimodal_data'):
            for data_type in patient.multimodal_data.get('metadata', {}).get('data_types', []):
                data_types[data_type] = data_types.get(data_type, 0) + 1
    
    if data_types:
        fig_data_types = px.bar(
            x=list(data_types.keys()),
            y=list(data_types.values()),
            title="Multimodal Data Type Availability"
        )
        st.plotly_chart(fig_data_types, use_container_width=True)
    
    # Select patient for detailed view
    if multimodal_patients:
        selected_patient = st.selectbox(
            "Select Patient for Detailed Multimodal View:",
            multimodal_patients,
            format_func=lambda p: f"Patient {p.patient_id}"
        )
        
        if st.button("View Detailed Multimodal Data"):
            show_patient_multimodal_detail(selected_patient)

def show_patient_multimodal_detail(patient):
    """Show detailed multimodal data for a specific patient"""
    
    if not hasattr(patient, 'multimodal_data'):
        st.warning("No multimodal data available for this patient.")
        return
    
    multimodal_data = patient.multimodal_data
    
    st.subheader(f"🏥 Multimodal Data - Patient {patient.patient_id}")
    
    # Clinical notes
    if 'unstructured_data' in multimodal_data:
        st.subheader("📝 Clinical Notes")
        
        notes = multimodal_data['unstructured_data']
        
        if notes.get('admission_note'):
            with st.expander("Admission Note"):
                st.write(notes['admission_note']['content'])
        
        if notes.get('progress_notes'):
            with st.expander(f"Progress Notes ({len(notes['progress_notes'])})"):
                for note in notes['progress_notes']:
                    st.write(f"**Day {note['hospital_day']}:** {note['content'][:200]}...")
    
    # Time series data
    if 'time_series_data' in multimodal_data:
        st.subheader("📈 Time Series Data")
        
        time_series = multimodal_data['time_series_data']
        
        if 'vital_signs' in time_series:
            vitals = time_series['vital_signs']
            
            # Create subplots for vitals
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=['Heart Rate', 'Blood Pressure', 'Temperature', 'Oxygen Saturation']
            )
            
            timestamps = vitals['timestamps']
            
            # Heart rate
            fig.add_trace(
                go.Scatter(x=timestamps, y=vitals['heart_rate'], name='Heart Rate'),
                row=1, col=1
            )
            
            # Blood pressure
            fig.add_trace(
                go.Scatter(x=timestamps, y=vitals['blood_pressure_systolic'], name='Systolic'),
                row=1, col=2
            )
            fig.add_trace(
                go.Scatter(x=timestamps, y=vitals['blood_pressure_diastolic'], name='Diastolic'),
                row=1, col=2
            )
            
            # Temperature
            fig.add_trace(
                go.Scatter(x=timestamps, y=vitals['temperature'], name='Temperature'),
                row=2, col=1
            )
            
            # Oxygen saturation
            fig.add_trace(
                go.Scatter(x=timestamps, y=vitals['oxygen_saturation'], name='SpO2'),
                row=2, col=2
            )
            
            fig.update_layout(height=600, title_text="Vital Signs Over Time")
            st.plotly_chart(fig, use_container_width=True)
    
    # Imaging data
    if 'multimodal_data' in multimodal_data and 'imaging' in multimodal_data['multimodal_data']:
        st.subheader("🔍 Imaging Studies")
        
        imaging = multimodal_data['multimodal_data']['imaging']
        
        for study in imaging.get('studies_ordered', []):
            with st.expander(f"{study['study_type']} - {study['study_date'][:10]}"):
                st.write(f"**Modality:** {study['modality']}")
                st.write(f"**Indication:** {study['indication']}")
                
                # Show report if available
                study_id = study['study_id']
                if study_id in imaging.get('reports', {}):
                    report = imaging['reports'][study_id]
                    st.write("**Report:**")
                    st.write(report['content'])

def show_validation_center():
    """Validation results and agent performance analysis"""
    st.header("🔍 Adversarial Validation Center")
    
    if not st.session_state.validation_results:
        st.warning("No validation results available. Generate some cohorts first!")
        return
    
    # Overall validation statistics
    st.subheader("📊 Validation Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_validations = len(st.session_state.validation_results)
    total_patients = sum(r['summary']['total_patients'] for r in st.session_state.validation_results)
    total_passed = sum(r['summary']['passed_patients'] for r in st.session_state.validation_results)
    avg_score = np.mean([r['summary']['average_score'] for r in st.session_state.validation_results])
    
    with col1:
        st.metric("Total Cohorts Validated", total_validations)
    
    with col2:
        st.metric("Total Patients Validated", total_patients)
    
    with col3:
        st.metric("Overall Pass Rate", f"{(total_passed/total_patients)*100:.1f}%")
    
    with col4:
        st.metric("Average Quality Score", f"{avg_score:.2f}")
    
    # Validation trends
    st.subheader("📈 Validation Trends")
    
    if len(st.session_state.validation_results) > 1:
        cohort_scores = [r['summary']['average_score'] for r in st.session_state.validation_results]
        
        fig_trends = px.line(
            x=range(1, len(cohort_scores) + 1),
            y=cohort_scores,
            title="Quality Score Trends Across Cohorts",
            labels={'x': 'Cohort Number', 'y': 'Average Quality Score'}
        )
        st.plotly_chart(fig_trends, use_container_width=True)
    
    # Agent performance comparison
    st.subheader("🤖 Agent Performance Analysis")
    
    agent_stats = st.session_state.validation_orchestrator.get_validation_statistics()
    
    if 'agent_statistics' in agent_stats:
        agent_data = agent_stats['agent_statistics']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Agent scores
            agent_names = list(agent_data.keys())
            agent_scores = [data['average_score'] for data in agent_data.values()]
            
            fig_agent_scores = px.bar(
                x=agent_names,
                y=agent_scores,
                title="Average Agent Scores"
            )
            st.plotly_chart(fig_agent_scores, use_container_width=True)
        
        with col2:
            # Agent pass rates
            agent_pass_rates = [data['pass_rate'] * 100 for data in agent_data.values()]
            
            fig_pass_rates = px.bar(
                x=agent_names,
                y=agent_pass_rates,
                title="Agent Pass Rates (%)"
            )
            st.plotly_chart(fig_pass_rates, use_container_width=True)
    
    # Common validation issues
    st.subheader("⚠️ Common Validation Issues")
    
    all_issues = []
    for result in st.session_state.validation_results:
        if 'common_issues' in result['summary']:
            all_issues.extend([issue[0] for issue in result['summary']['common_issues']])
    
    if all_issues:
        issue_counts = pd.Series(all_issues).value_counts().head(10)
        
        fig_issues = px.bar(
            x=issue_counts.values,
            y=issue_counts.index,
            orientation='h',
            title="Most Common Validation Issues"
        )
        st.plotly_chart(fig_issues, use_container_width=True)

def show_agent_configuration():
    """Agent configuration and tuning interface"""
    st.header("⚙️ Agent Configuration")
    
    st.subheader("🎚️ Validation Agent Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Realism Agent")
        
        current_realism = st.session_state.validation_orchestrator.validation_agents['realism'].skepticism_level
        
        new_realism_skepticism = st.slider(
            "Realism Agent Skepticism Level",
            0.0, 1.0, current_realism,
            help="Controls how strictly the agent validates medical realism"
        )
        
        st.write("**Realism Agent Focus Areas:**")
        st.write("• Age-condition appropriateness")
        st.write("• Lab value clinical plausibility") 
        st.write("• Medication contraindications")
        st.write("• Comorbidity patterns")
        st.write("• Clinical notes consistency")
    
    with col2:
        st.subheader("Relevance Agent")
        
        current_relevance = st.session_state.validation_orchestrator.validation_agents['relevance'].skepticism_level
        
        new_relevance_skepticism = st.slider(
            "Relevance Agent Skepticism Level",
            0.0, 1.0, current_relevance,
            help="Controls how strictly the agent validates research relevance"
        )
        
        st.write("**Relevance Agent Focus Areas:**")
        st.write("• Condition alignment with research context")
        st.write("• Demographic matching")
        st.write("• Clinical severity appropriateness")
        st.write("• Overall research utility")
    
    # Apply configuration changes
    if st.button("Apply Configuration Changes"):
        st.session_state.validation_orchestrator.configure_agent_skepticism(
            'realism', new_realism_skepticism
        )
        st.session_state.validation_orchestrator.configure_agent_skepticism(
            'relevance', new_relevance_skepticism
        )
        st.success("✅ Agent configuration updated!")
    
    # Agent performance metrics
    st.subheader("📊 Current Agent Performance")
    
    agent_stats = st.session_state.validation_orchestrator.get_validation_statistics()
    
    if agent_stats and 'agent_statistics' in agent_stats:
        for agent_name, stats in agent_stats['agent_statistics'].items():
            with st.expander(f"{agent_name.title()} Agent Performance"):
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("Average Score", f"{stats['average_score']:.2f}")
                
                with col_b:
                    st.metric("Pass Rate", f"{stats['pass_rate']*100:.1f}%")
                
                with col_c:
                    st.metric("Skepticism Level", f"{stats['skepticism_level']:.2f}")

def show_analytics_page():
    """Advanced analytics and insights"""
    st.header("📈 Analytics & Insights")
    
    if not st.session_state.generated_cohorts:
        st.warning("No data available for analysis. Generate some cohorts first!")
        return
    
    # Aggregate all patients across cohorts
    all_patients = []
    for cohort_data in st.session_state.generated_cohorts:
        all_patients.extend(cohort_data['cohort'].patients)
    
    st.subheader(f"📊 Analysis of {len(all_patients)} Total Patients")
    
    # Bias analysis
    st.subheader("⚖️ Bias Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender distribution analysis
        genders = [p.gender for p in all_patients if p.gender]
        if genders:
            gender_counts = pd.Series(genders).value_counts()
            expected_ratio = 0.5  # Expected 50/50 split
            
            fig_bias = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                title="Gender Distribution Analysis"
            )
            
            # Add bias warning if needed
            if len(gender_counts) >= 2:
                ratio = min(gender_counts.values) / max(gender_counts.values)
                if ratio < 0.7:  # If minority group is less than 70% of majority
                    st.warning(f"⚠️ Potential gender bias detected. Ratio: {ratio:.2f}")
                else:
                    st.success("✅ Gender distribution appears balanced")
            
            st.plotly_chart(fig_bias, use_container_width=True)
    
    with col2:
        # Age distribution bias
        ages = [p.age for p in all_patients if p.age]
        if ages:
            fig_age_dist = px.histogram(
                x=ages,
                nbins=15,
                title="Age Distribution Analysis"
            )
            st.plotly_chart(fig_age_dist, use_container_width=True)
            
            # Age bias analysis
            age_groups = {
                'Young (18-40)': sum(1 for age in ages if 18 <= age <= 40),
                'Middle (41-64)': sum(1 for age in ages if 41 <= age <= 64),
                'Senior (65+)': sum(1 for age in ages if age >= 65)
            }
            
            most_represented = max(age_groups.values())
            least_represented = min(age_groups.values())
            
            if most_represented > 0 and least_represented / most_represented < 0.3:
                st.warning("⚠️ Potential age bias detected across groups")
            else:
                st.success("✅ Age distribution appears reasonably balanced")
    
    # Clinical complexity analysis
    st.subheader("🏥 Clinical Complexity Analysis")
    
    complexity_scores = []
    for patient in all_patients:
        # Calculate complexity based on number of conditions, medications, abnormal labs
        complexity = 0
        complexity += len(patient.conditions) * 0.3
        complexity += len(patient.medications) * 0.2
        
        # Factor in lab abnormalities
        abnormal_labs = 0
        for lab_name, (value, unit) in patient.lab_results.items():
            if lab_name.lower() == 'glucose' and (value < 70 or value > 140):
                abnormal_labs += 1
            elif lab_name.lower() == 'creatinine' and value > 1.3:
                abnormal_labs += 1
        
        complexity += abnormal_labs * 0.1
        complexity_scores.append(min(complexity, 3.0))  # Cap at 3.0
    
    if complexity_scores:
        fig_complexity = px.histogram(
            x=complexity_scores,
            nbins=20,
            title="Patient Clinical Complexity Distribution"
        )
        st.plotly_chart(fig_complexity, use_container_width=True)
        
        avg_complexity = np.mean(complexity_scores)
        st.metric("Average Clinical Complexity", f"{avg_complexity:.2f}", "Out of 3.0")

def show_audit_page():
    """Audit trail and transparency interface"""
    st.header("📋 Audit & Transparency")
    
    st.subheader("🔍 System Audit Trail")
    
    if st.session_state.generated_cohorts:
        # Generation audit log
        st.subheader("📝 Generation History")
        
        audit_data = []
        for cohort_data in st.session_state.generated_cohorts:
            audit_data.append({
                'Timestamp': cohort_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                'Cohort ID': cohort_data['id'],
                'Context': cohort_data['context'][:100] + '...',
                'Patients': len(cohort_data['cohort'].patients),
                'Validation Score': f"{cohort_data['validation']['summary']['average_score']:.2f}",
                'Pass Rate': f"{(cohort_data['validation']['summary']['passed_patients'] / cohort_data['validation']['summary']['total_patients']) * 100:.1f}%"
            })
        
        audit_df = pd.DataFrame(audit_data)
        st.dataframe(audit_df, use_container_width=True)
        
        # Export functionality
        if st.button("📥 Export Audit Log"):
            csv = audit_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"synthetic_ehr_audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    # System configuration audit
    st.subheader("⚙️ System Configuration")
    
    config_info = {
        'Validation Agents': list(st.session_state.validation_orchestrator.validation_agents.keys()),
        'Realism Agent Skepticism': st.session_state.validation_orchestrator.validation_agents['realism'].skepticism_level,
        'Relevance Agent Skepticism': st.session_state.validation_orchestrator.validation_agents['relevance'].skepticism_level,
        'Total Cohorts Generated': len(st.session_state.generated_cohorts),
        'Total Validations Performed': len(st.session_state.validation_results)
    }
    
    for key, value in config_info.items():
        st.write(f"**{key}:** {value}")
    
    # Data provenance
    st.subheader("🔗 Data Provenance")
    
    st.write("""
    **Data Generation Methodology:**
    - Literature-based context analysis using RAG
    - Ollama LLM for synthetic patient generation
    - Multi-agent validation with configurable skepticism
    - Comprehensive audit logging for full traceability
    
    **Validation Process:**
    - Realism Agent: Medical plausibility validation
    - Relevance Agent: Research context alignment
    - Statistical validation: Demographic and clinical distribution analysis
    - Medical terminology validation: Clinical accuracy assessment
    
    **Privacy & Compliance:**
    - All processing performed locally using Ollama
    - No external API calls for patient data generation
    - Complete audit trail maintained
    - Synthetic data only - no real patient information used
    """)

if __name__ == "__main__":
    main()