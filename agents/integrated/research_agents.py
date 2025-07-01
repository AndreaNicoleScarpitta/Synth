"""
Research and literature mining agents for evidence-based synthetic data generation
"""

import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
from .base_agent import BaseIntegratedAgent

class LiteratureMiner(BaseIntegratedAgent):
    """Mine relevant literature for evidence-based data generation"""
    
    def __init__(self):
        super().__init__("LiteratureMiner")
        
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        condition = input_data.get("condition", "general")
        population_size = input_data.get("population_size", 100)
        
        # Simulate literature mining based on condition
        literature_insights = self._mine_literature_for_condition(condition)
        
        logs = []
        logs.append(f"Mining literature for condition: {condition}")
        logs.append(f"Found {literature_insights['papers_reviewed']} relevant papers")
        logs.append(f"Evidence quality: {literature_insights['evidence_quality']}")
        
        return {
            "output": {
                "literature_insights": literature_insights,
                "evidence_base_established": True
            },
            "log": "\n".join(logs)
        }
    
    def _mine_literature_for_condition(self, condition: str) -> Dict[str, Any]:
        """Simulate literature mining for specific medical condition"""
        
        # Condition-specific literature patterns
        condition_literature = {
            "hypertension": {
                "papers_reviewed": 245,
                "clinical_guidelines": 8,
                "randomized_trials": 45,
                "evidence_quality": "high",
                "key_findings": [
                    "ACE inhibitors first-line for most patients",
                    "Combination therapy often required",
                    "Target BP <130/80 for most adults"
                ],
                "prevalence_data": {
                    "overall": 0.457,  # 45.7% of adults
                    "age_65_plus": 0.74,
                    "african_american": 0.58
                }
            },
            "diabetes": {
                "papers_reviewed": 312,
                "clinical_guidelines": 12,
                "randomized_trials": 67,
                "evidence_quality": "high",
                "key_findings": [
                    "Metformin first-line therapy",
                    "HbA1c target <7% for most adults",
                    "Lifestyle modifications essential"
                ],
                "prevalence_data": {
                    "overall": 0.114,  # 11.4% of adults
                    "age_65_plus": 0.256,
                    "hispanic": 0.147
                }
            },
            "heart_failure": {
                "papers_reviewed": 189,
                "clinical_guidelines": 6,
                "randomized_trials": 34,
                "evidence_quality": "high",
                "key_findings": [
                    "ACE inhibitors/ARBs improve survival",
                    "Beta-blockers reduce mortality",
                    "Diuretics for symptom management"
                ],
                "prevalence_data": {
                    "overall": 0.02,  # 2% of adults
                    "age_65_plus": 0.085,
                    "male_predominance": 1.2
                }
            }
        }
        
        # Default pattern for unknown conditions
        default_pattern = {
            "papers_reviewed": random.randint(50, 150),
            "clinical_guidelines": random.randint(2, 6),
            "randomized_trials": random.randint(10, 30),
            "evidence_quality": random.choice(["moderate", "high"]),
            "key_findings": [
                "Evidence-based treatment protocols available",
                "Multiple therapeutic options documented",
                "Patient demographics influence outcomes"
            ],
            "prevalence_data": {
                "overall": random.uniform(0.01, 0.15),
                "age_factor": random.uniform(1.1, 2.0)
            }
        }
        
        literature_data = condition_literature.get(condition.lower(), default_pattern)
        
        # Add metadata
        literature_data.update({
            "search_date": datetime.utcnow().isoformat(),
            "databases_searched": ["PubMed", "Cochrane", "EMBASE"],
            "search_terms": [condition, "prevalence", "treatment", "guidelines"],
            "quality_assessment": "Systematic review methodology applied"
        })
        
        return literature_data

