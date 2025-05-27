"""
Multi-layered database models for synthetic EHR system
Supports SQL (PostgreSQL), Document storage, and audit trails
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime
import uuid
import os

Base = declarative_base()

# Core EHR Tables (SQL Database)
class Patient(Base):
    __tablename__ = 'patients'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(String, unique=True, nullable=False)
    age = Column(Integer)
    gender = Column(String(50))
    ethnicity = Column(String(100))
    synthetic_cohort_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    encounters = relationship("Encounter", back_populates="patient")
    lab_results = relationship("LabResult", back_populates="patient")
    medications = relationship("Medication", back_populates="patient")
    conditions = relationship("Condition", back_populates="patient")
    clinical_notes = relationship("ClinicalNote", back_populates="patient")

class Encounter(Base):
    __tablename__ = 'encounters'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'))
    encounter_date = Column(DateTime)
    encounter_type = Column(String(100))  # outpatient, inpatient, emergency
    chief_complaint = Column(Text)
    diagnosis_codes = Column(ARRAY(String))  # ICD-10 codes
    
    patient = relationship("Patient", back_populates="encounters")

class LabResult(Base):
    __tablename__ = 'lab_results'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'))
    test_name = Column(String(200))
    value = Column(Float)
    unit = Column(String(50))
    reference_range = Column(String(100))
    abnormal_flag = Column(String(10))
    collection_date = Column(DateTime)
    
    patient = relationship("Patient", back_populates="lab_results")

class Medication(Base):
    __tablename__ = 'medications'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'))
    medication_name = Column(String(200))
    dosage = Column(String(100))
    frequency = Column(String(100))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    indication = Column(String(200))
    
    patient = relationship("Patient", back_populates="medications")

class Condition(Base):
    __tablename__ = 'conditions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'))
    condition_name = Column(String(200))
    icd10_code = Column(String(20))
    onset_date = Column(DateTime)
    status = Column(String(50))  # active, resolved, chronic
    severity = Column(String(50))
    
    patient = relationship("Patient", back_populates="conditions")

class ClinicalNote(Base):
    __tablename__ = 'clinical_notes'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'))
    note_type = Column(String(100))  # progress, discharge, consult
    note_text = Column(Text)
    author = Column(String(100))
    created_date = Column(DateTime)
    
    patient = relationship("Patient", back_populates="clinical_notes")

# Audit and Agent Tracking Tables
class AgentExecution(Base):
    __tablename__ = 'agent_executions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(String, unique=True, nullable=False)
    agent_name = Column(String(100))
    task_type = Column(String(100))
    input_data = Column(JSON)
    output_data = Column(JSON)
    status = Column(String(50))  # running, completed, failed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    
    # Relationships
    audit_logs = relationship("AuditLog", back_populates="agent_execution")

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), ForeignKey('agent_executions.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String(20))  # INFO, WARNING, ERROR
    message = Column(Text)
    meta_data = Column(JSON)
    
    agent_execution = relationship("AgentExecution", back_populates="audit_logs")

class WorkflowState(Base):
    __tablename__ = 'workflow_states'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(String, unique=True, nullable=False)
    current_step = Column(String(100))
    state_data = Column(JSON)
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# Research and Knowledge Base Tables
class LiteraturePaper(Base):
    __tablename__ = 'literature_papers'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text)
    authors = Column(ARRAY(String))
    abstract = Column(Text)
    doi = Column(String(100))
    pubmed_id = Column(String(50))
    publication_date = Column(DateTime)
    journal = Column(String(200))
    keywords = Column(ARRAY(String))
    full_text_url = Column(String(500))
    indexed_at = Column(DateTime, default=datetime.utcnow)

class WebScrapedContent(Base):
    __tablename__ = 'web_scraped_content'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text)
    content = Column(Text)
    url = Column(String(500))
    source_name = Column(String(200))
    content_hash = Column(String(64), unique=True)
    trustworthiness_score = Column(Float)
    keywords = Column(ARRAY(String))
    scraped_at = Column(DateTime, default=datetime.utcnow)

# Statistical Validation Results
class ValidationResult(Base):
    __tablename__ = 'validation_results'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cohort_id = Column(String, nullable=False)
    validation_type = Column(String(100))  # statistical, medical, literature
    overall_score = Column(Float)
    detailed_results = Column(JSON)
    recommendations = Column(ARRAY(String))
    validated_at = Column(DateTime, default=datetime.utcnow)

# Database Engine and Session Management
class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Create all tables in the database"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get a database session"""
        return self.SessionLocal()
    
    def drop_tables(self):
        """Drop all tables (use with caution)"""
        Base.metadata.drop_all(bind=self.engine)

# Context manager for database sessions
class DatabaseSession:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.session = None
    
    def __enter__(self):
        self.session = self.db_manager.get_session()
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

# Initialize database manager (singleton pattern)
db_manager = DatabaseManager()