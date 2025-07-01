# test_encounter.py

import uuid
from datetime import datetime
from sqlmodel import Session, select
from db import engine
from models.models import Encounter

# 1) Insert a new Encounter for your existing patient
with Session(engine) as session:
    e = Encounter(
        patient_id=uuid.UUID("89b41776-60a6-43d7-be6a-84e71dca88a5"),
        type="outpatient",
        period_start=datetime.utcnow(),
        location={"clinic": "A", "room": "101"},
        reason="routine check",
    )
    session.add(e)
    session.commit()
    print("Inserted encounter:", e.id)

# 2) Fetch and print all Encounters
with Session(engine) as session:
    encounters = session.exec(select(Encounter)).all()
    print("All encounters:", encounters)