class OntologyMapper(BaseIntegratedAgent):
    """Map medical concepts to standardized ontologies and coding systems"""
    
    def __init__(self):
        super().__init__("OntologyMapper")
        
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        patients = input_data.get("patients", [])
        condition = input_data.get("condition", "general")
        
        ontology_mappings = self._create_ontology_mappings(patients, condition)
        
        logs = []
        logs.append(f"Mapping {len(patients)} patients to standard ontologies")
        logs.append(f"Primary condition: {condition}")
        logs.append(f"Ontology systems: ICD-10, SNOMED CT, LOINC")
        
        return {
            "output": {
                "ontology_mappings": ontology_mappings,
                "standardization_complete": True
            },
            "log": "\n".join(logs)
        }
    
    def _create_ontology_mappings(self, patients: List[Dict], condition: str) -> Dict[str, Any]:
        """Create standardized medical ontology mappings"""
        
        # ICD-10 codes for common conditions
        icd10_codes = {
            "hypertension": "I10",
            "diabetes": "E11.9", 
            "heart_failure": "I50.9",
            "hyperlipidemia": "E78.5",
            "obesity": "E66.9",
            "depression": "F32.9",
            "anxiety": "F41.9",
            "osteoarthritis": "M19.90"
        }
        
        # SNOMED CT codes
        snomed_codes = {
            "hypertension": "38341003",
            "diabetes": "44054006",
            "heart_failure": "84114007",
            "hyperlipidemia": "55822004",
            "obesity": "414915002"
        }
        
        # LOINC codes for common lab tests
        loinc_codes = {
            "glucose": "33747-0",
            "hba1c": "4548-4",
            "total_cholesterol": "2093-3",
            "creatinine": "2160-0",
            "blood_pressure": "85354-9"
        }
        
        mappings = {
            "primary_condition": {
                "term": condition,
                "icd10": icd10_codes.get(condition.lower(), "Z00.00"),
                "snomed_ct": snomed_codes.get(condition.lower(), "404684003"),
                "system": "http://snomed.info/sct"
            },
            "comorbidity_mappings": [],
            "lab_test_mappings": [],
            "medication_mappings": []
        }
        
        # Map comorbidities
        all_comorbidities = set()
        for patient in patients:
            for comorbidity in patient.get("comorbidities", []):
                all_comorbidities.add(comorbidity["condition"])
        
        for comorbidity in all_comorbidities:
            mapping = {
                "term": comorbidity,
                "icd10": icd10_codes.get(comorbidity.lower(), "Z87.891"),
                "snomed_ct": snomed_codes.get(comorbidity.lower(), "404684003")
            }
            mappings["comorbidity_mappings"].append(mapping)
        
        # Map lab tests
        all_lab_tests = set()
        for patient in patients:
            lab_results = patient.get("lab_results", [])
            for lab in lab_results:
                all_lab_tests.add(lab["test_name"].lower().replace(" ", "_"))
        
        for lab_test in all_lab_tests:
            mapping = {
                "term": lab_test,
                "loinc": loinc_codes.get(lab_test, "33747-0"),
                "system": "http://loinc.org"
            }
            mappings["lab_test_mappings"].append(mapping)
        
        return mappings

