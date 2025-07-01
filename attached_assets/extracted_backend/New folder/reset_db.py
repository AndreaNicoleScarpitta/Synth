# reset_db.py

from sqlmodel import SQLModel
from db import engine
import models.models   # ensure all models are loaded

# Drop all existing tables…
SQLModel.metadata.drop_all(engine)
# …and recreate them from your models
SQLModel.metadata.create_all(engine)

print("Dropped and recreated all tables.")
