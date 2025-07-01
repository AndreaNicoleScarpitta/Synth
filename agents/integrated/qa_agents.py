"""
Quality Assurance and Validation agents for synthetic EHR data
"""

import statistics
import uuid
from datetime import datetime
from typing import Dict, Any, List
from .base_agent import BaseIntegratedAgent

class StatisticalValidator(BaseIntegratedAgent):
    """Validate statistical properties of generated data"""
    
    def __init__(self):
        super().__init__("StatisticalValidator")
        
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data, ["patients"])
        
        patients = input_data["patients"]
        encounters = input_data.get("encounters", [])
        
        validation_results = {}
        logs = []
        
        # Demographic validation
        demographic_stats = self._validate_demographics(patients)
        validation_results["demographics"] = demographic_stats
        logs.append(f"Demographic validation: {demographic_stats['score']:.2f}")
        
        # Clinical consistency validation
        clinical_stats = self._validate_clinical_consistency(patients, encounters)
        validation_results["clinical_consistency"] = clinical_stats
        logs.append(f"Clinical consistency: {clinical_stats['score']:.2f}")
        
        # Temporal validation
        temporal_stats = self._validate_temporal_consistency(encounters)
        validation_results["temporal_consistency"] = temporal_stats
        logs.append(f"Temporal consistency: {temporal_stats['score']:.2f}")
        
        # Overall score
        overall_score = statistics.mean([
            demographic_stats['score'],
            clinical_stats['score'],
            temporal_stats['score']
        ])
        validation_results["overall_score"] = overall_score
        
        return {
            "output": {
                "validation_results": validation_results,
                "validation_passed": overall_score >= 0.7
            },
            "log": "\n".join(logs + [f"Overall validation score: {overall_score:.2f}"])
        }
    
    def _validate_demographics(self, patients: List[Dict]) -> Dict[str, Any]:
        """Validate demographic distributions"""
        if not patients:
            return {"score": 0.0, "issues": ["No patients to validate"]}
        
        ages = [p["age"] for p in patients]
        sexes = [p["sex"] for p in patients]
        races = [p["race"] for p in patients]
        
        issues = []
        score = 1.0
        
        # Age distribution checks
        avg_age = statistics.mean(ages)
        if avg_age < 20 or avg_age > 70:
            issues.append(f"Unusual average age: {avg_age:.1f}")
            score -= 0.2
        
        # Sex distribution checks
        male_ratio = sum(1 for s in sexes if s.lower() == "male") / len(sexes)
        if male_ratio < 0.3 or male_ratio > 0.7:
            issues.append(f"Unusual sex distribution: {male_ratio:.1%} male")
            score -= 0.2
        
        # Race distribution checks
        white_ratio = sum(1 for r in races if r == "White") / len(races)
        if white_ratio > 0.8:
            issues.append("Potential lack of racial diversity")
            score -= 0.1
        
        return {
            "score": max(0.0, score),
            "issues": issues,
            "statistics": {
                "avg_age": avg_age,
                "age_range": [min(ages), max(ages)],
                "male_ratio": male_ratio,
                "race_distribution": {race: races.count(race) for race in set(races)}
            }
        }
    
    def _validate_clinical_consistency(self, patients: List[Dict], encounters: List[Dict]) -> Dict[str, Any]:
        """Validate clinical data consistency"""
        issues = []
        score = 1.0
        
        # Check medication-condition consistency
        for patient in patients:
            medications = patient.get("medications", [])
            comorbidities = patient.get("comorbidities", [])
            
            # Check if diabetes patients have appropriate medications
            has_diabetes = any(c["condition"] == "diabetes" for c in comorbidities)
            has_diabetes_med = any("metformin" in m["name"].lower() or "insulin" in m["name"].lower() for m in medications)
            
            if has_diabetes and not has_diabetes_med:
                issues.append(f"Diabetes patient without appropriate medication: {patient['patient_id'][:8]}")
                score -= 0.1
        
        # Check encounter frequency
        if encounters:
            encounter_counts = {}
            for encounter in encounters:
                patient_id = encounter["patient_id"]
                encounter_counts[patient_id] = encounter_counts.get(patient_id, 0) + 1
            
            avg_encounters = statistics.mean(encounter_counts.values())
            if avg_encounters < 1 or avg_encounters > 10:
                issues.append(f"Unusual encounter frequency: {avg_encounters:.1f} per patient")
                score -= 0.2
        
        return {
            "score": max(0.0, score),
            "issues": issues,
            "statistics": {
                "patients_with_medications": sum(1 for p in patients if p.get("medications")),
                "patients_with_comorbidities": sum(1 for p in patients if p.get("comorbidities")),
                "avg_encounters_per_patient": statistics.mean(encounter_counts.values()) if encounters else 0
            }
        }
    
    def _validate_temporal_consistency(self, encounters: List[Dict]) -> Dict[str, Any]:
        """Validate temporal relationships in data"""
        issues = []
        score = 1.0
        
        if not encounters:
            return {"score": 1.0, "issues": [], "statistics": {}}
        
        # Check for future encounters
        now = datetime.utcnow()
        future_encounters = [e for e in encounters if e["date"] > now]
        
        if len(future_encounters) > len(encounters) * 0.1:  # More than 10% in future
            issues.append(f"{len(future_encounters)} encounters scheduled in future")
            score -= 0.1
        
        # Check encounter spacing
        patient_encounters = {}
        for encounter in encounters:
            patient_id = encounter["patient_id"]
            if patient_id not in patient_encounters:
                patient_encounters[patient_id] = []
            patient_encounters[patient_id].append(encounter["date"])
        
        for patient_id, dates in patient_encounters.items():
            if len(dates) > 1:
                sorted_dates = sorted(dates)
                intervals = [(sorted_dates[i+1] - sorted_dates[i]).days for i in range(len(sorted_dates)-1)]
                
                # Check for unrealistic intervals (same day multiple visits)
                same_day_visits = sum(1 for interval in intervals if interval == 0)
                if same_day_visits > 1:
                    issues.append(f"Patient {patient_id[:8]} has multiple same-day encounters")
                    score -= 0.05
        
        return {
            "score": max(0.0, score),
            "issues": issues,
            "statistics": {
                "total_encounters": len(encounters),
                "future_encounters": len(future_encounters),
                "patients_with_multiple_encounters": len([p for p in patient_encounters.values() if len(p) > 1])
            }
        }

