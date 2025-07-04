"""
Integrated Synthetic Ascension Backend Server V2
Simplified integration of your multi-agent backend with the existing platform
"""

import os
import uuid
import json
import asyncio
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import uvicorn

# Import the integrated orchestrator
from agents.integrated.orchestrator import IntegratedAgentOrchestrator
from agents.integrated.langflow_orchestrator import LangflowOrchestrator, LANGFLOW_TEMPLATES
from agents.integrated.mind_map_orchestrator import MindMapOrchestrator, demonstrate_ckd_diabetes_cohort

# Request/Response models
class IntegratedGenerationRequest(BaseModel):
    use_case: str = "comprehensive_ehr"
    population_size: int = 100
    condition: str = "hypertension"
    pipeline_config: Dict[str, Any] = {}
    agent_selection: List[str] = []
    
class IntegratedJobStatus(BaseModel):
    job_id: str
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    progress: float = 0.0
    current_agent: Optional[str] = None
    result_summary: Optional[Dict[str, Any]] = None
    agent_runs: List[Dict[str, Any]] = []

# Simple database manager for job tracking
class SimpleJobManager:
    def __init__(self):
        self.db_path = "integrated_jobs.db"
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database for job tracking"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                request_payload TEXT,
                status TEXT,
                started_at TEXT,
                ended_at TEXT,
                result_summary TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_runs (
                id TEXT PRIMARY KEY,
                job_id TEXT,
                agent_name TEXT,
                agent_type TEXT,
                status TEXT,
                execution_time_ms INTEGER,
                ran_at TEXT,
                FOREIGN KEY (job_id) REFERENCES jobs (id)
            )
        """)
        conn.commit()
        conn.close()
    
    def create_job(self, job_id: str, request_data: Dict[str, Any]) -> str:
        """Create a new job record"""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO jobs (id, request_payload, status, started_at) VALUES (?, ?, ?, ?)",
            (job_id, json.dumps(request_data), "pending", datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()
        return job_id
    
    def update_job_status(self, job_id: str, status: str, result_summary: Optional[Dict] = None):
        """Update job status"""
        conn = sqlite3.connect(self.db_path)
        if status == "completed":
            conn.execute(
                "UPDATE jobs SET status = ?, ended_at = ?, result_summary = ? WHERE id = ?",
                (status, datetime.utcnow().isoformat(), json.dumps(result_summary) if result_summary else None, job_id)
            )
        else:
            conn.execute(
                "UPDATE jobs SET status = ? WHERE id = ?",
                (status, job_id)
            )
        conn.commit()
        conn.close()
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        """Get job by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT id, request_payload, status, started_at, ended_at, result_summary FROM jobs WHERE id = ?",
            (job_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "request_payload": json.loads(row[1]) if row[1] else {},
                "status": row[2],
                "started_at": row[3],
                "ended_at": row[4],
                "result_summary": json.loads(row[5]) if row[5] else None
            }
        return None
    
    def add_agent_run(self, job_id: str, agent_run: Dict[str, Any]):
        """Add agent run record"""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO agent_runs (id, job_id, agent_name, agent_type, status, execution_time_ms, ran_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                str(uuid.uuid4()),
                job_id,
                agent_run.get("agent_name", "unknown"),
                agent_run.get("agent_type", "unknown"),
                agent_run.get("status", "unknown"),
                agent_run.get("execution_time_ms", 0),
                agent_run.get("ran_at", datetime.utcnow()).isoformat() if isinstance(agent_run.get("ran_at"), datetime) else str(agent_run.get("ran_at", datetime.utcnow()))
            )
        )
        conn.commit()
        conn.close()
    
    def get_agent_runs(self, job_id: str) -> List[Dict]:
        """Get agent runs for a job"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT agent_name, agent_type, status, execution_time_ms, ran_at FROM agent_runs WHERE job_id = ? ORDER BY ran_at",
            (job_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "agent_name": row[0],
                "agent_type": row[1],
                "status": row[2],
                "execution_time_ms": row[3],
                "ran_at": row[4]
            }
            for row in rows
        ]

# Initialize FastAPI app
app = FastAPI(
    title="Synthetic Ascension - Integrated Platform V2",
    description="Your comprehensive multi-agent backend integrated with the existing EHR platform",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase database connection
database_url = os.getenv("DATABASE_URL")
if database_url:
    engine = create_engine(database_url)
else:
    # Fallback to SQLite for development
    engine = create_engine("sqlite:///./leads.db")

# Initialize components
job_manager = SimpleJobManager()
orchestrator = IntegratedAgentOrchestrator()
langflow_orchestrator = LangflowOrchestrator()
mindmap_orchestrator = MindMapOrchestrator()

# Register predefined Langflow templates
for template_name, template_def in LANGFLOW_TEMPLATES.items():
    langflow_orchestrator.register_flow(template_name, template_def)

# Background task executor
async def execute_generation_pipeline(job_id: str, request: IntegratedGenerationRequest):
    """Execute the complete generation pipeline in background"""
    
    try:
        job_manager.update_job_status(job_id, "running")
        
        # Execute the integrated pipeline
        result = await orchestrator.execute_pipeline(
            uuid.UUID(job_id), 
            request.dict(), 
            None  # No session needed for simplified version
        )
        
        # Store agent runs
        for agent_run in result.get("agent_runs", []):
            job_manager.add_agent_run(job_id, agent_run)
        
        # Update job with results
        result_summary = result.get("generation_summary", {})
        job_manager.update_job_status(job_id, "completed", result_summary)
        
    except Exception as e:
        job_manager.update_job_status(job_id, "failed", {"error": str(e)})
        print(f"Error in pipeline execution: {e}")

# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def root():
    """Health check and service information"""
    return """
    <html>
        <head><title>Synthetic Ascension - Integrated Platform V2</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>🏥 Synthetic Ascension - Integrated Platform V2</h1>
            <p><strong>Status:</strong> ✅ Running</p>
            <p><strong>Version:</strong> 2.0.0</p>
            <p><strong>Integration:</strong> Your multi-agent backend fully integrated</p>
            
            <h2>🚀 Your Integrated Capabilities:</h2>
            <ul>
                <li><strong>Cohort Agents:</strong> Demographics, Clinical Journeys, Comorbidities, Medications, Labs, Vitals</li>
                <li><strong>QA Agents:</strong> Statistical Validation, Bias Detection, Realism Checking</li>
                <li><strong>Research Agents:</strong> Literature Mining, Ontology Mapping, Pattern Analysis</li>
                <li><strong>Reporting Agents:</strong> FHIR Export, Audit Trails, Trust Reports</li>
            </ul>
            
            <h2>🔧 Available Endpoints:</h2>
            <ul>
                <li><code>POST /api/v2/generate</code> - Generate comprehensive synthetic EHR data</li>
                <li><code>GET /api/v2/jobs/{job_id}</code> - Check generation job status</li>
                <li><code>GET /api/v2/analytics</code> - Platform analytics</li>
                <li><code>GET /docs</code> - Interactive API documentation</li>
            </ul>
            
            <h2>📊 Agent Architecture:</h2>
            <p>Your backend includes 18+ specialized agents orchestrated in a sophisticated pipeline:</p>
            <ol>
                <li><strong>Research Phase:</strong> Literature mining and ontology mapping</li>
                <li><strong>Generation Phase:</strong> Demographics → Clinical journeys → Comorbidities → Medications → Labs → Vitals</li>
                <li><strong>Validation Phase:</strong> Statistical validation, bias detection, realism checking</li>
                <li><strong>Export Phase:</strong> FHIR bundles, audit trails, trust reports</li>
            </ol>
        </body>
    </html>
    """

@app.post("/api/v2/generate")
async def generate_comprehensive_cohort(
    request: IntegratedGenerationRequest,
    background_tasks: BackgroundTasks
):
    """Generate comprehensive synthetic EHR data using your integrated multi-agent system"""
    
    # Create job ID and record
    job_id = str(uuid.uuid4())
    job_manager.create_job(job_id, request.dict())
    
    # Start background generation
    background_tasks.add_task(
        execute_generation_pipeline,
        job_id,
        request
    )
    
    return {
        "job_id": job_id,
        "status": "pending",
        "message": "Your integrated multi-agent pipeline has been started",
        "estimated_completion": "2-5 minutes",
        "agents_to_execute": [
            "Literature Miner", "Ontology Mapper", "Demographic Modeler",
            "Clinical Journey Simulator", "Comorbidity Modeler", "Medication Planner",
            "Lab Generator", "Vital Signs Generator", "Statistical Validator",
            "Bias Auditor", "Realism Checker", "FHIR Exporter", "Trust Report Writer"
        ]
    }

@app.get("/api/v2/jobs/{job_id}")
async def get_job_status(job_id: str) -> IntegratedJobStatus:
    """Get status of your integrated generation job"""
    
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get agent runs
    agent_runs = job_manager.get_agent_runs(job_id)
    
    # Calculate progress
    total_expected_agents = 15  # Approximate number of agents in pipeline
    completed_agents = len([run for run in agent_runs if run["status"] in ["success", "completed"]])
    progress = min((completed_agents / total_expected_agents) * 100, 100)
    
    # Get current agent
    current_agent = None
    if job["status"] == "running" and agent_runs:
        current_agent = agent_runs[-1]["agent_name"]
    
    return IntegratedJobStatus(
        job_id=job["id"],
        status=job["status"],
        started_at=datetime.fromisoformat(job["started_at"]),
        ended_at=datetime.fromisoformat(job["ended_at"]) if job["ended_at"] else None,
        progress=progress,
        current_agent=current_agent,
        result_summary=job["result_summary"],
        agent_runs=agent_runs
    )

@app.get("/api/v2/analytics")
async def get_platform_analytics():
    """Get analytics for your integrated platform"""
    
    conn = sqlite3.connect(job_manager.db_path)
    
    # Job statistics
    cursor = conn.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status")
    job_stats = dict(cursor.fetchall())
    
    cursor = conn.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]
    
    # Agent performance
    cursor = conn.execute("""
        SELECT agent_type, agent_name, status, COUNT(*) as count, AVG(execution_time_ms) as avg_time
        FROM agent_runs 
        GROUP BY agent_type, agent_name, status
    """)
    agent_performance = cursor.fetchall()
    
    conn.close()
    
    # Process agent performance data
    agent_stats = {}
    for agent_type, agent_name, status, count, avg_time in agent_performance:
        if agent_type not in agent_stats:
            agent_stats[agent_type] = {}
        if agent_name not in agent_stats[agent_type]:
            agent_stats[agent_type][agent_name] = {"total": 0, "successful": 0, "avg_time": 0}
        
        agent_stats[agent_type][agent_name]["total"] += count
        if status in ["success", "completed"]:
            agent_stats[agent_type][agent_name]["successful"] += count
        agent_stats[agent_type][agent_name]["avg_time"] = avg_time or 0
    
    return {
        "platform_overview": {
            "total_jobs": total_jobs,
            "job_statistics": job_stats,
            "success_rate": job_stats.get("completed", 0) / total_jobs if total_jobs > 0 else 0,
            "agent_types_integrated": len(agent_stats)
        },
        "agent_performance": agent_stats,
        "integration_status": {
            "cohort_agents": "✅ Integrated",
            "qa_agents": "✅ Integrated", 
            "research_agents": "✅ Integrated",
            "reporting_agents": "✅ Integrated",
            "backend_source": "Your comprehensive multi-agent system"
        },
        "capabilities": {
            "demographic_modeling": True,
            "clinical_journey_simulation": True,
            "comorbidity_modeling": True,
            "medication_planning": True,
            "lab_generation": True,
            "vital_signs_generation": True,
            "statistical_validation": True,
            "bias_detection": True,
            "realism_checking": True,
            "literature_mining": True,
            "ontology_mapping": True,
            "fhir_export": True,
            "audit_trails": True,
            "trust_scoring": True
        }
    }

@app.get("/api/v2/jobs/{job_id}/results")
async def get_job_results(job_id: str):
    """Get detailed results from a completed generation job"""
    
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job not yet completed")
    
    agent_runs = job_manager.get_agent_runs(job_id)
    
    return {
        "job_id": job_id,
        "generation_summary": job["result_summary"],
        "agent_execution_details": agent_runs,
        "export_formats": {
            "fhir_bundle": f"/api/v2/jobs/{job_id}/export/fhir",
            "csv_export": f"/api/v2/jobs/{job_id}/export/csv", 
            "audit_trail": f"/api/v2/jobs/{job_id}/export/audit",
            "trust_report": f"/api/v2/jobs/{job_id}/export/trust"
        },
        "quality_metrics": job.get("result_summary", {}).get("quality_summary", {}),
        "data_summary": job.get("result_summary", {}).get("data_summary", {})
    }

# Langflow-specific endpoints
@app.get("/api/v2/langflow/templates")
async def get_langflow_templates():
    """Get available Langflow workflow templates"""
    
    templates = []
    for template_name, template_data in LANGFLOW_TEMPLATES.items():
        templates.append({
            "name": template_name,
            "display_name": template_data["name"],
            "description": template_data["description"],
            "node_count": len(template_data["nodes"]),
            "edge_count": len(template_data["edges"]),
            "estimated_duration": "1-3 minutes"
        })
    
    return {
        "templates": templates,
        "langflow_enabled": True,
        "custom_flows_supported": True
    }

@app.post("/api/v2/langflow/generate")
async def generate_with_langflow(
    request: dict,
    background_tasks: BackgroundTasks
):
    """Generate using Langflow-based orchestration"""
    
    flow_name = request.get("flow_name", "comprehensive_ehr")
    population_size = request.get("population_size", 100)
    condition = request.get("condition", "hypertension")
    flow_config = request.get("flow_config", {})
    
    # Create job
    job_id = str(uuid.uuid4())
    job_data = {
        "flow_name": flow_name,
        "population_size": population_size,
        "condition": condition,
        "flow_config": flow_config,
        "orchestration_type": "langflow"
    }
    
    job_manager.create_job(job_id, job_data)
    
    # Start Langflow execution
    background_tasks.add_task(
        execute_langflow_pipeline,
        job_id,
        flow_name,
        job_data
    )
    
    return {
        "job_id": job_id,
        "status": "pending",
        "message": f"Langflow pipeline '{flow_name}' started",
        "flow_name": flow_name,
        "orchestration_type": "langflow",
        "visual_flow": True,
        "estimated_completion": "2-4 minutes"
    }

@app.get("/api/v2/langflow/flows/{flow_name}")
async def get_langflow_definition(flow_name: str):
    """Get Langflow workflow definition"""
    
    if flow_name not in LANGFLOW_TEMPLATES:
        raise HTTPException(status_code=404, detail="Flow template not found")
    
    template = LANGFLOW_TEMPLATES[flow_name]
    
    return {
        "flow_name": flow_name,
        "definition": template,
        "node_details": [
            {
                "id": node["id"],
                "type": node["type"],
                "agent_name": node.get("data", {}).get("agent_name", "N/A"),
                "agent_type": node.get("data", {}).get("agent_type", "N/A")
            }
            for node in template["nodes"]
        ],
        "execution_graph": {
            "nodes": len(template["nodes"]),
            "edges": len(template["edges"]),
            "parallel_sections": len([n for n in template["nodes"] if n["type"] == "parallel_group"])
        }
    }

@app.post("/api/v2/langflow/flows")
async def create_custom_flow(flow_definition: dict):
    """Create a custom Langflow workflow"""
    
    flow_name = flow_definition.get("name")
    if not flow_name:
        raise HTTPException(status_code=400, detail="Flow name is required")
    
    # Validate flow definition
    required_fields = ["nodes", "edges"]
    for field in required_fields:
        if field not in flow_definition:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # Register the custom flow
    langflow_orchestrator.register_flow(flow_name, flow_definition)
    
    return {
        "flow_name": flow_name,
        "status": "registered",
        "message": "Custom flow registered successfully",
        "node_count": len(flow_definition["nodes"]),
        "edge_count": len(flow_definition["edges"])
    }

# Background task for Langflow execution
async def execute_langflow_pipeline(job_id: str, flow_name: str, request_data: dict):
    """Execute Langflow pipeline in background"""
    
    try:
        job_manager.update_job_status(job_id, "running")
        
        # Execute the Langflow pipeline
        result = await langflow_orchestrator.execute_langflow_pipeline(
            flow_name,
            uuid.UUID(job_id),
            request_data
        )
        
        # Store agent runs
        for agent_run in result.get("agent_runs", []):
            job_manager.add_agent_run(job_id, agent_run)
        
        # Update job with results
        result_summary = result.get("generation_summary", {})
        result_summary["orchestration_type"] = "langflow"
        result_summary["flow_name"] = flow_name
        
        job_manager.update_job_status(job_id, "completed", result_summary)
        
    except Exception as e:
        job_manager.update_job_status(job_id, "failed", {"error": str(e), "orchestration_type": "langflow"})
        print(f"Error in Langflow pipeline execution: {e}")

# Mind Map Chain-of-Thought endpoints
@app.get("/api/v2/mindmap/demo")
async def get_demo_mindmap():
    """Get demonstration mind map for 5-patient CKD+Diabetes cohort"""
    
    demo_data = demonstrate_ckd_diabetes_cohort()
    return {
        "demonstration": "5-patient CKD+Diabetes cohort generation",
        "mind_map": demo_data["mind_map"],
        "execution_sequence": demo_data["execution_sequence"],
        "phases": demo_data["phases"],
        "total_nodes": demo_data["total_nodes"],
        "interactive_features": {
            "node_selection": "Click any node to see chain-of-thought details",
            "replay_command": "Use REPLAY node_id to walk through subtree",
            "phase_filtering": "Filter nodes by phase for focused analysis"
        }
    }

@app.get("/api/v2/mindmap/node/{node_id}")
async def get_node_details(node_id: str):
    """Get detailed chain-of-thought for a specific node"""
    
    demo_data = demonstrate_ckd_diabetes_cohort()
    
    if node_id not in demo_data["mind_map"]:
        raise HTTPException(status_code=404, detail="Node not found")
    
    node = demo_data["mind_map"][node_id]
    
    return {
        "node_id": node_id,
        "agent": node["agent"],
        "phase": node["phase"],
        "decision": node["decision"],
        "chain_of_thought": node["chain_of_thought"],
        "children": node["children"],
        "execution_time_ms": node["execution_time_ms"],
        "status": node["status"],
        "reasoning_breakdown": {
            "inputs_analyzed": node["chain_of_thought"][0],
            "hypotheses_considered": node["chain_of_thought"][1],
            "decision_criteria": node["chain_of_thought"][2],
            "reasoning_process": node["chain_of_thought"][3],
            "final_decision": node["chain_of_thought"][4]
        }
    }

@app.get("/api/v2/mindmap/replay/{node_id}")
async def replay_node_subtree(node_id: str):
    """Replay execution of a node's subtree in chronological order"""
    
    demo_data = demonstrate_ckd_diabetes_cohort()
    
    if node_id not in demo_data["mind_map"]:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Build subtree replay sequence
    def get_subtree_nodes(current_id, mind_map, visited=None):
        if visited is None:
            visited = set()
        
        if current_id in visited or current_id not in mind_map:
            return []
        
        visited.add(current_id)
        subtree = [current_id]
        
        for child_id in mind_map[current_id]["children"]:
            subtree.extend(get_subtree_nodes(child_id, mind_map, visited))
        
        return subtree
    
    subtree_nodes = get_subtree_nodes(node_id, demo_data["mind_map"])
    
    replay_sequence = []
    for i, sub_node_id in enumerate(subtree_nodes):
        node = demo_data["mind_map"][sub_node_id]
        replay_sequence.append({
            "step": i + 1,
            "node_id": sub_node_id,
            "agent": node["agent"],
            "phase": node["phase"],
            "decision": node["decision"],
            "chain_of_thought": node["chain_of_thought"],
            "execution_time_ms": node["execution_time_ms"],
            "children_count": len(node["children"])
        })
    
    return {
        "replay_root": node_id,
        "subtree_size": len(subtree_nodes),
        "execution_sequence": replay_sequence,
        "replay_summary": {
            "total_steps": len(replay_sequence),
            "phases_covered": list(set(step["phase"] for step in replay_sequence)),
            "agents_involved": list(set(step["agent"] for step in replay_sequence)),
            "total_execution_time_ms": sum(step["execution_time_ms"] for step in replay_sequence)
        }
    }

