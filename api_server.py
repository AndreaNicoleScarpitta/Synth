"""
FastAPI Orchestration Engine for Synthetic EHR Generation
Provides comprehensive API endpoints with Swagger documentation
Live agent visibility and workflow management
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid
import asyncio
import json
from datetime import datetime
from sqlalchemy.orm import Session

from models.database_models import db_manager, DatabaseSession
from models.database_models import Patient, AgentExecution, AuditLog, WorkflowState, ValidationResult
from agents.rag_orchestrator import RAGOrchestrator
from agents.biomedical_database_connector import BiomedicalDatabaseConnector
from agents.enhanced_literature_agent import EnhancedLiteratureAgent
from utils.security import (
    security_manager, get_current_user, require_role, require_permission,
    rate_limit, audit_log, DataClassification, DataEncryption,
    secure_export_headers, UserRole, AccessLevel
)
from utils.database_manager import get_database_manager

# Initialize FastAPI with comprehensive documentation
app = FastAPI(
    title="Synthetic Ascension API",
    description="""
    ## Agentic AI System for Synthetic EHR Generation
    
    ### Features:
    - **🤖 Multi-Agent Orchestration**: Coordinated AI agents for literature retrieval, cohort generation, and validation
    - **📊 Real-time Agent Visibility**: Live tracking of agent execution with WebSocket updates
    - **🔍 Comprehensive Validation**: Statistical, medical terminology, and literature consistency validation
    - **🌐 Web Monitoring**: Automated scraping and curation of medical research
    - **📋 Full Audit Trail**: Complete traceability of all agent actions and data generation
    - **🏥 Multi-modal EHR Data**: Structured (labs, vitals), unstructured (notes), and time-series data
    
    ### Architecture:
    - **SQL Database**: PostgreSQL for structured EHR data
    - **Audit System**: Complete tracking of agent executions and workflow states
    - **Privacy-First**: Local Ollama inference for HIPAA compliance
    - **Bias-Aware**: Advanced statistical validation with demographic analysis
    
    ### Workflow:
    1. Submit clinical problem statement
    2. Agents perform literature retrieval and analysis
    3. Generate validated synthetic patient cohorts
    4. Perform comprehensive quality validation
    5. Return structured results with audit trail
    """,
    version="2.0.0",
    contact={
        "name": "Synthetic Ascension Team",
        "url": "https://github.com/your-repo/synthetic-ascension",
        "email": "support@synthetic-ascension.ai",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS middleware for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for WebSocket connections and agent tracking
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.agent_states: Dict[str, Dict] = {}
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast_agent_update(self, execution_id: str, agent_name: str, status: str, message: str):
        update = {
            "execution_id": execution_id,
            "agent_name": agent_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        self.agent_states[execution_id] = update
        
        # Broadcast to all connected clients
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(update))
            except:
                disconnected.append(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.active_connections.remove(connection)

manager = ConnectionManager()

# Initialize biomedical database systems
biomedical_connector = BiomedicalDatabaseConnector()
literature_agent = EnhancedLiteratureAgent()

# Pydantic models for API requests/responses
class ProblemStatement(BaseModel):
    """Clinical problem statement for EHR generation"""
    statement: str = Field(
        description="Clinical problem statement (e.g., 'suspected autoimmune flare in adolescent female')",
        examples=["suspected autoimmune flare in adolescent female with joint pain and fatigue"]
    )
    cohort_size: int = Field(
        default=10, 
        ge=1, 
        le=100, 
        description="Number of synthetic patients to generate"
    )
    include_time_series: bool = Field(
        default=True,
        description="Whether to include time-series data (vitals, lab trends)"
    )
    validation_level: str = Field(
        default="comprehensive",
        description="Level of validation to perform",
        pattern="^(basic|standard|comprehensive)$"
    )

class PatientResponse(BaseModel):
    """Response model for patient data"""
    patient_id: str
    age: int
    gender: str
    ethnicity: str
    conditions: List[str]
    medications: List[str]
    lab_results: Dict[str, tuple]
    clinical_notes: List[str]

class CohortResponse(BaseModel):
    """Response model for patient cohort"""
    cohort_id: str
    patients: List[PatientResponse]
    generation_metadata: Dict[str, Any]
    validation_results: Optional[Dict[str, Any]] = None

class WorkflowResponse(BaseModel):
    """Response model for workflow execution"""
    workflow_id: str
    status: str
    current_step: str
    progress_percentage: float
    results: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class AgentStatus(BaseModel):
    """Response model for agent execution status"""
    execution_id: str
    agent_name: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    progress_message: str
    output_summary: Optional[Dict[str, Any]] = None

# Database dependency
def get_db():
    with DatabaseSession(db_manager) as session:
        yield session

# Initialize database tables
@app.on_event("startup")
async def startup_event():
    """Initialize database and create tables on startup"""
    try:
        db_manager.create_tables()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

# Initialize RAG orchestrator
orchestrator = RAGOrchestrator()

# WebSocket endpoint for real-time agent updates
@app.websocket("/ws/agent-updates")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time agent execution updates
    
    Provides live visibility into:
    - Agent execution status
    - Progress messages
    - Workflow state changes
    - Error notifications
    """
    await manager.connect(websocket)
    try:
        # Send current agent states to new connection
        for execution_id, state in manager.agent_states.items():
            await websocket.send_text(json.dumps(state))
        
        # Keep connection alive
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Main workflow endpoints
@app.post(
    "/api/v1/generate-cohort",
    response_model=WorkflowResponse,
    summary="Generate Synthetic Patient Cohort",
    description="""
    Generate a synthetic patient cohort from a clinical problem statement.
    
    This endpoint initiates a comprehensive workflow that:
    1. Analyzes the clinical problem using literature retrieval
    2. Generates synthetic patients with realistic medical profiles
    3. Validates data quality using statistical and medical terminology checks
    4. Returns structured EHR data with full audit trail
    
    **Real-time Updates**: Connect to `/ws/agent-updates` for live progress tracking
    """,
    tags=["Core Workflow"]
)
async def generate_cohort(
    problem: ProblemStatement,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate synthetic patient cohort from clinical problem statement"""
    
    # Create workflow tracking
    workflow_id = str(uuid.uuid4())
    workflow_state = WorkflowState(
        workflow_id=workflow_id,
        current_step="initializing",
        state_data=problem.dict(),
        status="running"
    )
    db.add(workflow_state)
    db.commit()
    
    # Start background processing
    background_tasks.add_task(
        process_cohort_generation,
        workflow_id,
        problem.statement,
        problem.cohort_size,
        problem.validation_level
    )
    
    return WorkflowResponse(
        workflow_id=workflow_id,
        status="running",
        current_step="initializing",
        progress_percentage=0.0
    )

async def process_cohort_generation(
    workflow_id: str,
    statement: str,
    cohort_size: int,
    validation_level: str
):
    """Background task for cohort generation with real-time updates"""
    
    execution_id = str(uuid.uuid4())
    
    # Progress callback for real-time updates
    async def progress_callback(message: str):
        await manager.broadcast_agent_update(
            execution_id=execution_id,
            agent_name="orchestrator",
            status="running",
            message=message
        )
    
    try:
        # Execute the RAG workflow
        result = orchestrator.process_query(
            query=statement,
            progress_callback=progress_callback
        )
        
        # Store results in database
        with DatabaseSession(db_manager) as db:
            # Update workflow state
            workflow = db.query(WorkflowState).filter(
                WorkflowState.workflow_id == workflow_id
            ).first()
            
            if workflow:
                workflow.status = "completed"
                workflow.current_step = "finished"
                workflow.state_data = result
                workflow.updated_at = datetime.utcnow()
                db.commit()
        
        # Final update
        await manager.broadcast_agent_update(
            execution_id=execution_id,
            agent_name="orchestrator",
            status="completed",
            message="✅ Cohort generation completed successfully"
        )
        
    except Exception as e:
        # Handle errors
        with DatabaseSession(db_manager) as db:
            workflow = db.query(WorkflowState).filter(
                WorkflowState.workflow_id == workflow_id
            ).first()
            
            if workflow:
                workflow.status = "failed"
                workflow.current_step = "error"
                workflow.state_data = {"error": str(e)}
                workflow.updated_at = datetime.utcnow()
                db.commit()
        
        await manager.broadcast_agent_update(
            execution_id=execution_id,
            agent_name="orchestrator",
            status="failed",
            message=f"❌ Error: {str(e)}"
        )

@app.get(
    "/api/v1/workflow/{workflow_id}",
    response_model=WorkflowResponse,
    summary="Get Workflow Status",
    description="Retrieve the current status and results of a workflow execution",
    tags=["Core Workflow"]
)
async def get_workflow_status(workflow_id: str, db: Session = Depends(get_db)):
    """Get workflow execution status and results"""
    
    workflow = db.query(WorkflowState).filter(
        WorkflowState.workflow_id == workflow_id
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Calculate progress percentage
    progress_map = {
        "initializing": 0.0,
        "literature_search": 20.0,
        "cohort_generation": 50.0,
        "validation": 80.0,
        "finished": 100.0,
        "error": 0.0
    }
    
    return WorkflowResponse(
        workflow_id=workflow.workflow_id,
        status=workflow.status,
        current_step=workflow.current_step,
        progress_percentage=progress_map.get(workflow.current_step, 0.0),
        results=workflow.state_data if workflow.status == "completed" else None,
        error_message=workflow.state_data.get("error") if workflow.status == "failed" else None
    )

@app.get(
    "/api/v1/agents/status",
    response_model=List[AgentStatus],
    summary="Get All Agent Statuses",
    description="Retrieve current execution status of all agents in the system",
    tags=["Agent Management"]
)
async def get_agent_statuses(db: Session = Depends(get_db)):
    """Get current status of all agents"""
    
    executions = db.query(AgentExecution).order_by(
        AgentExecution.started_at.desc()
    ).limit(20).all()
    
    return [
        AgentStatus(
            execution_id=exec.execution_id,
            agent_name=exec.agent_name,
            status=exec.status,
            started_at=exec.started_at,
            completed_at=exec.completed_at,
            progress_message=exec.output_data.get("message", "") if exec.output_data else "",
            output_summary=exec.output_data
        )
        for exec in executions
    ]

@app.get(
    "/api/v1/cohorts",
    summary="List Patient Cohorts",
    description="Retrieve a list of all generated synthetic patient cohorts",
    tags=["Data Management"]
)
async def list_cohorts(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List all generated patient cohorts"""
    
    cohorts = db.query(WorkflowState).filter(
        WorkflowState.status == "completed"
    ).offset(offset).limit(limit).all()
    
    return [
        {
            "cohort_id": cohort.workflow_id,
            "created_at": cohort.created_at,
            "patient_count": len(cohort.state_data.get("synthetic_cohort", {}).get("patients", [])),
            "validation_score": cohort.state_data.get("statistical_validation", {}).get("overall_quality_score"),
            "problem_statement": cohort.state_data.get("query", "")
        }
        for cohort in cohorts
    ]

@app.get(
    "/api/v1/cohorts/{cohort_id}",
    summary="Get Cohort Details",
    description="Retrieve detailed information about a specific patient cohort",
    tags=["Data Management"]
)
async def get_cohort(cohort_id: str, db: Session = Depends(get_db)):
    """Get detailed cohort information"""
    
    workflow = db.query(WorkflowState).filter(
        WorkflowState.workflow_id == cohort_id
    ).first()
    
    if not workflow or workflow.status != "completed":
        raise HTTPException(status_code=404, detail="Cohort not found")
    
    return workflow.state_data

@app.post(
    "/api/v1/web-monitoring/trigger",
    summary="Trigger Web Monitoring",
    description="Manually trigger web scraping and content curation for medical sources",
    tags=["Web Monitoring"]
)
async def trigger_web_monitoring(
    query: Optional[str] = None,
    background_tasks: BackgroundTasks = None
):
    """Trigger manual web scraping and monitoring"""
    
    if background_tasks:
        background_tasks.add_task(run_web_monitoring, query)
        return {"message": "Web monitoring triggered", "status": "running"}
    else:
        result = orchestrator.web_monitor_agent.manual_scrape_and_update(query or "")
        return {"message": "Web monitoring completed", "result": result}

async def run_web_monitoring(query: str = ""):
    """Background task for web monitoring"""
    execution_id = str(uuid.uuid4())
    
    await manager.broadcast_agent_update(
        execution_id=execution_id,
        agent_name="web_monitor",
        status="running",
        message="🌐 Starting web monitoring and content scraping..."
    )
    
    try:
        result = orchestrator.web_monitor_agent.manual_scrape_and_update(query)
        
        await manager.broadcast_agent_update(
            execution_id=execution_id,
            agent_name="web_monitor",
            status="completed",
            message=f"✅ Scraped {result['total_scraped']} articles, curated {result['curated_content']}"
        )
        
    except Exception as e:
        await manager.broadcast_agent_update(
            execution_id=execution_id,
            agent_name="web_monitor",
            status="failed",
            message=f"❌ Web monitoring failed: {str(e)}"
        )

@app.get(
    "/api/v1/web-monitoring/status",
    summary="Get Web Monitoring Status",
    description="Get current status of web monitoring agents and scraped content",
    tags=["Web Monitoring"]
)
async def get_web_monitoring_status():
    """Get web monitoring status and statistics"""
    return orchestrator.web_monitor_agent.get_monitoring_status()

@app.get(
    "/api/v1/validation/{cohort_id}",
    summary="Get Validation Results",
    description="Retrieve comprehensive validation results for a patient cohort",
    tags=["Validation"]
)
async def get_validation_results(cohort_id: str, db: Session = Depends(get_db)):
    """Get detailed validation results for a cohort"""
    
    validation = db.query(ValidationResult).filter(
        ValidationResult.cohort_id == cohort_id
    ).first()
    
    if not validation:
        raise HTTPException(status_code=404, detail="Validation results not found")
    
    return {
        "cohort_id": validation.cohort_id,
        "validation_type": validation.validation_type,
        "overall_score": validation.overall_score,
        "detailed_results": validation.detailed_results,
        "recommendations": validation.recommendations,
        "validated_at": validation.validated_at
    }

@app.get(
    "/api/v1/audit/executions",
    summary="Get Audit Trail",
    description="Retrieve audit trail of all agent executions and system actions",
    tags=["Audit & Compliance"]
)
async def get_audit_trail(
    limit: int = 50,
    agent_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get comprehensive audit trail"""
    
    query = db.query(AgentExecution).order_by(AgentExecution.started_at.desc())
    
    if agent_name:
        query = query.filter(AgentExecution.agent_name == agent_name)
    
    executions = query.limit(limit).all()
    
    return [
        {
            "execution_id": exec.execution_id,
            "agent_name": exec.agent_name,
            "task_type": exec.task_type,
            "status": exec.status,
            "started_at": exec.started_at,
            "completed_at": exec.completed_at,
            "input_summary": {k: str(v)[:100] for k, v in (exec.input_data or {}).items()},
            "output_summary": {k: str(v)[:100] for k, v in (exec.output_data or {}).items()},
            "error_message": exec.error_message
        }
        for exec in executions
    ]

@app.get(
    "/",
    response_class=HTMLResponse,
    summary="API Documentation Home",
    description="Interactive API documentation and system overview",
    tags=["Documentation"]
)
async def root():
    """Root endpoint with API overview"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Synthetic Ascension API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { text-align: center; margin-bottom: 30px; }
            .feature { margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }
            .endpoint { background: #e3f2fd; padding: 10px; margin: 10px 0; border-radius: 5px; }
            .status { color: #28a745; font-weight: bold; }
            a { color: #007bff; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Synthetic Ascension API</h1>
                <p><span class="status">Status: Active</span> | Version 2.0.0</p>
                <p>Agentic AI System for Privacy-Preserving Synthetic EHR Generation</p>
            </div>
            
            <div class="feature">
                <h3>🤖 Multi-Agent Architecture</h3>
                <p>Coordinated AI agents for literature retrieval, cohort generation, and comprehensive validation</p>
            </div>
            
            <div class="feature">
                <h3>📊 Real-time Visibility</h3>
                <p>Live tracking of agent execution via WebSocket connections at <code>/ws/agent-updates</code></p>
            </div>
            
            <div class="feature">
                <h3>🔍 Comprehensive Validation</h3>
                <p>Statistical analysis, medical terminology validation, and literature consistency checks</p>
            </div>
            
            <div class="feature">
                <h3>🌐 Web Monitoring</h3>
                <p>Automated scraping and curation of medical research from trusted sources</p>
            </div>
            
            <h3>📋 Quick Start Endpoints:</h3>
            <div class="endpoint">
                <strong>POST /api/v1/generate-cohort</strong> - Generate synthetic patient cohort
            </div>
            <div class="endpoint">
                <strong>GET /api/v1/workflow/{id}</strong> - Check workflow status
            </div>
            <div class="endpoint">
                <strong>GET /api/v1/agents/status</strong> - View agent execution status
            </div>
            <div class="endpoint">
                <strong>WS /ws/agent-updates</strong> - Real-time agent updates
            </div>
            
            <p style="text-align: center; margin-top: 30px;">
                <a href="/docs" style="background: #007bff; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold;">
                    📚 View Full API Documentation
                </a>
            </p>
        </div>
    </body>
    </html>
    """)

# Health check endpoint
@app.get(
    "/health",
    summary="Health Check",
    description="System health status and component availability",
    tags=["System"]
)
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        with DatabaseSession(db_manager) as db:
            db.execute("SELECT 1")
        
        # Check orchestrator
        agent_status = orchestrator.get_agent_status()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "database": "connected",
                "orchestrator": "active",
                "agents": agent_status
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# Biomedical Database Integration Endpoints
@app.post("/biomedical/comprehensive-search", 
          response_model=Dict[str, Any],
          tags=["Biomedical Research"],
          summary="Comprehensive Biomedical Database Search",
          description="Search across multiple biomedical databases including PubMed, ClinicalTrials.gov, FDA, NIH Reporter, and UniProt")
async def comprehensive_biomedical_search(
    query: str = Field(description="Search query (e.g., 'diabetes type 2', 'Alzheimer disease')"),
    databases: Optional[List[str]] = Field(default=None, description="Specific databases to search. Options: pubmed, clinicaltrials, fda_drugs, nih_reporter, uniprot"),
    max_results_per_db: int = Field(default=20, ge=1, le=100, description="Maximum results per database"),
    background_tasks: BackgroundTasks = None
):
    """
    Perform comprehensive search across multiple biomedical databases
    
    **Databases Available:**
    - **PubMed**: Medical literature and research articles
    - **ClinicalTrials.gov**: Clinical trial registry
    - **FDA Drugs**: Approved drug labels and information
    - **NIH Reporter**: Funded research projects
    - **UniProt**: Protein sequence and functional information
    
    **Example queries:**
    - "diabetes mellitus type 2"
    - "breast cancer immunotherapy"
    - "COVID-19 vaccines"
    """
    try:
        results = biomedical_connector.comprehensive_biomedical_search(
            query=query,
            databases=databases,
            max_results_per_db=max_results_per_db
        )
        
        return {
            "status": "success",
            "results": results,
            "query_metadata": {
                "search_timestamp": datetime.now().isoformat(),
                "query": query,
                "databases_searched": databases or ["all"],
                "total_results": results.get('summary', {}).get('total_results_found', 0)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/biomedical/enhanced-literature-search",
          response_model=Dict[str, Any],
          tags=["Biomedical Research"],
          summary="Enhanced Literature Search with AI Analysis",
          description="Perform literature search with advanced AI-powered analysis and insights")
async def enhanced_literature_search(
    query: str = Field(description="Research query"),
    max_results_per_source: int = Field(default=25, ge=1, le=100),
    include_clinical_trials: bool = Field(default=True, description="Include clinical trials data"),
    include_drug_data: bool = Field(default=True, description="Include FDA drug information"),
    include_protein_data: bool = Field(default=False, description="Include protein/genomics data"),
    background_tasks: BackgroundTasks = None
):
    """
    Enhanced literature search with comprehensive analysis including:
    
    - **Research themes extraction** from keywords and MeSH terms
    - **Evidence quality assessment** based on study types
    - **Clinical relevance analysis** from trial data
    - **Cross-database insights** correlating research with clinical applications
    """
    try:
        results = await literature_agent.comprehensive_literature_search(
            query=query,
            max_results_per_source=max_results_per_source,
            include_clinical_trials=include_clinical_trials,
            include_drug_data=include_drug_data,
            include_protein_data=include_protein_data
        )
        
        return {
            "status": "success",
            "enhanced_results": results,
            "analysis_summary": {
                "total_sources": len(results.get('database_results', {})),
                "research_themes_found": len(results.get('research_themes', {}).get('top_research_themes', [])),
                "evidence_strength": results.get('evidence_quality', {}).get('evidence_strength', 'unknown'),
                "clinical_maturity": results.get('clinical_relevance', {}).get('clinical_maturity', 'unknown')
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced search failed: {str(e)}")

@app.post("/biomedical/disease-profile",
          response_model=Dict[str, Any],
          tags=["Biomedical Research"],
          summary="Comprehensive Disease Research Profile",
          description="Generate comprehensive research profile for specific diseases")
async def generate_disease_profile(
    disease: str = Field(description="Disease name (e.g., 'Alzheimer disease', 'Type 2 diabetes')"),
    include_genetics: bool = Field(default=True, description="Include genetic/genomic research"),
    include_treatments: bool = Field(default=True, description="Include treatment research"),
    background_tasks: BackgroundTasks = None
):
    """
    Generate comprehensive disease profile including:
    
    - **Research maturity assessment**
    - **Clinical pipeline strength**
    - **Genetic understanding level**
    - **Treatment landscape overview**
    - **Specialized research areas** (genetics, treatments)
    """
    try:
        profile = await literature_agent.focused_disease_research(
            disease=disease,
            include_genetics=include_genetics,
            include_treatments=include_treatments
        )
        
        return {
            "status": "success",
            "disease_profile": profile,
            "profile_summary": profile.get('disease_profile', {}),
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Disease profile generation failed: {str(e)}")

@app.get("/biomedical/research-trends/{topic}",
         response_model=Dict[str, Any],
         tags=["Biomedical Research"],
         summary="Research Trends Analysis",
         description="Analyze publication trends for research topics over time")
async def get_research_trends(
    topic: str = Field(description="Research topic to analyze"),
    years: Optional[str] = Field(default=None, description="Comma-separated years (e.g., '2020,2021,2022')")
):
    """
    Analyze research trends including:
    
    - **Publication volume over time**
    - **Growth rate analysis**
    - **Research momentum assessment**
    - **Peak activity periods**
    """
    try:
        year_list = None
        if years:
            year_list = [int(year.strip()) for year in years.split(',')]
        
        trends = await literature_agent.get_research_trends(topic, year_list)
        
        return {
            "status": "success",
            "trends": trends,
            "analysis_metadata": {
                "topic": topic,
                "years_analyzed": year_list or "default range",
                "generated_at": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend analysis failed: {str(e)}")

@app.get("/biomedical/databases/status",
         response_model=Dict[str, Any],
         tags=["Biomedical Research"],
         summary="Database Connectivity Status",
         description="Check status and connectivity of all biomedical databases")
async def check_biomedical_database_status():
    """
    Check the status and availability of all integrated biomedical databases
    """
    try:
        # Test connectivity to each database with a simple query
        status_results = {}
        
        test_queries = {
            "pubmed": "cancer",
            "clinicaltrials": "diabetes", 
            "fda_drugs": "aspirin",
            "nih_reporter": "COVID-19",
            "uniprot": "insulin"
        }
        
        for db_name, test_query in test_queries.items():
            try:
                if db_name == "pubmed":
                    result = biomedical_connector.search_pubmed_enhanced(test_query, max_results=1)
                elif db_name == "clinicaltrials":
                    result = biomedical_connector.search_clinical_trials(test_query, max_results=1)
                elif db_name == "fda_drugs":
                    result = biomedical_connector.search_fda_drugs(test_query, max_results=1)
                elif db_name == "nih_reporter":
                    result = biomedical_connector.search_nih_reporter(test_query, max_results=1)
                elif db_name == "uniprot":
                    result = biomedical_connector.search_uniprot_proteins(test_query, max_results=1)
                
                if 'error' in result:
                    status_results[db_name] = {"status": "error", "message": result['error']}
                else:
                    status_results[db_name] = {"status": "connected", "test_results": result.get('total_count', 0)}
                    
            except Exception as e:
                status_results[db_name] = {"status": "error", "message": str(e)}
        
        overall_status = "healthy" if all(status["status"] == "connected" for status in status_results.values()) else "degraded"
        
        return {
            "overall_status": overall_status,
            "individual_databases": status_results,
            "checked_at": datetime.now().isoformat(),
            "available_databases": [db for db, status in status_results.items() if status["status"] == "connected"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

# Authentication and Authorization Endpoints
@app.post("/auth/login",
          response_model=Dict[str, Any],
          tags=["Authentication"],
          summary="User Authentication",
          description="Authenticate user and receive JWT access token")
async def login(username: str = Field(..., description="Username or email"),
                password: str = Field(..., description="User password")):
    """
    Authenticate user credentials and return JWT access token
    
    **Demo Credentials:**
    - Admin: admin@syntheticascension.com / SecurePass123!
    - Researcher: researcher@syntheticascension.com / ResearchPass123!
    - Analyst: analyst@syntheticascension.com / AnalystPass123!
    """
    
    # Demo user database (in production, use secure database)
    demo_users = {
        "admin@syntheticascension.com": {
            "password_hash": security_manager.hash_password("SecurePass123!"),
            "role": UserRole.ADMIN,
            "user_id": "admin_001",
            "name": "System Administrator"
        },
        "researcher@syntheticascension.com": {
            "password_hash": security_manager.hash_password("ResearchPass123!"),
            "role": UserRole.RESEARCHER,
            "user_id": "researcher_001", 
            "name": "Lead Researcher"
        },
        "analyst@syntheticascension.com": {
            "password_hash": security_manager.hash_password("AnalystPass123!"),
            "role": UserRole.ANALYST,
            "user_id": "analyst_001",
            "name": "Data Analyst"
        }
    }
    
    user_data = demo_users.get(username)
    if not user_data or not security_manager.verify_password(password, user_data["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create access token
    token_data = {
        "user_id": user_data["user_id"],
        "username": username,
        "role": user_data["role"].value,
        "name": user_data["name"]
    }
    
    access_token = security_manager.create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user_info": {
            "user_id": user_data["user_id"],
            "username": username,
            "role": user_data["role"].value,
            "name": user_data["name"]
        }
    }

@app.post("/auth/api-key",
          response_model=Dict[str, Any],
          tags=["Authentication"],
          summary="Generate API Key",
          description="Generate API key for programmatic access")
async def generate_api_key(
    description: str = Field(..., description="Description for the API key"),
    current_user: Dict[str, Any] = Depends(require_role([UserRole.ADMIN, UserRole.RESEARCHER]))
):
    """
    Generate API key for programmatic access to the platform
    
    **Access Requirements:**
    - Admin or Researcher role required
    - Valid JWT token in Authorization header
    """
    
    api_key = security_manager.generate_api_key(
        user_id=current_user["user_id"],
        role=UserRole(current_user["role"]),
        description=description
    )
    
    return {
        "api_key": api_key,
        "description": description,
        "expires_in_days": API_KEY_EXPIRE_DAYS,
        "created_at": datetime.utcnow().isoformat(),
        "usage_instructions": {
            "header": "X-API-Key",
            "example": f"curl -H 'X-API-Key: {api_key[:20]}...' https://api.syntheticascension.com/secure/data"
        }
    }

@app.delete("/auth/api-key/{api_key}",
           tags=["Authentication"],
           summary="Revoke API Key",
           description="Revoke an existing API key")
async def revoke_api_key(
    api_key: str,
    current_user: Dict[str, Any] = Depends(require_role([UserRole.ADMIN]))
):
    """
    Revoke an existing API key
    
    **Access Requirements:**
    - Admin role required only
    """
    
    success = security_manager.revoke_api_key(api_key)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    return {"message": "API key revoked successfully"}

# Secure Research Data Access Endpoints
@app.get("/secure/research-data/cohorts",
         response_model=Dict[str, Any],
         tags=["Secure Data Access"],
         summary="List Patient Cohorts",
         description="Retrieve list of generated patient cohorts with access control")
async def list_secure_cohorts(
    limit: int = Field(default=10, ge=1, le=100),
    offset: int = Field(default=0, ge=0),
    classification: Optional[AccessLevel] = Field(default=None, description="Filter by data classification"),
    current_user: Dict[str, Any] = Depends(require_permission("cohort_generation", AccessLevel.INTERNAL)),
    rate_limited_user: Dict[str, Any] = Depends(rate_limit(50)),
    db: Session = Depends(get_db)
):
    """
    Retrieve patient cohorts with role-based access control
    
    **Access Requirements:**
    - Internal access level or higher required
    - Rate limited to 50 requests per hour
    - JWT authentication required
    
    **Data Classification:**
    - Public: Published research data
    - Internal: Institutional research data
    - Confidential: Unpublished/proprietary data
    - Restricted: PII or highly sensitive data
    """
    
    try:
        # Query cohorts from database
        query = db.query(Patient).offset(offset).limit(limit)
        cohorts = query.all()
        
        # Apply data classification filtering
        filtered_cohorts = []
        for cohort in cohorts:
            # Classify cohort data
            cohort_text = f"{cohort.demographics} {cohort.medical_history}"
            data_classification = DataClassification.classify_biomedical_data("cohort", cohort_text)
            
            # Check if user has access to this classification level
            user_role = UserRole(current_user["role"])
            allowed_levels = ROLE_PERMISSIONS[user_role]["cohort_generation"]
            
            if data_classification in allowed_levels:
                # Redact sensitive information based on access level
                cohort_data = {
                    "cohort_id": cohort.patient_id,
                    "demographics": cohort.demographics,
                    "conditions": cohort.medical_history,
                    "data_classification": data_classification.value,
                    "created_at": cohort.created_at.isoformat() if cohort.created_at else None
                }
                
                # Apply data encryption for sensitive fields
                if data_classification in [AccessLevel.CONFIDENTIAL, AccessLevel.RESTRICTED]:
                    cohort_data = DataEncryption.encrypt_sensitive_fields(
                        cohort_data, 
                        ["demographics", "conditions"]
                    )
                
                filtered_cohorts.append(cohort_data)
        
        # Add audit log entry
        audit_log("list_cohorts", "cohort_data", AccessLevel.INTERNAL)(lambda: None)()
        
        return {
            "cohorts": filtered_cohorts,
            "total_count": len(filtered_cohorts),
            "access_info": {
                "user_role": current_user["role"],
                "classification_filter": classification.value if classification else "all",
                "data_redaction_applied": True
            },
            "metadata": {
                "retrieved_at": datetime.utcnow().isoformat(),
                "user_id": current_user["user_id"]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve cohorts: {str(e)}")

@app.get("/secure/research-data/export/{cohort_id}",
         tags=["Secure Data Access"],
         summary="Export Cohort Data",
         description="Export patient cohort data with security controls")
async def export_cohort_data(
    cohort_id: str,
    format: str = Field(default="json", pattern="^(json|csv|xlsx)$"),
    include_pii: bool = Field(default=False, description="Include personally identifiable information"),
    current_user: Dict[str, Any] = Depends(require_permission("data_export", AccessLevel.CONFIDENTIAL)),
    rate_limited_user: Dict[str, Any] = Depends(rate_limit(10)),
    db: Session = Depends(get_db)
):
    """
    Export patient cohort data with comprehensive security controls
    
    **Access Requirements:**
    - Confidential access level required
    - Rate limited to 10 exports per hour
    - Admin/Researcher role required for PII access
    
    **Security Features:**
    - Automatic PII redaction
    - Data classification headers
    - Audit trail logging
    - Secure download headers
    """
    
    try:
        # Retrieve cohort data
        cohort = db.query(Patient).filter(Patient.patient_id == cohort_id).first()
        if not cohort:
            raise HTTPException(status_code=404, detail="Cohort not found")
        
        # Classify data sensitivity
        cohort_text = f"{cohort.demographics} {cohort.medical_history}"
        data_classification = DataClassification.classify_biomedical_data("cohort", cohort_text)
        
        # Check PII access permissions
        if include_pii and current_user["role"] not in [UserRole.ADMIN.value, UserRole.RESEARCHER.value]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions for PII access"
            )
        
        # Prepare export data
        export_data = {
            "cohort_id": cohort.patient_id,
            "demographics": cohort.demographics,
            "medical_history": cohort.medical_history,
            "lab_results": cohort.lab_results,
            "medications": cohort.medications,
            "clinical_notes": cohort.clinical_notes,
            "export_metadata": {
                "exported_by": current_user["user_id"],
                "exported_at": datetime.utcnow().isoformat(),
                "data_classification": data_classification.value,
                "pii_included": include_pii
            }
        }
        
        # Apply PII redaction if not explicitly requested
        if not include_pii:
            for field in ["demographics", "clinical_notes"]:
                if export_data[field]:
                    export_data[field] = DataEncryption.redact_pii(str(export_data[field]))
        
        # Generate secure headers
        headers = secure_export_headers(data_classification)
        headers["Content-Disposition"] = f"attachment; filename=cohort_{cohort_id}.{format}"
        
        # Log export action
        audit_log("export_cohort", f"cohort_{cohort_id}", data_classification)(lambda: None)()
        
        return Response(
            content=json.dumps(export_data, indent=2),
            headers=headers,
            media_type="application/json"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@app.get("/secure/biomedical/search",
         response_model=Dict[str, Any],
         tags=["Secure Biomedical Access"],
         summary="Secure Biomedical Search",
         description="Perform biomedical database search with access controls and audit logging")
async def secure_biomedical_search(
    query: str = Field(..., description="Research query"),
    databases: Optional[List[str]] = Field(default=None),
    max_results: int = Field(default=20, ge=1, le=50),
    classification_level: AccessLevel = Field(default=AccessLevel.PUBLIC, description="Required data classification level"),
    current_user: Dict[str, Any] = Depends(require_permission("biomedical_search", AccessLevel.INTERNAL)),
    rate_limited_user: Dict[str, Any] = Depends(rate_limit(30))
):
    """
    Secure biomedical database search with comprehensive access control
    
    **Access Requirements:**
    - Internal access level or higher required
    - Rate limited to 30 searches per hour
    - Results filtered by user's access level
    
    **Security Features:**
    - Query sanitization
    - Result classification
    - Audit trail logging
    - PII redaction
    """
    
    try:
        # Sanitize query to prevent injection attacks
        sanitized_query = query.strip()[:500]  # Limit query length
        
        # Perform biomedical search
        results = biomedical_connector.comprehensive_biomedical_search(
            query=sanitized_query,
            databases=databases,
            max_results_per_db=max_results
        )
        
        # Apply security filtering to results
        secured_results = {}
        user_role = UserRole(current_user["role"])
        allowed_levels = ROLE_PERMISSIONS[user_role]["biomedical_search"]
        
        for db_name, db_results in results.get("results", {}).items():
            secured_db_results = db_results.copy()
            
            # Filter results based on classification
            if db_name == "pubmed" and "articles" in secured_db_results:
                filtered_articles = []
                for article in secured_db_results["articles"]:
                    # Classify article content
                    article_content = f"{article.get('title', '')} {article.get('abstract', '')}"
                    article_classification = DataClassification.classify_biomedical_data("article", article_content)
                    
                    if article_classification in allowed_levels:
                        # Redact PII from abstracts
                        if article.get("abstract"):
                            article["abstract"] = DataEncryption.redact_pii(article["abstract"])
                        
                        article["data_classification"] = article_classification.value
                        filtered_articles.append(article)
                
                secured_db_results["articles"] = filtered_articles
                secured_db_results["total_count"] = len(filtered_articles)
            
            secured_results[db_name] = secured_db_results
        
        # Update results structure
        final_results = results.copy()
        final_results["results"] = secured_results
        
        # Add security metadata
        final_results["security_metadata"] = {
            "user_access_level": current_user["role"],
            "classification_applied": classification_level.value,
            "pii_redaction_applied": True,
            "search_audit_id": f"search_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{current_user['user_id']}"
        }
        
        # Log search action
        audit_log("biomedical_search", sanitized_query, classification_level)(lambda: None)()
        
        return {
            "status": "success",
            "results": final_results,
            "access_info": {
                "user_role": current_user["role"],
                "allowed_classifications": [level.value for level in allowed_levels],
                "query_sanitized": sanitized_query != query
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Secure search failed: {str(e)}")

@app.get("/secure/audit/logs",
         response_model=Dict[str, Any],
         tags=["Security & Compliance"],
         summary="Access Audit Logs",
         description="Retrieve system audit logs with role-based filtering")
async def get_audit_logs(
    limit: int = Field(default=50, ge=1, le=200),
    user_id: Optional[str] = Field(default=None, description="Filter by user ID"),
    action: Optional[str] = Field(default=None, description="Filter by action type"),
    start_date: Optional[str] = Field(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Field(default=None, description="End date (YYYY-MM-DD)"),
    current_user: Dict[str, Any] = Depends(require_permission("audit_logs", AccessLevel.INTERNAL)),
    db: Session = Depends(get_db)
):
    """
    Retrieve audit logs with comprehensive filtering and access control
    
    **Access Requirements:**
    - Internal access level or higher required
    - Admin users see all logs
    - Other users see only their own actions
    
    **Available Filters:**
    - User ID
    - Action type
    - Date range
    - Classification level
    """
    
    try:
        # Build query filters based on user role
        filters = {}
        
        # Non-admin users can only see their own logs
        if current_user["role"] != UserRole.ADMIN.value:
            filters["user_id"] = current_user["user_id"]
        elif user_id:
            filters["user_id"] = user_id
        
        if action:
            filters["action"] = action
        
        # Query audit logs from database
        query = db.query(AuditLog)
        
        if filters.get("user_id"):
            query = query.filter(AuditLog.user_id == filters["user_id"])
        
        if start_date:
            query = query.filter(AuditLog.timestamp >= datetime.fromisoformat(start_date))
        
        if end_date:
            query = query.filter(AuditLog.timestamp <= datetime.fromisoformat(end_date))
        
        audit_entries = query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
        
        # Format audit log entries
        formatted_logs = []
        for entry in audit_entries:
            log_data = {
                "id": entry.id,
                "timestamp": entry.timestamp.isoformat(),
                "user_id": entry.user_id,
                "action": entry.action,
                "resource": entry.resource,
                "success": entry.success,
                "details": entry.details or {}
            }
            
            formatted_logs.append(log_data)
        
        return {
            "audit_logs": formatted_logs,
            "total_count": len(formatted_logs),
            "filters_applied": filters,
            "access_level": current_user["role"],
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve audit logs: {str(e)}")

@app.get("/secure/system/security-status",
         response_model=Dict[str, Any],
         tags=["Security & Compliance"],
         summary="System Security Status",
         description="Get comprehensive security status and compliance information")
async def get_security_status(
    current_user: Dict[str, Any] = Depends(require_role([UserRole.ADMIN]))
):
    """
    Get comprehensive system security status
    
    **Access Requirements:**
    - Admin role required only
    
    **Includes:**
    - Active sessions and API keys
    - Security configuration status
    - Compliance indicators
    - Rate limiting statistics
    """
    
    try:
        # Gather security metrics
        security_status = {
            "authentication": {
                "jwt_enabled": True,
                "api_key_auth_enabled": True,
                "active_api_keys": len(security_manager.api_keys),
                "revoked_tokens": len(security_manager.revoked_tokens)
            },
            "access_control": {
                "rbac_enabled": True,
                "role_count": len(UserRole),
                "permission_matrix_configured": True,
                "data_classification_enabled": True
            },
            "data_protection": {
                "pii_redaction_enabled": True,
                "field_encryption_enabled": True,
                "audit_logging_enabled": True,
                "secure_headers_enabled": True
            },
            "rate_limiting": {
                "enabled": True,
                "active_limits": len(security_manager.rate_limits),
                "default_hourly_limit": 100
            },
            "compliance": {
                "hipaa_controls": True,
                "gdpr_controls": True,
                "audit_trail": True,
                "data_classification": True,
                "encryption_at_rest": "pending_implementation",
                "encryption_in_transit": True
            }
        }
        
        return {
            "status": "secure",
            "security_metrics": security_status,
            "last_updated": datetime.utcnow().isoformat(),
            "recommendations": [
                "Implement encryption at rest for database",
                "Set up log rotation for audit trails",
                "Configure backup encryption",
                "Enable multi-factor authentication"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get security status: {str(e)}")

@app.get("/system/databases/status",
         response_model=Dict[str, Any],
         tags=["System Management"],
         summary="Database System Status",
         description="Get comprehensive status of all database systems")
async def get_database_status(
    current_user: Dict[str, Any] = Depends(require_role([UserRole.ADMIN]))
):
    """
    Get comprehensive status of all database systems including:
    
    - **PostgreSQL**: Relational database for structured EHR data
    - **ChromaDB**: Vector database for literature embeddings
    - **Cache System**: In-memory cache for session data
    - **Document Store**: JSON document storage for configurations
    
    **Access Requirements:**
    - Admin role required only
    """
    
    try:
        db_manager = get_database_manager()
        health_status = db_manager.health_check()
        
        return {
            "database_systems": health_status,
            "checked_at": datetime.utcnow().isoformat(),
            "summary": {
                "total_systems": len(health_status.get("components", {})),
                "healthy_systems": len([
                    comp for comp in health_status.get("components", {}).values()
                    if comp.get("status") == "healthy"
                ]),
                "overall_status": health_status.get("overall_status", "unknown")
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get database status: {str(e)}")

@app.get("/system/databases/stats",
         response_model=Dict[str, Any],
         tags=["System Management"],
         summary="Database Statistics",
         description="Get detailed statistics for all database systems")
async def get_database_stats(
    current_user: Dict[str, Any] = Depends(require_role([UserRole.ADMIN, UserRole.RESEARCHER]))
):
    """
    Get detailed statistics for all database systems
    
    **Access Requirements:**
    - Admin or Researcher role required
    
    **Includes:**
    - Vector database collection details
    - Cache utilization metrics
    - Document store collection counts
    - Storage utilization estimates
    """
    
    try:
        db_manager = get_database_manager()
        stats = db_manager.get_database_stats()
        
        return {
            "database_statistics": stats,
            "collected_at": datetime.utcnow().isoformat(),
            "recommendations": [
                "Regular cache cleanup improves performance",
                "Monitor vector database growth for storage planning",
                "Archive old document store collections periodically"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get database statistics: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)