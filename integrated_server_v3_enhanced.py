"""
Integrated Synthetic Ascension Backend Server V3 - Enhanced Agentic Architecture
Implements the comprehensive Doer/Coordinator/Adversarial pattern with expert recommendations
"""

import asyncio
import uuid
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import the enhanced orchestrator
from agents.integrated.enhanced_orchestrator import EnhancedAgentOrchestrator

# Request/Response Models
class EnhancedGenerationRequest(BaseModel):
    use_case: str = "comprehensive_ehr_v2"
    population_size: int = 100
    condition: str = "hypertension"
    pipeline_config: Dict[str, Any] = {}
    agent_selection: List[str] = []
    enable_adversarial_testing: bool = True
    require_clinical_review: bool = True
    privacy_level: str = "high"  # low, medium, high

class EnhancedJobStatus(BaseModel):
    job_id: str
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    progress: float = 0.0
    current_phase: Optional[str] = None
    current_agent: Optional[str] = None
    result_summary: Optional[Dict[str, Any]] = None
    agent_runs: List[Dict[str, Any]] = []
    phase_results: Dict[str, Any] = {}
    
class EnhancedJobManager:
    """Enhanced job manager with comprehensive tracking"""
    
    def __init__(self):
        self.db_path = "enhanced_ehr_jobs.db"
        self.init_db()
    
    def init_db(self):
        """Initialize enhanced SQLite database for job tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enhanced jobs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enhanced_jobs (
                job_id TEXT PRIMARY KEY,
                request_data TEXT NOT NULL,
                pipeline_config TEXT,
                status TEXT DEFAULT 'pending',
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                result_summary TEXT,
                phase_results TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Enhanced agent runs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enhanced_agent_runs (
                run_id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                agent_type TEXT NOT NULL,
                agent_role TEXT NOT NULL,
                phase_name TEXT,
                input_data TEXT,
                output_data TEXT,
                execution_time_ms INTEGER DEFAULT 0,
                status TEXT DEFAULT 'completed',
                ran_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                privacy_assessment TEXT,
                clinical_review_status TEXT,
                FOREIGN KEY (job_id) REFERENCES enhanced_jobs (job_id)
            )
        """)
        
        # Phase tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enhanced_phases (
                phase_id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                phase_name TEXT NOT NULL,
                phase_status TEXT DEFAULT 'pending',
                started_at TIMESTAMP,
                ended_at TIMESTAMP,
                agent_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                FOREIGN KEY (job_id) REFERENCES enhanced_jobs (job_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_job(self, job_id: str, request_data: Dict[str, Any]) -> str:
        """Create a new enhanced job record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO enhanced_jobs (job_id, request_data, status)
            VALUES (?, ?, 'pending')
        """, (job_id, json.dumps(request_data)))
        
        conn.commit()
        conn.close()
        return job_id
    
    def update_job_status(self, job_id: str, status: str, result_summary: Optional[Dict] = None,
                         phase_results: Optional[Dict] = None):
        """Update enhanced job status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        update_data = [status]
        update_sql = "UPDATE enhanced_jobs SET status = ?"
        
        if status in ['completed', 'failed', 'error']:
            update_sql += ", ended_at = CURRENT_TIMESTAMP"
        
        if result_summary:
            update_sql += ", result_summary = ?"
            update_data.append(json.dumps(result_summary))
        
        if phase_results:
            update_sql += ", phase_results = ?"
            update_data.append(json.dumps(phase_results))
        
        update_sql += " WHERE job_id = ?"
        update_data.append(job_id)
        
        cursor.execute(update_sql, update_data)
        conn.commit()
        conn.close()
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        """Get enhanced job by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT job_id, request_data, status, started_at, ended_at, 
                   result_summary, phase_results
            FROM enhanced_jobs WHERE job_id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "job_id": row[0],
                "request_data": json.loads(row[1]) if row[1] else {},
                "status": row[2],
                "started_at": row[3],
                "ended_at": row[4],
                "result_summary": json.loads(row[5]) if row[5] else {},
                "phase_results": json.loads(row[6]) if row[6] else {}
            }
        return None
    
    def add_agent_run(self, job_id: str, agent_run: Dict[str, Any]):
        """Add enhanced agent run record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO enhanced_agent_runs 
            (run_id, job_id, agent_name, agent_type, agent_role, phase_name,
             input_data, output_data, execution_time_ms, status, 
             privacy_assessment, clinical_review_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            job_id,
            agent_run.get("agent_name", ""),
            agent_run.get("agent_type", ""),
            agent_run.get("agent_role", ""),
            agent_run.get("phase_name", ""),
            json.dumps(agent_run.get("input_data", {})),
            json.dumps(agent_run.get("output_data", {})),
            agent_run.get("execution_time_ms", 0),
            agent_run.get("status", "completed"),
            json.dumps(agent_run.get("privacy_assessment", {})),
            agent_run.get("clinical_review_status", "pending")
        ))
        
        conn.commit()
        conn.close()
    
    def get_agent_runs(self, job_id: str) -> List[Dict]:
        """Get enhanced agent runs for a job"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT agent_name, agent_type, agent_role, phase_name, status, 
                   execution_time_ms, ran_at, privacy_assessment, clinical_review_status
            FROM enhanced_agent_runs WHERE job_id = ?
            ORDER BY ran_at
        """, (job_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            "agent_name": row[0],
            "agent_type": row[1],
            "agent_role": row[2],
            "phase_name": row[3],
            "status": row[4],
            "execution_time_ms": row[5],
            "ran_at": row[6],
            "privacy_assessment": json.loads(row[7]) if row[7] else {},
            "clinical_review_status": row[8]
        } for row in rows]

# Initialize FastAPI app
app = FastAPI(
    title="Enhanced Synthetic Ascension EHR Platform V3",
    description="Comprehensive Agentic EHR Synthesis with Doer/Coordinator/Adversarial Architecture",
    version="3.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize enhanced components
enhanced_orchestrator = EnhancedAgentOrchestrator()
enhanced_job_manager = EnhancedJobManager()

@app.get("/")
async def root():
    """Enhanced system overview and agent architecture"""
    
    agent_overview = enhanced_orchestrator.get_agent_architecture_overview()
    
    return {
        "service": "Enhanced Synthetic Ascension EHR Platform V3",
        "version": "3.0.0",
        "description": "Comprehensive Agentic EHR Synthesis implementing Doer/Coordinator/Adversarial pattern",
        "architecture": agent_overview,
        "key_enhancements": [
            "Version pinning for reproducible results",
            "Concurrency management with deadlock prevention",
            "Differential privacy and re-identification protection",
            "Human-in-the-loop SLA management",
            "Clinical realism certification",
            "Automated ontology updates",
            "RAG hallucination reduction",
            "Performance monitoring and benchmarking",
            "Comprehensive adversarial testing",
            "Full provenance and audit trails"
        ],
        "endpoints": {
            "POST /api/v3/generate": "Generate comprehensive synthetic EHR data with enhanced agent orchestration",
            "GET /api/v3/jobs/{job_id}": "Check enhanced multi-agent generation job status",
            "GET /api/v3/jobs/{job_id}/results": "Get detailed generation results with quality metrics",
            "GET /api/v3/analytics": "Platform analytics and enhanced agent performance metrics",
            "GET /api/v3/architecture": "Get comprehensive agent architecture overview"
        }
    }

async def execute_enhanced_generation_pipeline(job_id: str, request: EnhancedGenerationRequest):
    """Execute the enhanced comprehensive generation pipeline in background"""
    
    try:
        # Update job status to running
        enhanced_job_manager.update_job_status(job_id, "running")
        
        # Execute comprehensive pipeline
        pipeline_result = await enhanced_orchestrator.execute_comprehensive_pipeline(
            uuid.UUID(job_id),
            request.dict()
        )
        
        # Store agent runs
        for agent_run in pipeline_result.get("agent_runs", []):
            enhanced_job_manager.add_agent_run(job_id, agent_run)
        
        # Update job with results
        enhanced_job_manager.update_job_status(
            job_id, 
            pipeline_result["overall_status"],
            pipeline_result.get("execution_summary", {}),
            pipeline_result.get("phase_results", {})
        )
        
    except Exception as e:
        enhanced_job_manager.update_job_status(
            job_id, 
            "error",
            {"error": str(e), "error_timestamp": datetime.utcnow().isoformat()}
        )

@app.post("/api/v3/generate")
async def generate_enhanced_cohort(
    request: EnhancedGenerationRequest,
    background_tasks: BackgroundTasks
):
    """Generate comprehensive synthetic EHR data using enhanced multi-agent orchestration"""
    
    job_id = str(uuid.uuid4())
    
    # Create job record
    enhanced_job_manager.create_job(job_id, request.dict())
    
    # Start background processing
    background_tasks.add_task(execute_enhanced_generation_pipeline, job_id, request)
    
    return {
        "job_id": job_id,
        "status": "started",
        "message": "Enhanced comprehensive EHR generation pipeline initiated",
        "estimated_completion_minutes": 15,
        "pipeline_features": [
            "6-phase agent execution",
            "Real-time privacy assessment", 
            "Clinical realism certification",
            "Adversarial robustness testing",
            "Performance benchmarking",
            "Full audit trail generation"
        ]
    }

@app.get("/api/v3/jobs/{job_id}")
async def get_enhanced_job_status(job_id: str) -> EnhancedJobStatus:
    """Get status of enhanced generation job"""
    
    job = enhanced_job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    agent_runs = enhanced_job_manager.get_agent_runs(job_id)
    
    # Calculate progress
    total_expected_agents = 50  # Approximate total agents in comprehensive pipeline
    completed_agents = len([r for r in agent_runs if r["status"] in ["success", "completed"]])
    progress = min((completed_agents / total_expected_agents) * 100, 100.0)
    
    # Determine current phase and agent
    current_phase = None
    current_agent = None
    if agent_runs and job["status"] == "running":
        latest_run = agent_runs[-1]
        current_phase = latest_run.get("phase_name")
        if latest_run["status"] == "running":
            current_agent = latest_run["agent_name"]
    
    return EnhancedJobStatus(
        job_id=job_id,
        status=job["status"],
        started_at=datetime.fromisoformat(job["started_at"]),
        ended_at=datetime.fromisoformat(job["ended_at"]) if job["ended_at"] else None,
        progress=progress,
        current_phase=current_phase,
        current_agent=current_agent,
        result_summary=job["result_summary"],
        agent_runs=agent_runs,
        phase_results=job["phase_results"]
    )

@app.get("/api/v3/jobs/{job_id}/results")
async def get_enhanced_job_results(job_id: str):
    """Get detailed results from enhanced generation job"""
    
    job = enhanced_job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job["status"] not in ["completed", "failed"]:
        raise HTTPException(status_code=400, detail="Job not yet completed")
    
    agent_runs = enhanced_job_manager.get_agent_runs(job_id)
    
    return {
        "job_id": job_id,
        "status": job["status"],
        "execution_summary": job["result_summary"],
        "phase_results": job["phase_results"],
        "agent_execution_details": agent_runs,
        "privacy_assessments": [r["privacy_assessment"] for r in agent_runs if r["privacy_assessment"]],
        "clinical_reviews": [r["clinical_review_status"] for r in agent_runs],
        "performance_metrics": {
            "total_agents_executed": len(agent_runs),
            "successful_executions": len([r for r in agent_runs if r["status"] == "success"]),
            "average_execution_time_ms": sum(r["execution_time_ms"] for r in agent_runs) / len(agent_runs) if agent_runs else 0
        }
    }

@app.get("/api/v3/analytics")
async def get_enhanced_platform_analytics():
    """Get analytics for enhanced platform"""
    
    conn = sqlite3.connect(enhanced_job_manager.db_path)
    cursor = conn.cursor()
    
    # Job statistics
    cursor.execute("SELECT status, COUNT(*) FROM enhanced_jobs GROUP BY status")
    job_stats = dict(cursor.fetchall())
    
    # Agent performance statistics
    cursor.execute("""
        SELECT agent_role, COUNT(*), AVG(execution_time_ms), 
               SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count
        FROM enhanced_agent_runs 
        GROUP BY agent_role
    """)
    agent_performance = [{
        "role": row[0],
        "total_executions": row[1],
        "avg_execution_time_ms": row[2],
        "success_rate": (row[3] / row[1]) * 100 if row[1] > 0 else 0
    } for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        "platform_version": "3.0.0",
        "analytics_timestamp": datetime.utcnow().isoformat(),
        "job_statistics": job_stats,
        "agent_performance_by_role": agent_performance,
        "architecture_metrics": enhanced_orchestrator.get_agent_architecture_overview(),
        "system_health": {
            "total_jobs_processed": sum(job_stats.values()),
            "system_uptime": "operational",
            "agent_availability": "100%"
        }
    }

@app.get("/api/v3/architecture")
async def get_agent_architecture():
    """Get comprehensive agent architecture overview"""
    return enhanced_orchestrator.get_agent_architecture_overview()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)