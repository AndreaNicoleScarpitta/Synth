from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import json

@dataclass
class Patient:
    """Represents a synthetic patient with medical history and demographics"""
    
    patient_id: str
    age: Optional[int] = None
    gender: Optional[str] = None
    ethnicity: Optional[str] = None
    conditions: List[str] = None
    medications: List[str] = None
    lab_results: Dict[str, Tuple[float, str]] = None  # {test_name: (value, unit)}
    clinical_notes: List[Dict[str, str]] = None  # List of note dictionaries
    created_at: datetime = None
    
    def __post_init__(self):
        """Initialize default values for mutable fields"""
        if self.conditions is None:
            self.conditions = []
        if self.medications is None:
            self.medications = []
        if self.lab_results is None:
            self.lab_results = {}
        if self.clinical_notes is None:
            self.clinical_notes = []
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def add_condition(self, condition: str):
        """Add a medical condition to the patient"""
        if condition and condition not in self.conditions:
            self.conditions.append(condition)
    
    def add_medication(self, medication: str):
        """Add a medication to the patient"""
        if medication and medication not in self.medications:
            self.medications.append(medication)
    
    def add_lab_result(self, test_name: str, value: float, unit: str):
        """Add a lab result for the patient"""
        if test_name and value is not None and unit:
            self.lab_results[test_name] = (value, unit)
    
    def add_clinical_note(self, note_type: str, content: str, provider: str, date: str = None):
        """Add a clinical note for the patient"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        note = {
            "type": note_type,
            "content": content,
            "provider": provider,
            "date": date
        }
        self.clinical_notes.append(note)
    
    def get_age_group(self) -> str:
        """Get the age group category for the patient"""
        if self.age is None:
            return "unknown"
        elif self.age < 18:
            return "pediatric"
        elif 18 <= self.age < 35:
            return "young_adult"
        elif 35 <= self.age < 65:
            return "middle_aged"
        else:
            return "elderly"
    
    def has_condition(self, condition: str) -> bool:
        """Check if patient has a specific condition"""
        return condition.lower() in [c.lower() for c in self.conditions]
    
    def has_medication(self, medication: str) -> bool:
        """Check if patient is on a specific medication"""
        return medication.lower() in [m.lower() for m in self.medications]
    
    def get_lab_value(self, test_name: str) -> Optional[Tuple[float, str]]:
        """Get a specific lab value"""
        return self.lab_results.get(test_name)
    
    def get_comorbidity_count(self) -> int:
        """Get the number of comorbid conditions"""
        return len(self.conditions)
    
    def get_medication_count(self) -> int:
        """Get the number of medications"""
        return len(self.medications)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert patient to dictionary representation"""
        return {
            "patient_id": self.patient_id,
            "age": self.age,
            "gender": self.gender,
            "ethnicity": self.ethnicity,
            "conditions": self.conditions,
            "medications": self.medications,
            "lab_results": {
                test: {"value": value, "unit": unit} 
                for test, (value, unit) in self.lab_results.items()
            },
            "clinical_notes": self.clinical_notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "age_group": self.get_age_group(),
            "comorbidity_count": self.get_comorbidity_count(),
            "medication_count": self.get_medication_count()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Patient':
        """Create patient from dictionary representation"""
        # Handle lab_results conversion
        lab_results = {}
        if "lab_results" in data and data["lab_results"]:
            for test, result in data["lab_results"].items():
                if isinstance(result, dict):
                    lab_results[test] = (result["value"], result["unit"])
                elif isinstance(result, (list, tuple)) and len(result) == 2:
                    lab_results[test] = (result[0], result[1])
        
        # Handle created_at conversion
        created_at = None
        if "created_at" in data and data["created_at"]:
            if isinstance(data["created_at"], str):
                created_at = datetime.fromisoformat(data["created_at"])
            elif isinstance(data["created_at"], datetime):
                created_at = data["created_at"]
        
        return cls(
            patient_id=data.get("patient_id", ""),
            age=data.get("age"),
            gender=data.get("gender"),
            ethnicity=data.get("ethnicity"),
            conditions=data.get("conditions", []),
            medications=data.get("medications", []),
            lab_results=lab_results,
            clinical_notes=data.get("clinical_notes", []),
            created_at=created_at
        )
    
    def to_fhir_patient(self) -> Dict[str, Any]:
        """Convert to FHIR Patient resource format"""
        fhir_patient = {
            "resourceType": "Patient",
            "id": self.patient_id,
            "active": True
        }
        
        # Add demographics
        if self.gender:
            fhir_patient["gender"] = self.gender.lower()
        
        if self.age:
            birth_year = datetime.now().year - self.age
            fhir_patient["birthDate"] = f"{birth_year}-01-01"
        
        # Add ethnicity extension
        if self.ethnicity:
            fhir_patient["extension"] = [{
                "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
                "valueCodeableConcept": {
                    "coding": [{
                        "display": self.ethnicity
                    }]
                }
            }]
        
        return fhir_patient
    
    def to_clinical_summary(self) -> str:
        """Generate a clinical summary of the patient"""
        summary = f"Patient ID: {self.patient_id}\n"
        summary += f"Demographics: {self.age}-year-old {self.gender} {self.ethnicity}\n"
        
        if self.conditions:
            summary += f"Medical Conditions: {', '.join(self.conditions)}\n"
        
        if self.medications:
            summary += f"Current Medications: {', '.join(self.medications)}\n"
        
        if self.lab_results:
            summary += "Recent Lab Results:\n"
            for test, (value, unit) in self.lab_results.items():
                summary += f"  - {test}: {value} {unit}\n"
        
        summary += f"Number of Clinical Notes: {len(self.clinical_notes)}\n"
        summary += f"Record Created: {self.created_at.strftime('%Y-%m-%d') if self.created_at else 'Unknown'}\n"
        
        return summary
    
    def __str__(self) -> str:
        """String representation of patient"""
        return f"Patient({self.patient_id}, {self.age}y {self.gender}, {len(self.conditions)} conditions)"
    
    def __repr__(self) -> str:
        """Detailed representation of patient"""
        return (f"Patient(id='{self.patient_id}', age={self.age}, gender='{self.gender}', "
                f"conditions={len(self.conditions)}, medications={len(self.medications)})")


@dataclass
class PatientCohort:
    """Represents a cohort of synthetic patients"""
    
    patients: List[Patient]
    generation_parameters: Dict[str, Any] = None
    created_at: datetime = None
    cohort_id: str = None
    
    def __post_init__(self):
        """Initialize default values"""
        if self.generation_parameters is None:
            self.generation_parameters = {}
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.cohort_id is None:
            self.cohort_id = f"cohort_{int(self.created_at.timestamp())}"
    
    def get_size(self) -> int:
        """Get the number of patients in the cohort"""
        return len(self.patients)
    
    def get_demographics_summary(self) -> Dict[str, Any]:
        """Get demographic summary statistics for the cohort"""
        if not self.patients:
            return {}
        
        # Age statistics
        ages = [p.age for p in self.patients if p.age is not None]
        age_stats = {}
        if ages:
            age_stats = {
                "mean": sum(ages) / len(ages),
                "min": min(ages),
                "max": max(ages),
                "count": len(ages)
            }
        
        # Gender distribution
        genders = [p.gender for p in self.patients if p.gender]
        gender_dist = {}
        for gender in genders:
            gender_dist[gender] = gender_dist.get(gender, 0) + 1
        
        # Ethnicity distribution
        ethnicities = [p.ethnicity for p in self.patients if p.ethnicity]
        ethnicity_dist = {}
        for ethnicity in ethnicities:
            ethnicity_dist[ethnicity] = ethnicity_dist.get(ethnicity, 0) + 1
        
        # Age group distribution
        age_groups = [p.get_age_group() for p in self.patients]
        age_group_dist = {}
        for age_group in age_groups:
            age_group_dist[age_group] = age_group_dist.get(age_group, 0) + 1
        
        return {
            "total_patients": len(self.patients),
            "age_statistics": age_stats,
            "gender_distribution": gender_dist,
            "ethnicity_distribution": ethnicity_dist,
            "age_group_distribution": age_group_dist
        }
    
    def get_condition_prevalence(self) -> Dict[str, Dict[str, Any]]:
        """Get condition prevalence statistics"""
        condition_counts = {}
        total_patients = len(self.patients)
        
        for patient in self.patients:
            for condition in patient.conditions:
                if condition not in condition_counts:
                    condition_counts[condition] = 0
                condition_counts[condition] += 1
        
        # Calculate prevalence percentages
        condition_prevalence = {}
        for condition, count in condition_counts.items():
            condition_prevalence[condition] = {
                "count": count,
                "prevalence": (count / total_patients) * 100 if total_patients > 0 else 0
            }
        
        return condition_prevalence
    
    def get_medication_usage(self) -> Dict[str, Dict[str, Any]]:
        """Get medication usage statistics"""
        medication_counts = {}
        total_patients = len(self.patients)
        
        for patient in self.patients:
            for medication in patient.medications:
                if medication not in medication_counts:
                    medication_counts[medication] = 0
                medication_counts[medication] += 1
        
        # Calculate usage percentages
        medication_usage = {}
        for medication, count in medication_counts.items():
            medication_usage[medication] = {
                "count": count,
                "usage_rate": (count / total_patients) * 100 if total_patients > 0 else 0
            }
        
        return medication_usage
    
    def get_comorbidity_analysis(self) -> Dict[str, Any]:
        """Analyze comorbidity patterns in the cohort"""
        comorbidity_counts = [p.get_comorbidity_count() for p in self.patients]
        
        if not comorbidity_counts:
            return {}
        
        # Basic statistics
        stats = {
            "mean_comorbidities": sum(comorbidity_counts) / len(comorbidity_counts),
            "min_comorbidities": min(comorbidity_counts),
            "max_comorbidities": max(comorbidity_counts),
            "patients_with_multiple_conditions": sum(1 for count in comorbidity_counts if count > 1)
        }
        
        # Distribution
        distribution = {}
        for count in comorbidity_counts:
            distribution[count] = distribution.get(count, 0) + 1
        
        stats["distribution"] = distribution
        return stats
    
    def filter_by_condition(self, condition: str) -> 'PatientCohort':
        """Create a new cohort with patients having a specific condition"""
        filtered_patients = [p for p in self.patients if p.has_condition(condition)]
        
        return PatientCohort(
            patients=filtered_patients,
            generation_parameters=self.generation_parameters.copy(),
            cohort_id=f"{self.cohort_id}_filtered_{condition.lower().replace(' ', '_')}"
        )
    
    def filter_by_age_group(self, age_group: str) -> 'PatientCohort':
        """Create a new cohort with patients in a specific age group"""
        filtered_patients = [p for p in self.patients if p.get_age_group() == age_group]
        
        return PatientCohort(
            patients=filtered_patients,
            generation_parameters=self.generation_parameters.copy(),
            cohort_id=f"{self.cohort_id}_filtered_{age_group}"
        )
    
    def filter_by_gender(self, gender: str) -> 'PatientCohort':
        """Create a new cohort with patients of a specific gender"""
        filtered_patients = [p for p in self.patients if p.gender and p.gender.lower() == gender.lower()]
        
        return PatientCohort(
            patients=filtered_patients,
            generation_parameters=self.generation_parameters.copy(),
            cohort_id=f"{self.cohort_id}_filtered_{gender.lower()}"
        )
    
    def get_lab_statistics(self) -> Dict[str, Dict[str, float]]:
        """Get lab value statistics across the cohort"""
        lab_stats = {}
        
        # Collect all lab results
        all_labs = {}
        for patient in self.patients:
            for test_name, (value, unit) in patient.lab_results.items():
                if test_name not in all_labs:
                    all_labs[test_name] = {"values": [], "unit": unit}
                all_labs[test_name]["values"].append(value)
        
        # Calculate statistics for each lab test
        for test_name, data in all_labs.items():
            values = data["values"]
            if values:
                lab_stats[test_name] = {
                    "mean": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values),
                    "unit": data["unit"]
                }
        
        return lab_stats
    
    def to_csv_data(self) -> List[Dict[str, Any]]:
        """Convert cohort to CSV-compatible data structure"""
        csv_data = []
        
        for patient in self.patients:
            row = {
                "patient_id": patient.patient_id,
                "age": patient.age,
                "gender": patient.gender,
                "ethnicity": patient.ethnicity,
                "age_group": patient.get_age_group(),
                "conditions": "; ".join(patient.conditions),
                "medications": "; ".join(patient.medications),
                "condition_count": patient.get_comorbidity_count(),
                "medication_count": patient.get_medication_count(),
                "created_at": patient.created_at.strftime("%Y-%m-%d") if patient.created_at else ""
            }
            
            # Add lab results as separate columns
            for test_name, (value, unit) in patient.lab_results.items():
                row[f"lab_{test_name}"] = f"{value} {unit}"
            
            # Add clinical notes count
            row["clinical_notes_count"] = len(patient.clinical_notes)
            
            csv_data.append(row)
        
        return csv_data
    
    def to_fhir_bundle(self) -> Dict[str, Any]:
        """Convert cohort to FHIR Bundle format"""
        bundle = {
            "resourceType": "Bundle",
            "id": self.cohort_id,
            "type": "collection",
            "timestamp": self.created_at.isoformat() if self.created_at else None,
            "total": len(self.patients),
            "entry": []
        }
        
        for patient in self.patients:
            entry = {
                "resource": patient.to_fhir_patient(),
                "fullUrl": f"Patient/{patient.patient_id}"
            }
            bundle["entry"].append(entry)
        
        return bundle
    
    def export_summary(self) -> Dict[str, Any]:
        """Export comprehensive cohort summary"""
        return {
            "cohort_info": {
                "cohort_id": self.cohort_id,
                "total_patients": self.get_size(),
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "generation_parameters": self.generation_parameters
            },
            "demographics": self.get_demographics_summary(),
            "conditions": self.get_condition_prevalence(),
            "medications": self.get_medication_usage(),
            "comorbidities": self.get_comorbidity_analysis(),
            "lab_statistics": self.get_lab_statistics()
        }
    
    def __len__(self) -> int:
        """Return the number of patients in the cohort"""
        return len(self.patients)
    
    def __iter__(self):
        """Allow iteration over patients"""
        return iter(self.patients)
    
    def __getitem__(self, index):
        """Allow indexing into the patient list"""
        return self.patients[index]
    
    def __str__(self) -> str:
        """String representation of cohort"""
        return f"PatientCohort({len(self.patients)} patients, created {self.created_at.strftime('%Y-%m-%d') if self.created_at else 'unknown'})"
    
    def __repr__(self) -> str:
        """Detailed representation of cohort"""
        return f"PatientCohort(id='{self.cohort_id}', patients={len(self.patients)}, created='{self.created_at}')"
