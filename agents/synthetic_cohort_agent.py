import random
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from models.patient_data import Patient, PatientCohort
from utils.ollama_client import OllamaClient
import json

class SyntheticCohortAgent:
    """Agent responsible for generating synthetic patient cohorts"""
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
        
        # Demographics distributions
        self.age_ranges = {
            "pediatric": (0, 18),
            "young_adult": (18, 35),
            "middle_aged": (35, 65),
            "elderly": (65, 100)
        }
        
        self.ethnicities = [
            "White", "Black or African American", "Asian", "Hispanic or Latino",
            "Native American", "Pacific Islander", "Mixed", "Other"
        ]
        
        self.genders = ["Male", "Female", "Other"]
        
        # Common conditions and medications
        self.common_conditions = [
            "Hypertension", "Diabetes Mellitus Type 2", "Hyperlipidemia",
            "Coronary Artery Disease", "Chronic Kidney Disease", "COPD",
            "Depression", "Anxiety", "Osteoarthritis", "Hypothyroidism"
        ]
        
        self.common_medications = [
            "Metformin", "Lisinopril", "Atorvastatin", "Amlodipine",
            "Metoprolol", "Omeprazole", "Levothyroxine", "Albuterol",
            "Aspirin", "Sertraline"
        ]
        
        # Lab test reference ranges
        self.lab_references = {
            "glucose": (70, 200, "mg/dL"),
            "hemoglobin": (12, 16, "g/dL"),
            "creatinine": (0.6, 1.3, "mg/dL"),
            "cholesterol": (150, 300, "mg/dL"),
            "blood_pressure_systolic": (90, 180, "mmHg"),
            "blood_pressure_diastolic": (60, 110, "mmHg"),
            "heart_rate": (60, 100, "bpm"),
            "bmi": (18, 40, "kg/m²")
        }
    
    def generate_cohort(self, query: str, literature_context: Optional[str] = None, 
                       cohort_size: int = 100, include_notes: bool = True, 
                       include_labs: bool = True) -> PatientCohort:
        """Generate a synthetic patient cohort based on query and literature context"""
        
        # Extract cohort parameters from query and literature
        cohort_params = self._extract_cohort_parameters(query, literature_context)
        
        # Generate patients
        patients = []
        for i in range(cohort_size):
            patient = self._generate_patient(cohort_params, include_notes, include_labs)
            patients.append(patient)
        
        return PatientCohort(
            patients=patients,
            generation_parameters=cohort_params,
            created_at=datetime.now()
        )
    
    def _extract_cohort_parameters(self, query: str, literature_context: Optional[str] = None) -> Dict[str, Any]:
        """Extract patient cohort parameters from query and literature context"""
        
        prompt = f"""
        Based on the research query and literature context, extract parameters for generating a synthetic patient cohort.

        Query: {query}
        
        Literature Context: {literature_context or "No specific literature context provided"}

        Extract and format as JSON:
        {{
            "target_conditions": ["condition1", "condition2"],
            "age_group": "young_adult|middle_aged|elderly|mixed",
            "gender_distribution": {{"female": 0.5, "male": 0.5}},
            "key_medications": ["medication1", "medication2"],
            "severity_distribution": {{"mild": 0.4, "moderate": 0.4, "severe": 0.2}},
            "comorbidities": ["comorbidity1", "comorbidity2"],
            "demographic_focus": "general|specific_ethnicity|specific_region"
        }}

        Ensure realistic distributions based on epidemiological patterns.
        """
        
        try:
            response = self.ollama_client.generate_text(prompt)
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                params = json.loads(json_str)
                return params
        except Exception as e:
            print(f"Error extracting cohort parameters: {e}")
        
        # Fallback parameters
        return {
            "target_conditions": ["Hypertension", "Diabetes Mellitus Type 2"],
            "age_group": "mixed",
            "gender_distribution": {"female": 0.5, "male": 0.5},
            "key_medications": ["Metformin", "Lisinopril"],
            "severity_distribution": {"mild": 0.4, "moderate": 0.4, "severe": 0.2},
            "comorbidities": ["Hyperlipidemia"],
            "demographic_focus": "general"
        }
    
    def _generate_patient(self, cohort_params: Dict[str, Any], include_notes: bool, 
                         include_labs: bool) -> Patient:
        """Generate a single synthetic patient"""
        
        # Generate basic demographics
        patient_id = str(uuid.uuid4())[:8]
        
        # Age based on age group
        age = self._generate_age(cohort_params.get("age_group", "mixed"))
        
        # Gender based on distribution
        gender_dist = cohort_params.get("gender_distribution", {"female": 0.5, "male": 0.5})
        gender = self._sample_from_distribution(gender_dist)
        
        # Ethnicity
        ethnicity = random.choice(self.ethnicities)
        
        # Generate conditions
        conditions = self._generate_conditions(cohort_params)
        
        # Generate medications
        medications = self._generate_medications(cohort_params, conditions)
        
        # Generate lab results if requested
        lab_results = {}
        if include_labs:
            lab_results = self._generate_lab_results(conditions, age, gender)
        
        # Generate clinical notes if requested
        clinical_notes = []
        if include_notes:
            clinical_notes = self._generate_clinical_notes(
                patient_id, age, gender, conditions, medications
            )
        
        return Patient(
            patient_id=patient_id,
            age=age,
            gender=gender.title(),
            ethnicity=ethnicity,
            conditions=conditions,
            medications=medications,
            lab_results=lab_results,
            clinical_notes=clinical_notes,
            created_at=datetime.now()
        )
    
    def _generate_age(self, age_group: str) -> int:
        """Generate age based on age group"""
        if age_group == "mixed":
            # Weighted distribution favoring adults
            ranges = [
                (self.age_ranges["young_adult"], 0.3),
                (self.age_ranges["middle_aged"], 0.5),
                (self.age_ranges["elderly"], 0.2)
            ]
            selected_range = self._weighted_choice(ranges)
        else:
            selected_range = self.age_ranges.get(age_group, self.age_ranges["middle_aged"])
        
        return random.randint(selected_range[0], selected_range[1])
    
    def _generate_conditions(self, cohort_params: Dict[str, Any]) -> List[str]:
        """Generate medical conditions for patient"""
        conditions = []
        
        # Primary conditions from parameters
        target_conditions = cohort_params.get("target_conditions", [])
        if target_conditions:
            # Each patient has a high chance of having the target condition(s)
            for condition in target_conditions:
                if random.random() < 0.8:  # 80% chance
                    conditions.append(condition)
        
        # Comorbidities
        comorbidities = cohort_params.get("comorbidities", [])
        for comorbidity in comorbidities:
            if random.random() < 0.3:  # 30% chance
                conditions.append(comorbidity)
        
        # Additional random conditions
        additional_conditions = random.sample(
            self.common_conditions, 
            k=min(random.randint(0, 3), len(self.common_conditions))
        )
        conditions.extend(additional_conditions)
        
        # Remove duplicates and return
        return list(set(conditions))
    
    def _generate_medications(self, cohort_params: Dict[str, Any], conditions: List[str]) -> List[str]:
        """Generate medications based on conditions"""
        medications = []
        
        # Medications from parameters
        key_meds = cohort_params.get("key_medications", [])
        medications.extend(key_meds)
        
        # Condition-specific medications
        condition_med_map = {
            "Hypertension": ["Lisinopril", "Amlodipine", "Metoprolol"],
            "Diabetes Mellitus Type 2": ["Metformin", "Insulin", "Glipizide"],
            "Hyperlipidemia": ["Atorvastatin", "Simvastatin"],
            "Depression": ["Sertraline", "Escitalopram"],
            "COPD": ["Albuterol", "Tiotropium"]
        }
        
        for condition in conditions:
            if condition in condition_med_map:
                # Choose 1-2 medications for each condition
                condition_meds = random.sample(
                    condition_med_map[condition],
                    k=min(random.randint(1, 2), len(condition_med_map[condition]))
                )
                medications.extend(condition_meds)
        
        # Remove duplicates
        return list(set(medications))
    
    def _generate_lab_results(self, conditions: List[str], age: int, gender: str) -> Dict[str, tuple]:
        """Generate lab results based on conditions and demographics"""
        lab_results = {}
        
        # Generate basic labs for everyone
        basic_labs = ["glucose", "hemoglobin", "creatinine"]
        
        # Condition-specific labs
        if "Diabetes Mellitus Type 2" in conditions:
            basic_labs.extend(["glucose"])  # More focus on glucose
        if "Hyperlipidemia" in conditions or "Coronary Artery Disease" in conditions:
            basic_labs.append("cholesterol")
        if "Hypertension" in conditions:
            basic_labs.extend(["blood_pressure_systolic", "blood_pressure_diastolic"])
        
        # Generate values
        for lab in set(basic_labs):
            if lab in self.lab_references:
                min_val, max_val, unit = self.lab_references[lab]
                
                # Adjust ranges based on conditions
                if lab == "glucose" and "Diabetes Mellitus Type 2" in conditions:
                    min_val = max(min_val, 126)  # Diabetic range
                    max_val = min(max_val + 100, 300)
                elif lab == "cholesterol" and "Hyperlipidemia" in conditions:
                    min_val = max(min_val, 200)  # High cholesterol range
                
                # Generate value with some normal distribution
                value = random.uniform(min_val, max_val)
                lab_results[lab] = (round(value, 1), unit)
        
        return lab_results
    
    def _generate_clinical_notes(self, patient_id: str, age: int, gender: str, 
                                conditions: List[str], medications: List[str]) -> List[Dict[str, str]]:
        """Generate synthetic clinical notes using LLM"""
        notes = []
        
        # Generate different types of notes
        note_types = ["Initial Consultation", "Follow-up Visit", "Discharge Summary"]
        
        for note_type in note_types:
            prompt = f"""
            Generate a realistic clinical note for a {age}-year-old {gender.lower()} patient.

            Patient ID: {patient_id}
            Conditions: {', '.join(conditions)}
            Current Medications: {', '.join(medications)}
            Note Type: {note_type}

            Write a clinical note that includes:
            - Chief complaint or reason for visit
            - Physical examination findings
            - Assessment and plan
            - Current medication review

            Keep it realistic and professional, around 200-300 words.
            """
            
            try:
                note_content = self.ollama_client.generate_text(prompt)
                
                # Generate note metadata
                note_date = datetime.now() - timedelta(days=random.randint(1, 365))
                provider = random.choice([
                    "Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown", "Dr. Davis"
                ])
                
                notes.append({
                    "type": note_type,
                    "date": note_date.strftime("%Y-%m-%d"),
                    "provider": provider,
                    "content": note_content
                })
                
            except Exception as e:
                print(f"Error generating clinical note: {e}")
                # Fallback note
                notes.append({
                    "type": note_type,
                    "date": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
                    "provider": "Dr. System",
                    "content": f"Standard {note_type.lower()} for patient with {', '.join(conditions[:2])}."
                })
        
        return notes
    
    def _sample_from_distribution(self, distribution: Dict[str, float]) -> str:
        """Sample from a probability distribution"""
        items = list(distribution.keys())
        weights = list(distribution.values())
        
        # Normalize weights
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        
        return random.choices(items, weights=weights)[0]
    
    def _weighted_choice(self, choices: List[tuple]) -> Any:
        """Make a weighted random choice"""
        items, weights = zip(*choices)
        return random.choices(items, weights=weights)[0]
    
    def validate_cohort_realism(self, cohort: PatientCohort, literature_context: Optional[str] = None) -> Dict[str, Any]:
        """Validate the realism of a generated cohort"""
        validation_results = {
            "demographic_distribution": self._validate_demographics(cohort),
            "condition_prevalence": self._validate_condition_prevalence(cohort),
            "medication_appropriateness": self._validate_medications(cohort),
            "overall_score": 0.0,
            "recommendations": []
        }
        
        # Calculate overall score
        scores = [
            validation_results["demographic_distribution"]["score"],
            validation_results["condition_prevalence"]["score"],
            validation_results["medication_appropriateness"]["score"]
        ]
        validation_results["overall_score"] = sum(scores) / len(scores)
        
        return validation_results
    
    def _validate_demographics(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Validate demographic distribution"""
        ages = [p.age for p in cohort.patients if p.age]
        genders = [p.gender for p in cohort.patients if p.gender]
        
        # Check age distribution
        avg_age = sum(ages) / len(ages) if ages else 0
        age_score = 1.0 if 20 <= avg_age <= 80 else 0.7
        
        # Check gender distribution
        if genders:
            female_ratio = sum(1 for g in genders if g.lower() == 'female') / len(genders)
            gender_score = 1.0 if 0.3 <= female_ratio <= 0.7 else 0.8
        else:
            gender_score = 0.5
        
        return {
            "score": (age_score + gender_score) / 2,
            "details": {
                "average_age": avg_age,
                "gender_distribution": dict(pd.Series(genders).value_counts()) if genders else {}
            }
        }
    
    def _validate_condition_prevalence(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Validate condition prevalence"""
        all_conditions = []
        for patient in cohort.patients:
            all_conditions.extend(patient.conditions)
        
        if not all_conditions:
            return {"score": 0.0, "details": {"message": "No conditions found"}}
        
        condition_counts = {}
        for condition in all_conditions:
            condition_counts[condition] = condition_counts.get(condition, 0) + 1
        
        # Simple prevalence check - no condition should dominate too much
        max_prevalence = max(condition_counts.values()) / len(cohort.patients)
        prevalence_score = 1.0 if max_prevalence <= 0.9 else 0.7
        
        return {
            "score": prevalence_score,
            "details": {
                "condition_counts": condition_counts,
                "max_prevalence": max_prevalence
            }
        }
    
    def _validate_medications(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Validate medication appropriateness"""
        appropriate_pairs = 0
        total_pairs = 0
        
        # Simple validation: check if diabetes patients have diabetes medications
        diabetes_meds = ["Metformin", "Insulin", "Glipizide"]
        hypertension_meds = ["Lisinopril", "Amlodipine", "Metoprolol"]
        
        for patient in cohort.patients:
            if "Diabetes Mellitus Type 2" in patient.conditions:
                total_pairs += 1
                if any(med in patient.medications for med in diabetes_meds):
                    appropriate_pairs += 1
            
            if "Hypertension" in patient.conditions:
                total_pairs += 1
                if any(med in patient.medications for med in hypertension_meds):
                    appropriate_pairs += 1
        
        appropriateness_score = appropriate_pairs / total_pairs if total_pairs > 0 else 1.0
        
        return {
            "score": appropriateness_score,
            "details": {
                "appropriate_pairs": appropriate_pairs,
                "total_pairs": total_pairs
            }
        }
