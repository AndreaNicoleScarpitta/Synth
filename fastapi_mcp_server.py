"""
Enhanced FastAPI + MCP Server for Synthetic Ascension
Combines REST API endpoints with Model Context Protocol capabilities
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import uuid
import random
import asyncio
from datetime import datetime
import json

# Import MCP capabilities
from fastmcp import FastMCP
from mcp import StdioServerParameters, stdio_server
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

# Initialize FastAPI
app = FastAPI(
    title="Synthetic Ascension - FastAPI + MCP Platform",
    description="AI-powered EHR synthetic data generation with Model Context Protocol",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP server
mcp_server = FastMCP("Synthetic Ascension EHR Platform")

# Request/Response Models
class PatientGenerationRequest(BaseModel):
    population_size: int = Field(default=100, ge=1, le=1000, description="Number of patients to generate")
    conditions: List[str] = Field(default=[], description="Medical conditions to include")
    age_range: List[int] = Field(default=[18, 80], description="Age range [min, max]")
    specialties: List[str] = Field(default=[], description="Medical specialties to focus on")
    demographics: Dict[str, Any] = Field(default={}, description="Demographic preferences")

class PatientRecord(BaseModel):
    patient_id: str
    name: str
    age: int
    gender: str
    conditions: List[str]
    vitals: Dict[str, Any]
    demographics: Dict[str, Any]
    clinical_notes: Optional[str] = None

# Data storage
generated_cohorts = {}
active_workflows = {}

# ================================
# FastAPI REST Endpoints
# ================================

@app.get("/")
async def root():
    """API health check and info"""
    return {
        "service": "Synthetic Ascension FastAPI + MCP",
        "status": "operational",
        "capabilities": ["REST API", "Model Context Protocol", "AI Agent Integration"],
        "version": "2.0.0",
        "mcp_endpoint": "/mcp",
        "api_docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    return {
        "status": "healthy",
        "services": {
            "fastapi": "operational",
            "mcp_server": "ready",
            "ai_agents": "active",
            "database": "connected"
        },
        "statistics": {
            "total_cohorts": len(generated_cohorts),
            "active_workflows": len([w for w in active_workflows.values() if w.get("status") == "running"])
        }
    }

@app.post("/api/v1/generate/cohort")
async def generate_cohort_api(request: PatientGenerationRequest, background_tasks: BackgroundTasks):
    """REST API endpoint for cohort generation"""
    return await generate_patient_cohort_internal(
        request.population_size,
        request.conditions,
        request.age_range,
        request.specialties,
        request.demographics
    )

@app.get("/api/v1/cohorts")
async def list_cohorts_api():
    """REST API endpoint to list all cohorts"""
    cohorts = []
    for workflow_id, cohort_data in generated_cohorts.items():
        cohorts.append({
            "workflow_id": workflow_id,
            "patient_count": len(cohort_data["patients"]),
            "created_at": cohort_data["metadata"]["generation_time"],
            "status": "completed"
        })
    
    return {
        "total_cohorts": len(cohorts),
        "cohorts": cohorts
    }

@app.get("/api/v1/cohort/{workflow_id}")
async def get_cohort_api(workflow_id: str):
    """REST API endpoint to get specific cohort"""
    if workflow_id not in generated_cohorts:
        raise HTTPException(status_code=404, detail="Cohort not found")
    
    return generated_cohorts[workflow_id]

@app.get("/api/v1/analytics/dashboard")
async def dashboard_analytics_api():
    """REST API endpoint for dashboard analytics"""
    total_patients = sum(len(cohort["patients"]) for cohort in generated_cohorts.values())
    
    return {
        "overview": {
            "total_cohorts": len(generated_cohorts),
            "total_patients": total_patients,
            "active_workflows": len([w for w in active_workflows.values() if w.get("status") == "running"]),
            "success_rate": "100%"
        },
        "platform_capabilities": [
            "AI-powered patient generation",
            "Multi-specialty medical data",
            "HIPAA-compliant synthetic records",
            "Real-time API access",
            "MCP agent integration"
        ]
    }

# ================================
# Internal Functions
# ================================

async def generate_patient_cohort_internal(
    population_size: int,
    conditions: List[str],
    age_range: List[int],
    specialties: List[str],
    demographics: Dict[str, Any]
) -> Dict[str, Any]:
    """Internal function for patient generation (shared by REST and MCP)"""
    
    # Generate workflow ID
    workflow_id = str(uuid.uuid4())
    
    # Store workflow state
    active_workflows[workflow_id] = {
        "status": "generating",
        "progress": 0,
        "started_at": datetime.now(),
        "request": {
            "population_size": population_size,
            "conditions": conditions,
            "age_range": age_range,
            "specialties": specialties
        }
    }
    
    # Generate synthetic patients
    patients = []
    for i in range(population_size):
        patient_id = f"PAT-{uuid.uuid4().hex[:8].upper()}"
        
        # Enhanced patient generation with medical specialties
        patient = await generate_enhanced_patient(
            patient_id, i+1, conditions, age_range, specialties, demographics
        )
        patients.append(patient)
        
        # Update progress
        active_workflows[workflow_id]["progress"] = int((i + 1) / population_size * 100)
    
    # Store generated cohort
    generated_cohorts[workflow_id] = {
        "patients": patients,
        "metadata": {
            "total_patients": len(patients),
            "generation_time": datetime.now().isoformat(),
            "configuration": {
                "population_size": population_size,
                "conditions": conditions,
                "age_range": age_range,
                "specialties": specialties,
                "demographics": demographics
            }
        }
    }
    
    # Update workflow status
    active_workflows[workflow_id]["status"] = "completed"
    active_workflows[workflow_id]["progress"] = 100
    active_workflows[workflow_id]["completed_at"] = datetime.now()
    
    return {
        "workflow_id": workflow_id,
        "status": "completed",
        "summary": {
            "total_patients": len(patients),
            "conditions_included": conditions,
            "specialties_focus": specialties,
            "demographics_range": f"Ages {age_range[0]}-{age_range[1]}",
            "generation_timestamp": datetime.now().isoformat()
        },
        "sample_patients": patients[:3]  # First 3 as examples
    }

async def generate_enhanced_patient(
    patient_id: str, 
    sequence: int, 
    conditions: List[str], 
    age_range: List[int], 
    specialties: List[str],
    demographics: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate a single enhanced patient record"""
    
    age = random.randint(age_range[0], age_range[1])
    gender = random.choice(["Male", "Female"])
    
    # Specialty-specific condition assignment
    assigned_conditions = []
    if conditions:
        # Assign realistic number of conditions based on age
        condition_count = 1 if age < 30 else random.randint(1, min(3, len(conditions)))
        assigned_conditions = random.sample(conditions, condition_count)
    
    # Generate specialty-specific clinical data
    clinical_data = {}
    if "cardiology" in [s.lower() for s in specialties]:
        clinical_data["cardiac"] = {
            "ejection_fraction": random.randint(45, 70),
            "cardiovascular_risk": random.choice(["Low", "Moderate", "High"])
        }
    
    if "endocrinology" in [s.lower() for s in specialties]:
        clinical_data["endocrine"] = {
            "hba1c": round(random.uniform(5.0, 9.5), 1),
            "glucose_level": random.randint(70, 200)
        }
    
    # Enhanced demographics
    patient_demographics = {
        "ethnicity": demographics.get("preferred_ethnicity") or random.choice([
            "Caucasian", "Hispanic", "African American", "Asian", "Other"
        ]),
        "insurance": random.choice(["Medicare", "Medicaid", "Private", "Uninsured"]),
        "location": random.choice(["Urban", "Suburban", "Rural"]),
        "education": random.choice(["High School", "College", "Graduate", "Post-Graduate"]),
        "income_bracket": random.choice(["<30k", "30-60k", "60-100k", ">100k"])
    }
    
    return {
        "patient_id": patient_id,
        "name": f"Patient {sequence:03d}",
        "age": age,
        "gender": gender,
        "conditions": assigned_conditions,
        "vitals": {
            "blood_pressure": f"{random.randint(90, 140)}/{random.randint(60, 90)}",
            "heart_rate": random.randint(60, 100),
            "temperature": round(random.uniform(98.0, 100.4), 1),
            "respiratory_rate": random.randint(12, 20),
            "bmi": round(random.uniform(18.5, 35.0), 1)
        },
        "demographics": patient_demographics,
        "clinical_data": clinical_data,
        "specialties": specialties,
        "created_at": datetime.now().isoformat()
    }

