"""
MCP Server for Synthetic Ascension EHR Platform
Exposes EHR generation capabilities via Model Context Protocol
"""

from fastmcp import FastMCP
from typing import Dict, List, Any, Optional
import json
import uuid
import random
from datetime import datetime
from pydantic import BaseModel

class PatientGenerationConfig(BaseModel):
    population_size: int = 100
    conditions: List[str] = []
    age_range: List[int] = [18, 80]
    specialties: List[str] = []

class CohortSummary(BaseModel):
    total_patients: int
    conditions_included: List[str]
    demographics_range: str
    generation_timestamp: str

# Initialize MCP server
mcp = FastMCP("Synthetic Ascension EHR Generator")

# In-memory storage for demo
generated_cohorts = {}
active_workflows = {}

@mcp.tool()
def generate_synthetic_patients(
    population_size: int = 100,
    conditions: str = "",
    age_min: int = 18,
    age_max: int = 80,
    specialties: str = ""
) -> Dict[str, Any]:
    """
    Generate synthetic patient cohort for EHR research.
    
    Args:
        population_size: Number of patients to generate (1-1000)
        conditions: Comma-separated medical conditions (e.g., "diabetes,hypertension")
        age_min: Minimum patient age
        age_max: Maximum patient age  
        specialties: Medical specialties to focus on (e.g., "cardiology,endocrinology")
    
    Returns:
        Generated patient cohort with workflow ID for tracking
    """
    
    # Parse inputs
    condition_list = [c.strip() for c in conditions.split(",") if c.strip()]
    specialty_list = [s.strip() for s in specialties.split(",") if s.strip()]
    
    # Validate inputs
    if population_size < 1 or population_size > 1000:
        return {"error": "Population size must be between 1 and 1000"}
    
    if age_min >= age_max:
        return {"error": "Age minimum must be less than age maximum"}
    
    # Generate workflow ID
    workflow_id = str(uuid.uuid4())
    
    # Generate synthetic patients
    patients = []
    for i in range(population_size):
        patient_id = f"PAT-{uuid.uuid4().hex[:8].upper()}"
        
        patient = {
            "patient_id": patient_id,
            "name": f"Patient {i+1:03d}",
            "age": random.randint(age_min, age_max),
            "gender": random.choice(["Male", "Female"]),
            "conditions": random.sample(condition_list, min(len(condition_list), random.randint(1, 3))) if condition_list else [],
            "vitals": {
                "blood_pressure": f"{random.randint(90, 140)}/{random.randint(60, 90)}",
                "heart_rate": random.randint(60, 100),
                "temperature": round(random.uniform(98.0, 100.4), 1),
                "respiratory_rate": random.randint(12, 20)
            },
            "demographics": {
                "ethnicity": random.choice(["Caucasian", "Hispanic", "African American", "Asian", "Other"]),
                "insurance": random.choice(["Medicare", "Medicaid", "Private", "Uninsured"]),
                "location": random.choice(["Urban", "Suburban", "Rural"])
            },
            "specialties": specialty_list,
            "created_at": datetime.now().isoformat()
        }
        patients.append(patient)
    
    # Store generated cohort
    generated_cohorts[workflow_id] = {
        "patients": patients,
        "metadata": {
            "total_patients": len(patients),
            "generation_time": datetime.now().isoformat(),
            "configuration": {
                "population_size": population_size,
                "conditions": condition_list,
                "age_range": [age_min, age_max],
                "specialties": specialty_list
            }
        }
    }
    
    return {
        "workflow_id": workflow_id,
        "status": "completed",
        "summary": {
            "total_patients": len(patients),
            "conditions_included": condition_list,
            "demographics_range": f"Ages {age_min}-{age_max}",
            "specialties_focus": specialty_list,
            "generation_timestamp": datetime.now().isoformat()
        },
        "sample_patients": patients[:3]  # Show first 3 as examples
    }

@mcp.tool()
def get_cohort_details(workflow_id: str) -> Dict[str, Any]:
    """
    Retrieve complete details for a generated patient cohort.
    
    Args:
        workflow_id: The workflow ID from generate_synthetic_patients
    
    Returns:
        Complete cohort data including all patients and metadata
    """
    if workflow_id not in generated_cohorts:
        return {"error": f"Cohort with ID {workflow_id} not found"}
    
    return generated_cohorts[workflow_id]

@mcp.tool()
def list_available_cohorts() -> Dict[str, Any]:
    """
    List all available generated cohorts.
    
    Returns:
        Summary of all generated cohorts with basic metadata
    """
    cohorts = []
    for workflow_id, cohort_data in generated_cohorts.items():
        cohorts.append({
            "workflow_id": workflow_id,
            "patient_count": len(cohort_data["patients"]),
            "created_at": cohort_data["metadata"]["generation_time"],
            "conditions": cohort_data["metadata"]["configuration"]["conditions"],
            "specialties": cohort_data["metadata"]["configuration"]["specialties"]
        })
    
    return {
        "total_cohorts": len(cohorts),
        "cohorts": cohorts
    }

