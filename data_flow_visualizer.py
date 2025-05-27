"""
Data Flow Visualization for Synthetic Ascension Platform
Creates comprehensive system architecture diagrams using Graphviz
"""

import streamlit as st
import graphviz
from datetime import datetime
from ehr_schema_generator import CompleteEHRRecord, generate_complete_ehr_schema, track_ux_event, UXEventType

def create_system_architecture_diagram():
    """Create comprehensive data flow diagram"""
    
    # Track UX event for diagram generation
    ux_event = track_ux_event(
        UXEventType.CHART_INTERACTION,
        "data_flow_visualizer",
        {"action": "generate_diagram", "diagram_type": "system_architecture"}
    )
    
    dot = graphviz.Digraph(comment='Synthetic Ascension System Architecture')
    dot.attr(rankdir='TB', size='12,10')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
    dot.attr('edge', fontname='Arial')
    
    # Define color scheme for different component types
    colors = {
        'input': '#E8F4FD',
        'agent': '#FFF2CC', 
        'processing': '#D5E8D4',
        'storage': '#F8CECC',
        'output': '#E1D5E7',
        'validation': '#FFE6CC'
    }
    
    # Input Sources
    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='📚 Knowledge Sources & Input Data', style='filled', color='lightgrey')
        c.node('pubmed', 'PubMed\nNCBI Database', fillcolor=colors['input'])
        c.node('clinical_trials', 'ClinicalTrials.gov\nFDA Database', fillcolor=colors['input'])
        c.node('fda_guidance', 'FDA Guidance\nRegulatory Docs', fillcolor=colors['input'])
        c.node('who_reports', 'WHO Reports\nGlobal Health Data', fillcolor=colors['input'])
        c.node('user_queries', 'Clinical Problem\nStatements', fillcolor=colors['input'])
    
    # Agent Layer
    with dot.subgraph(name='cluster_1') as c:
        c.attr(label='🤖 Agentic AI Layer', style='filled', color='lightgrey')
        c.node('literature_agent', 'Literature\nRetrieval Agent', fillcolor=colors['agent'])
        c.node('synthetic_agent', 'Synthetic Cohort\nGeneration Agent', fillcolor=colors['agent'])
        c.node('validation_agent', 'Statistical\nValidation Agent', fillcolor=colors['agent'])
        c.node('terminology_agent', 'Medical Terminology\nValidation Agent', fillcolor=colors['agent'])
        c.node('web_monitor', 'Web Monitoring\n& Curation Agent', fillcolor=colors['agent'])
        c.node('rag_orchestrator', 'RAG Orchestrator\n& Coordinator', fillcolor=colors['agent'])
    
    # Processing Engine
    with dot.subgraph(name='cluster_2') as c:
        c.attr(label='⚙️ Synthetic Data Engine', style='filled', color='lightgrey')
        c.node('ehr_generator', 'EHR Schema\nGenerator', fillcolor=colors['processing'])
        c.node('clinical_engine', 'Clinical Data\nGeneration Engine', fillcolor=colors['processing'])
        c.node('bias_detector', 'Bias Detection\n& Mitigation', fillcolor=colors['processing'])
        c.node('quality_engine', 'Data Quality\nAssessment', fillcolor=colors['processing'])
    
    # Validation Layer
    with dot.subgraph(name='cluster_3') as c:
        c.attr(label='✅ Validation & Quality Assurance', style='filled', color='lightgrey')
        c.node('clinical_validation', 'Clinical Realism\nValidation', fillcolor=colors['validation'])
        c.node('statistical_validation', 'Statistical\nConsistency Check', fillcolor=colors['validation'])
        c.node('demographic_validation', 'Demographic\nRepresentation Analysis', fillcolor=colors['validation'])
        c.node('audit_engine', 'Audit Trail\n& Compliance', fillcolor=colors['validation'])
    
    # Storage Layer
    with dot.subgraph(name='cluster_4') as c:
        c.attr(label='💾 Data Storage & Management', style='filled', color='lightgrey')
        c.node('postgresql', 'PostgreSQL\nDatabase', fillcolor=colors['storage'])
        c.node('audit_db', 'Audit Trail\nDatabase', fillcolor=colors['storage'])
        c.node('ux_analytics', 'UX Analytics\nDatabase', fillcolor=colors['storage'])
        c.node('cache_layer', 'Redis Cache\nLayer', fillcolor=colors['storage'])
    
    # Output Layer
    with dot.subgraph(name='cluster_5') as c:
        c.attr(label='📊 Output & Delivery', style='filled', color='lightgrey')
        c.node('api_server', 'FastAPI Server\nSwagger Docs', fillcolor=colors['output'])
        c.node('research_dashboard', 'Research\nDashboard', fillcolor=colors['output'])
        c.node('pharma_workflows', 'Pharma Executive\nWorkflows', fillcolor=colors['output'])
        c.node('pediatric_demo', 'Pediatric Cardiology\nDemo', fillcolor=colors['output'])
        c.node('fhir_export', 'FHIR Bundle\nExport', fillcolor=colors['output'])
        c.node('csv_export', 'CSV/JSON\nExport', fillcolor=colors['output'])
    
    # Data Flow Connections
    
    # Input to Agents
    dot.edge('user_queries', 'rag_orchestrator', label='Clinical\nProblem')
    dot.edge('pubmed', 'literature_agent', label='Literature\nRetrieval')
    dot.edge('clinical_trials', 'literature_agent', label='Trial Data')
    dot.edge('fda_guidance', 'web_monitor', label='Regulatory\nGuidance')
    dot.edge('who_reports', 'web_monitor', label='Global\nGuidelines')
    
    # Agent Orchestration
    dot.edge('rag_orchestrator', 'literature_agent', label='Coordinate')
    dot.edge('rag_orchestrator', 'synthetic_agent', label='Generate')
    dot.edge('rag_orchestrator', 'validation_agent', label='Validate')
    dot.edge('literature_agent', 'synthetic_agent', label='Context')
    dot.edge('synthetic_agent', 'validation_agent', label='Review')
    
    # Processing Flow
    dot.edge('synthetic_agent', 'ehr_generator', label='Schema\nRequests')
    dot.edge('ehr_generator', 'clinical_engine', label='Templates')
    dot.edge('clinical_engine', 'bias_detector', label='Generated\nData')
    dot.edge('bias_detector', 'quality_engine', label='Cleaned\nData')
    
    # Validation Flow
    dot.edge('quality_engine', 'clinical_validation', label='Quality\nCheck')
    dot.edge('clinical_validation', 'statistical_validation', label='Clinical\nApproval')
    dot.edge('statistical_validation', 'demographic_validation', label='Stats\nValidated')
    dot.edge('demographic_validation', 'audit_engine', label='Final\nApproval')
    
    # Storage Connections
    dot.edge('audit_engine', 'postgresql', label='Patient\nData')
    dot.edge('audit_engine', 'audit_db', label='Audit\nTrails')
    dot.edge('pharma_workflows', 'ux_analytics', label='UX\nEvents')
    dot.edge('quality_engine', 'cache_layer', label='Temp\nStorage')
    
    # Output Connections
    dot.edge('postgresql', 'api_server', label='Data\nAccess')
    dot.edge('api_server', 'research_dashboard', label='API\nCalls')
    dot.edge('api_server', 'pharma_workflows', label='Workflow\nData')
    dot.edge('api_server', 'pediatric_demo', label='Specialized\nData')
    dot.edge('postgresql', 'fhir_export', label='FHIR\nConversion')
    dot.edge('postgresql', 'csv_export', label='Research\nExports')
    
    return dot

