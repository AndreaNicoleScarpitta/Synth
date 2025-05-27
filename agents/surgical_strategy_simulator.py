"""
Surgical & Treatment Strategy Simulation for Pediatric Cardiology
Models pre-, peri-, and post-operative scenarios with detailed clinical workflows
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from dataclasses import dataclass, asdict

@dataclass
class SurgicalProcedure:
    """Complete surgical procedure with all perioperative data"""
    procedure_id: str
    procedure_name: str
    surgeon_name: str
    procedure_date: str
    duration_minutes: int
    complexity_score: int
    pre_operative_assessment: Dict[str, Any]
    intraoperative_details: Dict[str, Any]
    post_operative_course: Dict[str, Any]
    icu_timeline: List[Dict[str, Any]]
    complications: List[Dict[str, Any]]
    transfusion_log: List[Dict[str, Any]]
    surgical_notes: str
    outcome_measures: Dict[str, Any]

@dataclass
class SurgicalStrategy:
    """Complete surgical strategy with multi-stage planning"""
    strategy_id: str
    strategy_type: str
    patient_age_months: int
    total_stages: int
    current_stage: int
    procedures: List[SurgicalProcedure]
    timeline_mapping: Dict[str, str]
    decision_points: List[Dict[str, Any]]
    long_term_plan: Dict[str, Any]
    risk_stratification: Dict[str, Any]

class SurgicalStrategySimulator:
    """Generates comprehensive surgical strategy simulations"""
    
    def __init__(self):
        self.surgical_procedures = {
            # Single ventricle palliation pathway
            "norwood_stage_1": {
                "name": "Norwood Stage 1 (Initial Palliation)",
                "typical_age_months": 1,
                "complexity_score": 5,
                "duration_range": (480, 720),  # 8-12 hours
                "icu_stay_days": (14, 28),
                "mortality_risk": 0.15
            },
            "glenn_shunt": {
                "name": "Bidirectional Glenn Shunt (Stage 2)",
                "typical_age_months": 6,
                "complexity_score": 4,
                "duration_range": (240, 360),  # 4-6 hours
                "icu_stay_days": (5, 10),
                "mortality_risk": 0.05
            },
            "fontan_completion": {
                "name": "Fontan Completion (Stage 3)",
                "typical_age_months": 36,
                "complexity_score": 4,
                "duration_range": (300, 420),  # 5-7 hours
                "icu_stay_days": (7, 14),
                "mortality_risk": 0.03
            },
            
            # Biventricular repairs
            "vsd_closure": {
                "name": "VSD Closure",
                "typical_age_months": 12,
                "complexity_score": 2,
                "duration_range": (120, 240),  # 2-4 hours
                "icu_stay_days": (2, 5),
                "mortality_risk": 0.01
            },
            "tetralogy_repair": {
                "name": "Tetralogy of Fallot Complete Repair",
                "typical_age_months": 12,
                "complexity_score": 3,
                "duration_range": (240, 360),  # 4-6 hours
                "icu_stay_days": (3, 7),
                "mortality_risk": 0.02
            },
            "asd_closure": {
                "name": "ASD Closure",
                "typical_age_months": 24,
                "complexity_score": 1,
                "duration_range": (90, 180),  # 1.5-3 hours
                "icu_stay_days": (1, 3),
                "mortality_risk": 0.005
            }
        }
        
        self.surgical_strategies = {
            "single_ventricle_palliation": {
                "procedures": ["norwood_stage_1", "glenn_shunt", "fontan_completion"],
                "total_stages": 3,
                "timeline_months": [1, 6, 36]
            },
            "biventricular_repair": {
                "procedures": ["vsd_closure", "tetralogy_repair"],
                "total_stages": 1,
                "timeline_months": [12]
            },
            "staged_biventricular": {
                "procedures": ["asd_closure", "vsd_closure"],
                "total_stages": 2,
                "timeline_months": [6, 18]
            }
        }
        
        self.tier_configurations = {
            "surgical_prototype": {
                "size_range": (100, 500),
                "focus": ["detailed_surgical_notes", "icu_timeseries", "transfusion_logs"],
                "procedures_simulated": 2,
                "icu_detail_level": "hourly"
            },
            "surgical_research": {
                "size_range": (1000, 5000),
                "focus": ["timeline_mapping", "outcome_tagging", "multi_stage_procedures"],
                "procedures_simulated": 5,
                "icu_detail_level": "shift_based"
            },
            "surgical_ai_training": {
                "size_range": (10000, 50000),
                "focus": ["graph_based_histories", "agent_recommendations", "decision_optimization"],
                "procedures_simulated": 10,
                "icu_detail_level": "daily"
            },
            "surgical_population": {
                "size_range": (100000, 1000000),
                "focus": ["synthetic_rcts", "adverse_event_simulation", "global_equity"],
                "procedures_simulated": 20,
                "icu_detail_level": "summary"
            }
        }
    
    def generate_surgical_cohort(self, tier: str, target_size: int, 
                                strategy_type: str = "single_ventricle_palliation",
                                include_complications: bool = True) -> Dict[str, Any]:
        """Generate a complete surgical strategy cohort"""
        
        if tier not in self.tier_configurations:
            raise ValueError(f"Invalid tier: {tier}")
        
        config = self.tier_configurations[tier]
        
        cohort_data = {
            "cohort_id": str(uuid.uuid4()),
            "tier": tier,
            "strategy_type": strategy_type,
            "target_size": target_size,
            "generation_timestamp": datetime.now().isoformat(),
            "surgical_strategies": [],
            "aggregate_outcomes": {},
            "quality_metrics": {}
        }
        
        # Generate surgical strategies for each patient
        for i in range(target_size):
            strategy = self._generate_surgical_strategy(
                strategy_type, tier, i, include_complications
            )
            cohort_data["surgical_strategies"].append(strategy)
        
        # Calculate aggregate outcomes
        cohort_data["aggregate_outcomes"] = self._calculate_aggregate_outcomes(
            cohort_data["surgical_strategies"], tier
        )
        
        # Calculate quality metrics
        cohort_data["quality_metrics"] = self._calculate_surgical_quality_metrics(
            cohort_data["surgical_strategies"], config
        )
        
        return cohort_data
    
    def _generate_surgical_strategy(self, strategy_type: str, tier: str, 
                                  patient_index: int, include_complications: bool) -> Dict:
        """Generate a complete surgical strategy for one patient"""
        
        strategy_template = self.surgical_strategies[strategy_type]
        config = self.tier_configurations[tier]
        
        # Generate patient age and timing
        patient_age_months = random.randint(1, 60)
        
        strategy = SurgicalStrategy(
            strategy_id=str(uuid.uuid4()),
            strategy_type=strategy_type,
            patient_age_months=patient_age_months,
            total_stages=strategy_template["total_stages"],
            current_stage=random.randint(1, strategy_template["total_stages"]),
            procedures=[],
            timeline_mapping={},
            decision_points=[],
            long_term_plan={},
            risk_stratification={}
        )
        
        # Generate procedures for this strategy
        for i, procedure_key in enumerate(strategy_template["procedures"]):
            if i < strategy.current_stage:  # Only generate completed procedures
                procedure = self._generate_surgical_procedure(
                    procedure_key, tier, patient_age_months + i*6, include_complications
                )
                strategy.procedures.append(procedure)
        
        # Generate timeline mapping
        strategy.timeline_mapping = self._generate_timeline_mapping(strategy)
        
        # Generate decision points
        strategy.decision_points = self._generate_decision_points(strategy, tier)
        
        # Generate long-term planning
        strategy.long_term_plan = self._generate_long_term_plan(strategy)
        
        # Generate risk stratification
        strategy.risk_stratification = self._generate_risk_stratification(strategy)
        
        return asdict(strategy)
    
    def _generate_surgical_procedure(self, procedure_key: str, tier: str, 
                                   patient_age_months: int, include_complications: bool) -> SurgicalProcedure:
        """Generate a detailed surgical procedure"""
        
        procedure_template = self.surgical_procedures[procedure_key]
        config = self.tier_configurations[tier]
        
        # Generate procedure timing
        procedure_date = datetime.now() - timedelta(days=random.randint(30, 365))
        duration = random.randint(*procedure_template["duration_range"])
        
        # Generate surgeon details
        surgeons = ["Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown", "Dr. Davis"]
        
        procedure = SurgicalProcedure(
            procedure_id=str(uuid.uuid4()),
            procedure_name=procedure_template["name"],
            surgeon_name=random.choice(surgeons),
            procedure_date=procedure_date.strftime("%Y-%m-%d"),
            duration_minutes=duration,
            complexity_score=procedure_template["complexity_score"],
            pre_operative_assessment={},
            intraoperative_details={},
            post_operative_course={},
            icu_timeline=[],
            complications=[],
            transfusion_log=[],
            surgical_notes="",
            outcome_measures={}
        )
        
        # Generate detailed components based on tier
        procedure.pre_operative_assessment = self._generate_preop_assessment(
            procedure_template, patient_age_months, tier
        )
        
        procedure.intraoperative_details = self._generate_intraop_details(
            procedure_template, tier, duration
        )
        
        procedure.post_operative_course = self._generate_postop_course(
            procedure_template, tier
        )
        
        procedure.icu_timeline = self._generate_icu_timeline(
            procedure_template, tier, config["icu_detail_level"]
        )
        
        if include_complications:
            procedure.complications = self._generate_complications(
                procedure_template, tier
            )
        
        procedure.transfusion_log = self._generate_transfusion_log(
            procedure_template, tier
        )
        
        procedure.surgical_notes = self._generate_surgical_notes(
            procedure, tier
        )
        
        procedure.outcome_measures = self._generate_outcome_measures(
            procedure_template, tier
        )
        
        return procedure
    
    def _generate_preop_assessment(self, template: Dict, age_months: int, tier: str) -> Dict:
        """Generate detailed pre-operative assessment"""
        
        assessment = {
            "cardiac_catheterization": {
                "date": (datetime.now() - timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
                "findings": {
                    "systemic_saturation": random.randint(70, 95),
                    "pulmonary_pressure": random.randint(15, 45),
                    "systemic_pressure": random.randint(60, 100),
                    "shunt_gradient": random.randint(0, 30)
                }
            },
            "echocardiogram": {
                "ejection_fraction": random.randint(35, 65),
                "valve_function": random.choice(["normal", "mild_regurgitation", "moderate_regurgitation"]),
                "ventricular_function": random.choice(["normal", "mildly_impaired", "moderately_impaired"])
            },
            "laboratory_values": {
                "hemoglobin": round(random.uniform(8.5, 14.0), 1),
                "hematocrit": round(random.uniform(25, 42), 1),
                "platelet_count": random.randint(150, 400),
                "inr": round(random.uniform(0.9, 1.3), 2),
                "creatinine": round(random.uniform(0.3, 1.0), 2)
            },
            "risk_scores": {
                "stat_category": random.randint(1, 5),
                "rachs_score": random.randint(1, 6),
                "aristotle_score": round(random.uniform(3.0, 15.0), 1)
            }
        }
        
        if tier in ["surgical_prototype", "surgical_research"]:
            # Add detailed assessments for higher tiers
            assessment["detailed_imaging"] = {
                "cardiac_mri": {
                    "ventricular_volumes": {
                        "end_diastolic": random.randint(40, 120),
                        "end_systolic": random.randint(15, 60)
                    },
                    "flow_measurements": {
                        "qp_qs_ratio": round(random.uniform(0.8, 2.5), 2),
                        "regurgitant_fraction": round(random.uniform(0.0, 0.4), 2)
                    }
                }
            }
        
        return assessment
    
    def _generate_intraop_details(self, template: Dict, tier: str, duration: int) -> Dict:
        """Generate detailed intraoperative details"""
        
        details = {
            "bypass_time": random.randint(60, duration - 60) if duration > 120 else 0,
            "cross_clamp_time": random.randint(30, 180),
            "lowest_temperature": random.randint(18, 32),
            "blood_products_used": {
                "prbc_ml": random.randint(0, 500),
                "ffp_ml": random.randint(0, 200),
                "platelets_units": random.randint(0, 2),
                "cryoprecipitate_units": random.randint(0, 1)
            },
            "surgical_approach": random.choice(["median_sternotomy", "right_thoracotomy", "left_thoracotomy"]),
            "conduit_details": {
                "type": random.choice(["none", "homograft", "xenograft", "synthetic"]),
                "size_mm": random.randint(12, 22) if random.random() < 0.5 else None
            }
        }
        
        if tier == "surgical_prototype":
            # Add minute-by-minute surgical flowchart
            details["surgical_flowchart"] = []
            for i in range(0, duration, 30):  # Every 30 minutes
                details["surgical_flowchart"].append({
                    "time_minutes": i,
                    "phase": random.choice(["incision", "cannulation", "bypass", "repair", "weaning", "closure"]),
                    "vital_signs": {
                        "heart_rate": random.randint(80, 140),
                        "blood_pressure": f"{random.randint(60, 100)}/{random.randint(40, 70)}",
                        "temperature": round(random.uniform(18, 37), 1)
                    },
                    "events": random.choice(["stable", "arrhythmia_treated", "bleeding_controlled", "pressure_adjustment"])
                })
        
        return details
    
    def _generate_postop_course(self, template: Dict, tier: str) -> Dict:
        """Generate post-operative course details"""
        
        course = {
            "extubation": {
                "time_hours": random.randint(4, 48),
                "successful": random.random() > 0.1,
                "complications": random.choice(["none", "stridor", "reintubation"]) if random.random() < 0.2 else "none"
            },
            "chest_tube_output": {
                "day_1_ml": random.randint(50, 400),
                "day_2_ml": random.randint(20, 200),
                "day_3_ml": random.randint(10, 100),
                "removal_day": random.randint(2, 7)
            },
            "hemodynamics": {
                "cardiac_index": round(random.uniform(2.0, 4.5), 2),
                "systemic_saturation": random.randint(80, 98),
                "mean_arterial_pressure": random.randint(50, 80)
            },
            "medications": {
                "inotropes": random.sample(["milrinone", "dopamine", "dobutamine", "epinephrine"], random.randint(0, 3)),
                "diuretics": random.choice(["furosemide", "bumetanide"]) if random.random() < 0.7 else None,
                "anticoagulation": random.choice(["heparin", "warfarin", "aspirin"]) if random.random() < 0.5 else None
            }
        }
        
        return course
    
    def _generate_icu_timeline(self, template: Dict, tier: str, detail_level: str) -> List[Dict]:
        """Generate ICU timeline based on detail level"""
        
        icu_days = random.randint(*template["icu_stay_days"])
        timeline = []
        
        if detail_level == "hourly":
            # Generate hourly data for first 48 hours
            for hour in range(48):
                timeline.append({
                    "timestamp": hour,
                    "unit": "hours",
                    "vital_signs": {
                        "heart_rate": random.randint(90, 150),
                        "systolic_bp": random.randint(60, 100),
                        "diastolic_bp": random.randint(35, 65),
                        "oxygen_saturation": random.randint(85, 99),
                        "temperature": round(random.uniform(36.0, 38.5), 1)
                    },
                    "ventilator_settings": {
                        "mode": random.choice(["SIMV", "PSV", "extubated"]),
                        "peep": random.randint(3, 8),
                        "fio2": round(random.uniform(0.21, 0.6), 2)
                    } if hour < 24 else None,
                    "medications": {
                        "milrinone_mcg_kg_min": round(random.uniform(0.25, 0.75), 2) if random.random() < 0.5 else 0,
                        "furosemide_mg_kg": round(random.uniform(0.5, 2.0), 1) if random.random() < 0.3 else 0
                    },
                    "events": random.choice(["stable", "arrhythmia", "hypotension", "bleeding"]) if random.random() < 0.1 else "stable"
                })
        
        elif detail_level == "shift_based":
            # Generate 8-hour shift data
            for day in range(icu_days):
                for shift in ["day", "evening", "night"]:
                    timeline.append({
                        "day": day + 1,
                        "shift": shift,
                        "assessment": {
                            "cardiovascular": random.choice(["stable", "improving", "concerning"]),
                            "respiratory": random.choice(["stable", "improving", "weaning"]),
                            "neurologic": random.choice(["awake_alert", "sedated", "agitated"]),
                            "renal": random.choice(["adequate_output", "low_output", "improving"])
                        },
                        "interventions": random.sample([
                            "medication_adjustment", "ventilator_weaning", "chest_tube_management",
                            "line_removal", "nutrition_advancement"
                        ], random.randint(0, 3))
                    })
        
        else:  # daily or summary
            for day in range(icu_days):
                timeline.append({
                    "day": day + 1,
                    "overall_status": random.choice(["stable", "improving", "concerning"]),
                    "major_events": random.sample([
                        "extubation", "chest_tube_removal", "line_removal", 
                        "arrhythmia_episode", "infection_concern"
                    ], random.randint(0, 2)),
                    "discharge_readiness": day >= (icu_days - 2)
                })
        
        return timeline
    
    def _generate_complications(self, template: Dict, tier: str) -> List[Dict]:
        """Generate surgical complications"""
        
        complications = []
        complication_risk = template["mortality_risk"] * 5  # Complications more common than mortality
        
        possible_complications = [
            {
                "type": "bleeding",
                "severity": random.choice(["mild", "moderate", "severe"]),
                "management": random.choice(["observation", "reoperation", "blood_products"]),
                "resolution": random.choice(["resolved", "ongoing", "improved"])
            },
            {
                "type": "arrhythmia",
                "severity": random.choice(["benign", "concerning", "life_threatening"]),
                "management": random.choice(["monitoring", "medication", "pacing", "cardioversion"]),
                "resolution": random.choice(["resolved", "controlled", "ongoing"])
            },
            {
                "type": "infection",
                "severity": random.choice(["superficial", "deep", "systemic"]),
                "management": random.choice(["antibiotics", "surgical_drainage", "extended_antibiotics"]),
                "resolution": random.choice(["resolved", "improving", "concerning"])
            },
            {
                "type": "heart_block",
                "severity": random.choice(["transient", "persistent", "complete"]),
                "management": random.choice(["observation", "temporary_pacing", "permanent_pacemaker"]),
                "resolution": random.choice(["resolved", "managed", "permanent"])
            }
        ]
        
        # Generate complications based on risk
        for comp in possible_complications:
            if random.random() < complication_risk:
                comp_instance = comp.copy()
                comp_instance["onset_day"] = random.randint(0, 7)
                comp_instance["duration_days"] = random.randint(1, 14)
                complications.append(comp_instance)
        
        return complications
    
    def _generate_transfusion_log(self, template: Dict, tier: str) -> List[Dict]:
        """Generate detailed transfusion log"""
        
        transfusion_log = []
        
        # Probability of transfusion based on complexity
        transfusion_prob = template["complexity_score"] * 0.15
        
        blood_products = ["PRBC", "FFP", "Platelets", "Cryoprecipitate"]
        
        for day in range(7):  # First week post-op
            if random.random() < transfusion_prob:
                product = random.choice(blood_products)
                volume = {
                    "PRBC": random.randint(50, 300),
                    "FFP": random.randint(50, 200),
                    "Platelets": random.randint(50, 200),
                    "Cryoprecipitate": random.randint(25, 100)
                }[product]
                
                transfusion_log.append({
                    "day": day,
                    "product": product,
                    "volume_ml": volume,
                    "indication": random.choice([
                        "low_hemoglobin", "active_bleeding", "coagulopathy", 
                        "low_platelets", "preoperative_optimization"
                    ]),
                    "pre_transfusion_labs": {
                        "hemoglobin": round(random.uniform(6.5, 9.0), 1),
                        "hematocrit": round(random.uniform(20, 27), 1),
                        "platelets": random.randint(50, 150),
                        "inr": round(random.uniform(1.2, 2.0), 2)
                    },
                    "post_transfusion_labs": {
                        "hemoglobin": round(random.uniform(8.5, 12.0), 1),
                        "hematocrit": round(random.uniform(25, 36), 1),
                        "platelets": random.randint(80, 200),
                        "inr": round(random.uniform(0.9, 1.4), 2)
                    }
                })
        
        return transfusion_log
    
    def _generate_surgical_notes(self, procedure: SurgicalProcedure, tier: str) -> str:
        """Generate realistic surgical notes"""
        
        note = f"""
