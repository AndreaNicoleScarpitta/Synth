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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)