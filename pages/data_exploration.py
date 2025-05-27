"""
Data Exploration Dashboard for Synthetic EHR Records
Comprehensive analytics and drill-down capabilities for pediatric cardiology data
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
from agents.surgical_strategy_simulator import SurgicalStrategySimulator

def main():
    st.title("📊 Synthetic EHR Data Exploration Dashboard")
    st.markdown("**Comprehensive Analytics and Individual Record Drill-Down**")
    
    # Initialize generators
    if 'generated_cohort' not in st.session_state:
        st.session_state.generated_cohort = None
    
    # Data source selection
    st.sidebar.header("🎯 Data Source Configuration")
    
    data_source = st.sidebar.selectbox(
        "Select Data Source",
        ["Generate New Cohort", "Load Existing Dataset", "Demo Dataset"]
    )
    
    if data_source == "Generate New Cohort":
        generate_new_cohort_interface()
    elif data_source == "Demo Dataset":
        load_demo_dataset()
    
    # Main exploration interface
    if st.session_state.generated_cohort is not None:
        display_exploration_dashboard(st.session_state.generated_cohort)

def generate_new_cohort_interface():
    """Interface for generating a new cohort for exploration"""
    st.sidebar.subheader("🔬 Cohort Generation")
    
    # Quick generation options
    cohort_size = st.sidebar.slider("Cohort Size", 10, 1000, 100)
    condition_focus = st.sidebar.selectbox(
        "Primary Condition",
        ["Hypoplastic Left Heart Syndrome", "Tetralogy of Fallot", "VSD", "ASD", "Mixed Conditions"]
    )
    
    if st.sidebar.button("🚀 Generate Cohort for Exploration"):
        with st.spinner("Generating comprehensive synthetic cohort..."):
            # Generate synthetic cohort using enhanced generator
            generator = PediatricCardiologyGenerator()
            
            cohort_data = []
            for i in range(cohort_size):
                record = generator.generate_complete_record("congenital_heart_disease")
                # Convert to dict and add index
                record_dict = record.__dict__.copy()
                record_dict['record_id'] = i
                cohort_data.append(record_dict)
            
            st.session_state.generated_cohort = {
                "records": cohort_data,
                "metadata": {
                    "generation_date": datetime.now().isoformat(),
                    "cohort_size": cohort_size,
                    "primary_condition": condition_focus,
                    "generator_version": "enhanced_v2.0"
                }
            }
            
            st.sidebar.success(f"✅ Generated {cohort_size} synthetic records!")

def load_demo_dataset():
    """Load a demo dataset for exploration"""
    if st.sidebar.button("📋 Load Demo Dataset"):
        with st.spinner("Loading demo synthetic cohort..."):
            # Generate a small demo cohort
            generator = PediatricCardiologyGenerator()
            
            demo_data = []
            for i in range(50):  # Demo size
                record = generator.generate_complete_record("congenital_heart_disease")
                record_dict = record.__dict__.copy()
                record_dict['record_id'] = i
                demo_data.append(record_dict)
            
            st.session_state.generated_cohort = {
                "records": demo_data,
                "metadata": {
                    "generation_date": datetime.now().isoformat(),
                    "cohort_size": 50,
                    "primary_condition": "Demo Dataset",
                    "generator_version": "demo_v1.0"
                }
            }
            
            st.sidebar.success("✅ Demo dataset loaded!")

def display_exploration_dashboard(cohort_data):
    """Main exploration dashboard with aggregated trends and drill-down capabilities"""
    
    records = cohort_data["records"]
    metadata = cohort_data["metadata"]
    
    # Dashboard overview
    st.success(f"🎯 **Exploring {len(records)} synthetic EHR records** | Generated: {metadata['generation_date'][:10]}")
    
    # Create exploration tabs
    overview_tab, demographics_tab, clinical_tab, surgical_tab, individual_tab = st.tabs([
        "📊 Overview", "👥 Demographics", "🫀 Clinical Data", "🏥 Surgical Data", "🔍 Individual Records"
    ])
    
    with overview_tab:
        display_overview_analytics(records)
    
    with demographics_tab:
        display_demographics_analytics(records)
    
    with clinical_tab:
        display_clinical_analytics(records)
    
    with surgical_tab:
        display_surgical_analytics(records)
    
    with individual_tab:
        display_individual_records(records)

def display_overview_analytics(records):
    """Display high-level overview analytics"""
    
    st.subheader("📊 Cohort Overview Analytics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_age = np.mean([r['age_months'] for r in records])
        st.metric("Average Age", f"{avg_age:.1f} months")
    
    with col2:
        male_count = sum(1 for r in records if r['sex'] == 'M')
        male_pct = (male_count / len(records)) * 100
        st.metric("Male Patients", f"{male_pct:.1f}%")
    
    with col3:
        icu_patients = sum(1 for r in records if r['icu_stay'])
        icu_pct = (icu_patients / len(records)) * 100
        st.metric("ICU Admissions", f"{icu_pct:.1f}%")
    
    with col4:
        avg_los = np.mean([len(r.get('surgical_dates', [])) for r in records])
        st.metric("Avg Procedures", f"{avg_los:.1f}")
    
    # Age distribution
    col1, col2 = st.columns(2)
    
    with col1:
        ages = [r['age_months'] for r in records]
        fig_age = px.histogram(
            x=ages, 
            title="Age Distribution (Months)",
            labels={'x': 'Age (months)', 'y': 'Count'},
            color_discrete_sequence=['#6B4EFF']
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        # Condition severity distribution
        severities = []
        for r in records:
            if r['ejection_fraction'] < 40:
                severities.append('Severe')
            elif r['ejection_fraction'] < 55:
                severities.append('Moderate')
            else:
                severities.append('Mild')
        
        severity_counts = pd.Series(severities).value_counts()
        fig_severity = px.pie(
            values=severity_counts.values,
            names=severity_counts.index,
            title="Condition Severity Distribution",
            color_discrete_sequence=['#34C759', '#6B4EFF', '#0A1F44']
        )
        st.plotly_chart(fig_severity, use_container_width=True)

def display_demographics_analytics(records):
    """Display detailed demographics analytics"""
    
    st.subheader("👥 Demographics Analytics")
    
    # Create demographic dataframe
    demo_data = []
    for r in records:
        demo_data.append({
            'age_months': r['age_months'],
            'sex': r['sex'],
            'race_ethnicity': r['race_ethnicity'],
            'weight_kg': r['weight_kg'],
            'height_cm': r['height_cm'],
            'bmi': r['bmi'],
            'family_history_cvd': r['family_history_cvd'],
            'icu_stay': r['icu_stay']
        })
    
    demo_df = pd.DataFrame(demo_data)
    
    # Demographics charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Race/ethnicity distribution
        ethnicity_counts = demo_df['race_ethnicity'].value_counts()
        fig_ethnicity = px.bar(
            x=ethnicity_counts.index,
            y=ethnicity_counts.values,
            title="Race/Ethnicity Distribution",
            labels={'x': 'Race/Ethnicity', 'y': 'Count'},
            color_discrete_sequence=['#6B4EFF']
        )
        fig_ethnicity.update_xaxis(tickangle=45)
        st.plotly_chart(fig_ethnicity, use_container_width=True)
    
    with col2:
        # BMI distribution by age group
        demo_df['age_group'] = pd.cut(demo_df['age_months'], 
                                     bins=[0, 12, 36, 72, 216], 
                                     labels=['Infant', 'Toddler', 'Child', 'Adolescent'])
        
        fig_bmi = px.box(
            demo_df, 
            x='age_group', 
            y='bmi',
            title="BMI Distribution by Age Group",
            color_discrete_sequence=['#34C759']
        )
        st.plotly_chart(fig_bmi, use_container_width=True)
    
    # Family history analysis
    st.subheader("🧬 Genetic Risk Factors")
    
    family_history_stats = {
        'CVD Family History': demo_df['family_history_cvd'].mean() * 100,
        'ICU Admission Rate': demo_df['icu_stay'].mean() * 100
    }
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Family CVD History", f"{family_history_stats['CVD Family History']:.1f}%")
    with col2:
        st.metric("ICU Admission Rate", f"{family_history_stats['ICU Admission Rate']:.1f}%")

def display_clinical_analytics(records):
    """Display clinical data analytics"""
    
    st.subheader("🫀 Clinical Analytics")
    
    # Create clinical dataframe
    clinical_data = []
    for r in records:
        clinical_data.append({
            'heart_rate_bpm': r['heart_rate_bpm'],
            'systolic_bp_mmhg': r['systolic_bp_mmhg'],
            'diastolic_bp_mmhg': r['diastolic_bp_mmhg'],
            'ejection_fraction': r['ejection_fraction'],
            'oxygen_saturation': r['oxygen_saturation'],
            'hemoglobin_g_dl': r['hemoglobin_g_dl'],
            'platelet_count_k_ul': r['platelet_count_k_ul'],
            'age_months': r['age_months'],
            'race_ethnicity': r['race_ethnicity']
        })
    
    clinical_df = pd.DataFrame(clinical_data)
    
    # Clinical parameter correlations
    col1, col2 = st.columns(2)
    
    with col1:
        # Heart rate vs age
        fig_hr = px.scatter(
            clinical_df,
            x='age_months',
            y='heart_rate_bpm',
            color='race_ethnicity',
            title="Heart Rate vs Age",
            labels={'age_months': 'Age (months)', 'heart_rate_bpm': 'Heart Rate (bpm)'}
        )
        st.plotly_chart(fig_hr, use_container_width=True)
    
    with col2:
        # Ejection fraction distribution
        fig_ef = px.histogram(
            clinical_df,
            x='ejection_fraction',
            title="Ejection Fraction Distribution",
            labels={'ejection_fraction': 'Ejection Fraction (%)', 'y': 'Count'},
            color_discrete_sequence=['#0A1F44']
        )
        st.plotly_chart(fig_ef, use_container_width=True)
    
    # Hemodynamic parameters heatmap
    st.subheader("🔥 Clinical Parameter Correlations")
    
    numeric_cols = ['heart_rate_bpm', 'systolic_bp_mmhg', 'ejection_fraction', 
                   'oxygen_saturation', 'hemoglobin_g_dl']
    corr_matrix = clinical_df[numeric_cols].corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        title="Clinical Parameter Correlations",
        color_continuous_scale="RdBu",
        aspect="auto"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

def display_surgical_analytics(records):
    """Display surgical and procedure analytics"""
    
    st.subheader("🏥 Surgical Analytics")
    
    # Extract surgical data
    surgical_data = []
    for i, r in enumerate(records):
        surgical_dates = r.get('surgical_dates', [])
        has_surgery = len(surgical_dates) > 0
        
        surgical_data.append({
            'patient_id': i,
            'has_surgery': has_surgery,
            'surgery_count': len(surgical_dates),
            'age_months': r['age_months'],
            'icu_stay': r['icu_stay'],
            'ejection_fraction': r['ejection_fraction']
        })
    
    surgical_df = pd.DataFrame(surgical_data)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        surgery_rate = surgical_df['has_surgery'].mean() * 100
        st.metric("Surgical Intervention Rate", f"{surgery_rate:.1f}%")
    
    with col2:
        avg_procedures = surgical_df[surgical_df['surgery_count'] > 0]['surgery_count'].mean()
        st.metric("Avg Procedures per Patient", f"{avg_procedures:.1f}")
    
    with col3:
        icu_surgery_rate = surgical_df[surgical_df['has_surgery']]['icu_stay'].mean() * 100
        st.metric("ICU Rate (Surgical)", f"{icu_surgery_rate:.1f}%")
    
    # Surgical outcomes analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Surgery count distribution
        surgery_counts = surgical_df['surgery_count'].value_counts().sort_index()
        fig_surgery = px.bar(
            x=surgery_counts.index,
            y=surgery_counts.values,
            title="Number of Procedures per Patient",
            labels={'x': 'Number of Procedures', 'y': 'Patient Count'},
            color_discrete_sequence=['#34C759']
        )
        st.plotly_chart(fig_surgery, use_container_width=True)
    
    with col2:
        # Age at surgery vs outcomes
        fig_age_surgery = px.scatter(
            surgical_df[surgical_df['has_surgery']],
            x='age_months',
            y='ejection_fraction',
            size='surgery_count',
            title="Age at Surgery vs Cardiac Function",
            labels={'age_months': 'Age (months)', 'ejection_fraction': 'Ejection Fraction (%)'}
        )
        st.plotly_chart(fig_age_surgery, use_container_width=True)

def display_individual_records(records):
    """Display individual record drill-down interface"""
    
    st.subheader("🔍 Individual Record Explorer")
    
    # Record selection
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_record_id = st.selectbox(
            "Select Patient Record",
            range(len(records)),
            format_func=lambda x: f"Patient {x+1} ({records[x]['age_months']}mo, {records[x]['sex']})"
        )
        
        # Filter options
        st.subheader("🔧 Filters")
        age_filter = st.slider("Age Range (months)", 0, 216, (0, 216))
        sex_filter = st.multiselect("Sex", ["M", "F"], default=["M", "F"])
        
        # Apply filters
        filtered_records = [
            r for r in records 
            if age_filter[0] <= r['age_months'] <= age_filter[1] 
            and r['sex'] in sex_filter
        ]
        
        st.info(f"Showing {len(filtered_records)} of {len(records)} records")
    
    with col2:
        if selected_record_id < len(records):
            display_detailed_patient_record(records[selected_record_id])

def display_detailed_patient_record(record):
    """Display comprehensive individual patient record"""
    
    st.markdown(f"### 👤 Patient {record['record_id']+1} - Detailed Clinical Record")
    
    # Patient overview
    overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)
    
    with overview_col1:
        st.metric("Age", f"{record['age_months']} months")
        st.metric("Sex", record['sex'])
    
    with overview_col2:
        st.metric("Weight", f"{record['weight_kg']} kg")
        st.metric("Height", f"{record['height_cm']} cm")
    
    with overview_col3:
        st.metric("BMI", f"{record['bmi']}")
        st.metric("Race/Ethnicity", record['race_ethnicity'])
    
    with overview_col4:
        st.metric("ICU Stay", "Yes" if record['icu_stay'] else "No")
        st.metric("Family CVD History", "Yes" if record['family_history_cvd'] else "No")
    
    # Detailed clinical tabs
    patient_tab1, patient_tab2, patient_tab3, patient_tab4 = st.tabs([
        "🫀 Cardiac Data", "🩸 Laboratory Results", "💊 Therapeutics", "📋 Clinical Notes"
    ])
    
    with patient_tab1:
        display_patient_cardiac_data(record)
    
    with patient_tab2:
        display_patient_laboratory_data(record)
    
    with patient_tab3:
        display_patient_therapeutics(record)
    
    with patient_tab4:
        display_patient_clinical_notes(record)

def display_patient_cardiac_data(record):
    """Display detailed cardiac data for individual patient"""
    
    # Vital signs
    st.subheader("🫀 Cardiac Vital Signs")
    
    vital_col1, vital_col2, vital_col3 = st.columns(3)
    
    with vital_col1:
        st.metric("Heart Rate", f"{record['heart_rate_bpm']} bpm")
        st.metric("Systolic BP", f"{record['systolic_bp_mmhg']} mmHg")
        st.metric("Diastolic BP", f"{record['diastolic_bp_mmhg']} mmHg")
    
    with vital_col2:
        st.metric("O2 Saturation", f"{record['oxygen_saturation']}%")
        st.metric("Mixed Venous O2", f"{record['mixed_venous_o2']}%")
        st.metric("CVP", f"{record['central_venous_pressure']} mmHg")
    
    with vital_col3:
        st.metric("Ejection Fraction", f"{record['ejection_fraction']}%")
        st.metric("Stroke Volume", f"{record['stroke_volume']} mL")
        st.metric("Cardiac Output", f"{record['cardiac_output']} L/min")
    
    # Imaging data
    if 'echocardiogram' in record:
        st.subheader("🔍 Imaging Findings")
        st.json(record['echocardiogram'])

def display_patient_laboratory_data(record):
    """Display laboratory results for individual patient"""
    
    st.subheader("🩸 Laboratory Results")
    
    lab_col1, lab_col2, lab_col3 = st.columns(3)
    
    with lab_col1:
        st.metric("Hemoglobin", f"{record['hemoglobin_g_dl']} g/dL")
        st.metric("Hematocrit", f"{record['hematocrit_percent']}%")
        st.metric("Platelets", f"{record['platelet_count_k_ul']} K/μL")
    
    with lab_col2:
        st.metric("WBC Count", f"{record['wbc_count_k_ul']} K/μL")
        st.metric("PT", f"{record['pt_seconds']} sec")
        st.metric("INR", f"{record['inr']}")
    
    with lab_col3:
        st.metric("Fibrinogen", f"{record['fibrinogen_mg_dl']} mg/dL")
        st.metric("D-dimer", f"{record['d_dimer_ng_ml']} ng/mL")
        st.metric("Reticulocytes", f"{record['reticulocyte_count_percent']}%")

def display_patient_therapeutics(record):
    """Display therapeutic interventions for individual patient"""
    
    st.subheader("💊 Therapeutic Interventions")
    
    # Medications
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Anticoagulants")
        if record['anticoagulants']:
            for med in record['anticoagulants']:
                st.write(f"• {med}")
        else:
            st.write("None prescribed")
        
        st.subheader("ESA Therapy")
        st.write("Yes" if record['esa_therapy'] else "No")
    
    with col2:
        st.subheader("Antiplatelets")
        if record['antiplatelets']:
            for med in record['antiplatelets']:
                st.write(f"• {med}")
        else:
            st.write("None prescribed")
    
    # Transfusion history
    if record['transfusion_history']:
        st.subheader("🩸 Transfusion History")
        transfusion_df = pd.DataFrame(record['transfusion_history'])
        st.dataframe(transfusion_df, use_container_width=True)

def display_patient_clinical_notes(record):
    """Display clinical notes for individual patient"""
    
    st.subheader("📋 Clinical Documentation")
    
    note_tab1, note_tab2, note_tab3 = st.tabs([
        "Cardiology", "Hematology", "Surgical"
    ])
    
    with note_tab1:
        st.text_area("Cardiology Consultation", record['cardiology_consultation'], height=300)
    
    with note_tab2:
        st.text_area("Hematology Assessment", record['hematology_assessment'], height=300)
    
    with note_tab3:
        st.text_area("Surgical Narrative", record['surgical_narrative'], height=300)

if __name__ == "__main__":
    main()