# Synthetic Ascension EHR Platform

An advanced AI-powered Electronic Health Record (EHR) synthesis platform that generates comprehensive synthetic medical data with cutting-edge visualization and privacy-preserving technologies.

## 🏗️ Architecture Overview

### Comprehensive Agentic System
- **50+ Specialized Agents** across 6 categories with Doer/Coordinator/Adversarial roles
- **6-Phase Pipeline** with real-time monitoring and comprehensive audit trails
- **Enterprise-Grade Safeguards** including differential privacy and clinical realism certification
- **Full Langflow Integration** for visual workflow modification and export

### Frontend & Backend Services
- **React Frontend** (Port 5000) - Professional TypeScript interface with Tailwind CSS
- **Enhanced Backend Server V3** (Port 8004) - **PRIMARY** - Complete agentic architecture
- **Integrated Backend Server** (Port 8003) - Legacy system for backward compatibility
- **React + Vite + TypeScript** - Modern development stack

## 🤖 Agent Architecture (50+ Agents)

### Cohort Constructor (11 Agents)
- **Phenotype Assembler** - Core phenotype definition and assembly
- **Demographics Generator** - Age, gender, ethnicity, socioeconomic factors
- **Comorbidity Orchestrator** - Multi-condition management and interactions
- **Temporal Dynamics Agent** - Disease progression and timeline modeling
- **Clinical Realism Certifier** - SME validation and clinical review
- **Population Stratifier** - Risk-based cohort segmentation
- **Genetic Variant Injector** - Hereditary factors and genomic data
- **Social Determinants Weaver** - Environmental and social health factors
- **Care Access Modeler** - Healthcare accessibility patterns
- **Health Equity Auditor** - Bias detection and fairness assessment
- **Cohort Diversity Optimizer** - Representative population modeling

### Clinical Journey Generator (11 Agents)
- **Procedure/Encounter Generator** - Medical procedures and healthcare encounters
- **Medication Journey Designer** - Prescription patterns and medication adherence
- **Diagnostic Pathway Creator** - Diagnostic workup and testing sequences
- **Care Transition Orchestrator** - Hospital admissions, transfers, discharges
- **Treatment Response Modeler** - Therapy outcomes and patient responses
- **Adverse Event Injector** - Medical complications and side effects
- **Clinical Decision Simulator** - Provider decision-making patterns
- **Provider Interaction Weaver** - Multi-disciplinary care coordination
- **Care Coordination Mapper** - Healthcare team communication patterns
- **Outcome Trajectory Designer** - Long-term health outcomes and prognosis
- **Journey Realism Certifier** - Clinical pathway validation

### Data Robustness & Noise (10 Agents)
- **Missingness Injection Agent** - Realistic data gaps and missing values
- **Measurement Error Introducer** - Lab and vital sign variability
- **Lab Variance Generator** - Reference range variations and lab drift
- **Imaging Artifact Injector** - Diagnostic imaging quality variations
- **Temporal Noise Weaver** - Time-based data inconsistencies
- **Data Entry Error Simulator** - Human error patterns in documentation
- **Systematic Bias Introducer** - Healthcare system biases and patterns
- **Equipment Drift Modeler** - Medical device calibration variations
- **Seasonal Variation Injector** - Time-of-year health pattern variations
- **Privacy Guard Agent** - Differential privacy and k-anonymity protection

### QA & Validation (13 Agents)
- **Summary Reporting Agent** - Comprehensive cohort summaries and statistics
- **Statistical Validation Engine** - Data quality and statistical coherence
- **Temporal Consistency Checker** - Timeline validation and chronological order
- **Clinical Logic Validator** - Medical knowledge and guideline compliance
- **FHIR Export Generator** - Healthcare interoperability standard compliance
- **Regulatory Compliance Auditor** - HIPAA, FDA, and healthcare regulation compliance
- **Bias Detection Scanner** - Algorithmic bias identification and mitigation
- **Privacy Risk Assessor** - Re-identification risk analysis
- **Data Quality Monitor** - Completeness, accuracy, and consistency metrics
- **Clinical Guidelines Validator** - Evidence-based medicine compliance
- **Longitudinal Coherence Checker** - Patient journey consistency validation
- **Cross-Referential Validator** - Inter-record relationship validation
- **Outlier Detection Agent** - Statistical anomaly identification