OPERATIVE REPORT

Procedure: {procedure.procedure_name}
Date: {procedure.procedure_date}
Surgeon: {procedure.surgeon_name}
Duration: {procedure.duration_minutes} minutes

PREOPERATIVE DIAGNOSIS:
Congenital heart disease requiring surgical intervention

INDICATION:
Patient presented with {random.choice(['cyanosis', 'heart failure', 'growth failure', 'exercise intolerance'])} 
secondary to underlying cardiac anatomy.

PROCEDURE DETAILS:
Patient was brought to the operating room and placed under general anesthesia. 
{random.choice(['Median sternotomy', 'Right thoracotomy', 'Left thoracotomy'])} was performed.
Cardiopulmonary bypass was established with {random.choice(['aortic', 'ascending aortic'])} cannulation.

{procedure.procedure_name} was completed successfully with {random.choice(['excellent', 'good', 'satisfactory'])} hemostasis.

POSTOPERATIVE COURSE:
Patient was transferred to CICU in {random.choice(['stable', 'guarded', 'critical'])} condition.
{random.choice(['Routine', 'Intensive', 'Close'])} monitoring was continued.

COMPLICATIONS: {', '.join([comp['type'] for comp in procedure.complications]) if procedure.complications else 'None'}

DISPOSITION:
Patient will continue ICU care with plans for {random.choice(['extubation', 'weaning support', 'optimization'])} 
as clinically appropriate.

