"""
Cohort Results Dashboard with Agent Reasoning and Individual EHR Browser
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json

from agents.pediatric_cardiology_enhanced_generator import PediatricCardiologyGenerator
from agents.advanced_clinical_configuration import AdvancedClinicalConfigurator
from utils.traceability_framework import TraceableDecision, ComponentType, DecisionType, ContextSource

def main():
    st.title("🫀 Pediatric Cardiology Cohort Results")
    st.markdown("**Complete cohort analysis with agent reasoning and individual EHR browser**")
    
    # Check if we have cohort data from generation
    if 'cohort_results' not in st.session_state:
        st.warning("⚠️ No cohort data found. Please generate a cohort first.")
        if st.button("↩️ Back to Cohort Generator"):
            st.session_state.current_page = "pediatric_demo"
            st.rerun()
        return
    
    cohort_data = st.session_state.cohort_results
    
    # Main navigation tabs
    config_tab, reasoning_tab, matrix_tab, ehr_tab = st.tabs([
        "⚙️ Configuration", "🧠 Agent Reasoning", "📊 Patient Matrix", "📋 Individual EHR"
    ])
    
    with config_tab:
        display_cohort_configuration(cohort_data)
    
    with reasoning_tab:
        display_agent_reasoning(cohort_data)
    
    with matrix_tab:
        selected_patient = display_patient_matrix(cohort_data)
        if selected_patient is not None:
            st.session_state.selected_patient = selected_patient
    
    with ehr_tab:
        if 'selected_patient' in st.session_state:
            display_individual_ehr(st.session_state.selected_patient, cohort_data)
        else:
            st.info("👆 Please select a patient from the Matrix tab first")

def display_cohort_configuration(cohort_data):
    """Display detailed cohort configuration and parameters"""
    
    st.subheader("⚙️ Cohort Generation Configuration")
    
    config = cohort_data.get('configuration', {})
    
    # Configuration overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Cohort Size", f"{len(cohort_data.get('patients', []))}")
        st.metric("Research Tier", config.get('tier', 'Unknown'))
        st.metric("Primary Condition", config.get('condition', 'Unknown'))
    
    with col2:
        st.metric("Age Group", config.get('age_group', 'Unknown'))
        st.metric("Multi-System", config.get('multi_system', 'Unknown'))
        st.metric("Generation Time", config.get('generation_time', 'Unknown'))
    
    with col3:
        st.metric("Surgical Strategy", config.get('surgical_strategy', 'Unknown'))
        st.metric("Genetic Profile", config.get('genetic_syndrome', 'Unknown'))
        st.metric("Demographics", config.get('demographic_focus', 'Unknown'))
    
    # Detailed configuration parameters
    st.subheader("📋 Detailed Parameters")
    
    with st.expander("🔬 Clinical Configuration Details"):
        config_df = pd.DataFrame([
            {"Parameter": "Research Tier", "Value": config.get('tier', 'N/A'), "Description": "Cohort complexity and scale"},
            {"Parameter": "Cohort Size", "Value": str(len(cohort_data.get('patients', []))), "Description": "Number of synthetic patients generated"},
            {"Parameter": "Primary Condition", "Value": config.get('condition', 'N/A'), "Description": "Main congenital heart defect"},
            {"Parameter": "Age Group", "Value": config.get('age_group', 'N/A'), "Description": "Target age demographic"},
            {"Parameter": "Multi-System Interactions", "Value": config.get('multi_system', 'N/A'), "Description": "Additional physiologic complexity"},
            {"Parameter": "Surgical Strategy", "Value": config.get('surgical_strategy', 'N/A'), "Description": "Primary surgical approach"},
            {"Parameter": "Device/Implant", "Value": config.get('device_implant', 'N/A'), "Description": "Medical devices or implants"},
            {"Parameter": "Clinical Scenario", "Value": config.get('clinical_scenario', 'N/A'), "Description": "Research use case context"},
            {"Parameter": "Genetic Syndrome", "Value": config.get('genetic_syndrome', 'N/A'), "Description": "Associated genetic conditions"},
            {"Parameter": "Demographic Focus", "Value": config.get('demographic_focus', 'N/A'), "Description": "Population representation"},
            {"Parameter": "Comorbidities", "Value": str(config.get('comorbidities', [])), "Description": "Additional medical conditions"},
            {"Parameter": "Medications", "Value": str(config.get('medications', [])), "Description": "Pharmaceutical protocols"},
            {"Parameter": "Monitoring", "Value": str(config.get('monitoring', [])), "Description": "Clinical monitoring parameters"},
            {"Parameter": "Imaging Studies", "Value": str(config.get('imaging', [])), "Description": "Diagnostic imaging protocols"}
        ])
        st.dataframe(config_df, use_container_width=True, hide_index=True)

def display_agent_reasoning(cohort_data):
    """Display detailed agent decision reasoning and chain of thought"""
    
    st.subheader("🧠 Agent Decision Chain & Reasoning")
    
    trace_data = cohort_data.get('trace_data', {})
    
    if not trace_data:
        st.warning("No agent reasoning data available for this cohort.")
        return
    
    # Agent progress overview
    st.subheader("🔄 Agent Progress Timeline")
    
    progress_data = trace_data.get('agent_progress', [])
    if progress_data:
        progress_df = pd.DataFrame(progress_data)
        
        # Timeline visualization
        fig = px.timeline(
            progress_df,
            x_start="start_time",
            x_end="end_time", 
            y="agent_name",
            color="status",
            title="Agent Execution Timeline",
            color_discrete_map={
                "running": "#FFA500",
                "completed": "#32CD32", 
                "failed": "#FF6B6B"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed reasoning steps
    st.subheader("🎯 Decision Reasoning Steps")
    
    reasoning_steps = trace_data.get('reasoning_steps', [])
    
    for i, step in enumerate(reasoning_steps):
        with st.expander(f"Step {i+1}: {step.get('description', 'Unknown Step')}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Reasoning:** {step.get('reasoning', 'No reasoning provided')}")
                st.markdown(f"**Context:** {step.get('context', 'No context provided')}")
                
                # Evidence sources
                if step.get('evidence_sources'):
                    st.markdown("**Evidence Sources:**")
                    for source in step['evidence_sources']:
                        st.markdown(f"• {source}")
            
            with col2:
                st.metric("Confidence", f"{step.get('confidence', 0)*100:.1f}%")
                st.metric("Duration", f"{step.get('duration_ms', 0)}ms")
                
                if step.get('validation_passed'):
                    st.success("✅ Validated")
                else:
                    st.error("❌ Validation Failed")
    
    # Context sources
    st.subheader("📚 Context Sources Used")
    
    context_sources = trace_data.get('context_sources', [])
    if context_sources:
        context_df = pd.DataFrame([
            {
                "Source": source.get('source_id', 'Unknown'),
                "Type": source.get('source_type', 'Unknown'),
                "Relevance": f"{source.get('relevance_score', 0)*100:.1f}%",
                "Retrieved": source.get('retrieval_timestamp', 'Unknown')
            }
            for source in context_sources
        ])
        st.dataframe(context_df, use_container_width=True, hide_index=True)

def display_patient_matrix(cohort_data):
    """Display patient matrix for selection and overview"""
    
    st.subheader("📊 Patient Matrix & Selection")
    
    patients = cohort_data.get('patients', [])
    
    if not patients:
        st.warning("No patient data available.")
        return None
    
    # Create patient summary matrix
    matrix_data = []
    for i, patient in enumerate(patients):
        matrix_data.append({
            "ID": f"PT-{i+1:03d}",
            "Age (months)": patient.get('age_months', 'N/A'),
            "Sex": patient.get('sex', 'N/A'),
            "Condition": patient.get('primary_diagnosis', 'N/A'),
            "EF (%)": patient.get('ejection_fraction', 'N/A'),
            "ICU": "Yes" if patient.get('icu_stay', False) else "No",
            "Surgeries": len(patient.get('surgical_dates', [])),
            "Risk": patient.get('risk_category', 'Unknown'),
            "Status": patient.get('clinical_status', 'Unknown')
        })
    
    matrix_df = pd.DataFrame(matrix_data)
    
    # Interactive patient selection
    st.subheader("🔍 Select Patient for EHR Review")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age_filter = st.slider("Age Range (months)", 0, 216, (0, 216))
        sex_filter = st.multiselect("Sex", ["M", "F"], default=["M", "F"])
    
    with col2:
        icu_filter = st.selectbox("ICU Status", ["All", "Yes", "No"])
        risk_filter = st.multiselect("Risk Category", 
                                   matrix_df['Risk'].unique(), 
                                   default=matrix_df['Risk'].unique())
    
    with col3:
        surgery_filter = st.slider("Number of Surgeries", 0, 5, (0, 5))
    
    # Apply filters
    filtered_df = matrix_df.copy()
    
    # Age filter
    filtered_df = filtered_df[
        (filtered_df['Age (months)'] >= age_filter[0]) & 
        (filtered_df['Age (months)'] <= age_filter[1])
    ]
    
    # Sex filter
    if sex_filter:
        filtered_df = filtered_df[filtered_df['Sex'].isin(sex_filter)]
    
    # ICU filter
    if icu_filter != "All":
        filtered_df = filtered_df[filtered_df['ICU'] == icu_filter]
    
    # Risk filter
    if risk_filter:
        filtered_df = filtered_df[filtered_df['Risk'].isin(risk_filter)]
    
    # Surgery filter
    filtered_df = filtered_df[
        (filtered_df['Surgeries'] >= surgery_filter[0]) & 
        (filtered_df['Surgeries'] <= surgery_filter[1])
    ]
    
    st.info(f"Showing {len(filtered_df)} of {len(matrix_df)} patients")
    
    # Display matrix with selection
    selected_indices = st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    # Patient selection
    if selected_indices.selection and selected_indices.selection.rows:
        selected_row = selected_indices.selection.rows[0]
        selected_patient_id = filtered_df.iloc[selected_row]['ID']
        
        # Find the actual patient data
        patient_index = int(selected_patient_id.split('-')[1]) - 1
        selected_patient = patients[patient_index]
        
        st.success(f"✅ Selected: {selected_patient_id}")
        
        # Quick preview
        with st.expander(f"Quick Preview: {selected_patient_id}"):
            preview_col1, preview_col2, preview_col3 = st.columns(3)
            
            with preview_col1:
                st.metric("Age", f"{selected_patient.get('age_months', 'N/A')} months")
                st.metric("Weight", f"{selected_patient.get('weight_kg', 'N/A')} kg")
                st.metric("Height", f"{selected_patient.get('height_cm', 'N/A')} cm")
            
            with preview_col2:
                st.metric("Heart Rate", f"{selected_patient.get('heart_rate_bpm', 'N/A')} bpm")
                st.metric("BP", f"{selected_patient.get('systolic_bp_mmhg', 'N/A')}/{selected_patient.get('diastolic_bp_mmhg', 'N/A')}")
                st.metric("O2 Sat", f"{selected_patient.get('oxygen_saturation', 'N/A')}%")
            
            with preview_col3:
                st.metric("Hemoglobin", f"{selected_patient.get('hemoglobin_g_dl', 'N/A')} g/dL")
                st.metric("Platelets", f"{selected_patient.get('platelet_count_k_ul', 'N/A')} K/μL")
                st.metric("INR", f"{selected_patient.get('inr', 'N/A')}")
        
        return selected_patient
    
    return None

def display_individual_ehr(patient, cohort_data):
    """Display comprehensive individual EHR with all modalities"""
    
    patient_id = f"PT-{cohort_data.get('patients', []).index(patient) + 1:03d}"
    
    st.subheader(f"📋 Electronic Health Record: {patient_id}")
    st.markdown(f"**Complete medical record with all modalities and clinical assets**")
    
    # EHR Navigation
    ehr_tabs = st.tabs([
        "📊 Overview", "🫀 Cardiology", "🩸 Laboratory", "💊 Medications", 
        "🏥 Procedures", "📈 Imaging", "📝 Notes", "📋 Documents"
    ])
    
    with ehr_tabs[0]:  # Overview
        display_patient_overview(patient, patient_id)
    
    with ehr_tabs[1]:  # Cardiology
        display_cardiology_records(patient)
    
    with ehr_tabs[2]:  # Laboratory
        display_laboratory_records(patient)
    
    with ehr_tabs[3]:  # Medications
        display_medication_records(patient)
    
    with ehr_tabs[4]:  # Procedures
        display_procedure_records(patient)
    
    with ehr_tabs[5]:  # Imaging
        display_imaging_records(patient)
    
    with ehr_tabs[6]:  # Notes
        display_clinical_notes(patient)
    
    with ehr_tabs[7]:  # Documents
        display_ehr_documents(patient)

def display_patient_overview(patient, patient_id):
    """Display patient overview and demographics"""
    
    st.markdown(f"### 👤 Patient Demographics")
    
    demo_col1, demo_col2, demo_col3, demo_col4 = st.columns(4)
    
    with demo_col1:
        st.metric("Patient ID", patient_id)
        st.metric("Age", f"{patient.get('age_months', 'N/A')} months")
        st.metric("Sex", patient.get('sex', 'N/A'))
        st.metric("Race/Ethnicity", patient.get('race_ethnicity', 'N/A'))
    
    with demo_col2:
        st.metric("Weight", f"{patient.get('weight_kg', 'N/A')} kg")
        st.metric("Height", f"{patient.get('height_cm', 'N/A')} cm")
        st.metric("BMI", f"{patient.get('bmi', 'N/A')}")
        st.metric("BSA", f"{patient.get('body_surface_area', 'N/A')} m²")
    
    with demo_col3:
        st.metric("Primary Diagnosis", patient.get('primary_diagnosis', 'N/A'))
        st.metric("Risk Category", patient.get('risk_category', 'N/A'))
        st.metric("Clinical Status", patient.get('clinical_status', 'N/A'))
        st.metric("ICU Stay", "Yes" if patient.get('icu_stay', False) else "No")
    
    with demo_col4:
        st.metric("Family CVD History", "Yes" if patient.get('family_history_cvd', False) else "No")
        st.metric("Genetic Syndrome", patient.get('genetic_syndrome', 'None'))
        st.metric("Birth Weight", f"{patient.get('birth_weight_kg', 'N/A')} kg")
        st.metric("Gestational Age", f"{patient.get('gestational_age_weeks', 'N/A')} weeks")

def display_cardiology_records(patient):
    """Display detailed cardiology records"""
    
    st.markdown("### 🫀 Cardiovascular Assessment")
    
    # Vital signs
    st.subheader("📊 Current Vital Signs")
    
    vital_col1, vital_col2, vital_col3, vital_col4 = st.columns(4)
    
    with vital_col1:
        st.metric("Heart Rate", f"{patient.get('heart_rate_bpm', 'N/A')} bpm")
        st.metric("Systolic BP", f"{patient.get('systolic_bp_mmhg', 'N/A')} mmHg")
    
    with vital_col2:
        st.metric("Diastolic BP", f"{patient.get('diastolic_bp_mmhg', 'N/A')} mmHg")
        st.metric("Mean BP", f"{patient.get('mean_arterial_pressure', 'N/A')} mmHg")
    
    with vital_col3:
        st.metric("O2 Saturation", f"{patient.get('oxygen_saturation', 'N/A')}%")
        st.metric("Mixed Venous O2", f"{patient.get('mixed_venous_o2', 'N/A')}%")
    
    with vital_col4:
        st.metric("CVP", f"{patient.get('central_venous_pressure', 'N/A')} mmHg")
        st.metric("Temperature", f"{patient.get('temperature_celsius', 'N/A')}°C")
    
    # Hemodynamic parameters
    st.subheader("💓 Hemodynamic Parameters")
    
    hemo_col1, hemo_col2, hemo_col3 = st.columns(3)
    
    with hemo_col1:
        st.metric("Ejection Fraction", f"{patient.get('ejection_fraction', 'N/A')}%")
        st.metric("Stroke Volume", f"{patient.get('stroke_volume', 'N/A')} mL")
        st.metric("Cardiac Output", f"{patient.get('cardiac_output', 'N/A')} L/min")
    
    with hemo_col2:
        st.metric("Cardiac Index", f"{patient.get('cardiac_index', 'N/A')} L/min/m²")
        st.metric("LVEDP", f"{patient.get('lv_end_diastolic_pressure', 'N/A')} mmHg")
        st.metric("PA Pressure", f"{patient.get('pulmonary_artery_pressure', 'N/A')} mmHg")
    
    with hemo_col3:
        st.metric("LA Pressure", f"{patient.get('left_atrial_pressure', 'N/A')} mmHg")
        st.metric("RA Pressure", f"{patient.get('right_atrial_pressure', 'N/A')} mmHg")
        st.metric("Wedge Pressure", f"{patient.get('wedge_pressure', 'N/A')} mmHg")
    
    # Echocardiogram findings
    if patient.get('echocardiogram'):
        st.subheader("🔍 Echocardiogram Findings")
        echo_data = patient['echocardiogram']
        
        echo_col1, echo_col2 = st.columns(2)
        
        with echo_col1:
            st.json(echo_data)
        
        with echo_col2:
            if 'measurements' in echo_data:
                measurements_df = pd.DataFrame(echo_data['measurements'].items(), 
                                             columns=['Parameter', 'Value'])
                st.dataframe(measurements_df, hide_index=True)

def display_laboratory_records(patient):
    """Display comprehensive laboratory results"""
    
    st.markdown("### 🩸 Laboratory Results")
    
    # Hematology
    st.subheader("🔴 Hematology")
    
    heme_col1, heme_col2, heme_col3 = st.columns(3)
    
    with heme_col1:
        st.metric("Hemoglobin", f"{patient.get('hemoglobin_g_dl', 'N/A')} g/dL")
        st.metric("Hematocrit", f"{patient.get('hematocrit_percent', 'N/A')}%")
        st.metric("RBC Count", f"{patient.get('rbc_count_m_ul', 'N/A')} M/μL")
    
    with heme_col2:
        st.metric("WBC Count", f"{patient.get('wbc_count_k_ul', 'N/A')} K/μL")
        st.metric("Platelet Count", f"{patient.get('platelet_count_k_ul', 'N/A')} K/μL")
        st.metric("Reticulocytes", f"{patient.get('reticulocyte_count_percent', 'N/A')}%")
    
    with heme_col3:
        st.metric("MCV", f"{patient.get('mcv_fl', 'N/A')} fL")
        st.metric("MCH", f"{patient.get('mch_pg', 'N/A')} pg")
        st.metric("MCHC", f"{patient.get('mchc_g_dl', 'N/A')} g/dL")
    
    # Coagulation
    st.subheader("🩸 Coagulation Panel")
    
    coag_col1, coag_col2, coag_col3 = st.columns(3)
    
    with coag_col1:
        st.metric("PT", f"{patient.get('pt_seconds', 'N/A')} sec")
        st.metric("PTT", f"{patient.get('ptt_seconds', 'N/A')} sec")
        st.metric("INR", f"{patient.get('inr', 'N/A')}")
    
    with coag_col2:
        st.metric("Fibrinogen", f"{patient.get('fibrinogen_mg_dl', 'N/A')} mg/dL")
        st.metric("D-dimer", f"{patient.get('d_dimer_ng_ml', 'N/A')} ng/mL")
        st.metric("Factor VIII", f"{patient.get('factor_viii_percent', 'N/A')}%")
    
    with coag_col3:
        st.metric("vWF Activity", f"{patient.get('vwf_activity_percent', 'N/A')}%")
        st.metric("vWF Antigen", f"{patient.get('vwf_antigen_percent', 'N/A')}%")
        st.metric("Bleeding Time", f"{patient.get('bleeding_time_minutes', 'N/A')} min")

def display_medication_records(patient):
    """Display medication history and current prescriptions"""
    
    st.markdown("### 💊 Medication Records")
    
    # Current medications
    st.subheader("📋 Current Medications")
    
    anticoagulants = patient.get('anticoagulants', [])
    antiplatelets = patient.get('antiplatelets', [])
    
    med_col1, med_col2 = st.columns(2)
    
    with med_col1:
        st.markdown("**Anticoagulants:**")
        if anticoagulants:
            for med in anticoagulants:
                st.markdown(f"• {med}")
        else:
            st.markdown("• None prescribed")
    
    with med_col2:
        st.markdown("**Antiplatelets:**")
        if antiplatelets:
            for med in antiplatelets:
                st.markdown(f"• {med}")
        else:
            st.markdown("• None prescribed")
    
    # ESA Therapy
    st.subheader("🩸 Hematopoietic Support")
    
    esa_col1, esa_col2 = st.columns(2)
    
    with esa_col1:
        st.metric("ESA Therapy", "Yes" if patient.get('esa_therapy', False) else "No")
    
    with esa_col2:
        if patient.get('esa_therapy'):
            st.metric("ESA Type", patient.get('esa_type', 'Not specified'))

def display_procedure_records(patient):
    """Display surgical and procedural history"""
    
    st.markdown("### 🏥 Procedures & Surgical History")
    
    # Surgical dates
    surgical_dates = patient.get('surgical_dates', [])
    
    if surgical_dates:
        st.subheader("📅 Surgical Timeline")
        
        surgery_data = []
        for i, date in enumerate(surgical_dates):
            surgery_data.append({
                "Surgery": f"Procedure {i+1}",
                "Date": date,
                "Type": patient.get('surgical_types', ['Unknown'])[i] if i < len(patient.get('surgical_types', [])) else 'Unknown',
                "Status": "Completed"
            })
        
        surgery_df = pd.DataFrame(surgery_data)
        st.dataframe(surgery_df, hide_index=True, use_container_width=True)
    else:
        st.info("No surgical procedures recorded")
    
    # Transfusion history
    transfusion_history = patient.get('transfusion_history', [])
    
    if transfusion_history:
        st.subheader("🩸 Transfusion History")
        transfusion_df = pd.DataFrame(transfusion_history)
        st.dataframe(transfusion_df, hide_index=True, use_container_width=True)

def display_imaging_records(patient):
    """Display imaging studies and reports"""
    
    st.markdown("### 📈 Imaging Studies")
    
    # Mock imaging data for demonstration
    imaging_studies = [
        {
            "Study": "Echocardiogram",
            "Date": "2024-01-15",
            "Status": "Final",
            "Findings": "Moderate LV dysfunction, EF 45%"
        },
        {
            "Study": "Cardiac MRI",
            "Date": "2024-01-10", 
            "Status": "Final",
            "Findings": "Structural abnormalities consistent with TOF"
        },
        {
            "Study": "Chest X-ray",
            "Date": "2024-01-12",
            "Status": "Final", 
            "Findings": "Cardiomegaly, pulmonary vascular markings"
        }
    ]
    
    imaging_df = pd.DataFrame(imaging_studies)
    st.dataframe(imaging_df, hide_index=True, use_container_width=True)
    
    # Detailed imaging viewer
    selected_study = st.selectbox("Select Study for Details", imaging_studies)
    
    if selected_study:
        st.subheader(f"📋 {selected_study['Study']} Report")
        
        report_col1, report_col2 = st.columns([2, 1])
        
        with report_col1:
            st.markdown(f"**Date:** {selected_study['Date']}")
            st.markdown(f"**Status:** {selected_study['Status']}")
            st.markdown(f"**Findings:** {selected_study['Findings']}")
            
            # Detailed report
            st.text_area("Full Report", 
                        f"CLINICAL INDICATION: {patient.get('primary_diagnosis', 'CHD evaluation')}\n\n"
                        f"TECHNIQUE: Standard {selected_study['Study'].lower()} protocol\n\n"
                        f"FINDINGS:\n{selected_study['Findings']}\n\n"
                        f"IMPRESSION:\n{selected_study['Findings']}", 
                        height=200)
        
        with report_col2:
            st.info("📸 Image Viewer\n\n[Synthetic imaging data would be displayed here in a production environment]")

def display_clinical_notes(patient):
    """Display clinical notes and assessments"""
    
    st.markdown("### 📝 Clinical Notes")
    
    # Note types
    note_tabs = st.tabs(["Cardiology", "Hematology", "Surgical", "Nursing"])
    
    with note_tabs[0]:  # Cardiology
        st.subheader("🫀 Cardiology Consultation")
        cardiology_note = patient.get('cardiology_consultation', 'No cardiology notes available')
        st.text_area("Cardiology Assessment", cardiology_note, height=300)
    
    with note_tabs[1]:  # Hematology
        st.subheader("🩸 Hematology Assessment")
        hematology_note = patient.get('hematology_assessment', 'No hematology notes available')
        st.text_area("Hematology Assessment", hematology_note, height=300)
    
    with note_tabs[2]:  # Surgical
        st.subheader("🏥 Surgical Narrative")
        surgical_note = patient.get('surgical_narrative', 'No surgical notes available')
        st.text_area("Surgical Documentation", surgical_note, height=300)
    
    with note_tabs[3]:  # Nursing
        st.subheader("👩‍⚕️ Nursing Documentation")
        nursing_note = """
        NURSING ASSESSMENT:
        Patient alert and oriented. Vital signs stable.
        Cardiac monitor shows normal sinus rhythm.
        No acute distress noted.
        
        INTERVENTIONS:
        - Continuous cardiac monitoring
        - Vital signs q4h
        - Medication administration as ordered
        - Patient/family education provided
        
        PLAN:
        Continue current care plan.
        Monitor for signs of complications.
        """
        st.text_area("Nursing Notes", nursing_note, height=300)

def display_ehr_documents(patient):
    """Display EHR documents and exports"""
    
    st.markdown("### 📋 EHR Documents & Exports")
    
    # Document types
    doc_col1, doc_col2 = st.columns(2)
    
    with doc_col1:
        st.subheader("📄 Available Documents")
        
        documents = [
            "Admission History & Physical",
            "Operative Report", 
            "Discharge Summary",
            "Medication Reconciliation",
            "Care Plan",
            "Consent Forms",
            "Lab Results Summary",
            "Imaging Reports"
        ]
        
        for doc in documents:
            if st.button(f"📄 {doc}"):
                st.info(f"Opening {doc}...")
    
    with doc_col2:
        st.subheader("💾 Export Options")
        
        export_format = st.selectbox("Export Format", [
            "PDF Report",
            "FHIR Bundle", 
            "HL7 Message",
            "CSV Data Export",
            "JSON Complete Record"
        ])
        
        if st.button("📤 Export EHR"):
            st.success(f"Exporting patient record in {export_format} format...")
            
            # Generate export preview
            export_data = {
                "patient_id": f"PT-{cohort_data.get('patients', []).index(patient) + 1:03d}" if 'cohort_data' in locals() else "Unknown",
                "export_date": datetime.now().isoformat(),
                "format": export_format,
                "data": patient
            }
            
            st.json(export_data)

if __name__ == "__main__":
    main()