### Explanation & Provenance (13 Agents)
- **Cohort Summary Reporter** - Executive summaries and key insights
- **Clinical Narrative Generator** - Human-readable clinical stories
- **Statistical Insights Extractor** - Pattern recognition and trend analysis
- **Quality Metrics Calculator** - Data quality scoring and assessment
- **Provenance Tracker** - Data lineage and generation audit trails
- **Decision Tree Explainer** - Agent decision logic transparency
- **Feature Importance Analyzer** - Variable significance assessment
- **Correlation Discovery Agent** - Statistical relationship identification
- **Pattern Recognition Reporter** - Clinical pattern documentation
- **Ontology Mapper** - Medical terminology and coding standardization
- **Literature Evidence Linker** - Research citation and evidence base
- **RAG Retrieval Agent** - Knowledge base integration and fact-checking
- **Hallucination Detector** - AI-generated content validation

### Supervision & Orchestration (9 Agents)
- **Priority Routing Coordinator** - Agent execution sequencing and prioritization
- **Resource Allocation Manager** - Computational resource optimization
- **Workflow Orchestrator** - Multi-agent pipeline coordination
- **Exception Handling Supervisor** - Error management and recovery
- **Performance Monitor** - Agent performance tracking and optimization
- **Log Aggregation Service** - Centralized logging and audit trail management
- **Audit Trail Manager** - Compliance and regulatory audit support
- **Replay Management System** - Deterministic execution replay capability
- **Chaos Testing Adversary** - System resilience and stress testing

## 🔧 Enhanced Backend Server V3 (Port 8004) - PRIMARY

### Core API Endpoints
```http
GET  /                          # Enhanced system overview with comprehensive agent architecture
POST /api/v3/generate           # Generate synthetic EHR data using 50+ agents in 6-phase pipeline
GET  /api/v3/jobs/{job_id}      # Check enhanced job status with phase-by-phase progress tracking
GET  /api/v3/jobs/{job_id}/results # Get detailed results with privacy assessments and clinical reviews
GET  /api/v3/analytics          # Enhanced platform analytics with agent performance by role
GET  /api/v3/architecture       # Complete agent architecture overview with all categories
```

### Langflow Integration
```http
GET  /api/v3/langflow/export    # Export all workflows as Langflow-compatible JSON files
GET  /api/v3/langflow/download  # Download complete Langflow export as ZIP file
GET  /api/v3/langflow/templates # Get available Langflow workflow templates
POST /api/v3/langflow/execute   # Execute Langflow workflows with backend integration
```

### Six-Phase Pipeline Execution
1. **Phase 1: Literature Mining & Research** - Evidence-based foundation
2. **Phase 2: Cohort Construction** - Demographics and population modeling
3. **Phase 3: Clinical Journey Generation** - Healthcare pathways and encounters
4. **Phase 4: Data Robustness Enhancement** - Noise injection and privacy protection
5. **Phase 5: QA & Validation** - Quality assurance and compliance verification
6. **Phase 6: Reporting & Export** - Documentation and data export

## 🌊 Langflow Integration & Export

### Plug-and-Play Workflow Export
Your complete agent architecture can be exported as Langflow-compatible workflows for visual modification and local execution.

#### Quick Start with Langflow
```bash
# 1. Export workflows from Synthetic Ascension
curl http://localhost:8004/api/v3/langflow/download -o workflows.zip

# 2. Install Langflow locally  
pip install langflow

# 3. Start Langflow
langflow run

# 4. Import workflows and modify visually
# 5. Execute modified workflows locally or via backend
```