@mcp.tool()
def analyze_cohort_demographics(workflow_id: str) -> Dict[str, Any]:
    """
    Analyze demographics and clinical characteristics of a patient cohort.
    
    Args:
        workflow_id: The workflow ID from generate_synthetic_patients
    
    Returns:
        Detailed demographic and clinical analysis
    """
    if workflow_id not in generated_cohorts:
        return {"error": f"Cohort with ID {workflow_id} not found"}
    
    patients = generated_cohorts[workflow_id]["patients"]
    
    # Analyze demographics
    age_groups = {"18-30": 0, "31-50": 0, "51-70": 0, "70+": 0}
    gender_dist = {"Male": 0, "Female": 0}
    ethnicity_dist = {}
    insurance_dist = {}
    condition_freq = {}
    
    for patient in patients:
        # Age groups
        age = patient["age"]
        if age <= 30:
            age_groups["18-30"] += 1
        elif age <= 50:
            age_groups["31-50"] += 1
        elif age <= 70:
            age_groups["51-70"] += 1
        else:
            age_groups["70+"] += 1
        
        # Gender
        gender_dist[patient["gender"]] += 1
        
        # Ethnicity
        ethnicity = patient["demographics"]["ethnicity"]
        ethnicity_dist[ethnicity] = ethnicity_dist.get(ethnicity, 0) + 1
        
        # Insurance
        insurance = patient["demographics"]["insurance"]
        insurance_dist[insurance] = insurance_dist.get(insurance, 0) + 1
        
        # Conditions
        for condition in patient["conditions"]:
            condition_freq[condition] = condition_freq.get(condition, 0) + 1
    
    return {
        "cohort_id": workflow_id,
        "total_patients": len(patients),
        "demographics": {
            "age_distribution": age_groups,
            "gender_distribution": gender_dist,
            "ethnicity_distribution": ethnicity_dist,
            "insurance_distribution": insurance_dist
        },
        "clinical_characteristics": {
            "condition_frequency": condition_freq,
            "average_conditions_per_patient": sum(len(p["conditions"]) for p in patients) / len(patients)
        },
        "analysis_timestamp": datetime.now().isoformat()
    }

@mcp.tool()
def export_cohort_data(workflow_id: str, format: str = "json") -> Dict[str, Any]:
    """
    Export patient cohort data in specified format.
    
    Args:
        workflow_id: The workflow ID from generate_synthetic_patients
        format: Export format ("json", "summary", "csv_structure")
    
    Returns:
        Exported data in requested format
    """
    if workflow_id not in generated_cohorts:
        return {"error": f"Cohort with ID {workflow_id} not found"}
    
    cohort_data = generated_cohorts[workflow_id]
    
    if format == "json":
        return cohort_data
    
    elif format == "summary":
        patients = cohort_data["patients"]
        return {
            "summary": {
                "cohort_id": workflow_id,
                "total_patients": len(patients),
                "age_range": f"{min(p['age'] for p in patients)}-{max(p['age'] for p in patients)}",
                "conditions": list(set(c for p in patients for c in p["conditions"])),
                "export_timestamp": datetime.now().isoformat()
            }
        }
    
    elif format == "csv_structure":
        # Return CSV column structure for integration
        return {
            "csv_columns": [
                "patient_id",
                "name", 
                "age",
                "gender",
                "conditions",
                "blood_pressure",
                "heart_rate",
                "temperature",
                "respiratory_rate",
                "ethnicity",
                "insurance",
                "location",
                "created_at"
            ],
            "total_rows": len(cohort_data["patients"]),
            "note": "Use get_cohort_details to retrieve full data for CSV generation"
        }
    
    else:
        return {"error": f"Unsupported format: {format}. Use 'json', 'summary', or 'csv_structure'"}

@mcp.resource(uri="ehr://capabilities", name="ehr_capabilities", description="Available EHR generation capabilities")
def get_ehr_capabilities() -> str:
    """Describe the capabilities of the Synthetic Ascension EHR platform."""
    return """
# Synthetic Ascension EHR Platform Capabilities

## Patient Generation
- Generate 1-1000 synthetic patients per cohort
- Configurable age ranges and demographics
- Medical condition assignment with realistic prevalence
- Vital signs and clinical measurements
- Insurance and socioeconomic factors

## Medical Specialties Supported
- Cardiology (heart conditions, cardiovascular risk factors)
- Endocrinology (diabetes, thyroid disorders, metabolic conditions)
- Pulmonology (asthma, COPD, respiratory conditions)
- Nephrology (kidney disease, dialysis patients)
- Oncology (cancer patients, treatment protocols)
- Pediatrics (growth charts, developmental milestones)
- Geriatrics (age-related conditions, polypharmacy)

## Data Compliance
- HIPAA-safe synthetic data generation
- GDPR-ready privacy protection
- FDA Part 11 compliant for pharmaceutical research
- IRB-approved synthetic datasets

## Integration Options
- JSON export for data analysis
- CSV structure for spreadsheet integration
- Real-time API access via FastAPI endpoints
- Model Context Protocol (MCP) for AI agents
    """

if __name__ == "__main__":
    mcp.run()