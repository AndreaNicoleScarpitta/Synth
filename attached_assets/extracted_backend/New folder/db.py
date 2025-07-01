# db.py
import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()  # reads .env

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """Create all tables in the database."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Yields a database session (for FastAPI or scripts)."""
    with Session(engine) as session:
        yield session