#### Available Templates
- **Complete Pipeline** - All 50+ agents in 6-phase workflow
- **Cohort Constructor Only** - Demographics and comorbidity generation
- **Clinical Journey Focus** - Procedure and medication workflows
- **QA & Validation Suite** - Quality assurance and compliance workflows

#### Workflow Modification Capabilities
- **Drag-and-Drop Agent Arrangement** - Visual workflow editing
- **Parameter Customization** - Agent configuration through UI
- **Conditional Logic** - Add branching and decision points
- **Custom Components** - Integrate your own agents
- **Backend Integration** - Execute on Synthetic Ascension servers

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL database

### Installation & Setup
```bash
# Clone and setup
git clone <repository>
cd synthetic-ascension

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies  
npm install

# Start all services
npm run dev          # React frontend (Port 5000)
python integrated_server_v3_enhanced.py  # Enhanced backend (Port 8004)
```

### Basic Usage
```bash
# Generate synthetic EHR data
curl -X POST http://localhost:8004/api/v3/generate \
  -H "Content-Type: application/json" \
  -d '{
    "use_case": "comprehensive_ehr_v2",
    "population_size": 100,
    "condition": "diabetes",
    "enable_adversarial_testing": true,
    "require_clinical_review": true,
    "privacy_level": "high"
  }'

# Check job status
curl http://localhost:8004/api/v3/jobs/{job_id}

# Export Langflow workflows
curl http://localhost:8004/api/v3/langflow/export
```

## 🔒 Enterprise-Grade Features

### Privacy & Security
- **Differential Privacy** - Mathematical privacy guarantees
- **K-Anonymity Scoring** - Re-identification risk assessment
- **Clinical Review Integration** - Human-in-the-loop validation
- **Version Pinning** - Reproducible and auditable results
- **Audit Trail Management** - Complete execution logging

### Quality Assurance
- **Clinical Realism Certification** - SME validation workflows
- **Bias Detection & Mitigation** - Algorithmic fairness assessment
- **Regulatory Compliance** - HIPAA, FDA, and healthcare standards
- **Statistical Validation** - Data quality and coherence verification
- **Evidence-Based Generation** - Literature-backed synthetic data

### Performance & Scalability
- **Concurrency Management** - Deadlock prevention and resource optimization
- **Performance Monitoring** - Real-time agent performance tracking
- **Chaos Testing** - Adversarial robustness validation
- **Resource Allocation** - Intelligent computational resource management
- **Replay Capability** - Deterministic execution for debugging

## 📊 Agent Role Classification

### Doer Agents (Primary Execution)
Generate and transform data through specialized domain expertise

### Coordinator Agents (Orchestration)  
Manage sequences, validate outputs, and ensure workflow coherence

### Adversarial Agents (Stress Testing)
Challenge assumptions, inject failures, and validate robustness

## 🏥 Clinical Specialization

### Supported Medical Domains
- **Cardiology** - Heart disease, procedures, medications
- **Endocrinology** - Diabetes, hormonal disorders, metabolic conditions
- **Oncology** - Cancer staging, treatments, outcomes
- **Pediatrics** - Child-specific growth patterns and care pathways
- **Geriatrics** - Age-related conditions and care considerations
- **Emergency Medicine** - Acute care scenarios and triage patterns

### Healthcare Standards Compliance
- **FHIR R4** - Healthcare interoperability standard
- **ICD-10** - Medical diagnosis coding
- **CPT** - Medical procedure coding  
- **SNOMED CT** - Clinical terminology
- **LOINC** - Laboratory data standards

## 🔬 Research & Development Features

### Literature Integration
- **PubMed Integration** - Latest medical research incorporation
- **Evidence-Based Patterns** - Research-backed clinical pathways
- **Ontology Mapping** - Medical knowledge graph integration
- **Citation Tracking** - Research provenance and evidence links

### Advanced Analytics
- **Pattern Recognition** - Clinical trend identification
- **Correlation Analysis** - Multi-variate relationship discovery
- **Longitudinal Modeling** - Disease progression patterns
- **Population Stratification** - Risk-based cohort analysis

