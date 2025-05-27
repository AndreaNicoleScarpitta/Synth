"""
Enhanced Pediatric Cardiology Synthetic Record Generator
Generates comprehensive synthetic EHRs with complete clinical data for pediatric cardiology
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np
from dataclasses import dataclass, asdict

@dataclass
class PediatricCardiologyRecord:
    """Complete pediatric cardiology synthetic record with all clinical modalities"""
    
    # Patient Demographics & Encounter Metadata
    patient_id: str
    age_months: int
    sex: str
    weight_kg: float
    height_cm: float
    bmi: float
    race_ethnicity: str
    family_history_cvd: bool
    family_history_clotting: bool
    admission_date: str
    discharge_date: str
    icu_stay: bool
    surgical_dates: List[str]
    
    # Cardiac-Specific Vitals & Metrics
    heart_rate_bpm: int
    systolic_bp_mmhg: int
    diastolic_bp_mmhg: int
    pulse_pressure_variation: float
    central_venous_pressure: float
    oxygen_saturation: float
    mixed_venous_o2: float
    ejection_fraction: float
    stroke_volume: float
    cardiac_output: float
    
    # Hematologic Laboratory Results
    hemoglobin_g_dl: float
    hematocrit_percent: float
    platelet_count_k_ul: int
    wbc_count_k_ul: float
    mcv_fl: float
    mch_pg: float
    rdw_percent: float
    pt_seconds: float
    aptt_seconds: float
    inr: float
    fibrinogen_mg_dl: float
    d_dimer_ng_ml: float
    antithrombin_iii_percent: float
    reticulocyte_count_percent: float
    
    # Therapeutics
    anticoagulants: List[str]
    antiplatelets: List[str]
    esa_therapy: bool
    transfusion_history: List[Dict[str, Any]]
    
    # Unstructured Clinical Notes
    cardiology_consultation: str
    hematology_assessment: str
    transfusion_protocol: str
    surgical_narrative: str
    anticoagulation_plan: str
    
    # Time-Series Physiologic Data
    ecg_findings: Dict[str, Any]
    arterial_pressure_traces: List[float]
    pulse_oximetry_timeseries: List[Dict[str, float]]
    blood_gas_data: List[Dict[str, Any]]
    
    # Genomic/Molecular Data
    factor_v_leiden: str
    prothrombin_mutation: str
    jak2_mutation: str
    hba_hbb_mutations: str
    hfe_mutations: str
    platelet_function_genes: Dict[str, str]
    
    # Imaging Findings
    echocardiogram: Dict[str, Any]
    cardiac_mri: Dict[str, Any]
    coronary_angiogram: Optional[Dict[str, Any]]
    chest_xray: Dict[str, str]
    abdominal_imaging: Dict[str, str]
    brain_imaging: Optional[Dict[str, str]]
    
    # Administrative Data
    icd10_codes: List[str]
    cpt_codes: List[str]
    drg_codes: List[str]
    
    # Patient-Reported Outcomes
    fatigue_score: int
    nyha_class: int
    bleeding_questionnaire: Dict[str, Any]

class PediatricCardiologyGenerator:
    """Generates comprehensive pediatric cardiology synthetic records"""
    
    def __init__(self):
        self.condition_templates = {
            "congenital_heart_disease": {
                "age_range": (0, 216),  # 0-18 years in months
                "common_defects": ["VSD", "ASD", "TOF", "HLHS", "CoA"],
                "surgical_interventions": True
            },
            "acquired_heart_disease": {
                "age_range": (12, 216),
                "conditions": ["cardiomyopathy", "myocarditis", "rheumatic_heart"],
                "surgical_interventions": False
            },
            "hemodynamic_disorders": {
                "age_range": (0, 216),
                "conditions": ["pulmonary_hypertension", "heart_failure"],
                "monitoring_intensive": True
            }
        }
        
        # Race/ethnicity data for sickle cell and thalassemia relevance
        self.ethnicity_risks = {
            "African American": {"sickle_cell": 0.08, "thalassemia": 0.01},
            "Mediterranean": {"sickle_cell": 0.001, "thalassemia": 0.15},
            "Southeast Asian": {"sickle_cell": 0.001, "thalassemia": 0.12},
            "Middle Eastern": {"sickle_cell": 0.002, "thalassemia": 0.10},
            "Caucasian": {"sickle_cell": 0.001, "thalassemia": 0.02},
            "Hispanic": {"sickle_cell": 0.003, "thalassemia": 0.03}
        }
    
    def generate_demographics(self, condition_type: str) -> Dict[str, Any]:
        """Generate patient demographics and encounter metadata"""
        age_range = self.condition_templates[condition_type]["age_range"]
        age_months = random.randint(*age_range)
        sex = random.choice(["M", "F"])
        
        # Age-appropriate weight and height using pediatric growth charts
        weight_kg, height_cm = self._calculate_pediatric_measurements(age_months, sex)
        bmi = weight_kg / ((height_cm / 100) ** 2)
        
        ethnicity = random.choice(list(self.ethnicity_risks.keys()))
        
        # Family history more common in congenital conditions
        family_cvd_risk = 0.3 if condition_type == "congenital_heart_disease" else 0.15
        family_clot_risk = 0.1 if ethnicity in ["African American", "Mediterranean"] else 0.05
        
        admission_date = datetime.now() - timedelta(days=random.randint(1, 30))
        discharge_date = admission_date + timedelta(days=random.randint(3, 21))
        
        # Surgical dates for congenital conditions
        surgical_dates = []
        if condition_type == "congenital_heart_disease" and random.random() < 0.7:
            surgery_date = admission_date + timedelta(days=random.randint(1, 5))
            surgical_dates.append(surgery_date.strftime("%Y-%m-%d"))
        
        return {
            "patient_id": str(uuid.uuid4()),
            "age_months": age_months,
            "sex": sex,
            "weight_kg": round(weight_kg, 1),
            "height_cm": round(height_cm, 1),
            "bmi": round(bmi, 1),
            "race_ethnicity": ethnicity,
            "family_history_cvd": random.random() < family_cvd_risk,
            "family_history_clotting": random.random() < family_clot_risk,
            "admission_date": admission_date.strftime("%Y-%m-%d"),
            "discharge_date": discharge_date.strftime("%Y-%m-%d"),
            "icu_stay": random.random() < 0.4,
            "surgical_dates": surgical_dates
        }
    
    def generate_cardiac_vitals(self, age_months: int, condition_severity: str) -> Dict[str, Any]:
        """Generate age-appropriate cardiac vitals and hemodynamic parameters"""
        # Age-based normal ranges for pediatric patients
        if age_months < 12:  # Infant
            hr_base, sbp_base, dbp_base = 130, 85, 55
        elif age_months < 60:  # Toddler/Preschool
            hr_base, sbp_base, dbp_base = 110, 95, 60
        elif age_months < 144:  # School age
            hr_base, sbp_base, dbp_base = 95, 105, 65
        else:  # Adolescent
            hr_base, sbp_base, dbp_base = 80, 115, 75
        
        # Adjust for condition severity
        severity_multipliers = {
            "mild": (0.9, 1.1),
            "moderate": (0.8, 1.2),
            "severe": (0.7, 1.4)
        }
        low_mult, high_mult = severity_multipliers[condition_severity]
        
        return {
            "heart_rate_bpm": int(hr_base * random.uniform(low_mult, high_mult)),
            "systolic_bp_mmhg": int(sbp_base * random.uniform(low_mult, high_mult)),
            "diastolic_bp_mmhg": int(dbp_base * random.uniform(low_mult, high_mult)),
            "pulse_pressure_variation": round(random.uniform(8, 25), 1),
            "central_venous_pressure": round(random.uniform(2, 12), 1),
            "oxygen_saturation": round(random.uniform(85, 99), 1),
            "mixed_venous_o2": round(random.uniform(60, 80), 1),
            "ejection_fraction": round(random.uniform(35, 70), 1),
            "stroke_volume": round(random.uniform(15, 45), 1),
            "cardiac_output": round(random.uniform(2.5, 8.0), 2)
        }
    
    def generate_hematologic_labs(self, age_months: int, ethnicity: str) -> Dict[str, Any]:
        """Generate comprehensive hematologic laboratory results"""
        # Age-based normal ranges
        if age_months < 6:
            hgb_range, hct_range = (10.0, 15.0), (30, 45)
        elif age_months < 24:
            hgb_range, hct_range = (10.5, 13.5), (32, 40)
        elif age_months < 72:
            hgb_range, hct_range = (11.0, 14.0), (33, 42)
        else:
            hgb_range, hct_range = (11.5, 15.5), (35, 45)
        
        # Adjust for ethnicity-related conditions
        ethnicity_risk = self.ethnicity_risks[ethnicity]
        
        # Base values
        hemoglobin = random.uniform(*hgb_range)
        hematocrit = random.uniform(*hct_range)
        
        # Adjust for sickle cell or thalassemia if present
        if random.random() < ethnicity_risk["sickle_cell"]:
            hemoglobin *= 0.6  # Sickle cell anemia
            hematocrit *= 0.7
        elif random.random() < ethnicity_risk["thalassemia"]:
            hemoglobin *= 0.75  # Thalassemia
        
        return {
            "hemoglobin_g_dl": round(hemoglobin, 1),
            "hematocrit_percent": round(hematocrit, 1),
            "platelet_count_k_ul": random.randint(150, 450),
            "wbc_count_k_ul": round(random.uniform(4.5, 13.5), 1),
            "mcv_fl": round(random.uniform(70, 95), 1),
            "mch_pg": round(random.uniform(23, 33), 1),
            "rdw_percent": round(random.uniform(11.5, 16.0), 1),
            "pt_seconds": round(random.uniform(11, 15), 1),
            "aptt_seconds": round(random.uniform(25, 35), 1),
            "inr": round(random.uniform(0.8, 1.2), 2),
            "fibrinogen_mg_dl": random.randint(200, 400),
            "d_dimer_ng_ml": round(random.uniform(0, 500), 1),
            "antithrombin_iii_percent": random.randint(80, 120),
            "reticulocyte_count_percent": round(random.uniform(0.5, 2.5), 1)
        }
    
    def generate_therapeutics(self, condition_type: str, age_months: int) -> Dict[str, Any]:
        """Generate therapeutic interventions and medications"""
        anticoagulants = []
        antiplatelets = []
        
        # Age-appropriate anticoagulation
        if age_months >= 12 and random.random() < 0.3:
            anticoagulants.extend(random.sample(
                ["Warfarin", "Heparin", "Enoxaparin"], 
                random.randint(0, 2)
            ))
        
        if age_months >= 24 and random.random() < 0.2:
            antiplatelets.append("Aspirin (low-dose)")
        
        # Transfusion history
        transfusion_history = []
        if random.random() < 0.25:
            for i in range(random.randint(1, 3)):
                transfusion_history.append({
                    "date": (datetime.now() - timedelta(days=random.randint(7, 90))).strftime("%Y-%m-%d"),
                    "product": random.choice(["PRBC", "FFP", "Platelets", "Cryoprecipitate"]),
                    "volume_ml": random.randint(50, 250),
                    "indication": random.choice(["Anemia", "Bleeding", "Pre-operative", "Coagulopathy"])
                })
        
        return {
            "anticoagulants": anticoagulants,
            "antiplatelets": antiplatelets,
            "esa_therapy": random.random() < 0.1,
            "transfusion_history": transfusion_history
        }
    
    def generate_clinical_notes(self, demographics: Dict, vitals: Dict, condition_type: str) -> Dict[str, str]:
        """Generate realistic unstructured clinical notes"""
        age_years = demographics["age_months"] // 12
        age_display = f"{age_years} years" if age_years > 0 else f"{demographics['age_months']} months"
        
        cardiology_note = f"""