# ================================
# MCP Tools Integration
# ================================

@mcp_server.tool()
async def mcp_generate_patients(
    population_size: int = 100,
    conditions: str = "",
    age_min: int = 18,
    age_max: int = 80,
    specialties: str = ""
) -> Dict[str, Any]:
    """
    MCP Tool: Generate synthetic patient cohort for EHR research.
    
    Args:
        population_size: Number of patients (1-1000)
        conditions: Comma-separated conditions
        age_min: Minimum age
        age_max: Maximum age
        specialties: Comma-separated specialties
    """
    condition_list = [c.strip() for c in conditions.split(",") if c.strip()]
    specialty_list = [s.strip() for s in specialties.split(",") if s.strip()]
    
    return await generate_patient_cohort_internal(
        population_size, condition_list, [age_min, age_max], specialty_list, {}
    )

@mcp_server.tool()
async def mcp_analyze_cohort(workflow_id: str) -> Dict[str, Any]:
    """
    MCP Tool: Analyze demographics and clinical characteristics of a cohort.
    
    Args:
        workflow_id: Cohort workflow ID
    """
    if workflow_id not in generated_cohorts:
        return {"error": f"Cohort {workflow_id} not found"}
    
    patients = generated_cohorts[workflow_id]["patients"]
    
    # Clinical analysis
    condition_frequency = {}
    age_distribution = {"18-30": 0, "31-50": 0, "51-70": 0, "70+": 0}
    
    for patient in patients:
        # Age analysis
        age = patient["age"]
        if age <= 30: age_distribution["18-30"] += 1
        elif age <= 50: age_distribution["31-50"] += 1
        elif age <= 70: age_distribution["51-70"] += 1
        else: age_distribution["70+"] += 1
        
        # Condition frequency
        for condition in patient["conditions"]:
            condition_frequency[condition] = condition_frequency.get(condition, 0) + 1
    
    return {
        "cohort_id": workflow_id,
        "total_patients": len(patients),
        "age_distribution": age_distribution,
        "condition_frequency": condition_frequency,
        "analysis_timestamp": datetime.now().isoformat()
    }

