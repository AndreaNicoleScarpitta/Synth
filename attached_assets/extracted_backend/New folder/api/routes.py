from fastapi import APIRouter, HTTPException
from models.schemas import AgentRequest, JobStatusOut, AgentRunOut
from agents.generator import generate_patients_and_encounters
from sqlmodel import Session, select
from db import engine
from models.models import GenerationJob, AgentRun
import uuid

router = APIRouter()

@router.post("/generate")
def generate_endpoint(req: AgentRequest):
    try:
        job_id = generate_patients_and_encounters(req.condition, req.count)
        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs/{job_id}", response_model=JobStatusOut)
def get_job_status(job_id: str):
    try:
        job_uuid = uuid.UUID(job_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    with Session(engine) as session:
        job = session.get(GenerationJob, job_uuid)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        runs = session.exec(
            select(AgentRun).where(AgentRun.job_id == job_uuid)
        ).all()

    # serialize AgentRun into Pydantic models
    runs_out = [
        AgentRunOut(
            id=str(r.id),
            input=r.input,
            output=r.output,
            ran_at=r.ran_at
        )
        for r in runs
    ]

    return JobStatusOut(
        job_id=str(job.id),
        request_payload=job.request_payload,
        status=job.status,
        started_at=job.started_at,
        ended_at=job.ended_at,
        runs=runs_out
    )