PEDIATRIC CARDIOLOGY CONSULTATION

Patient: {age_display} old {demographics['sex']} with {condition_type.replace('_', ' ')}

HISTORY: Patient presents with {random.choice(['dyspnea on exertion', 'chest pain', 'syncope', 'palpitations'])}. 
Family history {'positive' if demographics['family_history_cvd'] else 'negative'} for cardiovascular disease.

PHYSICAL EXAM:
- Vitals: HR {vitals['heart_rate_bpm']}, BP {vitals['systolic_bp_mmhg']}/{vitals['diastolic_bp_mmhg']}, O2 sat {vitals['oxygen_saturation']}%
- Cardiac: {random.choice(['Regular rate and rhythm', 'Irregular rhythm', 'Murmur grade II/VI'])}
- Pulmonary: {random.choice(['Clear bilaterally', 'Mild rales', 'Decreased breath sounds'])}

ASSESSMENT: {condition_type.replace('_', ' ').title()} with {random.choice(['stable', 'worsening', 'improving'])} hemodynamics.

PLAN: Continue current management, follow-up in {random.choice(['2 weeks', '1 month', '3 months'])}.
        """.strip()
        
        hematology_note = f"""
HEMATOLOGY ASSESSMENT

{age_display} old patient with underlying cardiac condition and hematologic concerns.

