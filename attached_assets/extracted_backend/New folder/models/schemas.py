# models/schemas.py

from pydantic import BaseModel

class AgentRequest(BaseModel):
    condition: str
    count: int
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class AgentRunOut(BaseModel):
    id: str
    input: Dict[str, Any]
    output: Dict[str, Any]
    ran_at: datetime

class JobStatusOut(BaseModel):
    job_id: str
    request_payload: Dict[str, Any]
    status: str
    started_at: datetime
    ended_at: Optional[datetime]
    runs: List[AgentRunOut]
