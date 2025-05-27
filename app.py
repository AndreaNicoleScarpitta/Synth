"""
Synthetic Ascension Marketing Launch Page
The default landing experience for Synthetic Ascension platform
"""

import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import re
import uuid
from typing import Dict, Any
from utils.medical_tooltips import initialize_tooltips, medical_tooltip, wrap_medical_text

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="Synthetic Ascension - Enterprise Synthetic EHR Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Database setup for user registrations
def init_registration_db():
    """Initialize SQLite database for user registrations"""
    conn = sqlite3.connect('user_registrations.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        registration_id TEXT UNIQUE,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        company TEXT,
        job_title TEXT,
        company_size TEXT,
        use_case TEXT,
        interest_level TEXT,
        registration_timestamp DATETIME,
        ip_address TEXT,
        user_agent TEXT,
        referral_source TEXT,
        demo_requested BOOLEAN DEFAULT FALSE,
        follow_up_status TEXT DEFAULT 'pending'
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS demo_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT UNIQUE,
        email TEXT NOT NULL,
        login_timestamp DATETIME,
        ip_address TEXT,
        session_duration_minutes INTEGER,
        pages_visited TEXT,
        actions_performed TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def save_registration(registration_data: Dict[str, Any]) -> str:
    """Save user registration to database"""
    conn = sqlite3.connect('user_registrations.db')
    cursor = conn.cursor()
    
    registration_id = str(uuid.uuid4())
    
    cursor.execute('''
    INSERT INTO registrations 
    (registration_id, full_name, email, company, job_title, company_size, 
     use_case, interest_level, registration_timestamp, demo_requested)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        registration_id,
        registration_data['full_name'],
        registration_data['email'],
        registration_data['company'],
        registration_data['job_title'],
        registration_data['company_size'],
        registration_data['use_case'],
        registration_data['interest_level'],
        datetime.now(),
        registration_data.get('demo_requested', False)
    ))
    
    conn.commit()
    conn.close()
    
    return registration_id

def validate_demo_login(email: str, password: str) -> bool:
    """Validate demo access credentials"""
    valid_email = "andrew.scarpitta@gmail.com"
    valid_password = "Sofia&Glacier2023"
    
    return email.lower() == valid_email.lower() and password == valid_password

def log_demo_session(email: str):
    """Log successful demo session"""
    conn = sqlite3.connect('user_registrations.db')
    cursor = conn.cursor()
    
    session_id = str(uuid.uuid4())
    
    cursor.execute('''
    INSERT INTO demo_sessions (session_id, email, login_timestamp)
    VALUES (?, ?, ?)
    ''', (session_id, email, datetime.now()))
    
    conn.commit()
    conn.close()
    
    return session_id

def main():
    """Main launch page with marketing content and registration"""
    
    # Initialize medical tooltips
    initialize_tooltips()
    
    # Initialize database
    init_registration_db()
    
    # Synthetic Ascension Design System Implementation
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');
    
    /* Design System Color Palette */
    :root {
        --ascension-blue: #0A1F44;
        --synth-white: #F5F7FA;
        --biotech-green: #34C759;
        --signal-violet: #6B4EFF;
        --slate-gray: #3C3C4E;
        --alert-red: #FF3B30;
        --base-unit: 8px;
    }
    
    /* Typography System */
    h1 { font-family: 'Syne', sans-serif; font-size: 48px; font-weight: 800; }
    h2 { font-family: 'Syne', sans-serif; font-size: 32px; font-weight: 700; }
    h3 { font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 600; }
    h4 { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 600; }
    body, p, div { font-family: 'Inter', sans-serif; font-size: 16px; font-weight: 400; }
    code { font-family: 'JetBrains Mono', monospace; }
    
    /* Global Background */
    .main .block-container {
        background: var(--synth-white);
        max-width: 1280px;
        padding: calc(var(--base-unit) * 3);
    }
    
    /* Brand Header Component */
    .brand-header {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        padding: calc(var(--base-unit) * 6);
        border-radius: calc(var(--base-unit) * 2);
        color: var(--ascension-blue);
        text-align: center;
        margin-bottom: calc(var(--base-unit) * 4);
        box-shadow: 0 calc(var(--base-unit) * 3) calc(var(--base-unit) * 6) rgba(10, 31, 68, 0.1);
        border: 2px solid #e2e8f0;
    }
    
    .brand-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: calc(var(--base-unit) * 3);
        gap: calc(var(--base-unit) * 2);
    }
    
    .logo-icon {
        font-size: calc(var(--base-unit) * 8);
        background: linear-gradient(45deg, var(--biotech-green), var(--signal-violet));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 calc(var(--base-unit) * 3) rgba(52, 199, 89, 0.3));
    }
    
    .brand-name {
        font-family: 'Syne', sans-serif;
        font-size: calc(var(--base-unit) * 7);
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .brand-tagline {
        font-size: calc(var(--base-unit) * 2);
        opacity: 0.8;
        letter-spacing: 3px;
        font-weight: 500;
        margin-top: calc(var(--base-unit));
        text-transform: uppercase;
    }
    
    .brand-description {
        font-size: calc(var(--base-unit) * 2.5);
        font-weight: 300;
        margin-top: calc(var(--base-unit) * 3);
        opacity: 0.9;
        line-height: 1.4;
    }
    
    /* Component: Stats Cards */
    .stats-card {
        background: white;
        color: var(--ascension-blue);
        padding: calc(var(--base-unit) * 3);
        border-radius: calc(var(--base-unit) * 2);
        text-align: center;
        margin: var(--base-unit);
        box-shadow: 0 calc(var(--base-unit) * 2) calc(var(--base-unit) * 4) rgba(10, 31, 68, 0.15);
        border: 2px solid var(--signal-violet);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stats-card:hover {
        transform: translateY(calc(var(--base-unit) * -0.5));
        box-shadow: 0 calc(var(--base-unit) * 3) calc(var(--base-unit) * 6) rgba(107, 78, 255, 0.35);
    }
    
    /* Component: Feature Cards */
    .feature-card {
        background: white;
        padding: calc(var(--base-unit) * 4);
        border-radius: calc(var(--base-unit) * 2);
        border: 1px solid rgba(60, 60, 78, 0.08);
        margin: calc(var(--base-unit) * 2) 0;
        box-shadow: 0 calc(var(--base-unit)) calc(var(--base-unit) * 4) rgba(60, 60, 78, 0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        color: var(--ascension-blue);
    }
    
    .feature-card p {
        color: var(--ascension-blue);
        line-height: 1.6;
        margin: 0;
    }
    
    .feature-card:hover {
        transform: translateY(calc(var(--base-unit) * -0.5));
        box-shadow: 0 calc(var(--base-unit) * 2) calc(var(--base-unit) * 8) rgba(60, 60, 78, 0.12);
        border-color: var(--signal-violet);
    }
    
    .feature-icon {
        font-size: calc(var(--base-unit) * 3);
        margin-bottom: calc(var(--base-unit) * 2);
        color: var(--signal-violet);
    }
    
    .feature-title {
        font-family: 'Syne', sans-serif;
        font-size: calc(var(--base-unit) * 2.5);
        font-weight: 600;
        color: var(--ascension-blue);
        margin-bottom: calc(var(--base-unit) * 1.5);
    }
    
    /* Component: Testimonials */
    .testimonial-card {
        background: linear-gradient(135deg, var(--ascension-blue) 0%, #1a2b5c 100%);
        color: white;
        padding: calc(var(--base-unit) * 4);
        border-radius: calc(var(--base-unit) * 2);
        font-style: italic;
        margin: calc(var(--base-unit) * 3) 0;
        box-shadow: 0 calc(var(--base-unit) * 2) calc(var(--base-unit) * 6) rgba(10, 31, 68, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
    }
    
    .testimonial-card::before {
        content: '"';
        font-size: calc(var(--base-unit) * 8);
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        color: var(--biotech-green);
        position: absolute;
        top: calc(var(--base-unit) * -1);
        left: calc(var(--base-unit) * 2);
        opacity: 0.3;
    }
    
    /* Component: Technology Section */
    .tech-section {
        background: linear-gradient(135deg, var(--ascension-blue) 0%, #1a2b5c 100%);
        color: white;
        padding: calc(var(--base-unit) * 6);
        border-radius: calc(var(--base-unit) * 3);
        margin: calc(var(--base-unit) * 6) 0;
        box-shadow: 0 calc(var(--base-unit) * 3) calc(var(--base-unit) * 8) rgba(10, 31, 68, 0.3);
    }
    
    .tech-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: calc(var(--base-unit) * 4);
        margin-top: calc(var(--base-unit) * 4);
    }
    
    .tech-column h4 {
        color: var(--biotech-green);
        margin-bottom: calc(var(--base-unit) * 2);
        font-size: calc(var(--base-unit) * 2.5);
    }
    
    .tech-column ul {
        list-style: none;
        padding-left: 0;
    }
    
    .tech-column li {
        padding: calc(var(--base-unit) * 0.5) 0;
        padding-left: calc(var(--base-unit) * 2);
        position: relative;
    }
    
    .tech-column li::before {
        content: '▸';
        color: var(--signal-violet);
        font-weight: bold;
        position: absolute;
        left: 0;
    }
    
    /* Component: Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--signal-violet) 0%, #8B5FFF 100%);
        color: white;
        border: none;
        border-radius: calc(var(--base-unit) * 1.5);
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        padding: calc(var(--base-unit) * 1.5) calc(var(--base-unit) * 3);
        box-shadow: 0 calc(var(--base-unit)) calc(var(--base-unit) * 3) rgba(107, 78, 255, 0.25);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: calc(var(--base-unit) * 2);
    }
    
    .stButton > button:hover {
        transform: translateY(calc(var(--base-unit) * -0.25));
        box-shadow: 0 calc(var(--base-unit) * 1.5) calc(var(--base-unit) * 4) rgba(107, 78, 255, 0.4);
        background: linear-gradient(135deg, #7B4FEF 0%, #9B6FFF 100%);
    }
    
    /* Component: Form Inputs */
    .stTextInput > div > div > input {
        border: 2px solid rgba(60, 60, 78, 0.1);
        border-radius: var(--base-unit);
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--signal-violet);
        box-shadow: 0 0 0 3px rgba(107, 78, 255, 0.1);
    }
    
    /* Component: Status Chips */
    .status-chip {
        display: inline-flex;
        align-items: center;
        padding: calc(var(--base-unit) * 0.5) calc(var(--base-unit) * 1.5);
        border-radius: calc(var(--base-unit) * 3);
        font-size: calc(var(--base-unit) * 1.5);
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }
    
    .status-validated {
        background: rgba(52, 199, 89, 0.1);
        color: var(--biotech-green);
        border: 1px solid rgba(52, 199, 89, 0.2);
    }
    
    .status-generated {
        background: rgba(107, 78, 255, 0.1);
        color: var(--signal-violet);
        border: 1px solid rgba(107, 78, 255, 0.2);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .brand-name { font-size: calc(var(--base-unit) * 5); }
        .brand-description { font-size: calc(var(--base-unit) * 2); }
        .tech-grid { grid-template-columns: 1fr; }
        .brand-logo { flex-direction: column; gap: var(--base-unit); }
    }
    
    /* Accessibility Enhancements */
    .stButton > button:focus {
        outline: 2px solid var(--biotech-green);
        outline-offset: 2px;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: var(--base-unit);
    }
    
    ::-webkit-scrollbar-track {
        background: var(--synth-white);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--signal-violet);
        border-radius: calc(var(--base-unit) * 0.5);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero section with brand identity
    st.markdown("""
    <div class="brand-header">
        <div class="brand-logo">
            <div>
                <h1 class="brand-name">Synthetic Ascension</h1>
                <div class="brand-tagline">Simulate. Validate. Ascend.</div>
            </div>
        </div>
        <div class="brand-description">
            The world's most advanced platform for privacy-preserving synthetic EHR generation, 
            powered by AI agents and validated against comprehensive medical literature.
        </div>
        <div style="margin-top: 2rem; font-size: 1.2rem; color: #34C759; font-weight: 500;">
            Accelerate pharmaceutical research while maintaining complete data privacy and regulatory compliance.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Value proposition
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stats-card">
            <h3 style="margin: 0; font-size: 2.5rem; font-weight: 800;">80%</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">Faster Model Development</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card">
            <h3 style="margin: 0; font-size: 2.5rem; font-weight: 800;">100%</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">Privacy Compliant</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card">
            <h3 style="margin: 0; font-size: 2.5rem; font-weight: 800;">FDA Ready</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">Regulatory Compliance</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Core capabilities section
    st.markdown("""
    <div style="margin: 3rem 0;">
        <h2 style="font-family: 'Syne', sans-serif; color: #0A1F44; font-weight: 600; font-size: 2.2rem; text-align: center; margin-bottom: 2rem;">
            Accelerate Your Healthcare AI Development
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="margin-bottom: 2.5rem;">
            <h3 style="color: #0A1F44; font-weight: 600; margin-bottom: 0.5rem; font-size: 1.3rem;">AI-Powered Generation</h3>
            <p style="color: #374151; line-height: 1.6; margin: 0; font-size: 1rem;">Multi-agent system retrieves real medical literature and generates clinically accurate synthetic patients with complete audit trails.</p>
        </div>
        
        <div style="margin-bottom: 2.5rem;">
            <h3 style="color: #0A1F44; font-weight: 600; margin-bottom: 0.5rem; font-size: 1.3rem;">Bias-Aware & Fair</h3>
            <p style="color: #374151; line-height: 1.6; margin: 0; font-size: 1rem;">Advanced statistical validation ensures demographic representation and eliminates AI bias across all patient populations.</p>
        </div>
        
        <div style="margin-bottom: 2.5rem;">
            <h3 style="color: #0A1F44; font-weight: 600; margin-bottom: 0.5rem; font-size: 1.3rem;">Complete Medical Records</h3>
            <p style="color: #374151; line-height: 1.6; margin: 0; font-size: 1rem;">Generate full EHRs with demographics, diagnoses, medications, labs, imaging, and specialized data like """ + medical_tooltip("hemodynamics") + """.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="margin-bottom: 2.5rem;">
            <h3 style="color: #0A1F44; font-weight: 600; margin-bottom: 0.5rem; font-size: 1.3rem;">Regulatory Compliant</h3>
            <p style="color: #374151; line-height: 1.6; margin: 0; font-size: 1rem;">Meets """ + medical_tooltip("hipaa", "HIPAA") + """, """ + medical_tooltip("gdpr", "GDPR") + """, and FDA """ + medical_tooltip("cfr_part_11", "21 CFR Part 11") + """ requirements with complete traceability and enterprise-grade security.</p>
        </div>
        
        <div style="margin-bottom: 2.5rem;">
            <h3 style="color: #0A1F44; font-weight: 600; margin-bottom: 0.5rem; font-size: 1.3rem;">Literature-Backed</h3>
            <p style="color: #374151; line-height: 1.6; margin: 0; font-size: 1rem;">Connects to PubMed, ClinicalTrials.gov, and FDA databases for authentic, up-to-date medical knowledge integration.</p>
        </div>
        
        <div style="margin-bottom: 2.5rem;">
            <h3 style="color: #0A1F44; font-weight: 600; margin-bottom: 0.5rem; font-size: 1.3rem;">Pharma-Ready Workflows</h3>
            <p style="color: #374151; line-height: 1.6; margin: 0; font-size: 1rem;">Specialized interfaces for CDOs, CMOs, RWE teams, and regulatory affairs with role-specific analytics.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Use cases section
    st.markdown("""
    <div style="margin: 3rem 0;">
        <h2 style="font-family: 'Syne', sans-serif; color: #0A1F44; font-weight: 600; font-size: 2.2rem; text-align: center; margin-bottom: 2rem;">
            Perfect For Your Use Case
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    use_case_tabs = st.tabs([
        "Pharmaceutical Companies",
        "Healthcare Systems", 
        "Academic Research",
        "AI/ML Companies"
    ])
    
    with use_case_tabs[0]:
        st.markdown("""
        **Accelerate Drug Development & Clinical Trials**
        - Generate diverse patient cohorts for AI model training
        - Simulate clinical trial outcomes and optimize protocols
        - Support regulatory submissions with bias-aware validation
        - Enable real-world evidence generation for payer negotiations
        """)
        
        st.markdown("""
        <div class="testimonial-card">
        "Synthetic Ascension reduced our AI model development time from 6 months to 3 weeks while ensuring demographic fairness across all patient groups."
        <br><br><strong>- Chief Data Officer, Top 10 Pharma Company</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with use_case_tabs[1]:
        st.markdown("""
        **Privacy-Safe Research & Analytics**
        - Generate synthetic patient data for quality improvement
        - Train predictive models without PHI exposure
        - Enable multi-site research collaboration
        - Support population health analytics
        """)
    
    with use_case_tabs[2]:
        st.markdown("""
        **Enable Groundbreaking Medical Research**
        - Access diverse patient populations for studies
        - Generate rare disease cohorts for research
        - Support reproducible AI research
        - Facilitate international research collaboration
        """)
    
    with use_case_tabs[3]:
        st.markdown("""
        **Build Healthcare AI Solutions**
        - Train models on comprehensive medical data
        - Validate AI fairness across demographics
        - Accelerate healthcare AI product development
        - Ensure regulatory compliance from day one
        """)
    
    # Technical highlights with professional styling
    st.markdown("""
    <div class="tech-section">
        <h2 style="text-align: center; margin-bottom: 3rem; font-size: 2.5rem; font-weight: 300;">Enterprise-Grade Technology</h2>
        <div class="tech-grid">
            <div class="tech-column">
                <h4>Multi-Agent Architecture</h4>
                <ul>
                    <li>Literature retrieval agents</li>
                    <li>Synthetic cohort generators</li>
                    <li>Statistical validation agents</li>
                    <li>Medical terminology validators</li>
                    <li>Web monitoring & curation</li>
                </ul>
            </div>
            <div class="tech-column">
                <h4>Data Quality Assurance</h4>
                <ul>
                    <li>Clinical realism validation</li>
                    <li>Statistical consistency checks</li>
                    <li>Demographic bias detection</li>
                    <li>Complete audit trails</li>
                    <li>Quality scoring metrics</li>
                </ul>
            </div>
            <div class="tech-column">
                <h4>Integration Ready</h4>
                <ul>
                    <li>REST API with Swagger docs</li>
                    <li>FHIR R4 bundle export</li>
                    <li>CSV/JSON data formats</li>
                    <li>PostgreSQL backend</li>
                    <li>Real-time WebSocket updates</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call-to-action section with scheduling
    st.markdown("""
    <div style="margin: 3rem 0; text-align: center;">
        <h2 style="font-family: 'Syne', sans-serif; color: #0A1F44; font-weight: 600; font-size: 2.2rem; margin-bottom: 1rem;">
            Ready to Transform Your Research?
        </h2>
        <p style="font-size: 1.2rem; color: #3C3C4E; margin-bottom: 2rem;">
            Join leading pharmaceutical companies and research institutions using Synthetic Ascension
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dual call-to-action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border: 2px solid #6B4EFF; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(107, 78, 255, 0.15);">
            <h3 style="color: #0A1F44; margin-top: 0; font-weight: 700;">Design Partnership Interest</h3>
            <p style="color: #3C3C4E; margin-bottom: 1.5rem; line-height: 1.5;">Partner with us to shape the future of synthetic EHR technology for your specific research needs.</p>
            <a href="https://calendly.com/andrew-scarpitta-cscb/30min" target="_blank" style="
                display: inline-block;
                background: linear-gradient(135deg, #6B4EFF 0%, #8B5FFF 100%);
                color: white;
                padding: 14px 28px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: 600;
                font-size: 1.1rem;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(107, 78, 255, 0.25);
            ">Explore Partnership</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border: 2px solid #34C759; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(52, 199, 89, 0.15);">
            <h3 style="color: #0A1F44; margin-top: 0; font-weight: 700;">Join Waitlist</h3>
            <p style="color: #3C3C4E; margin-bottom: 1.5rem; line-height: 1.5;">Get priority access and updates on platform availability.</p>
            <div style="padding-top: 14px;">
                <strong style="color: #34C759; font-size: 1.1rem;">Register below for early access</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Registration section
    st.markdown("""
    <div style="margin: 2rem 0;">
        <h2 style="font-family: 'Syne', sans-serif; color: #0A1F44; font-weight: 600; font-size: 2rem; text-align: center; margin-bottom: 2rem;">
            Get Early Access
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("registration_form", clear_on_submit=True):
        st.markdown("**Join the waitlist for early access to Synthetic Ascension**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *", placeholder="Dr. Jane Smith")
            email = st.text_input("Work Email *", placeholder="jane.smith@company.com")
            company = st.text_input("Company *", placeholder="Acme Pharmaceuticals")
            
        with col2:
            job_title = st.text_input("Job Title *", placeholder="Chief Data Officer")
            company_size = st.selectbox("Company Size", [
                "Startup (1-50 employees)",
                "Mid-size (51-500 employees)", 
                "Large (501-5000 employees)",
                "Enterprise (5000+ employees)"
            ])
            
        use_case = st.text_area("Primary Use Case", 
                               placeholder="Describe how you plan to use synthetic EHR data...",
                               height=100)
        
        interest_level = st.select_slider(
            "Interest Level",
            options=["Exploring", "Evaluating", "Planning Implementation", "Ready to Deploy"],
            value="Evaluating"
        )
        
        demo_requested = st.checkbox("Request priority demo access")
        
        submitted = st.form_submit_button("Join Waitlist", use_container_width=True)
        
        if submitted:
            if full_name and email and company and job_title:
                # Basic email validation
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if re.match(email_pattern, email):
                    registration_data = {
                        'full_name': full_name,
                        'email': email,
                        'company': company,
                        'job_title': job_title,
                        'company_size': company_size,
                        'use_case': use_case,
                        'interest_level': interest_level,
                        'demo_requested': demo_requested
                    }
                    
                    registration_id = save_registration(registration_data)
                    
                    st.success(f"""
                    **Registration Successful!**
                    
                    Thank you for your interest in Synthetic Ascension. We've added you to our priority access list.
                    
                    **Registration ID:** {registration_id[:8]}...
                    
                    Our team will contact you within 48 hours to discuss your use case and provide access details.
                    """)
                    
                    # Add partnership option
                    st.markdown("""
                    <div style="margin: 1.5rem 0; padding: 1.5rem; background: white; border: 2px solid #6B4EFF; border-radius: 12px; box-shadow: 0 4px 12px rgba(107, 78, 255, 0.15);">
                        <h4 style="color: #0A1F44; margin-top: 0; font-weight: 700;">Design Partnership Interest</h4>
                        <p style="color: #3C3C4E; margin-bottom: 1rem; line-height: 1.5;">Interested in shaping the future of synthetic EHR technology? Explore a design partnership tailored to your research needs.</p>
                        <a href="https://calendly.com/andrew-scarpitta-cscb/30min" target="_blank" style="
                            display: inline-block;
                            background: linear-gradient(135deg, #6B4EFF 0%, #8B5FFF 100%);
                            color: white;
                            padding: 12px 24px;
                            border-radius: 8px;
                            text-decoration: none;
                            font-weight: 600;
                            transition: all 0.3s ease;
                            border: none;
                            box-shadow: 0 4px 12px rgba(107, 78, 255, 0.25);
                        ">Explore Partnership</a>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if demo_requested:
                        st.info("**Priority Demo Access Requested** - You'll receive demo credentials via email within 24 hours.")
                else:
                    st.error("Please enter a valid email address.")
            else:
                st.error("Please fill in all required fields (*)")
    
    # Demo access section
    st.markdown("---")
    st.markdown("""
    <div style="margin: 3rem 0;">
        <h2 style="font-family: 'Syne', sans-serif; color: #0A1F44; font-weight: 600; font-size: 2.2rem; text-align: center; margin-bottom: 2rem;">
            Demo Access Portal
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Access Password-Protected Demo", use_container_width=True):
        st.session_state.show_demo_login = True
    
    if st.session_state.get('show_demo_login', False):
        with st.form("demo_login_form"):
            st.markdown("**Enter your demo credentials**")
            
            demo_email = st.text_input("Email", placeholder="your.email@company.com")
            demo_password = st.text_input("Password", type="password", placeholder="Enter demo password")
            
            login_submitted = st.form_submit_button("Access Demo")
            
            if login_submitted:
                if validate_demo_login(demo_email, demo_password):
                    session_id = log_demo_session(demo_email)
                    st.session_state.demo_authenticated = True
                    st.session_state.demo_session_id = session_id
                    
                    st.success("**Demo Access Granted!**")
                    
                    # Store demo authentication state
                    st.session_state.demo_authenticated = True
                    st.session_state.demo_session_id = session_id
                        
                else:
                    st.error("**Access Denied** - Invalid email or password. Please contact our team for demo credentials.")
    
    # Demo navigation - outside of forms
    if st.session_state.get('demo_authenticated', False):
        st.markdown("---")
        st.markdown("""
        <div style="margin: 2rem 0;">
            <h2 style="font-family: 'Syne', sans-serif; color: #0A1F44; font-weight: 600; font-size: 2rem; text-align: center; margin-bottom: 1rem;">
                Demo Access Granted
            </h2>
            <p style="text-align: center; color: #5A6F7A; font-size: 1.1rem; margin-bottom: 2rem;">
                Welcome to Synthetic Ascension Demo! Choose your workflow:
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("Pediatric Cardiology Demo", use_container_width=True):
                st.session_state.current_page = "pediatric_demo"
                st.rerun()
        
        with col2:
            if st.button("Pharma Executive Workflows", use_container_width=True):
                st.session_state.current_page = "pharma_workflows"
                st.rerun()
        
        with col3:
            if st.button("System Architecture", use_container_width=True):
                st.session_state.current_page = "architecture"
                st.rerun()
        
        with col4:
            if st.button("Research Dashboard", use_container_width=True):
                st.session_state.current_page = "research_dashboard"
                st.rerun()
    
    # Check if demo is authenticated and user wants to navigate
    if st.session_state.get('demo_authenticated', False) and st.session_state.get('current_page'):
        if st.session_state.current_page == "pediatric_demo":
            from pediatric_cardiology_demo import main as pediatric_main
            pediatric_main()
        elif st.session_state.current_page == "pharma_workflows":
            from pharma_executive_workflows import main as pharma_main
            pharma_main()
        elif st.session_state.current_page == "architecture":
            from data_flow_visualizer import main as arch_main
            arch_main()
        elif st.session_state.current_page == "research_dashboard":
            from research_dashboard import main as research_main
            research_main()
        return
    
    # Footer
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Contact**
        - hello@syntheticascension.com
        - Schedule a call
        - Book a demo
        """)
    
    with col2:
        st.markdown("""
        **Resources**
        - Documentation
        - Video demos
        - Case studies
        """)
    
    with col3:
        st.markdown("""
        **Security**
        - SOC 2 Type II
        - HIPAA Compliant
        - GDPR Ready
        """)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; color: #666;">
        © 2024 Synthetic Ascension. Transforming healthcare AI with privacy-preserving synthetic data.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()