LABORATORY REVIEW:
- Hemoglobin: {vitals.get('hemoglobin_g_dl', 'N/A')} g/dL
- Platelet count: {vitals.get('platelet_count_k_ul', 'N/A')} K/μL
- Coagulation studies: PT/INR/aPTT within normal limits

ASSESSMENT: {'Anemia likely secondary to chronic disease' if random.random() < 0.4 else 'Normal hematologic parameters'}

RECOMMENDATIONS: {random.choice(['Iron supplementation', 'Follow-up labs in 4 weeks', 'No acute intervention needed'])}
        """.strip()
        
        return {
            "cardiology_consultation": cardiology_note,
            "hematology_assessment": hematology_note,
            "transfusion_protocol": "Standard pediatric transfusion protocol followed per institutional guidelines.",
            "surgical_narrative": f"Successful {random.choice(['repair', 'palliation', 'correction'])} of congenital heart defect." if condition_type == "congenital_heart_disease" else "",
            "anticoagulation_plan": "Age-appropriate anticoagulation with close monitoring of coagulation parameters."
        }
    
    def generate_timeseries_data(self) -> Dict[str, Any]:
        """Generate physiologic monitoring time-series data"""
        # ECG findings
        ecg_findings = {
            "rhythm": random.choice(["Sinus rhythm", "Sinus tachycardia", "Atrial fibrillation", "Junctional rhythm"]),
            "rate": random.randint(80, 160),
            "axis": random.choice(["Normal", "Left deviation", "Right deviation"]),
            "intervals": {
                "pr_ms": random.randint(120, 200),
                "qrs_ms": random.randint(80, 120),
                "qt_ms": random.randint(350, 450)
            }
        }
        
        # Arterial pressure traces (24 hours of hourly readings)
        arterial_pressures = [random.uniform(60, 120) for _ in range(24)]
        
        # Pulse oximetry time series
        pulse_ox_data = []
        for hour in range(24):
            pulse_ox_data.append({
                "timestamp": hour,
                "spo2": random.uniform(92, 99),
                "heart_rate": random.randint(80, 140)
            })
        
        # Blood gas data
        blood_gas_data = []
        for i in range(random.randint(2, 6)):
            blood_gas_data.append({
                "timestamp": f"Day {i+1}",
                "ph": round(random.uniform(7.30, 7.45), 2),
                "pco2": round(random.uniform(35, 45), 1),
                "po2": round(random.uniform(80, 100), 1),
                "hco3": round(random.uniform(20, 26), 1),
                "lactate": round(random.uniform(0.5, 2.0), 1)
            })
        
        return {
            "ecg_findings": ecg_findings,
            "arterial_pressure_traces": arterial_pressures,
            "pulse_oximetry_timeseries": pulse_ox_data,
            "blood_gas_data": blood_gas_data
        }
    
    def generate_genomic_data(self, ethnicity: str) -> Dict[str, Any]:
        """Generate genomic and molecular data"""
        # Factor V Leiden more common in Caucasians
        factor_v_risk = 0.05 if ethnicity == "Caucasian" else 0.01
        
        return {
            "factor_v_leiden": "Positive" if random.random() < factor_v_risk else "Negative",
            "prothrombin_mutation": "G20210A variant" if random.random() < 0.02 else "Wild type",
            "jak2_mutation": "V617F positive" if random.random() < 0.001 else "Negative",
            "hba_hbb_mutations": self._get_hemoglobin_mutations(ethnicity),
            "hfe_mutations": "C282Y/H63D" if random.random() < 0.1 else "Wild type",
            "platelet_function_genes": {
                "GP1BA": "Normal" if random.random() < 0.95 else "Variant",
                "GP6": "Normal" if random.random() < 0.98 else "Variant"
            }
        }
    
    def generate_imaging_data(self, condition_type: str) -> Dict[str, Any]:
        """Generate comprehensive imaging findings"""
        # Echocardiogram
        echo_data = {
            "ejection_fraction": random.randint(35, 70),
            "valve_function": {
                "mitral": random.choice(["Normal", "Mild regurgitation", "Moderate regurgitation"]),
                "tricuspid": random.choice(["Normal", "Mild regurgitation"]),
                "aortic": random.choice(["Normal", "Mild stenosis"]),
                "pulmonary": "Normal"
            },
            "chamber_dimensions": {
                "lv_end_diastolic": random.uniform(3.5, 5.5),
                "la_dimension": random.uniform(2.5, 4.0),
                "rv_dimension": random.uniform(2.0, 3.5)
            },
            "clot_presence": random.choice(["None", "Small apical thrombus"]) if random.random() < 0.05 else "None"
        }
        
        # Cardiac MRI
        cardiac_mri = {
            "late_gadolinium_enhancement": "Present" if random.random() < 0.2 else "Absent",
            "perfusion": random.choice(["Normal", "Mild hypoperfusion", "Regional defect"]),
            "wall_motion": random.choice(["Normal", "Hypokinetic", "Akinetic segments"])
        }
        
        # Chest X-ray
        chest_xray = {
            "cardiomegaly": "Present" if random.random() < 0.3 else "Absent",
            "pulmonary_edema": "Mild" if random.random() < 0.15 else "None",
            "pleural_effusion": "Small bilateral" if random.random() < 0.1 else "None"
        }
        
        return {
            "echocardiogram": echo_data,
            "cardiac_mri": cardiac_mri,
            "coronary_angiogram": None,  # Rare in pediatric patients
            "chest_xray": chest_xray,
            "abdominal_imaging": {
                "splenomegaly": "Present" if random.random() < 0.1 else "Absent",
                "liver_congestion": "Mild" if random.random() < 0.2 else "None"
            },
            "brain_imaging": None
        }
    
    def generate_administrative_codes(self, condition_type: str) -> Dict[str, List[str]]:
        """Generate appropriate medical coding"""
        icd10_codes = []
        cpt_codes = []
        drg_codes = []
        
        if condition_type == "congenital_heart_disease":
            icd10_codes.extend(["Q21.0", "Q21.1", "Q22.4", "Q23.4"])  # Congenital heart defects
            cpt_codes.extend(["93307", "93312", "33735"])  # Echo, cardiac cath, surgery
            drg_codes.extend(["216", "217", "218"])  # Cardiac procedures
            
        elif condition_type == "acquired_heart_disease":
            icd10_codes.extend(["I42.9", "I40.9", "I05.9"])  # Cardiomyopathy, myocarditis
            cpt_codes.extend(["93307", "93350"])  # Echocardiogram, stress echo
            
        # Add hematologic codes if relevant
        if random.random() < 0.3:
            icd10_codes.extend(["D64.9", "D69.6"])  # Anemia, thrombocytopenia
            cpt_codes.extend(["85025", "85730"])  # CBC, thrombocytopenia workup
        
        return {
            "icd10_codes": icd10_codes,
            "cpt_codes": cpt_codes,
            "drg_codes": drg_codes
        }
    
    def generate_patient_outcomes(self, age_months: int) -> Dict[str, Any]:
        """Generate patient-reported outcomes"""
        # Age-appropriate fatigue scoring
        fatigue_max = 10 if age_months >= 96 else 5  # Simplified for younger children
        
        return {
            "fatigue_score": random.randint(1, fatigue_max),
            "nyha_class": random.randint(1, 3),  # Rare Class IV in pediatrics
            "bleeding_questionnaire": {
                "easy_bruising": random.choice(["Yes", "No"]),
                "nosebleeds": random.choice(["Frequent", "Occasional", "None"]),
                "dental_bleeding": random.choice(["Yes", "No"]),
                "menstrual_bleeding": "N/A" if age_months < 144 or random.choice(["M", "F"]) == "M" else random.choice(["Heavy", "Normal"])
            }
        }
    
    def generate_complete_record(self, condition_type: str = "congenital_heart_disease") -> PediatricCardiologyRecord:
        """Generate a complete pediatric cardiology synthetic record"""
        demographics = self.generate_demographics(condition_type)
        
        # Determine condition severity
        condition_severity = random.choice(["mild", "moderate", "severe"])
        
        # Generate all data components
        vitals = self.generate_cardiac_vitals(demographics["age_months"], condition_severity)
        hematologic = self.generate_hematologic_labs(demographics["age_months"], demographics["race_ethnicity"])
        therapeutics = self.generate_therapeutics(condition_type, demographics["age_months"])
        clinical_notes = self.generate_clinical_notes(demographics, {**vitals, **hematologic}, condition_type)
        timeseries = self.generate_timeseries_data()
        genomic = self.generate_genomic_data(demographics["race_ethnicity"])
        imaging = self.generate_imaging_data(condition_type)
        admin_codes = self.generate_administrative_codes(condition_type)
        outcomes = self.generate_patient_outcomes(demographics["age_months"])
        
        # Combine all data into complete record
        complete_record = PediatricCardiologyRecord(
            **demographics,
            **vitals,
            **hematologic,
            **therapeutics,
            **clinical_notes,
            **timeseries,
            **genomic,
            **imaging,
            **admin_codes,
            **outcomes
        )
        
        return complete_record
    
    def _calculate_pediatric_measurements(self, age_months: int, sex: str) -> tuple:
        """Calculate age and sex-appropriate weight and height using growth charts"""
        # Simplified pediatric growth curves
        if age_months <= 24:  # 0-2 years
            if sex == "M":
                weight_kg = 3.3 + (age_months * 0.5)  # Birth weight ~3.3kg, gain ~0.5kg/month
                height_cm = 50 + (age_months * 1.2)    # Birth length ~50cm, gain ~1.2cm/month
            else:
                weight_kg = 3.2 + (age_months * 0.45)
                height_cm = 49 + (age_months * 1.1)
        else:  # 2+ years
            years = age_months / 12
            if sex == "M":
                weight_kg = 12 + (years * 2.5)  # ~12kg at 2 years, gain ~2.5kg/year
                height_cm = 85 + ((years - 2) * 6)  # ~85cm at 2 years, gain ~6cm/year
            else:
                weight_kg = 11.5 + (years * 2.3)
                height_cm = 84 + ((years - 2) * 5.8)
        
        # Add some random variation
        weight_kg *= random.uniform(0.85, 1.15)
        height_cm *= random.uniform(0.95, 1.05)
        
        return weight_kg, height_cm
    
    def _get_hemoglobin_mutations(self, ethnicity: str) -> str:
        """Get ethnicity-appropriate hemoglobin mutations"""
        risks = self.ethnicity_risks[ethnicity]
        
        if random.random() < risks["sickle_cell"]:
            return "HbS/HbS (Sickle cell disease)"
        elif random.random() < risks["thalassemia"]:
            return "Beta-thalassemia trait"
        else:
            return "Normal (HbA/HbA)"

# Example usage and testing
if __name__ == "__main__":
    generator = PediatricCardiologyGenerator()
    
    # Generate a sample record
    record = generator.generate_complete_record("congenital_heart_disease")
    
    # Convert to JSON for review
    record_dict = asdict(record)
    print(json.dumps(record_dict, indent=2, default=str))