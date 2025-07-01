import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator.db import get_engine
from sqlmodel import SQLModel
from models.models import (
    Patient, Encounter, Condition, Observation,
    GenerationJob, AgentRun,
    TracerRun, AgentExecution
)


def main():
    engine = get_engine()
    print("🛠️ Creating all tables in Postgres...")
    SQLModel.metadata.create_all(engine)
    print("✅ All tables created successfully.")

if __name__ == "__main__":
    main()
