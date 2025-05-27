"""
Secure API Client Interface for Synthetic Ascension
Demonstrates secure authentication, role-based access, and data protection
"""

import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Secure API Access - Synthetic Ascension",
    page_icon="🔐",
    layout="wide"
)

# Initialize session state
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "api_key" not in st.session_state:
    st.session_state.api_key = None

def display_header():
    """Display the secure API interface header"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #0A1F44 0%, #6B4EFF 100%); border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; margin-bottom: 0.5rem;">🔐 Secure API Access Portal</h1>
        <p style="color: #E3F2FD; font-size: 1.2rem; margin: 0;">
            Enterprise-grade security with role-based access control
        </p>
    </div>
    """, unsafe_allow_html=True)

def login_interface():
    """User authentication interface"""
    st.subheader("🔑 Authentication")
    
    if st.session_state.access_token is None:
        st.markdown("""
        **Demo Credentials Available:**
        - **Admin**: admin@syntheticascension.com / SecurePass123!
        - **Researcher**: researcher@syntheticascension.com / ResearchPass123!
        - **Analyst**: analyst@syntheticascension.com / AnalystPass123!
        """)
        
        with st.form("login_form"):
            username = st.text_input("Username/Email", placeholder="admin@syntheticascension.com")
            password = st.text_input("Password", type="password", placeholder="SecurePass123!")
            
            if st.form_submit_button("🔐 Login", type="primary"):
                try:
                    response = requests.post(
                        "http://localhost:8000/auth/login",
                        data={"username": username, "password": password}
                    )
                    
                    if response.status_code == 200:
                        auth_data = response.json()
                        st.session_state.access_token = auth_data["access_token"]
                        st.session_state.user_info = auth_data["user_info"]
                        st.success(f"✅ Welcome, {auth_data['user_info']['name']}!")
                        st.rerun()
                    else:
                        st.error(f"❌ Authentication failed: {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Could not connect to API server. Please ensure the API server is running on port 8000.")
                except Exception as e:
                    st.error(f"Login error: {str(e)}")
    
    else:
        # Display logged-in user info
        user_info = st.session_state.user_info
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.success(f"✅ Logged in as: **{user_info['name']}** ({user_info['role'].title()})")
        
        with col2:
            if st.button("🔑 Generate API Key"):
                generate_api_key_interface()
        
        with col3:
            if st.button("🚪 Logout"):
                st.session_state.access_token = None
                st.session_state.user_info = None
                st.session_state.api_key = None
                st.rerun()

