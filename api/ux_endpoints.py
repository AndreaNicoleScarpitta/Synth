"""
UX-Focused REST API Endpoints
Frontend-optimized endpoints for user interface components
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

# Response Models for UX
class DashboardSummary(BaseModel):
    """Dashboard overview data"""
    total_jobs: int = Field(description="Total number of generation jobs")
    active_jobs: int = Field(description="Currently running jobs")
    completed_jobs: int = Field(description="Successfully completed jobs")
    total_patients_generated: int = Field(description="Total synthetic patients created")
    system_status: str = Field(description="Overall system health status")
    last_updated: datetime = Field(description="Last update timestamp")

class JobCard(BaseModel):
    """Job card data for UI display"""
    job_id: str = Field(description="Unique job identifier")
    job_name: str = Field(description="Human-readable job name")
    status: str = Field(description="Current job status", examples=["running", "completed", "failed"])
    progress: float = Field(description="Job completion percentage (0-100)")
    current_phase: Optional[str] = Field(description="Current execution phase")
    started_at: datetime = Field(description="Job start timestamp")
    estimated_completion: Optional[datetime] = Field(description="Estimated completion time")
    population_size: int = Field(description="Number of patients being generated")
    condition: str = Field(description="Primary medical condition")

class AgentStatusCard(BaseModel):
    """Agent status for monitoring UI"""
    agent_name: str = Field(description="Agent display name")
    agent_type: str = Field(description="Agent category")
    status: str = Field(description="Current agent status")
    last_execution: Optional[datetime] = Field(description="Last execution timestamp")
    success_rate: float = Field(description="Success rate percentage")
    avg_execution_time: float = Field(description="Average execution time in seconds")
    total_executions: int = Field(description="Total number of executions")

class SystemMetrics(BaseModel):
    """System performance metrics"""
    cpu_usage: float = Field(description="CPU utilization percentage")
    memory_usage: float = Field(description="Memory utilization percentage") 
    active_agents: int = Field(description="Number of active agents")
    queue_depth: int = Field(description="Number of queued jobs")
    avg_response_time: float = Field(description="Average API response time in ms")
    system_uptime: str = Field(description="System uptime duration")

class PatientPreview(BaseModel):
    """Patient data preview for UI"""
    patient_id: str = Field(description="Unique patient identifier")
    demographics: Dict[str, Any] = Field(description="Basic demographic information")
    conditions: List[str] = Field(description="List of medical conditions")
    last_encounter: Optional[str] = Field(description="Most recent healthcare encounter")
    data_quality_score: float = Field(description="Data quality assessment (0-100)")
    generated_at: datetime = Field(description="Generation timestamp")

class WorkflowTemplate(BaseModel):
    """Workflow template for UI selection"""
    template_id: str = Field(description="Unique template identifier")
    name: str = Field(description="Template display name")
    description: str = Field(description="Template description")
    category: str = Field(description="Template category")
    complexity: str = Field(description="Complexity level", examples=["beginner", "intermediate", "advanced"])
    estimated_runtime: str = Field(description="Estimated execution time")
    agent_count: int = Field(description="Number of agents involved")
    default_population_size: int = Field(description="Default patient population size")
    supported_conditions: List[str] = Field(description="Supported medical conditions")

class NotificationMessage(BaseModel):
    """System notification for UI"""
    notification_id: str = Field(description="Unique notification identifier")
    type: str = Field(description="Notification type", examples=["info", "warning", "error", "success"])
    title: str = Field(description="Notification title")
    message: str = Field(description="Notification content")
    timestamp: datetime = Field(description="Notification timestamp")
    read: bool = Field(description="Read status")
    action_url: Optional[str] = Field(description="Optional action URL")

# UX API Router
def create_ux_router():
    """Create UX-focused API router"""
    
    router = FastAPI(
        title="Synthetic Ascension UX API",
        description="Frontend-optimized endpoints for user interface components",
        version="3.0.0"
    )
    
    # Dashboard Endpoints
    @router.get("/api/ux/dashboard/summary", response_model=DashboardSummary)
    async def get_dashboard_summary():
        """Get dashboard overview data for main UI"""
        return DashboardSummary(
            total_jobs=156,
            active_jobs=3,
            completed_jobs=142,
            total_patients_generated=15600,
            system_status="healthy",
            last_updated=datetime.utcnow()
        )
    
    @router.get("/api/ux/dashboard/recent-jobs", response_model=List[JobCard])
    async def get_recent_jobs(limit: int = Query(5, description="Number of recent jobs to return")):
        """Get recent jobs for dashboard display"""
        return [
            JobCard(
                job_id=str(uuid.uuid4()),
                job_name="Diabetes Cohort Generation",
                status="running",
                progress=65.0,
                current_phase="Clinical Journey Generation",
                started_at=datetime.utcnow(),
                estimated_completion=datetime.utcnow(),
                population_size=500,
                condition="diabetes"
            ),
            JobCard(
                job_id=str(uuid.uuid4()),
                job_name="Hypertension Study",
                status="completed",
                progress=100.0,
                current_phase="Completed",
                started_at=datetime.utcnow(),
                estimated_completion=None,
                population_size=250,
                condition="hypertension"
            )
        ]
    
    return router