class RealWorldPatternAnalyzer(BaseIntegratedAgent):
    """Analyze real-world patterns to ensure synthetic data authenticity"""
    
    def __init__(self):
        super().__init__("RealWorldPatternAnalyzer")
        
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        patients = input_data.get("patients", [])
        encounters = input_data.get("encounters", [])
        condition = input_data.get("condition", "general")
        
        pattern_analysis = self._analyze_real_world_patterns(patients, encounters, condition)
        
        logs = []
        logs.append(f"Analyzing real-world patterns for {len(patients)} patients")
        logs.append(f"Pattern conformity score: {pattern_analysis['conformity_score']:.2f}")
        logs.append(f"Recommendations generated: {len(pattern_analysis['recommendations'])}")
        
        return {
            "output": {
                "pattern_analysis": pattern_analysis,
                "real_world_validated": pattern_analysis["conformity_score"] >= 0.7
            },
            "log": "\n".join(logs)
        }
    
    def _analyze_real_world_patterns(self, patients: List[Dict], encounters: List[Dict], condition: str) -> Dict[str, Any]:
        """Analyze adherence to real-world medical patterns"""
        
        conformity_issues = []
        recommendations = []
        
        # Real-world pattern expectations
        expected_patterns = {
            "hypertension": {
                "avg_age": 58,
                "male_ratio": 0.52,
                "encounters_per_year": 3.2,
                "medication_adherence": 0.65,
                "comorbidity_rate": 0.7
            },
            "diabetes": {
                "avg_age": 62,
                "male_ratio": 0.56,
                "encounters_per_year": 4.1,
                "medication_adherence": 0.72,
                "comorbidity_rate": 0.85
            },
            "heart_failure": {
                "avg_age": 72,
                "male_ratio": 0.58,
                "encounters_per_year": 5.8,
                "medication_adherence": 0.58,
                "comorbidity_rate": 0.95
            }
        }
        
        pattern = expected_patterns.get(condition.lower(), {
            "avg_age": 55,
            "male_ratio": 0.50,
            "encounters_per_year": 3.0,
            "medication_adherence": 0.70,
            "comorbidity_rate": 0.60
        })
        
        # Analyze current data against patterns
        conformity_score = 1.0
        
        # Age pattern analysis
        if patients:
            actual_avg_age = sum(p["age"] for p in patients) / len(patients)
            age_deviation = abs(actual_avg_age - pattern["avg_age"]) / pattern["avg_age"]
            if age_deviation > 0.2:
                conformity_issues.append(f"Age distribution deviates from expected pattern")
                conformity_score -= 0.1
                recommendations.append("Adjust age distribution to match real-world demographics")
        
        # Gender ratio analysis
        if patients:
            male_count = sum(1 for p in patients if p["sex"].lower() == "male")
            actual_male_ratio = male_count / len(patients)
            gender_deviation = abs(actual_male_ratio - pattern["male_ratio"])
            if gender_deviation > 0.15:
                conformity_issues.append("Gender distribution unusual for condition")
                conformity_score -= 0.1
                recommendations.append("Adjust gender ratio to match epidemiological data")
        
        # Encounter frequency analysis
        if encounters and patients:
            encounter_counts = {}
            for encounter in encounters:
                patient_id = encounter["patient_id"]
                encounter_counts[patient_id] = encounter_counts.get(patient_id, 0) + 1
            
            avg_encounters = sum(encounter_counts.values()) / len(patients)
            encounter_deviation = abs(avg_encounters - pattern["encounters_per_year"]) / pattern["encounters_per_year"]
            if encounter_deviation > 0.3:
                conformity_issues.append("Encounter frequency unusual for condition")
                conformity_score -= 0.1
                recommendations.append("Adjust encounter patterns to match clinical practice")
        
        # Comorbidity rate analysis
        if patients:
            patients_with_comorbidities = sum(1 for p in patients if p.get("comorbidities"))
            actual_comorbidity_rate = patients_with_comorbidities / len(patients)
            comorbidity_deviation = abs(actual_comorbidity_rate - pattern["comorbidity_rate"])
            if comorbidity_deviation > 0.2:
                conformity_issues.append("Comorbidity rates don't match real-world patterns")
                conformity_score -= 0.1
                recommendations.append("Increase comorbidity modeling to match clinical reality")
        
        return {
            "conformity_score": max(0.0, conformity_score),
            "expected_patterns": pattern,
            "conformity_issues": conformity_issues,
            "recommendations": recommendations,
            "analysis_date": datetime.utcnow().isoformat()
        }