def generate_api_key_interface():
    """Interface for generating API keys"""
    st.subheader("🔑 API Key Generation")
    
    if st.session_state.user_info["role"] in ["admin", "researcher"]:
        with st.form("api_key_form"):
            description = st.text_input(
                "API Key Description",
                placeholder="e.g., Data analysis script for Project Alpha"
            )
            
            if st.form_submit_button("Generate API Key", type="primary"):
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
                    response = requests.post(
                        "http://localhost:8000/auth/api-key",
                        json={"description": description},
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        api_data = response.json()
                        st.session_state.api_key = api_data["api_key"]
                        
                        st.success("✅ API Key Generated Successfully!")
                        st.code(api_data["api_key"], language="text")
                        
                        st.info(f"""
                        **Usage Instructions:**
                        - Header: `X-API-Key`
                        - Expires in: {api_data['expires_in_days']} days
                        - Store securely - this key won't be shown again!
                        """)
                        
                    else:
                        st.error(f"Failed to generate API key: {response.text}")
                        
                except Exception as e:
                    st.error(f"API key generation error: {str(e)}")
    else:
        st.warning("⚠️ API key generation requires Admin or Researcher role.")

def secure_data_access_interface():
    """Interface for secure data access"""
    if st.session_state.access_token is None:
        st.warning("🔐 Please log in to access secure data endpoints.")
        return
    
    st.subheader("🛡️ Secure Data Access")
    
    # Tab interface for different secure operations
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Patient Cohorts",
        "🔍 Secure Search", 
        "📋 Data Export",
        "📈 Audit Logs"
    ])
    
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    
    with tab1:
        st.markdown("**Access Patient Cohorts with Role-Based Security**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            limit = st.slider("Results Limit", 1, 50, 10)
        with col2:
            offset = st.slider("Offset", 0, 100, 0)
        with col3:
            classification = st.selectbox(
                "Classification Filter",
                ["All", "public", "internal", "confidential", "restricted"]
            )
        
        if st.button("🔍 Retrieve Secure Cohorts", type="primary"):
            try:
                params = {"limit": limit, "offset": offset}
                if classification != "All":
                    params["classification"] = classification
                
                response = requests.get(
                    "http://localhost:8000/secure/research-data/cohorts",
                    params=params,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Retrieved {data['total_count']} cohorts")
                    
                    # Display access information
                    access_info = data.get('access_info', {})
                    st.info(f"""
                    **Access Level**: {access_info.get('user_role', 'Unknown')}  
                    **Classification Filter**: {access_info.get('classification_filter', 'All')}  
                    **Data Redaction**: {'Applied' if access_info.get('data_redaction_applied') else 'Not Applied'}
                    """)
                    
                    # Display cohorts
                    if data['cohorts']:
                        df = pd.DataFrame(data['cohorts'])
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No cohorts found matching your access level and filters.")
                        
                else:
                    st.error(f"Request failed: {response.text}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with tab2:
        st.markdown("**Secure Biomedical Database Search**")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            search_query = st.text_input(
                "Research Query",
                placeholder="e.g., diabetes treatment, cancer immunotherapy"
            )
        with col2:
            max_results = st.slider("Max Results", 5, 50, 20)
        
        classification_level = st.selectbox(
            "Required Classification Level",
            ["public", "internal", "confidential", "restricted"]
        )
        
        if st.button("🔍 Secure Search", type="primary") and search_query:
            try:
                params = {
                    "query": search_query,
                    "max_results": max_results,
                    "classification_level": classification_level
                }
                
                response = requests.get(
                    "http://localhost:8000/secure/biomedical/search",
                    params=params,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Secure search completed!")
                    
                    # Display security metadata
                    security_meta = data.get('results', {}).get('security_metadata', {})
                    st.info(f"""
                    **Search Audit ID**: {security_meta.get('search_audit_id', 'N/A')}  
                    **User Access Level**: {security_meta.get('user_access_level', 'N/A')}  
                    **PII Redaction**: {'Applied' if security_meta.get('pii_redaction_applied') else 'Not Applied'}
                    """)
                    
                    # Display results summary
                    results = data.get('results', {}).get('results', {})
                    if results:
                        result_counts = {
                            db: data.get('total_count', 0) 
                            for db, data in results.items()
                        }
                        
                        fig = px.bar(
                            x=list(result_counts.keys()),
                            y=list(result_counts.values()),
                            title="Secure Search Results by Database",
                            labels={'x': 'Database', 'y': 'Results Found'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                else:
                    st.error(f"Search failed: {response.text}")
                    
            except Exception as e:
                st.error(f"Search error: {str(e)}")
    
    with tab3:
        st.markdown("**Secure Data Export with PII Controls**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            cohort_id = st.text_input("Cohort ID", placeholder="cohort_12345")
        with col2:
            export_format = st.selectbox("Format", ["json", "csv", "xlsx"])
        with col3:
            include_pii = st.checkbox("Include PII", help="Requires Admin/Researcher role")
        
        if st.button("📤 Export Data", type="primary") and cohort_id:
            try:
                params = {
                    "format": export_format,
                    "include_pii": include_pii
                }
                
                response = requests.get(
                    f"http://localhost:8000/secure/research-data/export/{cohort_id}",
                    params=params,
                    headers=headers
                )
                
                if response.status_code == 200:
                    st.success("✅ Data exported successfully!")
                    
                    # Display export metadata
                    export_data = response.json()
                    export_meta = export_data.get('export_metadata', {})
                    
                    st.info(f"""
                    **Exported By**: {export_meta.get('exported_by', 'N/A')}  
                    **Export Time**: {export_meta.get('exported_at', 'N/A')}  
                    **Data Classification**: {export_meta.get('data_classification', 'N/A')}  
                    **PII Included**: {'Yes' if export_meta.get('pii_included') else 'No'}
                    """)
                    
                    # Show download button
                    st.download_button(
                        label="📥 Download Export",
                        data=json.dumps(export_data, indent=2),
                        file_name=f"cohort_{cohort_id}_export.{export_format}",
                        mime="application/json"
                    )
                    
                else:
                    st.error(f"Export failed: {response.text}")
                    
            except Exception as e:
                st.error(f"Export error: {str(e)}")
    
    with tab4:
        st.markdown("**System Audit Logs**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            audit_limit = st.slider("Number of Logs", 10, 100, 50)
        with col2:
            action_filter = st.text_input("Action Filter", placeholder="e.g., export_cohort")
        with col3:
            user_filter = st.text_input("User ID Filter", placeholder="Optional")
        
        if st.button("📋 Retrieve Audit Logs", type="primary"):
            try:
                params = {"limit": audit_limit}
                if action_filter:
                    params["action"] = action_filter
                if user_filter:
                    params["user_id"] = user_filter
                
                response = requests.get(
                    "http://localhost:8000/secure/audit/logs",
                    params=params,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Retrieved {data['total_count']} audit log entries")
                    
                    # Display audit logs
                    if data['audit_logs']:
                        df = pd.DataFrame(data['audit_logs'])
                        st.dataframe(df, use_container_width=True)
                        
                        # Create activity timeline
                        if len(df) > 1:
                            df['timestamp'] = pd.to_datetime(df['timestamp'])
                            activity_counts = df.groupby(df['timestamp'].dt.hour)['action'].count()
                            
                            fig = px.line(
                                x=activity_counts.index,
                                y=activity_counts.values,
                                title="API Activity Timeline (by Hour)",
                                labels={'x': 'Hour of Day', 'y': 'Number of Actions'}
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No audit logs found matching your criteria.")
                        
                else:
                    st.error(f"Failed to retrieve audit logs: {response.text}")
                    
            except Exception as e:
                st.error(f"Audit log error: {str(e)}")

def security_status_interface():
    """Display system security status (Admin only)"""
    if st.session_state.access_token is None:
        st.warning("🔐 Please log in to view security status.")
        return
    
    if st.session_state.user_info.get("role") != "admin":
        st.warning("⚠️ Security status requires Admin role.")
        return
    
    st.subheader("🛡️ System Security Status")
    
    if st.button("🔄 Check Security Status", type="primary"):
        try:
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            response = requests.get(
                "http://localhost:8000/secure/system/security-status",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Security status retrieved successfully!")
                
                # Display security metrics
                metrics = data.get('security_metrics', {})
                
                # Authentication metrics
                auth_metrics = metrics.get('authentication', {})
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Active API Keys", auth_metrics.get('active_api_keys', 0))
                with col2:
                    st.metric("Revoked Tokens", auth_metrics.get('revoked_tokens', 0))
                with col3:
                    st.metric("JWT Enabled", "✅" if auth_metrics.get('jwt_enabled') else "❌")
                with col4:
                    st.metric("API Key Auth", "✅" if auth_metrics.get('api_key_auth_enabled') else "❌")
                
                # Compliance status
                compliance = metrics.get('compliance', {})
                st.subheader("📋 Compliance Status")
                
                compliance_items = [
                    ("HIPAA Controls", compliance.get('hipaa_controls')),
                    ("GDPR Controls", compliance.get('gdpr_controls')),
                    ("Audit Trail", compliance.get('audit_trail')),
                    ("Data Classification", compliance.get('data_classification')),
                    ("Encryption in Transit", compliance.get('encryption_in_transit')),
                ]
                
                for item_name, status in compliance_items:
                    if status:
                        st.success(f"✅ {item_name}: Enabled")
                    else:
                        st.error(f"❌ {item_name}: Disabled")
                
                # Recommendations
                recommendations = data.get('recommendations', [])
                if recommendations:
                    st.subheader("💡 Security Recommendations")
                    for rec in recommendations:
                        st.info(f"• {rec}")
                
            else:
                st.error(f"Failed to retrieve security status: {response.text}")
                
        except Exception as e:
            st.error(f"Security status error: {str(e)}")

def api_documentation_interface():
    """Display API documentation and examples"""
    st.subheader("📚 API Documentation & Examples")
    
    st.markdown("""
    ### Available Secure Endpoints
    
    #### Authentication
    - `POST /auth/login` - User authentication with JWT tokens
    - `POST /auth/api-key` - Generate API keys for programmatic access
    - `DELETE /auth/api-key/{key}` - Revoke API keys
    
    #### Secure Data Access
    - `GET /secure/research-data/cohorts` - List patient cohorts (role-based access)
    - `GET /secure/research-data/export/{id}` - Export cohort data (with PII controls)
    - `GET /secure/biomedical/search` - Secure biomedical database search
    
    #### Security & Compliance
    - `GET /secure/audit/logs` - System audit logs
    - `GET /secure/system/security-status` - Security status (Admin only)
    """)
    
    st.subheader("🔗 Example API Calls")
    
    # Example 1: Authentication
    with st.expander("🔑 Authentication Example"):
        st.code("""
# Login and get access token
curl -X POST "http://localhost:8000/auth/login" \\
     -H "Content-Type: application/x-www-form-urlencoded" \\
     -d "username=admin@syntheticascension.com&password=SecurePass123!"

# Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user_info": {
    "user_id": "admin_001",
    "username": "admin@syntheticascension.com",
    "role": "admin",
    "name": "System Administrator"
  }
}
        """, language="bash")
    
    # Example 2: Secure data access
    with st.expander("🛡️ Secure Data Access Example"):
        st.code("""
# Access patient cohorts with JWT authentication
curl -X GET "http://localhost:8000/secure/research-data/cohorts?limit=10" \\
     -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Or using API key
curl -X GET "http://localhost:8000/secure/research-data/cohorts?limit=10" \\
     -H "X-API-Key: sa_your_api_key_here"

# Response includes access control information:
{
  "cohorts": [...],
  "total_count": 5,
  "access_info": {
    "user_role": "admin",
    "classification_filter": "all",
    "data_redaction_applied": true
  }
}
        """, language="bash")
    
    # Example 3: Rate limiting
    with st.expander("⚡ Rate Limiting & Security Headers"):
        st.code("""
# All secure endpoints include rate limiting
# Default limits by endpoint:
# - Cohort access: 50 requests/hour
# - Biomedical search: 30 requests/hour  
# - Data export: 10 requests/hour

# Security headers in responses:
X-Data-Classification: confidential
X-Export-Timestamp: 2024-01-15T10:30:00Z
Cache-Control: no-cache, no-store, must-revalidate
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
        """, language="text")

def main():
    """Main secure API client interface"""
    display_header()
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔐 Authentication",
        "🛡️ Secure Data Access",
        "🔍 Security Status",
        "📚 API Documentation"
    ])
    
    with tab1:
        login_interface()
    
    with tab2:
        secure_data_access_interface()
    
    with tab3:
        security_status_interface()
    
    with tab4:
        api_documentation_interface()
    
    # Footer with security information
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: #F5F5F5; border-radius: 10px;">
        <h4 style="color: #0A1F44; margin-bottom: 0.5rem;">🛡️ Enterprise Security Features</h4>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div>✅ JWT Authentication</div>
            <div>✅ Role-Based Access Control</div>
            <div>✅ Rate Limiting</div>
            <div>✅ PII Redaction</div>
            <div>✅ Audit Logging</div>
            <div>✅ Data Classification</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()