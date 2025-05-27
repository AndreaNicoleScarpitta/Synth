#!/usr/bin/env python3
"""
Comprehensive EHR Database Models
Supporting complete electronic health record structure as per healthcare standards
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from typing import Dict, List, Any, Optional
import os

Base = declarative_base()

class Patient(Base):
    """Core patient demographics and identifiers"""
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, index=True)
    medical_record_number = Column(String, unique=True, index=True)
    
    # Patient Demographics (Complete)
    full_name = Column(String)
    date_of_birth = Column(String)
    age = Column(Integer)
    sex = Column(String)
    gender_identity = Column(String)
    pronouns = Column(String)
    
    # Contact Information
    address = Column(JSON)  # street, city, state, zip, country
    phone = Column(String)
    email = Column(String)
    emergency_contact = Column(JSON)
    
    # Race/Ethnicity/Language
    race = Column(String)
    ethnicity = Column(String)
    primary_language = Column(String)
    
    # Insurance Information
    insurance_primary = Column(String)
    insurance_member_id = Column(String)
    insurance_group = Column(String)
    insurance_subscriber = Column(String)
    
    # Anthropometric Data
    weight_kg = Column(Float)
    height_cm = Column(Float)
    bmi = Column(Float)
    bmi_percentile = Column(Float)
    head_circumference_cm = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships to other EHR components will be defined after all classes

class ProblemList(Base):
    """Active diagnoses and chronic conditions with ICD-10 codes"""
    __tablename__ = "problem_list"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    
    condition = Column(String)
    icd10_code = Column(String)
    onset_date = Column(String)
    resolution_date = Column(String, nullable=True)
    status = Column(String)  # Active, Resolved, Chronic, Inactive
    severity = Column(String)  # Mild, Moderate, Severe
    certainty = Column(String)  # Confirmed, Suspected, Rule-out
    domain = Column(String)  # Cardiovascular, Respiratory, Psychiatric, etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="problems")

class Allergy(Base):
    """Medication, food, and environmental allergies with reactions"""
    __tablename__ = "allergies"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    
    allergen = Column(String)
    allergen_type = Column(String)  # Medication, Food, Environmental
    reaction = Column(Text)  # Rash, Anaphylaxis, Nausea, etc.
    severity = Column(String)  # Mild, Moderate, Severe, Life-threatening
    onset_date = Column(String)
    confirmation_status = Column(String)  # Confirmed, Suspected, Unconfirmed
    triage_recommendation = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="allergies")

class LabPanel(Base):
    """Laboratory test panels with LOINC codes and time-series results"""
    __tablename__ = "lab_panels"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    
    panel_name = Column(String)
    loinc_code = Column(String)
    ordered_date = Column(String)
    collected_date = Column(String)
    resulted_date = Column(String)
    ordering_provider = Column(String)
    status = Column(String)  # Pending, Final, Corrected, Cancelled
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="lab_panels")
    results = relationship("LabResult", back_populates="panel", cascade="all, delete-orphan")

class LabResult(Base):
    """Individual lab test results within panels"""
    __tablename__ = "lab_results"
    
    id = Column(Integer, primary_key=True, index=True)
    panel_id = Column(Integer, ForeignKey("lab_panels.id"))
    
    test_name = Column(String)
    value = Column(Float)
    unit = Column(String)
    reference_range = Column(String)
    flag = Column(String)  # H (High), L (Low), Critical, etc.
    
    panel = relationship("LabPanel", back_populates="results")

class Medication(Base):
    """Current and past medications with RxNorm codes"""
    __tablename__ = "medications"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    
    name = Column(String)
    rxnorm_code = Column(String)
    generic_name = Column(String)
    brand_name = Column(String)
    dosage = Column(String)
    dose_amount = Column(String)
    route = Column(String)  # PO, IV, IM, etc.
    frequency = Column(String)
    start_date = Column(String)
    stop_date = Column(String, nullable=True)
    prescriber = Column(String)
    indication = Column(Text)
    status = Column(String)  # Active, Discontinued, Held, Completed
    pharmacy = Column(String)
    last_filled = Column(String, nullable=True)
    quantity_dispensed = Column(String, nullable=True)
    refills_remaining = Column(Integer, nullable=True)
    reason_discontinued = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="medications")

class ImagingStudy(Base):
    """Radiology studies, echocardiograms, and diagnostic imaging"""
    __tablename__ = "imaging_studies"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    
    study_type = Column(String)
    modality = Column(String)  # X-ray, CT, MRI, Ultrasound, Echo
    study_date = Column(String)
    ordering_provider = Column(String)
    performing_technologist = Column(String)
    interpreting_radiologist = Column(String)
    status = Column(String)
    indication = Column(Text)
    technique = Column(Text)
    findings = Column(JSON)  # Structured findings
    impression = Column(Text)
    recommendations = Column(Text)
    comparison = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="imaging_studies")

class ClinicalEncounter(Base):
    """All clinical visits and encounters"""
    __tablename__ = "clinical_encounters"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    
    encounter_id = Column(String, unique=True)
    date = Column(String)
    time = Column(String)
    encounter_type = Column(String)  # Inpatient, Outpatient, Emergency, Telehealth
    department = Column(String)
    location = Column(String)
    
    # Provider Information
    attending_provider = Column(String)
    resident_provider = Column(String, nullable=True)
    nurse = Column(String, nullable=True)
    
    # Visit Details
    chief_complaint = Column(Text)
    reason_for_visit = Column(Text)
    duration = Column(String)
    
    # Assessment and Plan
    assessment = Column(Text)
    plan = Column(Text)
    follow_up = Column(Text)
    patient_education = Column(Text)
    
    # Administrative
    billing_codes = Column(JSON)
    next_appointment = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="encounters")
    vital_signs = relationship("VitalSigns", back_populates="encounter", cascade="all, delete-orphan")

class VitalSigns(Base):
    """Vital signs measurements during encounters"""
    __tablename__ = "vital_signs"
    
    id = Column(Integer, primary_key=True, index=True)
    encounter_id = Column(String, ForeignKey("clinical_encounters.encounter_id"))
    
    temperature_f = Column(Float)
    heart_rate = Column(Integer)
    blood_pressure_systolic = Column(Integer)
    blood_pressure_diastolic = Column(Integer)
    respiratory_rate = Column(Integer)
    oxygen_saturation = Column(Float)
    weight_kg = Column(Float)
    height_cm = Column(Float)
    pain_score = Column(Integer)
    
    measurement_time = Column(DateTime, default=datetime.utcnow)
    
    encounter = relationship("ClinicalEncounter", back_populates="vital_signs")

class Procedure(Base):
    """Surgical procedures and interventions"""
    __tablename__ = "procedures"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    
    procedure_name = Column(String)
    cpt_code = Column(String)
    procedure_date = Column(String)
    location = Column(String)
    surgeon_operator = Column(String)
    assistant = Column(String, nullable=True)
    anesthesia_type = Column(String)
    indication = Column(Text)
    procedure_details = Column(Text)
    complications = Column(Text)
    outcome = Column(Text)
    post_op_course = Column(Text)
    pathology_report = Column(Text, nullable=True)
    follow_up_required = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="procedures")

class Immunization(Base):
    """Vaccination records with manufacturer and lot tracking"""
    __tablename__ = "immunizations"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    
    vaccine_name = Column(String)
    date_administered = Column(String)
    dose_number = Column(String)
    manufacturer = Column(String)
    lot_number = Column(String)
    route = Column(String)  # IM, SubQ, Intranasal, etc.
    site = Column(String)  # Left deltoid, Right thigh, etc.
    administered_by = Column(String)
    clinic_location = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="immunizations")

class FamilyHistory(Base):
    """Family medical history and genetic information"""
    __tablename__ = "family_history"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    
    relationship = Column(String)  # Mother, Father, Maternal Grandmother, etc.
    condition = Column(String)
    age_of_onset = Column(Integer, nullable=True)
    current_status = Column(String)  # Living, Deceased, Unknown
    family_side = Column(String)  # Maternal, Paternal
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="family_history")

class AdvanceDirective(Base):
    """Advance directives and legal documents"""
    __tablename__ = "advance_directives"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    
    code_status = Column(String)  # Full Code, DNR, DNI, etc.
    healthcare_proxy = Column(String)
    emergency_contact_primary = Column(String)
    emergency_contact_secondary = Column(String, nullable=True)
    special_instructions = Column(Text)
    organ_donation_status = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CareTeamMember(Base):
    """Multidisciplinary care team members"""
    __tablename__ = "care_team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    
    provider_name = Column(String)
    specialty = Column(String)
    role = Column(String)  # Primary Care, Specialist, Case Manager, Nurse
    phone = Column(String)
    email = Column(String, nullable=True)
    last_contact = Column(String)
    is_primary_care = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="care_team_members")

class ClinicalNote(Base):
    """Clinical documentation and progress notes"""
    __tablename__ = "clinical_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    encounter_id = Column(String, ForeignKey("clinical_encounters.encounter_id"), nullable=True)
    
    note_type = Column(String)  # Progress Note, Consultation, Discharge Summary, etc.
    author = Column(String)
    note_date = Column(String)
    subject = Column(String)
    note_text = Column(Text)
    
    # SOAP Format
    subjective = Column(Text, nullable=True)
    objective = Column(Text, nullable=True)
    assessment = Column(Text, nullable=True)
    plan = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    """HIPAA-compliant audit trail"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    
    user_id = Column(String)
    action = Column(String)  # CREATE, READ, UPDATE, DELETE
    resource_type = Column(String)  # Patient, LabResult, Medication, etc.
    resource_id = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)
    user_agent = Column(String)
    
# Database initialization and utilities
def get_database_url():
    """Get database URL from environment or use default"""
    return os.getenv('DATABASE_URL', 'postgresql://localhost:5432/synthetic_ehr')

def create_database_engine():
    """Create SQLAlchemy engine with proper configuration"""
    database_url = get_database_url()
    engine = create_engine(
        database_url,
        echo=False,  # Set to True for SQL debugging
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True
    )
    return engine

def create_all_tables():
    """Create all database tables"""
    engine = create_database_engine()
    Base.metadata.create_all(bind=engine)
    return engine

def get_db_session():
    """Get database session"""
    engine = create_database_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

# Export all models for import
__all__ = [
    'Patient', 'ProblemList', 'Allergy', 'LabPanel', 'LabResult', 'Medication',
    'ImagingStudy', 'ClinicalEncounter', 'VitalSigns', 'Procedure', 'Immunization',
    'FamilyHistory', 'AdvanceDirective', 'CareTeamMember', 'ClinicalNote', 'AuditLog',
    'Base', 'create_all_tables', 'get_db_session'
]