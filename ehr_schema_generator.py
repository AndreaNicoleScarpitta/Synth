"""
Comprehensive EHR Schema Generator for Synthetic Ascension
Creates complete, realistic medical records with full audit trails and UX tracking
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, date
from enum import Enum
import uuid
import json
from pydantic import BaseModel, Field

# UX Tracking Tags for Frontend Analytics
class UXEventType(Enum):
    """UX event tracking for platform analytics"""
    PAGE_VIEW = "page_view"
    BUTTON_CLICK = "button_click"
    FORM_SUBMIT = "form_submit"
    DATA_EXPORT = "data_export"
    SEARCH_QUERY = "search_query"
    FILTER_APPLIED = "filter_applied"
    CHART_INTERACTION = "chart_interaction"
    COHORT_GENERATION = "cohort_generation"
    VALIDATION_RUN = "validation_run"
    LITERATURE_SEARCH = "literature_search"

@dataclass
class UXTrackingEvent:
    """Complete UX tracking for frontend analytics"""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: UXEventType = UXEventType.PAGE_VIEW
    timestamp: datetime = field(default_factory=datetime.now)
    user_session_id: str = ""
    page_path: str = ""
    component_name: str = ""
    action_details: Dict[str, Any] = field(default_factory=dict)
    user_agent: str = ""
    ip_address: str = ""
    persona_type: str = ""  # CDO, CMO, RWE, etc.
    workflow_context: str = ""

# Complete EHR Schema Components

@dataclass
class Demographics:
    """Complete patient demographics with realistic detail"""
    patient_id: str = field(default_factory=lambda: f"PAT_{uuid.uuid4().hex[:8].upper()}")
    mrn: str = field(default_factory=lambda: f"MRN{uuid.uuid4().hex[:10].upper()}")
    
    # Core demographics
    first_name: str = ""
    last_name: str = ""
    middle_name: Optional[str] = None
    date_of_birth: date = None
    age_years: int = 0
    age_months: int = 0
    gender: str = ""  # Male, Female, Other, Unknown
    sex_assigned_at_birth: str = ""
    
    # Ethnicity and race (detailed for bias analysis)
    ethnicity: str = ""  # Hispanic/Latino, Not Hispanic/Latino
    race_primary: str = ""  # White, Black/African American, Asian, etc.
    race_secondary: List[str] = field(default_factory=list)
    
    # Address and contact
    address_line1: str = ""
    address_line2: Optional[str] = None
    city: str = ""
    state: str = ""
    zip_code: str = ""
    country: str = "United States"
    phone_primary: str = ""
    phone_secondary: Optional[str] = None
    email: Optional[str] = None
    
    # Social determinants
    preferred_language: str = "English"
    marital_status: str = ""
    education_level: str = ""
    employment_status: str = ""
    insurance_type: str = ""
    socioeconomic_status: str = ""
    
    # Emergency contact
    emergency_contact_name: str = ""
    emergency_contact_relationship: str = ""
    emergency_contact_phone: str = ""

@dataclass
class ClinicalEncounter:
    """Detailed clinical encounter with complete documentation"""
    encounter_id: str = field(default_factory=lambda: f"ENC_{uuid.uuid4().hex[:8].upper()}")
    patient_id: str = ""
    
    # Encounter details
    encounter_datetime: datetime = field(default_factory=datetime.now)
    encounter_type: str = ""  # Inpatient, Outpatient, Emergency, Urgent Care
    encounter_class: str = ""  # Initial, Follow-up, Consultation
    department: str = ""
    facility_name: str = ""
    
    # Provider information
    attending_provider_id: str = ""
    attending_provider_name: str = ""
    specialty: str = ""
    resident_provider_id: Optional[str] = None
    consulting_providers: List[Dict[str, str]] = field(default_factory=list)
    
    # Clinical notes
    chief_complaint: str = ""
    history_present_illness: str = ""
    review_of_systems: str = ""
    past_medical_history: str = ""
    past_surgical_history: str = ""
    family_history: str = ""
    social_history: str = ""
    medications_current: str = ""
    allergies: str = ""
    
    # Physical examination
    vital_signs: Dict[str, Any] = field(default_factory=dict)
    physical_exam: str = ""
    
    # Assessment and plan
    assessment: str = ""
    plan: str = ""
    
    # Disposition
    disposition: str = ""  # Discharged, Admitted, Transferred, etc.
    discharge_instructions: str = ""
    follow_up_instructions: str = ""

@dataclass
class DiagnosisCode:
    """Complete diagnosis with multiple coding systems"""
    diagnosis_id: str = field(default_factory=lambda: f"DX_{uuid.uuid4().hex[:8].upper()}")
    patient_id: str = ""
    encounter_id: str = ""
    
    # ICD-10 coding
    icd10_code: str = ""
    icd10_description: str = ""
    
    # SNOMED CT coding
    snomed_code: Optional[str] = None
    snomed_description: Optional[str] = None
    
    # Clinical details
    diagnosis_type: str = ""  # Primary, Secondary, Admitting, etc.
    diagnosis_status: str = ""  # Active, Resolved, Chronic, etc.
    onset_date: Optional[date] = None
    resolution_date: Optional[date] = None
    severity: str = ""  # Mild, Moderate, Severe
    
    # Provider information
    diagnosing_provider: str = ""
    diagnosis_confidence: float = 0.0  # 0.0 to 1.0
    
    # Documentation
    clinical_notes: str = ""
    supporting_evidence: List[str] = field(default_factory=list)

@dataclass
class Medication:
    """Complete medication record with RxNorm coding"""
    medication_id: str = field(default_factory=lambda: f"MED_{uuid.uuid4().hex[:8].upper()}")
    patient_id: str = ""
    encounter_id: str = ""
    
    # RxNorm coding
    rxnorm_code: str = ""
    generic_name: str = ""
    brand_name: Optional[str] = None
    
    # Prescription details
    dosage_amount: float = 0.0
    dosage_unit: str = ""  # mg, mcg, units, etc.
    dosage_form: str = ""  # tablet, capsule, injection, etc.
    route_of_administration: str = ""  # oral, IV, IM, etc.
    frequency: str = ""  # BID, TID, QID, PRN, etc.
    frequency_per_day: float = 0.0
    
    # Timing
    start_date: date = None
    end_date: Optional[date] = None
    duration_days: Optional[int] = None
    
    # Prescribing information
    prescribing_provider: str = ""
    indication: str = ""
    instructions: str = ""
    quantity_prescribed: int = 0
    refills_authorized: int = 0
    
    # Clinical monitoring
    therapeutic_class: str = ""
    mechanism_of_action: str = ""
    contraindications: List[str] = field(default_factory=list)
    drug_interactions: List[str] = field(default_factory=list)
    adverse_effects_noted: List[str] = field(default_factory=list)

@dataclass
class LabResult:
    """Complete laboratory result with LOINC coding"""
    lab_result_id: str = field(default_factory=lambda: f"LAB_{uuid.uuid4().hex[:8].upper()}")
    patient_id: str = ""
    encounter_id: str = ""
    
    # LOINC coding
    loinc_code: str = ""
    lab_name: str = ""
    lab_category: str = ""  # Chemistry, Hematology, Microbiology, etc.
    
    # Result details
    result_value: Union[float, str] = ""
    result_unit: str = ""
    reference_range_low: Optional[float] = None
    reference_range_high: Optional[float] = None
    reference_range_text: str = ""
    
    # Status and flags
    result_status: str = ""  # Final, Preliminary, Corrected
    abnormal_flag: str = ""  # Normal, High, Low, Critical
    critical_flag: bool = False
    
    # Timing
    collection_datetime: datetime = field(default_factory=datetime.now)
    result_datetime: datetime = field(default_factory=datetime.now)
    
    # Provider and lab information
    ordering_provider: str = ""
    performing_lab: str = ""
    specimen_type: str = ""
    specimen_source: str = ""
    
    # Clinical interpretation
    interpretation: str = ""
    clinical_significance: str = ""

@dataclass
class ImagingStudy:
    """Complete imaging study with detailed results"""
    imaging_id: str = field(default_factory=lambda: f"IMG_{uuid.uuid4().hex[:8].upper()}")
    patient_id: str = ""
    encounter_id: str = ""
    
    # Study details
    study_type: str = ""  # CT, MRI, X-Ray, Ultrasound, etc.
    body_part: str = ""
    indication: str = ""
    technique: str = ""
    
    # Timing
    study_datetime: datetime = field(default_factory=datetime.now)
    
    # Provider information
    ordering_provider: str = ""
    interpreting_radiologist: str = ""
    
    # Results
    findings: str = ""
    impression: str = ""
    recommendations: str = ""
    
    # Technical details
    contrast_used: bool = False
    contrast_type: Optional[str] = None
    radiation_dose: Optional[float] = None
    
    # DICOM information
    study_instance_uid: str = field(default_factory=lambda: f"1.2.3.{uuid.uuid4().hex}")
    series_count: int = 1
    image_count: int = 1

@dataclass
class HemodynamicData:
    """Detailed hemodynamic measurements for cardiac patients"""
    hemodynamic_id: str = field(default_factory=lambda: f"HEMO_{uuid.uuid4().hex[:8].upper()}")
    patient_id: str = ""
    encounter_id: str = ""
    
    # Timing
    measurement_datetime: datetime = field(default_factory=datetime.now)
    measurement_type: str = ""  # Catheterization, Echo, Swan-Ganz, etc.
    
    # Pressures (mmHg)
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None
    mean_arterial_pressure: Optional[float] = None
    central_venous_pressure: Optional[float] = None
    pulmonary_artery_pressure_systolic: Optional[float] = None
    pulmonary_artery_pressure_diastolic: Optional[float] = None
    pulmonary_capillary_wedge_pressure: Optional[float] = None
    
    # Cardiac output measurements
    cardiac_output_l_min: Optional[float] = None
    cardiac_index_l_min_m2: Optional[float] = None
    stroke_volume_ml: Optional[float] = None
    heart_rate_bpm: Optional[float] = None
    
    # Resistance calculations
    systemic_vascular_resistance: Optional[float] = None
    pulmonary_vascular_resistance: Optional[float] = None
    
    # Echo-specific measurements
    ejection_fraction_percent: Optional[float] = None
    left_ventricular_end_diastolic_dimension: Optional[float] = None
    left_ventricular_end_systolic_dimension: Optional[float] = None
    
    # Clinical context
    measurement_indication: str = ""
    clinical_notes: str = ""
    interpreting_provider: str = ""

@dataclass
class HematologyData:
    """Complete blood count and hematologic markers"""
    hematology_id: str = field(default_factory=lambda: f"HEME_{uuid.uuid4().hex[:8].upper()}")
    patient_id: str = ""
    encounter_id: str = ""
    
    # Timing
    collection_datetime: datetime = field(default_factory=datetime.now)
    
    # Complete blood count
    white_blood_cell_count: Optional[float] = None  # cells/μL
    red_blood_cell_count: Optional[float] = None
    hemoglobin: Optional[float] = None  # g/dL
    hematocrit: Optional[float] = None  # %
    platelet_count: Optional[float] = None  # cells/μL
    
    # RBC indices
    mean_corpuscular_volume: Optional[float] = None  # fL
    mean_corpuscular_hemoglobin: Optional[float] = None  # pg
    mean_corpuscular_hemoglobin_concentration: Optional[float] = None  # g/dL
    
    # Differential count
    neutrophils_percent: Optional[float] = None
    lymphocytes_percent: Optional[float] = None
    monocytes_percent: Optional[float] = None
    eosinophils_percent: Optional[float] = None
    basophils_percent: Optional[float] = None
    
    # Coagulation studies
    prothrombin_time: Optional[float] = None  # seconds
    inr: Optional[float] = None
    partial_thromboplastin_time: Optional[float] = None  # seconds
    
    # Blood flow markers
    d_dimer: Optional[float] = None  # ng/mL
    fibrinogen: Optional[float] = None  # mg/dL
    
    # Clinical context
    clinical_indication: str = ""
    abnormal_findings: List[str] = field(default_factory=list)

@dataclass
class GenomicData:
    """Genomic and genetic testing information"""
    genomic_id: str = field(default_factory=lambda: f"GEN_{uuid.uuid4().hex[:8].upper()}")
    patient_id: str = ""
    
    # Test details
    test_type: str = ""  # Whole genome, exome, panel, single gene
    test_name: str = ""
    testing_lab: str = ""
    test_date: date = None
    
    # Variants found
    variants: List[Dict[str, Any]] = field(default_factory=list)
    
    # Pharmacogenomics
    pharmacogenomic_markers: Dict[str, str] = field(default_factory=dict)
    drug_metabolism_predictions: Dict[str, str] = field(default_factory=dict)
    
    # Clinical interpretation
    pathogenic_variants: List[str] = field(default_factory=list)
    variants_of_uncertain_significance: List[str] = field(default_factory=list)
    disease_risk_predictions: Dict[str, float] = field(default_factory=dict)
    
    # Genetic counseling
    genetic_counselor: str = ""
    counseling_notes: str = ""
    family_history_relevant: bool = False

@dataclass
class WearableData:
    """IoT and wearable device data"""
    wearable_id: str = field(default_factory=lambda: f"WEAR_{uuid.uuid4().hex[:8].upper()}")
    patient_id: str = ""
    
    # Device information
    device_type: str = ""  # Fitbit, Apple Watch, continuous glucose monitor, etc.
    device_model: str = ""
    device_serial: str = ""
    
    # Data collection period
    start_datetime: datetime = field(default_factory=datetime.now)
    end_datetime: datetime = field(default_factory=datetime.now)
    
    # Vital sign trends
    heart_rate_data: List[Dict[str, Any]] = field(default_factory=list)
    blood_pressure_data: List[Dict[str, Any]] = field(default_factory=list)
    glucose_data: List[Dict[str, Any]] = field(default_factory=list)
    
    # Activity data
    steps_daily: List[Dict[str, int]] = field(default_factory=list)
    sleep_data: List[Dict[str, Any]] = field(default_factory=list)
    exercise_sessions: List[Dict[str, Any]] = field(default_factory=list)
    
    # Clinical integration
    clinically_significant_events: List[str] = field(default_factory=list)
    provider_reviewed: bool = False
    clinical_actions_taken: List[str] = field(default_factory=list)

@dataclass
class AdministrativeData:
    """Billing, claims, and administrative information"""
    admin_id: str = field(default_factory=lambda: f"ADM_{uuid.uuid4().hex[:8].upper()}")
    patient_id: str = ""
    encounter_id: str = ""
    
    # Insurance information
    insurance_primary: Dict[str, str] = field(default_factory=dict)
    insurance_secondary: Optional[Dict[str, str]] = None
    insurance_authorization_number: Optional[str] = None
    
    # Billing codes
    cpt_codes: List[Dict[str, Any]] = field(default_factory=list)
    hcpcs_codes: List[Dict[str, Any]] = field(default_factory=list)
    drg_code: Optional[str] = None
    
    # Financial data
    total_charges: float = 0.0
    insurance_payments: float = 0.0
    patient_responsibility: float = 0.0
    adjustments: float = 0.0
    
    # Claims processing
    claim_number: Optional[str] = None
    claim_status: str = ""
    denial_reasons: List[str] = field(default_factory=list)

@dataclass
class AuditTrail:
    """Complete audit trail for regulatory compliance"""
    audit_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    
    # System information
    component_name: str = ""
    component_version: str = "1.0.0"
    operation_type: str = ""  # CREATE, READ, UPDATE, DELETE, GENERATE
    
    # User information
    user_id: Optional[str] = None
    user_role: Optional[str] = None
    session_id: Optional[str] = None
    
    # Data context
    patient_id: Optional[str] = None
    record_type: str = ""
    record_id: str = ""
    
    # Change details
    field_changed: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    change_reason: str = ""
    
    # Traceability
    source_system: str = "Synthetic Ascension"
    data_lineage: List[str] = field(default_factory=list)
    validation_status: str = "VALIDATED"
    
    # Compliance
    hipaa_compliant: bool = True
    gdpr_compliant: bool = True
    regulatory_framework: List[str] = field(default_factory=lambda: ["FDA_21CFR11", "HIPAA"])

# Complete EHR Schema Container
@dataclass
class CompleteEHRRecord:
    """Complete synthetic EHR with all modules"""
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    generation_timestamp: datetime = field(default_factory=datetime.now)
    
    # Core patient data
    demographics: Demographics = field(default_factory=Demographics)
    
    # Clinical data
    encounters: List[ClinicalEncounter] = field(default_factory=list)
    diagnoses: List[DiagnosisCode] = field(default_factory=list)
    medications: List[Medication] = field(default_factory=list)
    lab_results: List[LabResult] = field(default_factory=list)
    imaging_studies: List[ImagingStudy] = field(default_factory=list)
    
    # Specialized data
    hemodynamic_data: List[HemodynamicData] = field(default_factory=list)
    hematology_data: List[HematologyData] = field(default_factory=list)
    genomic_data: Optional[GenomicData] = None
    wearable_data: List[WearableData] = field(default_factory=list)
    
    # Administrative
    administrative_data: List[AdministrativeData] = field(default_factory=list)
    
    # Metadata and audit
    audit_trail: List[AuditTrail] = field(default_factory=list)
    data_quality_score: float = 0.0
    clinical_validity_score: float = 0.0
    bias_assessment: Dict[str, Any] = field(default_factory=dict)
    
    # UX tracking
    ux_events: List[UXTrackingEvent] = field(default_factory=list)
    
    def to_fhir_bundle(self) -> Dict[str, Any]:
        """Convert to FHIR R4 Bundle format"""
        # Implementation would create proper FHIR Bundle
        return {
            "resourceType": "Bundle",
            "id": self.record_id,
            "type": "collection",
            "timestamp": self.generation_timestamp.isoformat(),
            "entry": []  # Would populate with FHIR resources
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export"""
        return {
            "record_id": self.record_id,
            "generation_timestamp": self.generation_timestamp.isoformat(),
            "demographics": self.demographics.__dict__,
            "encounters": [enc.__dict__ for enc in self.encounters],
            "diagnoses": [dx.__dict__ for dx in self.diagnoses],
            "medications": [med.__dict__ for med in self.medications],
            "lab_results": [lab.__dict__ for lab in self.lab_results],
            "imaging_studies": [img.__dict__ for img in self.imaging_studies],
            "hemodynamic_data": [hemo.__dict__ for hemo in self.hemodynamic_data],
            "hematology_data": [heme.__dict__ for heme in self.hematology_data],
            "genomic_data": self.genomic_data.__dict__ if self.genomic_data else None,
            "wearable_data": [wear.__dict__ for wear in self.wearable_data],
            "administrative_data": [admin.__dict__ for admin in self.administrative_data],
            "audit_trail": [audit.__dict__ for audit in self.audit_trail],
            "data_quality_score": self.data_quality_score,
            "clinical_validity_score": self.clinical_validity_score,
            "bias_assessment": self.bias_assessment,
            "ux_events": [event.__dict__ for event in self.ux_events]
        }