class BiasAuditor(BaseIntegratedAgent):
    """Detect potential bias in synthetic data generation"""
    
    def __init__(self):
        super().__init__("BiasAuditor")
        
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data, ["patients"])
        
        patients = input_data["patients"]
        
        bias_results = {}
        logs = []
        
        # Age bias analysis
        age_bias = self._analyze_age_bias(patients)
        bias_results["age_bias"] = age_bias
        logs.append(f"Age bias score: {age_bias['bias_score']:.3f}")
        
        # Gender bias analysis
        gender_bias = self._analyze_gender_bias(patients)
        bias_results["gender_bias"] = gender_bias
        logs.append(f"Gender bias score: {gender_bias['bias_score']:.3f}")
        
        # Racial bias analysis
        racial_bias = self._analyze_racial_bias(patients)
        bias_results["racial_bias"] = racial_bias
        logs.append(f"Racial bias score: {racial_bias['bias_score']:.3f}")
        
        # Condition bias analysis
        condition_bias = self._analyze_condition_bias(patients)
        bias_results["condition_bias"] = condition_bias
        logs.append(f"Condition bias score: {condition_bias['bias_score']:.3f}")
        
        # Overall bias score
        overall_bias = statistics.mean([
            age_bias['bias_score'],
            gender_bias['bias_score'],
            racial_bias['bias_score'],
            condition_bias['bias_score']
        ])
        bias_results["overall_bias_score"] = overall_bias
        
        return {
            "output": {
                "bias_audit": bias_results,
                "bias_acceptable": overall_bias < 0.3  # Lower is better for bias
            },
            "log": "\n".join(logs + [f"Overall bias score: {overall_bias:.3f}"])
        }
    
    def _analyze_age_bias(self, patients: List[Dict]) -> Dict[str, Any]:
        """Analyze age-related bias patterns"""
        ages = [p["age"] for p in patients]
        
        # Check for age clustering
        age_groups = {
            "young": sum(1 for age in ages if age < 30),
            "middle": sum(1 for age in ages if 30 <= age < 65),
            "elderly": sum(1 for age in ages if age >= 65)
        }
        
        total = len(ages)
        proportions = {k: v/total for k, v in age_groups.items()}
        
        # Calculate bias score (higher variance indicates more bias)
        expected_proportions = {"young": 0.3, "middle": 0.5, "elderly": 0.2}
        bias_score = sum(abs(proportions[k] - expected_proportions[k]) for k in proportions) / 2
        
        return {
            "bias_score": bias_score,
            "age_distribution": proportions,
            "issues": [f"Overrepresented: {k}" for k, v in proportions.items() if v > expected_proportions[k] + 0.1]
        }
    
    def _analyze_gender_bias(self, patients: List[Dict]) -> Dict[str, Any]:
        """Analyze gender-related bias patterns"""
        genders = [p["sex"].lower() for p in patients]
        
        gender_counts = {"male": genders.count("male"), "female": genders.count("female")}
        total = len(genders)
        proportions = {k: v/total for k, v in gender_counts.items()}
        
        # Bias score based on deviation from 50/50
        bias_score = abs(proportions.get("male", 0) - 0.5) * 2
        
        return {
            "bias_score": bias_score,
            "gender_distribution": proportions,
            "issues": ["Significant gender imbalance"] if bias_score > 0.2 else []
        }
    
    def _analyze_racial_bias(self, patients: List[Dict]) -> Dict[str, Any]:
        """Analyze racial representation bias"""
        races = [p["race"] for p in patients]
        
        race_counts = {}
        for race in races:
            race_counts[race] = race_counts.get(race, 0) + 1
        
        total = len(races)
        proportions = {k: v/total for k, v in race_counts.items()}
        
        # Check for overrepresentation of any single race
        max_proportion = max(proportions.values()) if proportions else 0
        bias_score = max(0, max_proportion - 0.7)  # Bias if any race > 70%
        
        return {
            "bias_score": bias_score,
            "racial_distribution": proportions,
            "issues": [f"Overrepresented race: {k}" for k, v in proportions.items() if v > 0.7]
        }
    
    def _analyze_condition_bias(self, patients: List[Dict]) -> Dict[str, Any]:
        """Analyze condition assignment bias"""
        # Analyze comorbidity patterns across demographics
        demographics_with_comorbidities = {}
        
        for patient in patients:
            comorbidity_count = len(patient.get("comorbidities", []))
            
            # Group by age
            age_group = "young" if patient["age"] < 30 else "middle" if patient["age"] < 65 else "elderly"
            if age_group not in demographics_with_comorbidities:
                demographics_with_comorbidities[age_group] = []
            demographics_with_comorbidities[age_group].append(comorbidity_count)
        
        # Calculate bias based on unrealistic patterns
        bias_score = 0.0
        issues = []
        
        # Check if young patients have too many comorbidities
        if "young" in demographics_with_comorbidities:
            young_avg = statistics.mean(demographics_with_comorbidities["young"])
            if young_avg > 1.0:
                bias_score += 0.2
                issues.append("Young patients have excessive comorbidities")
        
        return {
            "bias_score": bias_score,
            "comorbidity_distribution": {k: statistics.mean(v) if v else 0 for k, v in demographics_with_comorbidities.items()},
            "issues": issues
        }

