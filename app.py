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
    
    # Page configuration
    st.set_page_config(
        page_title="Synthetic Ascension - Enterprise Synthetic EHR Platform",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize database
    init_registration_db()
    
    # Custom CSS for marketing appeal
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .stats-box {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .testimonial {
        background: #e3f2fd;
        padding: 1.5rem;
        border-radius: 10px;
        font-style: italic;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🧬 Synthetic Ascension</h1>
        <h2>Enterprise-Grade Synthetic EHR for Pharmaceutical Research</h2>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            Generate privacy-preserving, bias-aware synthetic patient data powered by AI agents and real medical literature
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Value proposition
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stats-box">
            <h3>80%</h3>
            <p>Faster Model Development</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-box">
            <h3>100%</h3>
            <p>Privacy Compliant</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-box">
            <h3>FDA Ready</h3>
            <p>Regulatory Compliance</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key benefits
    st.markdown("## 🚀 Accelerate Your Healthcare AI Development")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🤖 AI-Powered Generation</h4>
            <p>Multi-agent system retrieves real medical literature and generates clinically accurate synthetic patients with complete audit trails.</p>
        </div>
        
        <div class="feature-card">
            <h4>⚖️ Bias-Aware & Fair</h4>
            <p>Advanced statistical validation ensures demographic representation and eliminates AI bias across all patient populations.</p>
        </div>
        
        <div class="feature-card">
            <h4>🏥 Complete Medical Records</h4>
            <p>Generate full EHRs with demographics, diagnoses, medications, labs, imaging, and specialized data like hemodynamics.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>📋 Regulatory Compliant</h4>
            <p>Meets HIPAA, GDPR, and FDA 21 CFR Part 11 requirements with complete traceability and enterprise-grade security.</p>
        </div>
        
        <div class="feature-card">
            <h4>🔬 Literature-Backed</h4>
            <p>Connects to PubMed, ClinicalTrials.gov, and FDA databases for authentic, up-to-date medical knowledge integration.</p>
        </div>
        
        <div class="feature-card">
            <h4>💊 Pharma-Ready Workflows</h4>
            <p>Specialized interfaces for CDOs, CMOs, RWE teams, and regulatory affairs with role-specific analytics.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Use cases
    st.markdown("## 💼 Perfect For Your Use Case")
    
    use_case_tabs = st.tabs([
        "🏢 Pharmaceutical Companies",
        "🏥 Healthcare Systems", 
        "🎓 Academic Research",
        "🤖 AI/ML Companies"
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
        <div class="testimonial">
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
    
    # Technical highlights
    st.markdown("## 🔧 Enterprise-Grade Technology")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Multi-Agent Architecture**
        - Literature retrieval agents
        - Synthetic cohort generators  
        - Statistical validation agents
        - Medical terminology validators
        - Web monitoring & curation
        """)
    
    with col2:
        st.markdown("""
        **Data Quality Assurance**
        - Clinical realism validation
        - Statistical consistency checks
        - Demographic bias detection
        - Complete audit trails
        - Quality scoring metrics
        """)
    
    with col3:
        st.markdown("""
        **Integration Ready**
        - REST API with Swagger docs
        - FHIR R4 bundle export
        - CSV/JSON data formats
        - PostgreSQL backend
        - Real-time WebSocket updates
        """)
    
    # Registration form
    st.markdown("## 📝 Get Early Access")
    
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
        
        submitted = st.form_submit_button("🚀 Join Waitlist", use_container_width=True)
        
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
                    🎉 **Registration Successful!**
                    
                    Thank you for your interest in Synthetic Ascension. We've added you to our priority access list.
                    
                    **Registration ID:** {registration_id[:8]}...
                    
                    Our team will contact you within 48 hours to discuss your use case and provide access details.
                    """)
                    
                    if demo_requested:
                        st.info("✨ **Priority Demo Access Requested** - You'll receive demo credentials via email within 24 hours.")
                else:
                    st.error("Please enter a valid email address.")
            else:
                st.error("Please fill in all required fields (*)")
    
    # Demo access section
    st.markdown("---")
    st.markdown("## 🔐 Demo Access Portal")
    
    if st.button("🎮 Access Password-Protected Demo", use_container_width=True):
        st.session_state.show_demo_login = True
    
    if st.session_state.get('show_demo_login', False):
        with st.form("demo_login_form"):
            st.markdown("**Enter your demo credentials**")
            
            demo_email = st.text_input("Email", placeholder="your.email@company.com")
            demo_password = st.text_input("Password", type="password", placeholder="Enter demo password")
            
            login_submitted = st.form_submit_button("🔑 Access Demo")
            
            if login_submitted:
                if validate_demo_login(demo_email, demo_password):
                    session_id = log_demo_session(demo_email)
                    st.session_state.demo_authenticated = True
                    st.session_state.demo_session_id = session_id
                    
                    st.success("✅ **Demo Access Granted!**")
                    st.balloons()
                    
                    # Store demo authentication state
                    st.session_state.demo_authenticated = True
                    st.session_state.demo_session_id = session_id
                        
                else:
                    st.error("❌ **Access Denied** - Invalid email or password. Please contact our team for demo credentials.")
    
    # Demo navigation - outside of forms
    if st.session_state.get('demo_authenticated', False):
        st.markdown("---")
        st.markdown("## 🎮 **Demo Access Granted!**")
        st.markdown("**Welcome to Synthetic Ascension Demo! Choose your workflow:**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🫀 Pediatric Cardiology Demo", use_container_width=True):
                st.session_state.current_page = "pediatric_demo"
                st.rerun()
        
        with col2:
            if st.button("💊 Pharma Executive Workflows", use_container_width=True):
                st.session_state.current_page = "pharma_workflows"
                st.rerun()
        
        with col3:
            if st.button("🏗️ System Architecture", use_container_width=True):
                st.session_state.current_page = "architecture"
                st.rerun()
        
        with col4:
            if st.button("🔬 Research Dashboard", use_container_width=True):
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
        - 📧 hello@syntheticascension.com
        - 📞 Schedule a call
        - 💬 Book a demo
        """)
    
    with col2:
        st.markdown("""
        **Resources**
        - 📚 Documentation
        - 🎥 Video demos
        - 📊 Case studies
        """)
    
    with col3:
        st.markdown("""
        **Security**
        - 🔒 SOC 2 Type II
        - 🏥 HIPAA Compliant
        - 🌍 GDPR Ready
        """)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; color: #666;">
        © 2024 Synthetic Ascension. Transforming healthcare AI with privacy-preserving synthetic data.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()