# Schema validation and generation functions
def create_audit_entry(operation: str, component: str, details: Dict[str, Any]) -> AuditTrail:
    """Create standardized audit trail entry"""
    return AuditTrail(
        component_name=component,
        operation_type=operation,
        change_reason=details.get("reason", "Synthetic data generation"),
        data_lineage=details.get("sources", []),
        validation_status="VALIDATED"
    )

def track_ux_event(event_type: UXEventType, component: str, details: Dict[str, Any]) -> UXTrackingEvent:
    """Create UX tracking event for frontend analytics"""
    return UXTrackingEvent(
        event_type=event_type,
        component_name=component,
        action_details=details,
        user_session_id=details.get("session_id", ""),
        persona_type=details.get("persona", ""),
        workflow_context=details.get("workflow", "")
    )

def generate_complete_ehr_schema() -> Dict[str, Any]:
    """Generate complete EHR schema definition"""
    return {
        "schema_version": "1.0.0",
        "generated_at": datetime.now().isoformat(),
        "modules": {
            "demographics": Demographics.__annotations__,
            "encounters": ClinicalEncounter.__annotations__,
            "diagnoses": DiagnosisCode.__annotations__,
            "medications": Medication.__annotations__,
            "lab_results": LabResult.__annotations__,
            "imaging_studies": ImagingStudy.__annotations__,
            "hemodynamic_data": HemodynamicData.__annotations__,
            "hematology_data": HematologyData.__annotations__,
            "genomic_data": GenomicData.__annotations__,
            "wearable_data": WearableData.__annotations__,
            "administrative_data": AdministrativeData.__annotations__,
            "audit_trail": AuditTrail.__annotations__,
            "ux_tracking": UXTrackingEvent.__annotations__
        },
        "compliance_frameworks": [
            "HIPAA", "GDPR", "FDA_21CFR_Part_11", "ICH_GCP", "ISO_27001"
        ],
        "coding_standards": [
            "ICD-10-CM", "SNOMED_CT", "RxNorm", "LOINC", "CPT", "HCPCS"
        ]
    }

if __name__ == "__main__":
    # Generate and display schema
    schema = generate_complete_ehr_schema()
    print(json.dumps(schema, indent=2, default=str))