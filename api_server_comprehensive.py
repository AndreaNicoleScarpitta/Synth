#!/usr/bin/env python3
"""
Comprehensive EHR API Server
Supporting all clinical modalities with proper database backend
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import and_, or_, desc
from typing import List, Dict, Any, Optional
import os
import json
import logging
from datetime import datetime, timedelta
import random

# Import the comprehensive EHR models
from models.comprehensive_ehr_models import (
    Patient, ProblemList, Allergy, LabPanel, LabResult, Medication,
    ImagingStudy, ClinicalEncounter, VitalSigns, Procedure, Immunization,
    FamilyHistory, AdvanceDirective, CareTeamMember, ClinicalNote, AuditLog,
    create_all_tables, get_db_session
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Synthetic Ascension EHR API",
    description="Comprehensive Electronic Health Record API with full clinical modalities",
    version="2.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    try:
        create_all_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

# ============================================================================
# PATIENT ENDPOINTS
# ============================================================================

@app.get("/api/patients")
async def get_all_patients(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get all patients with pagination"""
    try:
        patients = db.query(Patient).offset(offset).limit(limit).all()
        total_count = db.query(Patient).count()
        
        return {
            "patients": [patient.to_dict() for patient in patients],
            "total_count": total_count,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error fetching patients: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/patients/{patient_id}")
async def get_patient_complete_record(
    patient_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get complete patient record with all clinical modalities"""
    try:
        # Fetch patient with all related data
        patient = db.query(Patient).options(
            selectinload(Patient.problems),
            selectinload(Patient.allergies),
            selectinload(Patient.lab_panels).selectinload(LabPanel.results),
            selectinload(Patient.medications),
            selectinload(Patient.imaging_studies),
            selectinload(Patient.encounters).selectinload(ClinicalEncounter.vital_signs),
            selectinload(Patient.procedures),
            selectinload(Patient.immunizations),
            selectinload(Patient.family_history),
            selectinload(Patient.care_team_members)
        ).filter(Patient.patient_id == patient_id).first()
        
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Build comprehensive patient record
        complete_record = {
            "patient_id": patient.patient_id,
            "demographics": {
                "full_name": patient.full_name,
                "date_of_birth": patient.date_of_birth,
                "age": patient.age,
                "sex": patient.sex,
                "gender_identity": patient.gender_identity,
                "pronouns": patient.pronouns,
                "address": patient.address,
                "phone": patient.phone,
                "email": patient.email,
                "emergency_contact": patient.emergency_contact,
                "race_ethnicity": {
                    "race": patient.race,
                    "ethnicity": patient.ethnicity,
                    "primary_language": patient.primary_language
                },
                "insurance": {
                    "primary": patient.insurance_primary,
                    "member_id": patient.insurance_member_id,
                    "group_number": patient.insurance_group,
                    "subscriber": patient.insurance_subscriber
                },
                "anthropometrics": {
                    "weight_kg": patient.weight_kg,
                    "height_cm": patient.height_cm,
                    "bmi": patient.bmi,
                    "bmi_percentile": patient.bmi_percentile,
                    "head_circumference_cm": patient.head_circumference_cm
                },
                "medical_record_number": patient.medical_record_number
            },
            "problem_list": {
                "active_diagnoses": [
                    {
                        "condition": problem.condition,
                        "icd10_code": problem.icd10_code,
                        "onset_date": problem.onset_date,
                        "status": problem.status,
                        "severity": problem.severity,
                        "certainty": problem.certainty,
                        "domain": problem.domain
                    }
                    for problem in patient.problems if problem.status == "Active"
                ]
            },
            "allergies_adverse_reactions": [
                {
                    "allergen": allergy.allergen,
                    "type": allergy.allergen_type,
                    "reaction": allergy.reaction,
                    "severity": allergy.severity,
                    "onset_date": allergy.onset_date,
                    "status": allergy.confirmation_status,
                    "triage_recommendation": allergy.triage_recommendation
                }
                for allergy in patient.allergies
            ],
            "laboratory_results": {
                "panels": [
                    {
                        "panel_name": panel.panel_name,
                        "loinc_code": panel.loinc_code,
                        "ordered_date": panel.ordered_date,
                        "collected_date": panel.collected_date,
                        "resulted_date": panel.resulted_date,
                        "ordering_provider": panel.ordering_provider,
                        "status": panel.status,
                        "results": [
                            {
                                "test": result.test_name,
                                "value": result.value,
                                "unit": result.unit,
                                "reference_range": result.reference_range,
                                "flag": result.flag
                            }
                            for result in panel.results
                        ]
                    }
                    for panel in patient.lab_panels
                ]
            },
            "medication_history": {
                "current_medications": [
                    {
                        "name": med.name,
                        "rxnorm_code": med.rxnorm_code,
                        "generic_name": med.generic_name,
                        "brand_name": med.brand_name,
                        "dosage": med.dosage,
                        "dose_amount": med.dose_amount,
                        "route": med.route,
                        "frequency": med.frequency,
                        "start_date": med.start_date,
                        "prescriber": med.prescriber,
                        "indication": med.indication,
                        "status": med.status,
                        "pharmacy": med.pharmacy,
                        "last_filled": med.last_filled,
                        "quantity_dispensed": med.quantity_dispensed,
                        "refills_remaining": med.refills_remaining
                    }
                    for med in patient.medications if med.status == "Active"
                ],
                "discontinued_medications": [
                    {
                        "name": med.name,
                        "rxnorm_code": med.rxnorm_code,
                        "start_date": med.start_date,
                        "stop_date": med.stop_date,
                        "reason_discontinued": med.reason_discontinued,
                        "prescriber": med.prescriber
                    }
                    for med in patient.medications if med.status == "Discontinued"
                ]
            },
            "imaging_diagnostics": {
                "studies": [
                    {
                        "study_type": study.study_type,
                        "modality": study.modality,
                        "study_date": study.study_date,
                        "ordering_provider": study.ordering_provider,
                        "performing_technologist": study.performing_technologist,
                        "interpreting_radiologist": study.interpreting_radiologist,
                        "status": study.status,
                        "indication": study.indication,
                        "technique": study.technique,
                        "findings": study.findings,
                        "impression": study.impression,
                        "recommendations": study.recommendations,
                        "comparison": study.comparison
                    }
                    for study in patient.imaging_studies
                ]
            },
            "clinical_encounters": {
                "visits": [
                    {
                        "encounter_id": encounter.encounter_id,
                        "date": encounter.date,
                        "time": encounter.time,
                        "type": encounter.encounter_type,
                        "department": encounter.department,
                        "location": encounter.location,
                        "provider": {
                            "attending": encounter.attending_provider,
                            "resident": encounter.resident_provider,
                            "nurse": encounter.nurse
                        },
                        "chief_complaint": encounter.chief_complaint,
                        "reason_for_visit": encounter.reason_for_visit,
                        "vital_signs": {
                            vitals.measurement_time.isoformat(): {
                                "temperature": f"{vitals.temperature_f}°F",
                                "heart_rate": f"{vitals.heart_rate} bpm",
                                "blood_pressure": f"{vitals.blood_pressure_systolic}/{vitals.blood_pressure_diastolic} mmHg",
                                "respiratory_rate": f"{vitals.respiratory_rate} breaths/min",
                                "oxygen_saturation": f"{vitals.oxygen_saturation}%",
                                "weight": f"{vitals.weight_kg} kg",
                                "height": f"{vitals.height_cm} cm",
                                "pain_score": f"{vitals.pain_score}/10"
                            }
                            for vitals in encounter.vital_signs
                        },
                        "assessment_plan": {
                            "assessment": encounter.assessment,
                            "plan": encounter.plan,
                            "follow_up": encounter.follow_up,
                            "patient_education": encounter.patient_education
                        },
                        "duration": encounter.duration,
                        "billing_codes": encounter.billing_codes,
                        "next_appointment": encounter.next_appointment
                    }
                    for encounter in patient.encounters
                ]
            },
            "procedures_surgeries": {
                "procedures": [
                    {
                        "procedure_name": proc.procedure_name,
                        "cpt_code": proc.cpt_code,
                        "date": proc.procedure_date,
                        "location": proc.location,
                        "surgeon_operator": proc.surgeon_operator,
                        "assistant": proc.assistant,
                        "anesthesia_type": proc.anesthesia_type,
                        "indication": proc.indication,
                        "procedure_details": proc.procedure_details,
                        "complications": proc.complications,
                        "outcome": proc.outcome,
                        "post_op_course": proc.post_op_course,
                        "pathology": proc.pathology_report,
                        "follow_up_required": proc.follow_up_required
                    }
                    for proc in patient.procedures
                ]
            },
            "immunization_records": {
                "vaccinations": [
                    {
                        "vaccine": imm.vaccine_name,
                        "date_administered": imm.date_administered,
                        "dose_number": imm.dose_number,
                        "manufacturer": imm.manufacturer,
                        "lot_number": imm.lot_number,
                        "route": imm.route,
                        "site": imm.site,
                        "administered_by": imm.administered_by,
                        "clinic": imm.clinic_location
                    }
                    for imm in patient.immunizations
                ]
            },
            "family_history": {
                "maternal": [
                    {
                        "relationship": fh.relationship,
                        "condition": fh.condition,
                        "age_of_onset": fh.age_of_onset,
                        "status": fh.current_status
                    }
                    for fh in patient.family_history if fh.family_side == "Maternal"
                ],
                "paternal": [
                    {
                        "relationship": fh.relationship,
                        "condition": fh.condition,
                        "age_of_onset": fh.age_of_onset,
                        "status": fh.current_status
                    }
                    for fh in patient.family_history if fh.family_side == "Paternal"
                ]
            },
            "care_team": {
                "primary_care": next((
                    {
                        "provider": member.provider_name,
                        "role": member.role,
                        "phone": member.phone,
                        "last_contact": member.last_contact
                    }
                    for member in patient.care_team_members if member.is_primary_care
                ), None),
                "specialists": [
                    {
                        "provider": member.provider_name,
                        "specialty": member.specialty,
                        "phone": member.phone,
                        "role": member.role,
                        "last_contact": member.last_contact
                    }
                    for member in patient.care_team_members if not member.is_primary_care
                ]
            }
        }
        
        return complete_record
        
    except Exception as e:
        logger.error(f"Error fetching patient {patient_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/patients")
async def create_patient(
    patient_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """Create a new patient record"""
    try:
        # Create patient
        new_patient = Patient(
            patient_id=patient_data.get("patient_id"),
            medical_record_number=patient_data.get("medical_record_number"),
            full_name=patient_data.get("full_name"),
            date_of_birth=patient_data.get("date_of_birth"),
            age=patient_data.get("age"),
            sex=patient_data.get("sex"),
            gender_identity=patient_data.get("gender_identity"),
            pronouns=patient_data.get("pronouns"),
            address=patient_data.get("address"),
            phone=patient_data.get("phone"),
            email=patient_data.get("email"),
            emergency_contact=patient_data.get("emergency_contact"),
            race=patient_data.get("race"),
            ethnicity=patient_data.get("ethnicity"),
            primary_language=patient_data.get("primary_language"),
            insurance_primary=patient_data.get("insurance_primary"),
            insurance_member_id=patient_data.get("insurance_member_id"),
            insurance_group=patient_data.get("insurance_group"),
            insurance_subscriber=patient_data.get("insurance_subscriber"),
            weight_kg=patient_data.get("weight_kg"),
            height_cm=patient_data.get("height_cm"),
            bmi=patient_data.get("bmi"),
            bmi_percentile=patient_data.get("bmi_percentile"),
            head_circumference_cm=patient_data.get("head_circumference_cm")
        )
        
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
        
        return {"message": "Patient created successfully", "patient_id": new_patient.patient_id}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating patient: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# ============================================================================
# SYNTHETIC DATA GENERATION ENDPOINTS
# ============================================================================

@app.post("/api/generate-synthetic-cohort")
async def generate_synthetic_cohort(
    cohort_size: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Generate a synthetic patient cohort with complete EHR data"""
    try:
        generated_patients = []
        
        for i in range(cohort_size):
            patient_id = f"CHD-2024-{str(i+1).zfill(3)}"
            
            # Generate synthetic patient with comprehensive data
            synthetic_patient = await generate_comprehensive_synthetic_patient(patient_id, db)
            generated_patients.append(synthetic_patient)
        
        return {
            "message": f"Successfully generated {cohort_size} synthetic patients",
            "cohort_size": cohort_size,
            "patients": generated_patients
        }
        
    except Exception as e:
        logger.error(f"Error generating synthetic cohort: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def generate_comprehensive_synthetic_patient(patient_id: str, db: Session) -> Dict[str, Any]:
    """Generate a single comprehensive synthetic patient with all EHR modalities"""
    # Seed random number generator for reproducible results
    random.seed(hash(patient_id) % 2**32)
    
    age = random.randint(1, 18)
    sex = random.choice(['Male', 'Female'])
    
    # Create patient demographics
    patient = Patient(
        patient_id=patient_id,
        medical_record_number=f"MRN-{random.randint(100000, 999999)}",
        full_name=f"Patient {patient_id.split('-')[2]}",
        date_of_birth=(datetime.now() - timedelta(days=age*365.25)).strftime("%Y-%m-%d"),
        age=age,
        sex=sex,
        gender_identity=sex,
        pronouns="He/Him" if sex == "Male" else "She/Her",
        address={
            "street": f"{random.randint(1, 9999)} Medical Center Dr",
            "city": "Children's Hospital City",
            "state": "CA",
            "zip": "90210"
        },
        phone=f"(555) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
        email=f"guardian.{patient_id.lower()}@email.com",
        emergency_contact={
            "name": "Parent/Guardian",
            "phone": f"(555) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
        },
        race=random.choice(['White', 'Black or African American', 'Asian', 'American Indian/Alaska Native']),
        ethnicity=random.choice(['Not Hispanic or Latino', 'Hispanic or Latino']),
        primary_language='English',
        insurance_primary='Pediatric Health Plan',
        insurance_member_id=f"PHP{random.randint(100000, 999999)}",
        insurance_group='GRP001',
        insurance_subscriber='Parent/Guardian',
        weight_kg=round(15 + random.random() * 45, 1),
        height_cm=round(80 + random.random() * 100),
        bmi=round(random.uniform(14, 25), 1),
        bmi_percentile=random.randint(5, 95),
        head_circumference_cm=round(35 + random.random() * 15) if age < 3 else None
    )
    
    db.add(patient)
    db.commit()
    db.refresh(patient)
    
    # Add comprehensive clinical data
    await add_synthetic_clinical_data(patient, db)
    
    return {"patient_id": patient_id, "status": "generated"}

async def add_synthetic_clinical_data(patient: Patient, db: Session):
    """Add comprehensive synthetic clinical data for a patient"""
    
    # Add problem list
    cardiac_conditions = [
        ("Tetralogy of Fallot", "Q21.3"),
        ("Ventricular Septal Defect", "Q21.0"),
        ("Atrial Septal Defect", "Q21.1"),
        ("Hypoplastic Left Heart Syndrome", "Q23.4")
    ]
    
    condition, icd_code = random.choice(cardiac_conditions)
    problem = ProblemList(
        patient_id=patient.patient_id,
        condition=condition,
        icd10_code=icd_code,
        onset_date=(datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
        status="Active",
        severity=random.choice(["Mild", "Moderate", "Severe"]),
        certainty="Confirmed",
        domain="Cardiovascular"
    )
    db.add(problem)
    
    # Add allergy
    allergy = Allergy(
        patient_id=patient.patient_id,
        allergen="Penicillin",
        allergen_type="Medication",
        reaction="Rash, Hives",
        severity="Moderate",
        onset_date=(datetime.now() - timedelta(days=random.randint(100, 1000))).strftime("%Y-%m-%d"),
        confirmation_status="Confirmed",
        triage_recommendation="Avoid - use alternative antibiotics"
    )
    db.add(allergy)
    
    # Add lab panel
    lab_panel = LabPanel(
        patient_id=patient.patient_id,
        panel_name="Complete Blood Count with Differential",
        loinc_code="58410-2",
        ordered_date=(datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
        collected_date=(datetime.now() - timedelta(days=random.randint(1, 28))).strftime("%Y-%m-%d"),
        resulted_date=(datetime.now() - timedelta(days=random.randint(1, 27))).strftime("%Y-%m-%d"),
        ordering_provider="Dr. Sarah Chen, Pediatric Cardiology",
        status="Final"
    )
    db.add(lab_panel)
    db.commit()
    db.refresh(lab_panel)
    
    # Add lab results
    lab_results = [
        LabResult(panel_id=lab_panel.id, test_name="Hemoglobin", value=round(11 + random.random() * 4, 1), unit="g/dL", reference_range="11.0-15.5 g/dL", flag=""),
        LabResult(panel_id=lab_panel.id, test_name="Hematocrit", value=round(33 + random.random() * 12, 1), unit="%", reference_range="33-46%", flag=""),
        LabResult(panel_id=lab_panel.id, test_name="White Blood Cell Count", value=round(4 + random.random() * 8, 2), unit="K/uL", reference_range="4.5-13.5 K/uL", flag=""),
        LabResult(panel_id=lab_panel.id, test_name="Platelet Count", value=round(150 + random.random() * 300), unit="K/uL", reference_range="150-450 K/uL", flag="")
    ]
    
    for result in lab_results:
        db.add(result)
    
    # Add medication
    medication = Medication(
        patient_id=patient.patient_id,
        name="Furosemide (Lasix)",
        rxnorm_code="4603",
        generic_name="Furosemide",
        brand_name="Lasix",
        dosage=f"{round(1 + random.random() * 2, 1)} mg/kg/day",
        dose_amount=f"{round(5 + random.random() * 15, 1)} mg",
        route="PO (By mouth)",
        frequency="BID (Twice daily)",
        start_date=(datetime.now() - timedelta(days=random.randint(30, 180))).strftime("%Y-%m-%d"),
        prescriber="Dr. Sarah Chen, Pediatric Cardiology",
        indication="Heart failure management - fluid retention",
        status="Active",
        pharmacy="Children's Hospital Pharmacy",
        last_filled=(datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
        quantity_dispensed="30 tablets",
        refills_remaining=random.randint(0, 5)
    )
    db.add(medication)
    
    db.commit()

# ============================================================================
# HEALTH CHECKS AND UTILITIES
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/stats")
async def get_system_stats(db: Session = Depends(get_db)):
    """Get system statistics"""
    try:
        patient_count = db.query(Patient).count()
        problem_count = db.query(ProblemList).count()
        medication_count = db.query(Medication).count()
        lab_count = db.query(LabPanel).count()
        
        return {
            "total_patients": patient_count,
            "total_problems": problem_count,
            "total_medications": medication_count,
            "total_lab_panels": lab_count,
            "system_status": "operational"
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)