def create_data_pipeline_diagram():
    """Create detailed data processing pipeline"""
    
    dot = graphviz.Digraph(comment='Data Processing Pipeline')
    dot.attr(rankdir='LR', size='14,8')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
    
    # Pipeline stages
    stages = [
        ('input', 'Clinical Problem\nStatement', '#E8F4FD'),
        ('literature', 'Literature\nRetrieval', '#FFF2CC'),
        ('context', 'Context\nExtraction', '#FFF2CC'),
        ('generation', 'Patient\nGeneration', '#D5E8D4'),
        ('validation', 'Multi-layer\nValidation', '#FFE6CC'),
        ('audit', 'Audit Trail\nCreation', '#F8CECC'),
        ('export', 'Data\nExport', '#E1D5E7')
    ]
    
    # Create nodes
    for stage_id, label, color in stages:
        dot.node(stage_id, label, fillcolor=color)
    
    # Create pipeline flow
    for i in range(len(stages) - 1):
        current_stage = stages[i][0]
        next_stage = stages[i + 1][0]
        dot.edge(current_stage, next_stage)
    
    # Add details for each stage
    with dot.subgraph(name='cluster_details') as c:
        c.attr(label='📋 Pipeline Details', style='filled', color='lightgrey')
        
        # Literature retrieval details
        c.node('pubmed_api', 'PubMed API\nNCBI E-utilities', fillcolor='#FFF2CC', shape='ellipse')
        c.node('trials_api', 'ClinicalTrials.gov\nAPI', fillcolor='#FFF2CC', shape='ellipse')
        
        # Validation details  
        c.node('clinical_check', 'Clinical Realism\nValidation', fillcolor='#FFE6CC', shape='ellipse')
        c.node('stats_check', 'Statistical\nConsistency', fillcolor='#FFE6CC', shape='ellipse')
        c.node('bias_check', 'Bias Detection\n& Mitigation', fillcolor='#FFE6CC', shape='ellipse')
        
        # Export formats
        c.node('fhir_out', 'FHIR R4\nBundle', fillcolor='#E1D5E7', shape='ellipse')
        c.node('csv_out', 'CSV\nDataset', fillcolor='#E1D5E7', shape='ellipse')
        c.node('json_out', 'JSON\nRecords', fillcolor='#E1D5E7', shape='ellipse')
    
    # Connect details to main pipeline
    dot.edge('literature', 'pubmed_api', style='dashed')
    dot.edge('literature', 'trials_api', style='dashed')
    dot.edge('validation', 'clinical_check', style='dashed')
    dot.edge('validation', 'stats_check', style='dashed')
    dot.edge('validation', 'bias_check', style='dashed')
    dot.edge('export', 'fhir_out', style='dashed')
    dot.edge('export', 'csv_out', style='dashed')
    dot.edge('export', 'json_out', style='dashed')
    
    return dot

