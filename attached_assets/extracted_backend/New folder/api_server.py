from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define the input model
class AgentRequest(BaseModel):
    condition: str
    count: int

@app.post("/run-agent")
async def run_agent(request: AgentRequest):
    condition = request.condition
    count = request.count

    def generate_record(index):
        return {
            "patient_id": f"{condition[:3].upper()}-{index}",
            "condition": condition,
            "age_weeks": random.randint(10, 22),
            "NT_mm": round(random.uniform(3.5, 8.0), 1),
            "genetic_result": random.choice(["Normal", "Turner", "Trisomy 21"]),
            "outcome": random.choice(["Live Birth", "Termination", "Stillbirth"]),
        }

    data = [generate_record(i) for i in range(count)]
    return {"cohort": data}
