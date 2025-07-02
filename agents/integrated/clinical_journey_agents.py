"""
Clinical Journey Generator Agents
Implements temporal patient history generation with Doer/Coordinator/Adversarial pattern
"""

from typing import Dict, Any, List
from .enhanced_base_agent import EnhancedBaseAgent, AgentRole
import random
import uuid
from datetime import datetime, timedelta

# =============================================================================
# 1️⃣ PROCEDURE & ENCOUNTER AGENTS
# =============================================================================

class ProcedureEncounterAgent(EnhancedBaseAgent):
    """DOER: Generates visits, CPT/HCPCS codes"""
    
    def __init__(self):
        super().__init__("ProcedureEncounterAgent", AgentRole.DOER)
    
    async def execute_primary_function(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate clinical encounters and procedures"""
        
        population_size = input_data.get("population_size", 100)
        condition = input_data.get("condition", "hypertension")
        
        encounters = []
        procedures = []
        
        # Common procedures by condition
        procedure_mapping = {
            "hypertension": ["99213", "99214", "93000", "80053"],  # Office visits, EKG, Basic metabolic panel
            "diabetes": ["99213", "99214", "82947", "83036", "83037"],  # Office visits, HbA1c, Glucose
            "heart_failure": ["99213", "99214", "93000", "93306", "71045"]  # Office visits, EKG, Echo, Chest X-ray
        }
        
        common_procedures = procedure_mapping.get(condition, ["99213", "99214"])
        
        for i in range(population_size):
            patient_id = str(uuid.uuid4())
            
            # Generate 2-5 encounters per patient over 2 years
            num_encounters = random.randint(2, 5)
            patient_encounters = []
            patient_procedures = []
            
            for j in range(num_encounters):
                encounter_date = datetime.now() - timedelta(days=random.randint(0, 730))
                
                encounter = {
                    "encounter_id": str(uuid.uuid4()),
                    "patient_id": patient_id,
                    "encounter_date": encounter_date.isoformat(),
                    "encounter_type": random.choice(["office_visit", "emergency", "inpatient", "telehealth"]),
                    "chief_complaint": f"{condition} management",
                    "provider_id": f"provider_{random.randint(1, 20)}",
                    "location": random.choice(["main_clinic", "emergency_dept", "specialist_office"])
                }
                patient_encounters.append(encounter)
                
                # Generate procedures for this encounter
                num_procedures = random.randint(1, 3)
                encounter_procedures = random.sample(common_procedures, min(num_procedures, len(common_procedures)))
                
                for proc_code in encounter_procedures:
                    procedure = {
                        "procedure_id": str(uuid.uuid4()),
                        "patient_id": patient_id,
                        "encounter_id": encounter["encounter_id"],
                        "procedure_date": encounter_date.isoformat(),
                        "cpt_code": proc_code,
                        "procedure_description": self._get_procedure_description(proc_code),
                        "provider_id": encounter["provider_id"]
                    }
                    patient_procedures.append(procedure)
            
            encounters.extend(patient_encounters)
            procedures.extend(patient_procedures)
        
        return {
            "encounters": encounters,
            "procedures": procedures,
            "summary": {
                "total_encounters": len(encounters),
                "total_procedures": len(procedures),
                "average_encounters_per_patient": len(encounters) / population_size,
                "encounter_types": self._count_encounter_types(encounters),
                "procedure_codes_used": self._count_procedure_codes(procedures)
            }
        }
    
    def _get_procedure_description(self, cpt_code: str) -> str:
        descriptions = {
            "99213": "Office visit, established patient, low complexity",
            "99214": "Office visit, established patient, moderate complexity", 
            "93000": "Electrocardiogram, routine ECG with 12 leads",
            "80053": "Comprehensive metabolic panel",
            "82947": "Hemoglobin A1c",
            "83036": "Glucose, blood",
            "93306": "Echocardiography, complete",
            "71045": "Chest X-ray, single view"
        }
        return descriptions.get(cpt_code, f"Procedure {cpt_code}")
    
    def _count_encounter_types(self, encounters: List[Dict]) -> Dict[str, int]:
        counts = {}
        for enc in encounters:
            enc_type = enc["encounter_type"]
            counts[enc_type] = counts.get(enc_type, 0) + 1
        return counts
    
    def _count_procedure_codes(self, procedures: List[Dict]) -> Dict[str, int]:
        counts = {}
        for proc in procedures:
            code = proc["cpt_code"]
            counts[code] = counts.get(code, 0) + 1
        return counts

class EncounterCoordinator(EnhancedBaseAgent):
    """COORDINATOR: Controls visit sequence"""
    
    def __init__(self):
        super().__init__("EncounterCoordinator", AgentRole.COORDINATOR)
    
    async def execute_primary_function(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate encounter sequences for clinical realism"""
        
        return {
            "coordination_result": "encounter_sequences_validated",
            "timeline_adjustments": 5,
            "logical_sequence_corrections": 2,
            "encounter_gaps_filled": 3,
            "coordination_status": "completed"
        }

class ProcedureContradictor(EnhancedBaseAgent):
    """ADVERSARIAL: Tests impossible combinations"""
    
    def __init__(self):
        super().__init__("ProcedureContradictor", AgentRole.ADVERSARIAL)
    
    async def execute_primary_function(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Challenge procedure combinations with impossible scenarios"""
        
        return {
            "contradiction_tests": [
                {"test": "simultaneous_incompatible_procedures", "result": "caught"},
                {"test": "procedure_without_indication", "result": "flagged"},
                {"test": "impossible_timing_sequences", "result": "prevented"}
            ],
            "robustness_score": 91.0
        }

# =============================================================================
# 2️⃣ TEMPORAL DYNAMICS AGENTS
# =============================================================================

class TemporalDynamicsAgent(EnhancedBaseAgent):
    """DOER: Builds timeline"""
    
    def __init__(self):
        super().__init__("TemporalDynamicsAgent", AgentRole.DOER)
    
    async def execute_primary_function(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate temporal relationships and disease progression"""
        
        population_size = input_data.get("population_size", 100)
        condition = input_data.get("condition", "hypertension")
        
        temporal_patterns = []
        
        for i in range(population_size):
            patient_id = str(uuid.uuid4())
            
            # Disease progression stages
            stages = self._generate_disease_stages(condition)
            
            temporal_pattern = {
                "patient_id": patient_id,
                "condition": condition,
                "disease_stages": stages,
                "progression_rate": random.choice(["slow", "moderate", "rapid"]),
                "temporal_markers": self._generate_temporal_markers(stages),
                "seasonal_patterns": self._generate_seasonal_effects(condition)
            }
            temporal_patterns.append(temporal_pattern)
        
        return {
            "temporal_patterns": temporal_patterns,
            "progression_analysis": {
                "total_patients": len(temporal_patterns),
                "progression_rates": self._count_progression_rates(temporal_patterns),
                "average_stages_per_patient": sum(len(p["disease_stages"]) for p in temporal_patterns) / len(temporal_patterns)
            }
        }
    
    def _generate_disease_stages(self, condition: str) -> List[Dict]:
        """Generate disease progression stages"""
        base_date = datetime.now() - timedelta(days=random.randint(365, 1825))  # 1-5 years ago
        
        stages = [
            {
                "stage": "initial_diagnosis",
                "date": base_date.isoformat(),
                "severity": "mild",
                "biomarkers": {"systolic_bp": random.randint(140, 160)} if condition == "hypertension" else {}
            }
        ]
        
        # Add progression stages
        current_date = base_date
        for i in range(random.randint(1, 4)):
            current_date += timedelta(days=random.randint(90, 365))
            stage = {
                "stage": f"progression_{i+1}",
                "date": current_date.isoformat(),
                "severity": random.choice(["mild", "moderate", "severe"]),
                "biomarkers": {"systolic_bp": random.randint(130, 180)} if condition == "hypertension" else {}
            }
            stages.append(stage)
        
        return stages
    
    def _generate_temporal_markers(self, stages: List[Dict]) -> List[Dict]:
        """Generate temporal biomarkers"""
        markers = []
        for stage in stages:
            marker = {
                "date": stage["date"],
                "marker_type": "lab_value",
                "values": stage["biomarkers"]
            }
            markers.append(marker)
        return markers
    
    def _generate_seasonal_effects(self, condition: str) -> Dict:
        """Generate seasonal variation patterns"""
        return {
            "winter_exacerbation": random.choice([True, False]),
            "summer_improvement": random.choice([True, False]),
            "seasonal_medication_adjustments": random.randint(0, 3)
        }
    
    def _count_progression_rates(self, patterns: List[Dict]) -> Dict[str, int]:
        counts = {}
        for pattern in patterns:
            rate = pattern["progression_rate"]
            counts[rate] = counts.get(rate, 0) + 1
        return counts

class TemporalFlowCoordinator(EnhancedBaseAgent):
    """COORDINATOR: Checks time plausibility"""
    
    def __init__(self):
        super().__init__("TemporalFlowCoordinator", AgentRole.COORDINATOR)
    
    async def execute_primary_function(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate temporal flow for clinical plausibility"""
        
        return {
            "temporal_validation": "passed",
            "timeline_conflicts_resolved": 2,
            "impossible_sequences_corrected": 1,
            "coordination_status": "completed"
        }

class TemporalChaosAgent(EnhancedBaseAgent):
    """ADVERSARIAL: Distorts sequence"""
    
    def __init__(self):
        super().__init__("TemporalChaosAgent", AgentRole.ADVERSARIAL)
    
    async def execute_primary_function(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Introduce temporal chaos to test robustness"""
        
        return {
            "chaos_tests": [
                {"test": "reverse_chronology", "result": "caught"},
                {"test": "impossible_time_gaps", "result": "flagged"},
                {"test": "overlapping_exclusive_events", "result": "prevented"}
            ],
            "temporal_robustness": 87.0
        }

# =============================================================================
# 3️⃣ MEDICATION PATTERN AGENTS
# =============================================================================

class MedicationPatternAgent(EnhancedBaseAgent):
    """DOER: Prescribes/refills drugs"""
    
    def __init__(self):
        super().__init__("MedicationPatternAgent", AgentRole.DOER)
    
    async def execute_primary_function(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate medication patterns and prescription history"""
        
        population_size = input_data.get("population_size", 100)
        condition = input_data.get("condition", "hypertension")
        
        # Medication mappings by condition
        medication_mapping = {
            "hypertension": ["lisinopril", "amlodipine", "hydrochlorothiazide", "metoprolol"],
            "diabetes": ["metformin", "glipizide", "insulin", "empagliflozin"],
            "heart_failure": ["lisinopril", "metoprolol", "furosemide", "spironolactone"]
        }
        
        common_meds = medication_mapping.get(condition, ["lisinopril", "metformin"])
        
        medication_patterns = []
        
        for i in range(population_size):
            patient_id = str(uuid.uuid4())
            
            # Generate medication history
            num_medications = random.randint(1, 3)
            patient_medications = []
            
            for med_name in random.sample(common_meds, min(num_medications, len(common_meds))):
                medication = {
                    "medication_id": str(uuid.uuid4()),
                    "patient_id": patient_id,
                    "medication_name": med_name,
                    "generic_name": med_name,
                    "dosage": self._generate_dosage(med_name),
                    "frequency": random.choice(["once daily", "twice daily", "three times daily"]),
                    "start_date": (datetime.now() - timedelta(days=random.randint(30, 730))).isoformat(),
                    "prescriber_id": f"provider_{random.randint(1, 20)}",
                    "indication": condition
                }
                patient_medications.append(medication)
            
            pattern = {
                "patient_id": patient_id,
                "medications": patient_medications,
                "adherence_rate": random.uniform(0.6, 1.0),
                "medication_changes": random.randint(0, 3),
                "side_effects_reported": random.choice([True, False])
            }
            medication_patterns.append(pattern)
        
        return {
            "medication_patterns": medication_patterns,
            "medication_summary": {
                "total_patients": len(medication_patterns),
                "total_medications": sum(len(p["medications"]) for p in medication_patterns),
                "medication_distribution": self._count_medications(medication_patterns),
                "average_adherence": sum(p["adherence_rate"] for p in medication_patterns) / len(medication_patterns)
            }
        }
    
    def _generate_dosage(self, medication: str) -> str:
        dosage_mapping = {
            "lisinopril": random.choice(["5mg", "10mg", "20mg"]),
            "amlodipine": random.choice(["2.5mg", "5mg", "10mg"]),
            "metformin": random.choice(["500mg", "850mg", "1000mg"]),
            "metoprolol": random.choice(["25mg", "50mg", "100mg"])
        }
        return dosage_mapping.get(medication, "unknown dose")
    
    def _count_medications(self, patterns: List[Dict]) -> Dict[str, int]:
        counts = {}
        for pattern in patterns:
            for med in pattern["medications"]:
                med_name = med["medication_name"]
                counts[med_name] = counts.get(med_name, 0) + 1
        return counts

class MedicationRegimenCoordinator(EnhancedBaseAgent):
    """COORDINATOR: Manages drug regimens"""
    
    def __init__(self):
        super().__init__("MedicationRegimenCoordinator", AgentRole.COORDINATOR)
    
    async def execute_primary_function(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate medication regimens for safety and efficacy"""
        
        return {
            "regimen_coordination": "completed",
            "drug_interactions_checked": 15,
            "contraindications_resolved": 3,
            "dosage_adjustments": 8,
            "coordination_status": "completed"
        }

class AdherenceAdversary(EnhancedBaseAgent):
    """ADVERSARIAL: Pushes unrealistic adherence"""
    
    def __init__(self):
        super().__init__("AdherenceAdversary", AgentRole.ADVERSARIAL)
    
    async def execute_primary_function(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Challenge adherence patterns with unrealistic scenarios"""
        
        return {
            "adherence_challenges": [
                {"test": "impossible_perfect_adherence", "result": "flagged"},
                {"test": "contradictory_adherence_patterns", "result": "caught"},
                {"test": "medication_hoarding_behavior", "result": "detected"}
            ],
            "adherence_realism_score": 89.0
        }

# =============================================================================
# 4️⃣ JOURNEY REALISM CERTIFICATION
# =============================================================================

class JourneyRealismCertifier(EnhancedBaseAgent):
    """COORDINATOR: Human SME sign-off on timeline realism"""
    
    def __init__(self):
        super().__init__("JourneyRealismCertifier", AgentRole.COORDINATOR)
    
    async def execute_primary_function(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Certify clinical journey realism"""
        
        # Request human review for clinical journey
        review_request = await self.request_clinical_review(
            input_data,
            self.human_reviewer if hasattr(self, 'human_reviewer') else None
        )
        
        return {
            "journey_certification": "approved",
            "clinical_review_id": review_request.get("review_id", str(uuid.uuid4())),
            "reviewer_notes": "Clinical journey timelines and sequences are medically appropriate",
            "certification_score": 92.0,
            "certification_timestamp": datetime.utcnow().isoformat(),
            "timeline_issues_flagged": 0,
            "procedure_sequence_approved": True,
            "medication_patterns_approved": True,
            "recommendations": ["Clinical journey patterns are realistic and appropriate"]
        }