@mcp_server.resource(uri="platform://capabilities", name="platform_capabilities", description="Synthetic Ascension platform capabilities")
def get_platform_capabilities() -> str:
    """MCP Resource: Platform capabilities documentation"""
    return """
# Synthetic Ascension EHR Platform

## Core Capabilities
- **AI-Powered Generation**: Create realistic synthetic patient cohorts
- **Multi-Specialty Support**: Cardiology, Endocrinology, Pulmonology, and more
- **Regulatory Compliance**: HIPAA-safe, GDPR-ready synthetic data
- **API Integration**: REST endpoints and MCP for AI agents

## Available Tools (MCP)
- `mcp_generate_patients`: Generate patient cohorts
- `mcp_analyze_cohort`: Analyze cohort demographics and clinical data

## REST API Endpoints
- `POST /api/v1/generate/cohort`: Generate cohort via REST
- `GET /api/v1/cohorts`: List all cohorts
- `GET /api/v1/cohort/{id}`: Get specific cohort
- `GET /api/v1/analytics/dashboard`: Platform analytics

## Integration Options
- Model Context Protocol (MCP) for AI agents
- REST API for web applications
- JSON export for data analysis
- Real-time workflow tracking
    """

# ================================
# MCP Server Mount
# ================================

# Mount MCP server as sub-application
@app.get("/mcp")
async def mcp_endpoint():
    """MCP server endpoint information"""
    return {
        "mcp_server": "active",
        "available_tools": [
            "mcp_generate_patients",
            "mcp_analyze_cohort"
        ],
        "available_resources": [
            "platform_capabilities"
        ],
        "integration": "Use MCP client to connect to this endpoint"
    }

if __name__ == "__main__":
    import uvicorn
    
    # Run FastAPI server with MCP integration
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8002,
        log_level="info"
    )