def create_compliance_framework_diagram():
    """Create regulatory compliance framework visualization"""
    
    dot = graphviz.Digraph(comment='Compliance Framework')
    dot.attr(rankdir='TB', size='10,12')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
    
    # Compliance standards
    with dot.subgraph(name='cluster_standards') as c:
        c.attr(label='📋 Regulatory Standards', style='filled', color='lightgrey')
        c.node('hipaa', 'HIPAA\nPrivacy & Security', fillcolor='#FFE6CC')
        c.node('gdpr', 'GDPR\nData Protection', fillcolor='#FFE6CC')
        c.node('fda_21cfr', 'FDA 21 CFR Part 11\nElectronic Records', fillcolor='#FFE6CC')
        c.node('ich_gcp', 'ICH GCP\nClinical Practice', fillcolor='#FFE6CC')
        c.node('iso_27001', 'ISO 27001\nInformation Security', fillcolor='#FFE6CC')
    
    # Implementation layer
    with dot.subgraph(name='cluster_implementation') as c:
        c.attr(label='⚙️ Implementation Layer', style='filled', color='lightgrey')
        c.node('audit_trails', 'Complete Audit\nTrails', fillcolor='#D5E8D4')
        c.node('data_lineage', 'Data Lineage\nTracking', fillcolor='#D5E8D4')
        c.node('access_controls', 'Access Controls\n& Authentication', fillcolor='#D5E8D4')
        c.node('encryption', 'Data Encryption\n& Security', fillcolor='#D5E8D4')
        c.node('validation_framework', 'Validation\nFramework', fillcolor='#D5E8D4')
    
    # Technical controls
    with dot.subgraph(name='cluster_technical') as c:
        c.attr(label='🔧 Technical Controls', style='filled', color='lightgrey')
        c.node('database_audit', 'Database\nAudit Logging', fillcolor='#F8CECC')
        c.node('ux_tracking', 'UX Event\nTracking', fillcolor='#F8CECC')
        c.node('enterprise_framework', 'Enterprise DoD\nFramework', fillcolor='#F8CECC')
        c.node('traceability', 'Complete\nTraceability', fillcolor='#F8CECC')
    
    # Connect compliance requirements to implementation
    dot.edge('hipaa', 'audit_trails')
    dot.edge('hipaa', 'access_controls')
    dot.edge('gdpr', 'data_lineage')
    dot.edge('gdpr', 'encryption')
    dot.edge('fda_21cfr', 'validation_framework')
    dot.edge('fda_21cfr', 'audit_trails')
    dot.edge('ich_gcp', 'validation_framework')
    dot.edge('iso_27001', 'encryption')
    dot.edge('iso_27001', 'access_controls')
    
    # Connect implementation to technical controls
    dot.edge('audit_trails', 'database_audit')
    dot.edge('audit_trails', 'enterprise_framework')
    dot.edge('data_lineage', 'traceability')
    dot.edge('validation_framework', 'ux_tracking')
    dot.edge('access_controls', 'enterprise_framework')
    
    return dot