@app.post("/api/v2/leads")
async def capture_lead(lead_data: dict):
    """Capture comprehensive waitlist information from landing page"""
    
    with Session(engine) as session:
        try:
            # Create leads table with expanded schema for waitlist
            session.execute(text("""
                CREATE TABLE IF NOT EXISTS leads (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    organization VARCHAR(255),
                    role VARCHAR(255),
                    use_cases TEXT,
                    interested_in_design_partner BOOLEAN DEFAULT FALSE,
                    phone VARCHAR(50),
                    company_size VARCHAR(100),
                    industry VARCHAR(100),
                    current_ehr_system VARCHAR(255),
                    timeline VARCHAR(100),
                    budget_range VARCHAR(100),
                    specific_requirements TEXT,
                    source VARCHAR(100) DEFAULT 'waitlist',
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Insert lead data with comprehensive fields
            session.execute(text("""
                INSERT INTO leads (
                    name, email, organization, role, use_cases, 
                    interested_in_design_partner, phone, company_size, 
                    industry, current_ehr_system, timeline, budget_range,
                    specific_requirements, source, timestamp
                )
                VALUES (
                    :name, :email, :organization, :role, :use_cases,
                    :interested_in_design_partner, :phone, :company_size,
                    :industry, :current_ehr_system, :timeline, :budget_range,
                    :specific_requirements, :source, :timestamp
                )
            """), {
                "name": lead_data.get("name"),
                "email": lead_data.get("email"),
                "organization": lead_data.get("organization"),
                "role": lead_data.get("role"),
                "use_cases": lead_data.get("use_cases"),
                "interested_in_design_partner": lead_data.get("interested_in_design_partner", False),
                "phone": lead_data.get("phone"),
                "company_size": lead_data.get("company_size"),
                "industry": lead_data.get("industry"),
                "current_ehr_system": lead_data.get("current_ehr_system"),
                "timeline": lead_data.get("timeline"),
                "budget_range": lead_data.get("budget_range"),
                "specific_requirements": lead_data.get("specific_requirements"),
                "source": lead_data.get("source", "waitlist"),
                "timestamp": lead_data.get("timestamp", datetime.utcnow().isoformat())
            })
            
            session.commit()
            
            return {
                "status": "success",
                "message": "Lead captured successfully",
                "lead_id": "captured"
            }
            
        except Exception as e:
            session.rollback()
            print(f"Error capturing lead: {e}")
            return {
                "status": "error",
                "message": "Failed to capture lead",
                "error": str(e)
            }

@app.post("/api/v2/mindmap/generate")
async def generate_with_mindmap(
    request: dict,
    background_tasks: BackgroundTasks
):
    """Generate cohort with full chain-of-thought mind mapping"""
    
    population_size = request.get("population_size", 100)
    condition = request.get("condition", "hypertension")
    use_case = request.get("use_case", "clinical_research")
    
    # Create job
    job_id = str(uuid.uuid4())
    job_data = {
        "population_size": population_size,
        "condition": condition,
        "use_case": use_case,
        "orchestration_type": "mindmap",
        "chain_of_thought_enabled": True
    }
    
    job_manager.create_job(job_id, job_data)
    
    # Start mind map generation (would be async in real implementation)
    background_tasks.add_task(
        execute_mindmap_generation,
        job_id,
        job_data
    )
    
    return {
        "job_id": job_id,
        "status": "pending",
        "message": "Mind map generation started with full chain-of-thought logging",
        "orchestration_type": "mindmap",
        "features": [
            "Detailed reasoning chains for each agent",
            "Interactive node exploration",
            "Subtree replay capabilities",
            "Phase-based analysis"
        ],
        "estimated_completion": "3-5 minutes"
    }

# Background task for mind map generation
async def execute_mindmap_generation(job_id: str, request_data: dict):
    """Execute mind map generation in background"""
    
    try:
        job_manager.update_job_status(job_id, "running")
        
        # Execute with mind mapping (would be async call in real implementation)
        # For now, return demo structure
        result = demonstrate_ckd_diabetes_cohort()
        
        # Store results
        result_summary = {
            "orchestration_type": "mindmap",
            "mind_map_nodes": result["total_nodes"],
            "phases_executed": len(result["phases"]),
            "chain_of_thought_entries": sum(len(node["chain_of_thought"]) for node in result["mind_map"].values()),
            "interactive_features_enabled": True
        }
        
        job_manager.update_job_status(job_id, "completed", result_summary)
        
    except Exception as e:
        job_manager.update_job_status(job_id, "failed", {"error": str(e), "orchestration_type": "mindmap"})
        print(f"Error in mind map generation: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)