## 🚀 Deployment Configuration

**Important:** This is a **React application**, not a Streamlit app. The `.replit` configuration references Streamlit for legacy reasons, but `app.py` handles proper React deployment.

### Service Architecture
- **Frontend:** Port 5000 (React + Vite + TypeScript) - Primary UI
- **Enhanced Backend V3:** Port 8004 (50+ agent comprehensive system) - **PRIMARY API**
- **Legacy Backend:** Port 8003 (18+ agent integrated system) - Legacy support
- **API Documentation:** Port 8001 (Swagger/OpenAPI docs)

### Deployment Process
1. **Development Mode:** `app.py` starts Vite dev server directly
2. **Production Mode:** `app.py` builds React app and serves static files
3. **Backend Services:** Automatically started in parallel with frontend
4. **Health Monitoring:** All services include health checks and graceful shutdown

### Deployment Commands
```bash
# Development (local)
npm run dev

# Production deployment
python app.py

# Manual build
npm run build && npx serve -s dist -l 5000
```

### External Deployment
- **📖 [DEPLOYMENT.md](./DEPLOYMENT.md)** - Comprehensive deployment guide for all platforms
- **⚡ [QUICK_DEPLOY.md](./QUICK_DEPLOY.md)** - Fast deployment for common scenarios

**Supported Platforms:**
- Docker & Docker Compose
- Vercel (Frontend) + Railway (Backend)
- DigitalOcean App Platform
- AWS (EC2 + RDS)
- Google Cloud Platform (Cloud Run)
- Traditional VPS with Nginx
- Local development environment

## 📋 API Documentation

### Interactive Documentation
- **Swagger UI** - Available at `/docs` on each server
- **OpenAPI 3.0** - Complete API specification
- **Request/Response Examples** - Comprehensive usage examples
- **Authentication** - Security scheme documentation

### Client SDKs
- **Python SDK** - Native Python integration
- **JavaScript SDK** - Web application integration  
- **REST API** - Standard HTTP/JSON interface
- **GraphQL** - Flexible query interface (coming soon)

## 🧪 Development & Testing

### Testing Framework
- **Unit Tests** - Individual agent validation
- **Integration Tests** - Multi-agent workflow testing
- **Performance Tests** - Scalability and load testing
- **Clinical Validation** - Medical accuracy verification

### Development Tools
- **Hot Reload** - Real-time development feedback
- **Debug Mode** - Detailed execution tracing
- **Performance Profiling** - Bottleneck identification
- **Error Tracking** - Comprehensive error logging

## 📈 Monitoring & Analytics

### Real-Time Dashboards
- **Agent Performance** - Execution time and success rates
- **System Health** - Resource utilization and availability
- **Data Quality** - Completeness and accuracy metrics
- **Clinical Metrics** - Medical realism and compliance scores

### Audit & Compliance
- **Execution Logs** - Complete audit trail
- **Privacy Assessments** - Re-identification risk reports
- **Clinical Reviews** - SME validation status
- **Regulatory Reports** - Compliance documentation

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Submit pull request with documentation

### Agent Development
- **Base Agent Framework** - Inherit from EnhancedBaseAgent
- **Role Classification** - Define as Doer/Coordinator/Adversarial
- **Privacy Guards** - Implement differential privacy safeguards
- **Clinical Validation** - Include medical accuracy checks

## 📞 Support & Documentation

### Resources
- **API Documentation** - `/docs` endpoint on each server
- **Agent Architecture** - `/api/v3/architecture` endpoint
- **Langflow Integration** - `/api/v3/langflow/templates` endpoint
- **Performance Metrics** - `/api/v3/analytics` endpoint

### Community
- **Issues** - GitHub issue tracker
- **Discussions** - Community forum
- **Documentation** - Comprehensive guides and tutorials
- **Examples** - Sample implementations and use cases

---

**Synthetic Ascension EHR Platform** - Advanced AI-powered synthetic medical data generation with enterprise-grade privacy, quality, and compliance features.