def main():
    """Main visualization dashboard"""
    

    
    st.title("🏗️ Synthetic Ascension System Architecture")
    st.markdown("**Complete data flow visualization and compliance framework**")
    
    # Track page view
    ux_event = track_ux_event(
        UXEventType.PAGE_VIEW,
        "data_flow_visualizer",
        {"page": "system_architecture", "timestamp": datetime.now().isoformat()}
    )
    
    # Diagram selection
    diagram_type = st.selectbox(
        "Select Visualization",
        [
            "Complete System Architecture",
            "Data Processing Pipeline", 
            "Compliance Framework",
            "EHR Schema Overview"
        ]
    )
    
    # Track user interaction
    if diagram_type:
        track_ux_event(
            UXEventType.FILTER_APPLIED,
            "diagram_selector",
            {"selected_diagram": diagram_type}
        )
    
    if diagram_type == "Complete System Architecture":
        st.subheader("🌐 Complete System Architecture")
        st.markdown("""
        **Enterprise-grade synthetic EHR platform with multi-agent orchestration**
        
        This diagram shows how authentic medical literature flows through our AI agents to generate 
        validated synthetic patient cohorts with complete audit trails and regulatory compliance.
        """)
        
        diagram = create_system_architecture_diagram()
        st.graphviz_chart(diagram.source)
        
        # Show data flow statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Data Sources", "4", "PubMed, ClinicalTrials.gov, FDA, WHO")
        with col2:
            st.metric("AI Agents", "6", "Specialized medical agents")
        with col3:
            st.metric("Validation Layers", "4", "Multi-tier quality assurance")
        with col4:
            st.metric("Output Formats", "5", "FHIR, CSV, JSON, API, Dashboard")
    
    elif diagram_type == "Data Processing Pipeline":
        st.subheader("⚙️ Data Processing Pipeline")
        st.markdown("""
        **Step-by-step synthetic EHR generation process**
        
        From clinical problem statement to validated synthetic patient data with complete traceability.
        """)
        
        diagram = create_data_pipeline_diagram()
        st.graphviz_chart(diagram.source)
        
        # Pipeline metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Processing Stages", "7", "End-to-end pipeline")
        with col2:
            st.metric("Validation Steps", "3", "Clinical, statistical, bias")
        with col3:
            st.metric("Export Options", "3", "FHIR, CSV, JSON")
    
    elif diagram_type == "Compliance Framework":
        st.subheader("📋 Regulatory Compliance Framework")
        st.markdown("""
        **Healthcare-grade compliance and audit framework**
        
        Meets FDA, HIPAA, GDPR, and ICH GCP requirements for pharmaceutical and healthcare deployments.
        """)
        
        diagram = create_compliance_framework_diagram()
        st.graphviz_chart(diagram.source)
        
        # Compliance metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Regulatory Standards", "5", "Healthcare compliant")
        with col2:
            st.metric("Technical Controls", "4", "Enterprise security")
        with col3:
            st.metric("Audit Coverage", "100%", "Complete traceability")
    
    elif diagram_type == "EHR Schema Overview":
        st.subheader("📊 Complete EHR Schema")
        st.markdown("""
        **Comprehensive medical record structure with full clinical detail**
        
        Each synthetic patient includes demographics, encounters, diagnoses, medications, labs, 
        imaging, hemodynamics, hematology, genomics, wearables, and administrative data.
        """)
        
        # Display schema structure
        schema = generate_complete_ehr_schema()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Core Clinical Modules:**")
            core_modules = [
                "Demographics", "Clinical Encounters", "Diagnoses (ICD-10/SNOMED)",
                "Medications (RxNorm)", "Lab Results (LOINC)", "Imaging Studies"
            ]
            for module in core_modules:
                st.write(f"✅ {module}")
                
        with col2:
            st.write("**Specialized Data:**")
            specialized_modules = [
                "Hemodynamic Data", "Hematology/CBC", "Genomic Data",
                "Wearable/IoT Data", "Administrative/Billing", "Audit Trails"
            ]
            for module in specialized_modules:
                st.write(f"✅ {module}")
        
        # Schema metrics
        st.subheader("📈 Schema Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Data Modules", "13", "Complete coverage")
        with col2:
            st.metric("Coding Standards", "5", "ICD-10, SNOMED, RxNorm, LOINC, CPT")
        with col3:
            st.metric("Compliance Frameworks", "5", "Healthcare regulations")
        with col4:
            st.metric("Audit Fields", "15+", "Per record")
        
        # Show detailed schema
        if st.expander("🔍 Detailed Schema Structure", expanded=False):
            st.json(schema)
    
    # UX Analytics Dashboard
    st.subheader("📊 UX Analytics & Tracking")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Page Views Tracked", "Real-time", "Complete user journey")
    with col2:
        st.metric("User Interactions", "All Events", "Button clicks, form submits")
    with col3:
        st.metric("Persona Analytics", "Role-based", "CDO, CMO, RWE, Innovation")
    
    st.info("""
    **🎯 Enterprise Features Active:**
    - ✅ Complete audit trails for every synthetic record
    - ✅ UX event tracking for frontend analytics  
    - ✅ Regulatory compliance framework (HIPAA, GDPR, FDA)
    - ✅ Authentic data connections (PubMed, ClinicalTrials.gov)
    - ✅ Multi-agent orchestration with quality validation
    - ✅ Specialized pharmaceutical and pediatric workflows
    """)

if __name__ == "__main__":
    main()