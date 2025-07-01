"""
Cohort generation agents integrated from your comprehensive backend
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List
from .base_agent import BaseIntegratedAgent

class DemographicModeler(BaseIntegratedAgent):
    """Generate realistic demographics for patient cohorts"""
    
    def __init__(self):
        super().__init__("DemographicModeler")
        self.config = {
            "age_distribution": [(0, 18), (19, 40), (41, 65), (66, 90)],
            "age_weights": [0.1, 0.35, 0.35, 0.2],
            "sex_distribution": ["male", "female"],
            "sex_weights": [0.49, 0.51],
            "race_distribution": ["White", "Black", "Asian", "Hispanic", "Other"],
            "race_weights": [0.6, 0.13, 0.06, 0.18, 0.03]
        }
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data, ["population_size"])
        
        population_size = input_data["population_size"]
        condition = input_data.get("condition", "general")
        
        patients = []
        logs = []
        
        for i in range(population_size):
            # Sample age
            age_bucket = random.choices(
                self.config["age_distribution"],
                weights=self.config["age_weights"],
                k=1
            )[0]
            age = random.randint(age_bucket[0], age_bucket[1])
            
            # Sample sex and race
            sex = random.choices(self.config["sex_distribution"], weights=self.config["sex_weights"], k=1)[0]
            race = random.choices(self.config["race_distribution"], weights=self.config["race_weights"], k=1)[0]
            
            patient = {
                "patient_id": str(uuid.uuid4()),
                "age": age,
                "sex": sex,
                "race": race,
                "ethnicity": "Not Hispanic" if random.random() > 0.3 else "Hispanic",
                "condition": condition,
                "generated_by": "DemographicModeler"
            }
            patients.append(patient)
        
        logs.append(f"Generated demographics for {len(patients)} patients")
        logs.append(f"Age distribution: {dict(zip(['0-18', '19-40', '41-65', '66-90'], self.config['age_weights']))}")
        
        return {
            "output": {
                "patients": patients,
                "demographics_generated": len(patients)
            },
            "log": "\n".join(logs)
        }

class ClinicalJourneySimulator(BaseIntegratedAgent):
    """Simulate realistic clinical encounters and patient journeys"""
    
    def __init__(self):
        super().__init__("ClinicalJourneySimulator")
        self.config = {
            "min_visits": 2,
            "max_visits": 6,
            "visit_types": ["primary_care", "specialist", "emergency", "inpatient"],
            "visit_weights": [0.4, 0.3, 0.2, 0.1],
            "start_date_range_days": 180
        }
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data, ["patients"])
        
        patients = input_data["patients"]
        condition = input_data.get("condition", "general")
        
        encounters = []
        logs = []
        
        for patient in patients:
            visit_count = random.randint(self.config["min_visits"], self.config["max_visits"])
            today = datetime.utcnow()
            first_visit_date = today - timedelta(days=random.randint(0, self.config["start_date_range_days"]))
            
            patient_encounters = []
            for i in range(visit_count):
                visit_date = first_visit_date + timedelta(days=random.randint(14, 90) * i)
                visit_type = random.choices(
                    self.config["visit_types"], 
                    weights=self.config["visit_weights"], 
                    k=1
                )[0]
                
                encounter = {
                    "encounter_id": str(uuid.uuid4()),
                    "patient_id": patient["patient_id"],
                    "type": visit_type,
                    "date": visit_date,
                    "reason": condition,
                    "status": "finished" if visit_date < today else "planned",
                    "location": {
                        "facility": "Synthetic Medical Center",
                        "department": visit_type.replace("_", " ").title()
                    }
                }
                patient_encounters.append(encounter)
                encounters.append(encounter)
            
            logs.append(f"Generated {len(patient_encounters)} encounters for patient {patient['patient_id'][:8]}")
        
        return {
            "output": {
                "encounters": encounters,
                "encounters_generated": len(encounters)
            },
            "log": "\n".join(logs)
        }

class ComorbidityModeler(BaseIntegratedAgent):
    """Model realistic comorbidities based on primary condition and demographics"""
    
    def __init__(self):
        super().__init__("ComorbidityModeler")
        self.comorbidity_rules = {
            "hypertension": {
                "common": ["diabetes", "hyperlipidemia", "obesity"],
                "weights": [0.4, 0.3, 0.5],
                "age_factor": 1.2  # Higher chance with age
            },
            "diabetes": {
                "common": ["hypertension", "hyperlipidemia", "neuropathy"],
                "weights": [0.6, 0.4, 0.3],
                "age_factor": 1.1
            },
            "heart_failure": {
                "common": ["hypertension", "diabetes", "atrial_fibrillation"],
                "weights": [0.7, 0.4, 0.3],
                "age_factor": 1.3
            }
        }
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data, ["patients"])
        
        patients = input_data["patients"]
        condition = input_data.get("condition", "general")
        
        updated_patients = []
        logs = []
        
        for patient in patients:
            comorbidities = []
            
            if condition.lower() in self.comorbidity_rules:
                rules = self.comorbidity_rules[condition.lower()]
                age_multiplier = rules["age_factor"] if patient["age"] > 50 else 1.0
                
                for comorbidity, base_prob in zip(rules["common"], rules["weights"]):
                    adjusted_prob = base_prob * age_multiplier
                    if random.random() < adjusted_prob:
                        comorbidities.append({
                            "condition": comorbidity,
                            "onset_date": datetime.utcnow() - timedelta(days=random.randint(30, 1095)),  # 1 month to 3 years ago
                            "severity": random.choice(["mild", "moderate", "severe"]),
                            "status": "active"
                        })
            
            # Add random additional comorbidities based on age
            if patient["age"] > 65 and random.random() < 0.3:
                additional_conditions = ["osteoarthritis", "depression", "anxiety"]
                comorbidities.append({
                    "condition": random.choice(additional_conditions),
                    "onset_date": datetime.utcnow() - timedelta(days=random.randint(180, 2190)),
                    "severity": random.choice(["mild", "moderate"]),
                    "status": "active"
                })
            
            patient_copy = patient.copy()
            patient_copy["comorbidities"] = comorbidities
            updated_patients.append(patient_copy)
            
            if comorbidities:
                logs.append(f"Patient {patient['patient_id'][:8]}: Added {len(comorbidities)} comorbidities")
        
        return {
            "output": {
                "patients": updated_patients,
                "comorbidities_modeled": sum(len(p.get("comorbidities", [])) for p in updated_patients)
            },
            "log": "\n".join(logs) or "No comorbidities added based on current rules"
        }

class MedicationPlanner(BaseIntegratedAgent):
    """Generate realistic medication regimens"""
    
    def __init__(self):
        super().__init__("MedicationPlanner")
        self.medication_protocols = {
            "hypertension": [
                {"name": "Lisinopril", "dose": "10mg", "frequency": "daily", "category": "ACE inhibitor"},
                {"name": "Amlodipine", "dose": "5mg", "frequency": "daily", "category": "Calcium channel blocker"},
                {"name": "Hydrochlorothiazide", "dose": "25mg", "frequency": "daily", "category": "Diuretic"}
            ],
            "diabetes": [
                {"name": "Metformin", "dose": "500mg", "frequency": "twice daily", "category": "Biguanide"},
                {"name": "Insulin glargine", "dose": "20 units", "frequency": "daily", "category": "Long-acting insulin"},
                {"name": "Glipizide", "dose": "5mg", "frequency": "daily", "category": "Sulfonylurea"}
            ],
            "heart_failure": [
                {"name": "Enalapril", "dose": "5mg", "frequency": "twice daily", "category": "ACE inhibitor"},
                {"name": "Metoprolol", "dose": "25mg", "frequency": "twice daily", "category": "Beta blocker"},
                {"name": "Furosemide", "dose": "40mg", "frequency": "daily", "category": "Loop diuretic"}
            ]
        }
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data, ["patients"])
        
        patients = input_data["patients"]
        condition = input_data.get("condition", "general")
        
        updated_patients = []
        total_medications = 0
        logs = []
        
        for patient in patients:
            medications = []
            
            # Primary condition medications
            if condition.lower() in self.medication_protocols:
                available_meds = self.medication_protocols[condition.lower()]
                # Select 1-3 medications for primary condition
                selected_count = random.randint(1, min(3, len(available_meds)))
                selected_meds = random.sample(available_meds, selected_count)
                
                for med in selected_meds:
                    medication = {
                        "name": med["name"],
                        "dose": med["dose"],
                        "frequency": med["frequency"],
                        "category": med["category"],
                        "indication": condition,
                        "start_date": datetime.utcnow() - timedelta(days=random.randint(30, 365)),
                        "status": "active"
                    }
                    medications.append(medication)
            
            # Comorbidity medications
            for comorbidity in patient.get("comorbidities", []):
                comorbidity_condition = comorbidity["condition"]
                if comorbidity_condition in self.medication_protocols:
                    available_meds = self.medication_protocols[comorbidity_condition]
                    selected_med = random.choice(available_meds)
                    
                    medication = {
                        "name": selected_med["name"],
                        "dose": selected_med["dose"],
                        "frequency": selected_med["frequency"],
                        "category": selected_med["category"],
                        "indication": comorbidity_condition,
                        "start_date": comorbidity["onset_date"] + timedelta(days=random.randint(7, 90)),
                        "status": "active"
                    }
                    medications.append(medication)
            
            patient_copy = patient.copy()
            patient_copy["medications"] = medications
            updated_patients.append(patient_copy)
            total_medications += len(medications)
            
            if medications:
                logs.append(f"Patient {patient['patient_id'][:8]}: {len(medications)} medications prescribed")
        
        return {
            "output": {
                "patients": updated_patients,
                "medications_prescribed": total_medications
            },
            "log": "\n".join(logs) or "No medications prescribed"
        }

class LabGenerator(BaseIntegratedAgent):
    """Generate realistic lab values and test results"""
    
    def __init__(self):
        super().__init__("LabGenerator")
        self.lab_panels = {
            "basic_metabolic": [
                {"name": "Glucose", "unit": "mg/dL", "normal_range": (70, 100), "condition_modifier": {"diabetes": 1.5}},
                {"name": "Creatinine", "unit": "mg/dL", "normal_range": (0.6, 1.2), "condition_modifier": {"heart_failure": 1.2}},
                {"name": "Sodium", "unit": "mEq/L", "normal_range": (136, 145), "condition_modifier": {}},
                {"name": "Potassium", "unit": "mEq/L", "normal_range": (3.5, 5.0), "condition_modifier": {}}
            ],
            "lipid_panel": [
                {"name": "Total Cholesterol", "unit": "mg/dL", "normal_range": (125, 200), "condition_modifier": {"hyperlipidemia": 1.3}},
                {"name": "HDL", "unit": "mg/dL", "normal_range": (40, 60), "condition_modifier": {"hyperlipidemia": 0.8}},
                {"name": "LDL", "unit": "mg/dL", "normal_range": (50, 100), "condition_modifier": {"hyperlipidemia": 1.4}},
                {"name": "Triglycerides", "unit": "mg/dL", "normal_range": (50, 150), "condition_modifier": {"diabetes": 1.2}}
            ],
            "hba1c": [
                {"name": "HbA1c", "unit": "%", "normal_range": (4.0, 5.6), "condition_modifier": {"diabetes": 1.5}}
            ]
        }
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data, ["patients", "encounters"])
        
        patients = input_data["patients"]
        encounters = input_data["encounters"]
        condition = input_data.get("condition", "general")
        
        lab_results = []
        logs = []
        
        for patient in patients:
            patient_encounters = [e for e in encounters if e["patient_id"] == patient["patient_id"]]
            
            # Generate labs for some encounters
            lab_encounters = random.sample(patient_encounters, min(2, len(patient_encounters)))
            
            for encounter in lab_encounters:
                # Determine lab panels to order
                panels_to_order = ["basic_metabolic"]
                
                # Add condition-specific panels
                if condition.lower() == "diabetes" or any(c["condition"] == "diabetes" for c in patient.get("comorbidities", [])):
                    panels_to_order.append("hba1c")
                
                if any(c["condition"] in ["hyperlipidemia", "hypertension"] for c in patient.get("comorbidities", [])):
                    panels_to_order.append("lipid_panel")
                
                for panel_name in panels_to_order:
                    if panel_name in self.lab_panels:
                        for lab_test in self.lab_panels[panel_name]:
                            # Calculate value with condition modifiers
                            base_min, base_max = lab_test["normal_range"]
                            modifier = 1.0
                            
                            # Apply condition modifiers
                            patient_conditions = [condition] + [c["condition"] for c in patient.get("comorbidities", [])]
                            for patient_condition in patient_conditions:
                                if patient_condition in lab_test["condition_modifier"]:
                                    modifier *= lab_test["condition_modifier"][patient_condition]
                            
                            # Generate value with some randomness
                            adjusted_min = base_min * modifier * random.uniform(0.8, 1.0)
                            adjusted_max = base_max * modifier * random.uniform(1.0, 1.2)
                            value = round(random.uniform(adjusted_min, adjusted_max), 2)
                            
                            lab_result = {
                                "lab_id": str(uuid.uuid4()),
                                "patient_id": patient["patient_id"],
                                "encounter_id": encounter["encounter_id"],
                                "test_name": lab_test["name"],
                                "value": value,
                                "unit": lab_test["unit"],
                                "normal_range": f"{base_min}-{base_max}",
                                "status": "final",
                                "ordered_date": encounter["date"],
                                "result_date": encounter["date"] + timedelta(hours=random.randint(2, 24))
                            }
                            lab_results.append(lab_result)
        
        logs.append(f"Generated {len(lab_results)} lab results")
        logs.append(f"Lab panels ordered: {set(panels_to_order)}")
        
        return {
            "output": {
                "lab_results": lab_results,
                "labs_generated": len(lab_results)
            },
            "log": "\n".join(logs)
        }

class VitalSignsGenerator(BaseIntegratedAgent):
    """Generate realistic vital signs for encounters"""
    
    def __init__(self):
        super().__init__("VitalSignsGenerator")
        self.vital_ranges = {
            "blood_pressure_systolic": {"normal": (90, 120), "hypertension": (140, 180)},
            "blood_pressure_diastolic": {"normal": (60, 80), "hypertension": (90, 110)},
            "heart_rate": {"normal": (60, 100), "heart_failure": (80, 110)},
            "temperature": {"normal": (97.0, 99.5), "infection": (100.0, 103.0)},
            "respiratory_rate": {"normal": (12, 20), "heart_failure": (16, 24)},
            "oxygen_saturation": {"normal": (95, 100), "heart_failure": (88, 95)}
        }
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data, ["patients", "encounters"])
        
        patients = input_data["patients"]
        encounters = input_data["encounters"]
        condition = input_data.get("condition", "general")
        
        vital_signs = []
        logs = []
        
        patient_lookup = {p["patient_id"]: p for p in patients}
        
        for encounter in encounters:
            patient = patient_lookup.get(encounter["patient_id"])
            if not patient:
                continue
            
            # Generate vital signs for this encounter
            encounter_vitals = {
                "vitals_id": str(uuid.uuid4()),
                "patient_id": encounter["patient_id"],
                "encounter_id": encounter["encounter_id"],
                "measurement_time": encounter["date"],
                "measurements": {}
            }
            
            # Determine which ranges to use based on conditions
            patient_conditions = [condition.lower()] + [c["condition"].lower() for c in patient.get("comorbidities", [])]
            
            for vital_name, ranges in self.vital_ranges.items():
                # Use condition-specific range if available
                selected_range = ranges.get("normal")
                for patient_condition in patient_conditions:
                    if patient_condition in ranges:
                        selected_range = ranges[patient_condition]
                        break
                
                # Generate value with age adjustments
                min_val, max_val = selected_range
                if vital_name == "blood_pressure_systolic" and patient["age"] > 65:
                    min_val += 10
                    max_val += 20
                
                value = round(random.uniform(min_val, max_val), 1)
                encounter_vitals["measurements"][vital_name] = {
                    "value": value,
                    "unit": self._get_vital_unit(vital_name)
                }
            
            vital_signs.append(encounter_vitals)
        
        logs.append(f"Generated vital signs for {len(vital_signs)} encounters")
        
        return {
            "output": {
                "vital_signs": vital_signs,
                "vitals_generated": len(vital_signs)
            },
            "log": "\n".join(logs)
        }
    
    def _get_vital_unit(self, vital_name: str) -> str:
        """Get the appropriate unit for a vital sign"""
        units = {
            "blood_pressure_systolic": "mmHg",
            "blood_pressure_diastolic": "mmHg",
            "heart_rate": "bpm",
            "temperature": "°F",
            "respiratory_rate": "breaths/min",
            "oxygen_saturation": "%"
        }
        return units.get(vital_name, "")