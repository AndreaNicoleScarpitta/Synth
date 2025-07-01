# agents/generator.py

import sys
import uuid
from datetime import datetime
from typing import Dict, Any

from sqlmodel import Session
from db import engine
from models.models import GenerationJob, AgentRun, Patient, Encounter
from utils.base_agent import BaseAgent

class PatientEncounterGenerator(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        condition = input_data.get("condition", "unknown")
        count = input_data.get("count", 1)

        logs = []
        job_id = str(uuid.uuid4())

        with Session(engine) as session:
            job = GenerationJob(
                id=job_id,
                request_payload={"condition": condition, "count": count},
                status="pending",
                started_at=datetime.utcnow(),
                ended_at=None,
            )
            session.add(job)
            session.commit()
            logs.append(f"Created GenerationJob {job.id}")

            for i in range(count):
                record = {
                    "demographics": {
                        "age": str(30 + i),
                        "gender": "M" if i % 2 == 0 else "F"
                    },
                    "encounter": {
                        "type": "outpatient",
                        "period_start": datetime.utcnow().isoformat(),
                        "location": {"clinic": "A", "room": str(100 + i)},
                        "reason": condition,
                    }
                }

                agent_run = AgentRun(
                    job_id=job.id,
                    agent_name="PatientEncounterGenerator",
                    input={"condition": condition, "iteration": i},
                    output=record,
                    ran_at=datetime.utcnow()
                )
                session.add(agent_run)
                session.commit()
                logs.append(f"Logged AgentRun {agent_run.id}")

                p = Patient(demographics=record["demographics"])
                session.add(p)
                session.commit()
                logs.append(f"Inserted Patient {p.id}")

                enc = record["encounter"]
                e = Encounter(
                    patient_id=p.id,
                    type=enc["type"],
                    period_start=datetime.fromisoformat(enc["period_start"]),
                    location=enc["location"],
                    reason=enc["reason"],
                    created_at=datetime.utcnow()
                )
                session.add(e)
                session.commit()
                logs.append(f"Inserted Encounter {e.id}")

            job.status = "completed"
            job.ended_at = datetime.utcnow()
            session.add(job)
            session.commit()
            logs.append(f"Job {job.id} completed")

        return {
            "output": {"job_id": job.id, "patient_count": count},
            "log": "\n".join(logs)
        }

# CLI entrypoint — preserved for compatibility
def generate_patients_and_encounters(condition: str, count: int):
    agent = PatientEncounterGenerator()
    return agent.run({"condition": condition, "count": count})

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        cond = sys.argv[1]
        cnt = int(sys.argv[2])
    else:
        cond, cnt = "hypertension", 3

    result = generate_patients_and_encounters(cond, cnt)
    print(result["log"])