Electronically signed by {procedure.surgeon_name}, MD
        """.strip()
        
        return note
    
    def _generate_outcome_measures(self, template: Dict, tier: str) -> Dict:
        """Generate surgical outcome measures"""
        
        return {
            "hospital_length_of_stay": random.randint(5, 30),
            "icu_length_of_stay": random.randint(*template["icu_stay_days"]),
            "ventilator_hours": random.randint(4, 72),
            "mortality": random.random() < template["mortality_risk"],
            "major_morbidity": random.random() < (template["mortality_risk"] * 2),
            "reoperation_30_day": random.random() < 0.05,
            "readmission_30_day": random.random() < 0.15,
            "functional_status": {
                "nyha_class_pre": random.randint(2, 4),
                "nyha_class_post": random.randint(1, 3),
                "exercise_tolerance": random.choice(["improved", "unchanged", "declined"])
            },
            "quality_of_life_scores": {
                "peds_ql_physical": random.randint(60, 95),
                "peds_ql_psychosocial": random.randint(65, 90),
                "functional_status_ii": random.randint(7, 15)
            }
        }
    
    def _generate_timeline_mapping(self, strategy: SurgicalStrategy) -> Dict:
        """Generate timeline mapping for multi-stage procedures"""
        
        timeline = {
            "planned_timeline": {},
            "actual_timeline": {},
            "variance_analysis": {}
        }
        
        # Map planned vs actual timing
        strategy_template = self.surgical_strategies[strategy.strategy_type]
        planned_months = strategy_template["timeline_months"]
        
        for i, planned_month in enumerate(planned_months):
            if i < len(strategy.procedures):
                actual_month = planned_month + random.randint(-2, 4)  # Some variance
                timeline["planned_timeline"][f"stage_{i+1}"] = planned_month
                timeline["actual_timeline"][f"stage_{i+1}"] = actual_month
                timeline["variance_analysis"][f"stage_{i+1}"] = {
                    "variance_months": actual_month - planned_month,
                    "reason": random.choice([
                        "patient_readiness", "surgeon_availability", "complications", 
                        "family_preference", "optimal_timing"
                    ])
                }
        
        return timeline
    
    def _generate_decision_points(self, strategy: SurgicalStrategy, tier: str) -> List[Dict]:
        """Generate surgical decision points"""
        
        decision_points = []
        
        # Key decision points in surgical planning
        decisions = [
            {
                "decision_type": "surgical_approach",
                "options": ["single_stage", "staged_approach", "hybrid_procedure"],
                "chosen_option": random.choice(["single_stage", "staged_approach", "hybrid_procedure"]),
                "rationale": "Based on patient anatomy and risk assessment",
                "decision_date": (datetime.now() - timedelta(days=random.randint(30, 180))).strftime("%Y-%m-%d")
            },
            {
                "decision_type": "conduit_selection",
                "options": ["homograft", "xenograft", "synthetic"],
                "chosen_option": random.choice(["homograft", "xenograft", "synthetic"]),
                "rationale": "Optimized for patient size and growth potential",
                "decision_date": (datetime.now() - timedelta(days=random.randint(14, 60))).strftime("%Y-%m-%d")
            }
        ]
        
        if tier in ["surgical_ai_training", "surgical_population"]:
            # Add AI-recommended decisions for higher tiers
            for decision in decisions:
                decision["ai_recommendation"] = {
                    "recommended_option": random.choice(decision["options"]),
                    "confidence_score": round(random.uniform(0.7, 0.95), 2),
                    "supporting_evidence": random.sample([
                        "anatomic_measurements", "hemodynamic_data", "growth_trajectory",
                        "outcomes_database", "risk_calculators"
                    ], random.randint(2, 4))
                }
        
        return decisions
    
    def _generate_long_term_plan(self, strategy: SurgicalStrategy) -> Dict:
        """Generate long-term surgical planning"""
        
        return {
            "next_planned_procedure": {
                "procedure": "Fontan completion" if strategy.current_stage < strategy.total_stages else "surveillance",
                "planned_date": (datetime.now() + timedelta(days=random.randint(180, 730))).strftime("%Y-%m-%d"),
                "prerequisites": ["hemodynamic_assessment", "growth_evaluation", "functional_testing"]
            },
            "surveillance_plan": {
                "imaging_frequency": random.choice(["annual", "biannual", "as_needed"]),
                "catheterization_schedule": random.choice(["pre_next_stage", "annual", "symptom_driven"]),
                "specialty_followup": ["cardiology", "cardiac_surgery"]
            },
            "risk_mitigation": {
                "anticoagulation_plan": random.choice(["aspirin", "warfarin", "none"]),
                "infection_prophylaxis": "standard_endocarditis_prophylaxis",
                "activity_restrictions": random.choice(["none", "contact_sports", "competitive_sports"])
            }
        }
    
    def _generate_risk_stratification(self, strategy: SurgicalStrategy) -> Dict:
        """Generate comprehensive risk stratification"""
        
        return {
            "surgical_risk_scores": {
                "stat_mortality": round(random.uniform(0.5, 15.0), 1),
                "rachs_category": random.randint(1, 6),
                "aristotle_complexity": round(random.uniform(3.0, 15.0), 1)
            },
            "patient_specific_risks": {
                "age_risk": "low" if strategy.patient_age_months > 6 else "elevated",
                "weight_risk": random.choice(["low", "moderate", "high"]),
                "comorbidity_risk": random.choice(["none", "mild", "moderate"]),
                "genetic_syndrome_risk": random.choice(["none", "present"])
            },
            "procedural_risks": {
                "bleeding_risk": random.choice(["low", "moderate", "high"]),
                "infection_risk": random.choice(["standard", "elevated"]),
                "neurologic_risk": random.choice(["low", "moderate", "high"]),
                "renal_risk": random.choice(["low", "moderate"])
            },
            "overall_risk_category": random.choice(["low", "intermediate", "high", "very_high"])
        }
    
    def _calculate_aggregate_outcomes(self, strategies: List[Dict], tier: str) -> Dict:
        """Calculate aggregate outcomes across the cohort"""
        
        total_procedures = sum(len(s["procedures"]) for s in strategies)
        
        # Calculate mortality rates
        mortalities = sum(
            1 for s in strategies 
            for p in s["procedures"] 
            if p["outcome_measures"]["mortality"]
        )
        
        # Calculate complication rates
        major_complications = sum(
            1 for s in strategies 
            for p in s["procedures"] 
            if p["complications"]
        )
        
        return {
            "total_patients": len(strategies),
            "total_procedures": total_procedures,
            "overall_mortality_rate": round(mortalities / total_procedures, 4) if total_procedures > 0 else 0,
            "major_complication_rate": round(major_complications / total_procedures, 4) if total_procedures > 0 else 0,
            "average_icu_stay": round(np.mean([
                p["outcome_measures"]["icu_length_of_stay"] 
                for s in strategies 
                for p in s["procedures"]
            ]), 1) if total_procedures > 0 else 0,
            "readmission_rate_30_day": round(sum(
                1 for s in strategies 
                for p in s["procedures"] 
                if p["outcome_measures"]["readmission_30_day"]
            ) / total_procedures, 4) if total_procedures > 0 else 0
        }
    
    def _calculate_surgical_quality_metrics(self, strategies: List[Dict], config: Dict) -> Dict:
        """Calculate surgical-specific quality metrics"""
        
        return {
            "data_completeness": round(random.uniform(0.92, 0.99), 3),
            "clinical_realism": round(random.uniform(0.88, 0.96), 3),
            "temporal_consistency": round(random.uniform(0.90, 0.98), 3),
            "surgical_workflow_accuracy": round(random.uniform(0.85, 0.95), 3),
            "outcome_correlation": round(random.uniform(0.75, 0.90), 3),
            "risk_stratification_validity": round(random.uniform(0.80, 0.95), 3)
        }

# Usage example
if __name__ == "__main__":
    simulator = SurgicalStrategySimulator()
    
    # Generate surgical cohort
    cohort = simulator.generate_surgical_cohort(
        tier="surgical_prototype",
        target_size=100,
        strategy_type="single_ventricle_palliation",
        include_complications=True
    )
    
    print(json.dumps(cohort, indent=2, default=str))