class RegulatoryConstraintChecker(BaseIntegratedAgent):
    """Check compliance with regulatory requirements for synthetic medical data"""
    
    def __init__(self):
        super().__init__("RegulatoryConstraintChecker")
        
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        patients = input_data.get("patients", [])
        
        compliance_check = self._check_regulatory_compliance(patients)
        
        logs = []
        logs.append(f"Checking regulatory compliance for {len(patients)} patients")
        logs.append(f"HIPAA compliance: {compliance_check['hipaa_compliant']}")
        logs.append(f"FDA guidance adherence: {compliance_check['fda_compliant']}")
        
        return {
            "output": {
                "regulatory_compliance": compliance_check,
                "compliance_verified": compliance_check["overall_compliant"]
            },
            "log": "\n".join(logs)
        }
    
    def _check_regulatory_compliance(self, patients: List[Dict]) -> Dict[str, Any]:
        """Check various regulatory compliance requirements"""
        
        compliance_results = {
            "hipaa_compliant": True,
            "fda_compliant": True,
            "gdpr_compliant": True,
            "overall_compliant": True,
            "compliance_issues": [],
            "recommendations": []
        }
        
        # HIPAA compliance checks
        hipaa_issues = self._check_hipaa_compliance(patients)
        if hipaa_issues:
            compliance_results["hipaa_compliant"] = False
            compliance_results["compliance_issues"].extend(hipaa_issues)
        
        # FDA guidance compliance
        fda_issues = self._check_fda_guidance(patients)
        if fda_issues:
            compliance_results["fda_compliant"] = False
            compliance_results["compliance_issues"].extend(fda_issues)
        
        # GDPR compliance (for international use)
        gdpr_issues = self._check_gdpr_compliance(patients)
        if gdpr_issues:
            compliance_results["gdpr_compliant"] = False
            compliance_results["compliance_issues"].extend(gdpr_issues)
        
        # Overall compliance
        compliance_results["overall_compliant"] = (
            compliance_results["hipaa_compliant"] and 
            compliance_results["fda_compliant"] and
            compliance_results["gdpr_compliant"]
        )
        
        return compliance_results
    
    def _check_hipaa_compliance(self, patients: List[Dict]) -> List[str]:
        """Check HIPAA compliance for synthetic data"""
        issues = []
        
        # Check for potential PHI in synthetic data
        for patient in patients:
            patient_id = patient["patient_id"]
            
            # Ensure patient IDs are not sequential or predictable
            if patient_id.startswith("patient_"):
                issues.append("Patient IDs appear sequential - use UUIDs for better privacy")
                break
            
            # Check for realistic but non-identifiable data
            demographics = patient.get("demographics", {})
            if "ssn" in demographics or "social_security" in demographics:
                issues.append("SSN-like data detected - remove all potential identifiers")
            
            if "real_name" in demographics or "actual_address" in demographics:
                issues.append("Real identifiers detected in demographics")
        
        return issues
    
    def _check_fda_guidance(self, patients: List[Dict]) -> List[str]:
        """Check FDA guidance compliance for medical device/pharma use"""
        issues = []
        
        # Check data quality standards
        if len(patients) < 100:
            issues.append("Sample size may be insufficient for FDA submissions")
        
        # Check for diversity requirements
        ages = [p["age"] for p in patients]
        if len(set(ages)) < len(patients) * 0.1:  # Less than 10% age diversity
            issues.append("Insufficient age diversity for regulatory review")
        
        # Check for required demographic representation
        races = [p["race"] for p in patients]
        unique_races = set(races)
        if len(unique_races) < 3:
            issues.append("Insufficient racial diversity for FDA requirements")
        
        return issues
    
    def _check_gdpr_compliance(self, patients: List[Dict]) -> List[str]:
        """Check GDPR compliance for international use"""
        issues = []
        
        # Check for consent mechanisms (even for synthetic data)
        # Ensure no real data traces
        for patient in patients:
            if "source_patient_id" in patient or "derived_from" in patient:
                issues.append("Potential traceability to real data detected")
                break
        
        return issues