class RealismChecker(BaseIntegratedAgent):
    """Check the realism of generated clinical data"""
    
    def __init__(self):
        super().__init__("RealismChecker")
        
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data, ["patients"])
        
        patients = input_data["patients"]
        encounters = input_data.get("encounters", [])
        lab_results = input_data.get("lab_results", [])
        vital_signs = input_data.get("vital_signs", [])
        
        realism_scores = {}
        logs = []
        
        # Clinical value realism
        if lab_results:
            lab_realism = self._check_lab_realism(lab_results, patients)
            realism_scores["lab_values"] = lab_realism
            logs.append(f"Lab value realism: {lab_realism['score']:.2f}")
        
        # Vital signs realism
        if vital_signs:
            vitals_realism = self._check_vitals_realism(vital_signs, patients)
            realism_scores["vital_signs"] = vitals_realism
            logs.append(f"Vital signs realism: {vitals_realism['score']:.2f}")
        
        # Medication realism
        medication_realism = self._check_medication_realism(patients)
        realism_scores["medications"] = medication_realism
        logs.append(f"Medication realism: {medication_realism['score']:.2f}")
        
        # Encounter pattern realism
        if encounters:
            encounter_realism = self._check_encounter_realism(encounters, patients)
            realism_scores["encounters"] = encounter_realism
            logs.append(f"Encounter realism: {encounter_realism['score']:.2f}")
        
        # Overall realism score
        scores = [score["score"] for score in realism_scores.values()]
        overall_realism = statistics.mean(scores) if scores else 0.0
        
        return {
            "output": {
                "realism_check": realism_scores,
                "overall_realism": overall_realism,
                "realism_acceptable": overall_realism >= 0.7
            },
            "log": "\n".join(logs + [f"Overall realism score: {overall_realism:.2f}"])
        }
    
    def _check_lab_realism(self, lab_results: List[Dict], patients: List[Dict]) -> Dict[str, Any]:
        """Check if lab values are clinically realistic"""
        patient_lookup = {p["patient_id"]: p for p in patients}
        
        realistic_count = 0
        total_count = len(lab_results)
        issues = []
        
        for lab in lab_results:
            patient = patient_lookup.get(lab["patient_id"])
            if not patient:
                continue
            
            test_name = lab["test_name"].lower()
            value = lab["value"]
            
            # Check for impossible values
            if test_name == "glucose" and (value < 20 or value > 800):
                issues.append(f"Impossible glucose value: {value}")
                continue
            elif test_name == "creatinine" and (value < 0.1 or value > 20):
                issues.append(f"Impossible creatinine value: {value}")
                continue
            elif "cholesterol" in test_name and (value < 50 or value > 500):
                issues.append(f"Impossible cholesterol value: {value}")
                continue
            
            realistic_count += 1
        
        score = realistic_count / total_count if total_count > 0 else 1.0
        
        return {
            "score": score,
            "issues": issues[:5],  # Limit to first 5 issues
            "total_labs": total_count,
            "realistic_labs": realistic_count
        }
    
    def _check_vitals_realism(self, vital_signs: List[Dict], patients: List[Dict]) -> Dict[str, Any]:
        """Check if vital signs are clinically realistic"""
        realistic_count = 0
        total_measurements = 0
        issues = []
        
        for vitals in vital_signs:
            measurements = vitals.get("measurements", {})
            
            for vital_name, measurement in measurements.items():
                total_measurements += 1
                value = measurement["value"]
                
                # Check for impossible vital signs
                if vital_name == "heart_rate" and (value < 30 or value > 200):
                    issues.append(f"Impossible heart rate: {value}")
                    continue
                elif vital_name == "blood_pressure_systolic" and (value < 60 or value > 250):
                    issues.append(f"Impossible systolic BP: {value}")
                    continue
                elif vital_name == "temperature" and (value < 90 or value > 110):
                    issues.append(f"Impossible temperature: {value}")
                    continue
                elif vital_name == "oxygen_saturation" and (value < 60 or value > 100):
                    issues.append(f"Impossible oxygen saturation: {value}")
                    continue
                
                realistic_count += 1
        
        score = realistic_count / total_measurements if total_measurements > 0 else 1.0
        
        return {
            "score": score,
            "issues": issues[:5],
            "total_measurements": total_measurements,
            "realistic_measurements": realistic_count
        }
    
    def _check_medication_realism(self, patients: List[Dict]) -> Dict[str, Any]:
        """Check if medication regimens are clinically realistic"""
        realistic_count = 0
        total_patients = len(patients)
        issues = []
        
        for patient in patients:
            medications = patient.get("medications", [])
            comorbidities = patient.get("comorbidities", [])
            
            # Check for drug interactions (simplified)
            drug_names = [med["name"].lower() for med in medications]
            
            # Flag potential issues
            has_insulin = any("insulin" in name for name in drug_names)
            has_metformin = any("metformin" in name for name in drug_names)
            has_diabetes = any(c["condition"] == "diabetes" for c in comorbidities)
            
            if has_diabetes and not (has_insulin or has_metformin):
                issues.append(f"Diabetes patient without diabetes medication: {patient['patient_id'][:8]}")
                continue
            
            realistic_count += 1
        
        score = realistic_count / total_patients if total_patients > 0 else 1.0
        
        return {
            "score": score,
            "issues": issues[:5],
            "total_patients": total_patients,
            "realistic_medication_patterns": realistic_count
        }
    
    def _check_encounter_realism(self, encounters: List[Dict], patients: List[Dict]) -> Dict[str, Any]:
        """Check if encounter patterns are realistic"""
        patient_encounters = {}
        for encounter in encounters:
            patient_id = encounter["patient_id"]
            if patient_id not in patient_encounters:
                patient_encounters[patient_id] = []
            patient_encounters[patient_id].append(encounter)
        
        realistic_patterns = 0
        total_patients = len(patient_encounters)
        issues = []
        
        for patient_id, patient_encounters_list in patient_encounters.items():
            encounter_types = [e["type"] for e in patient_encounters_list]
            
            # Check for realistic encounter progression
            # E.g., shouldn't have inpatient before emergency for same condition
            emergency_count = encounter_types.count("emergency")
            inpatient_count = encounter_types.count("inpatient")
            
            if emergency_count > 3:
                issues.append(f"Patient {patient_id[:8]} has excessive emergency visits: {emergency_count}")
                continue
            
            if inpatient_count > len(patient_encounters_list) / 2:
                issues.append(f"Patient {patient_id[:8]} has excessive inpatient stays")
                continue
            
            realistic_patterns += 1
        
        score = realistic_patterns / total_patients if total_patients > 0 else 1.0
        
        return {
            "score": score,
            "issues": issues[:5],
            "total_patients": total_patients,
            "realistic_patterns": realistic_patterns
        }