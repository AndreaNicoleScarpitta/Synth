from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load .env file from the project root
load_dotenv()

def get_engine():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in .env")
    return create_engine(db_url, echo=False)
