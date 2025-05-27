"""
Configuration Mapper for Synthetic Ascension
Translates frontend multi-select configurations into EHR schema generation parameters
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import random
from ehr_schema_generator import *

@dataclass
class SyntheticDataConfiguration:
    """Maps frontend configuration to data generation parameters"""
    
    # Population parameters
    population_size: int = 1000
    age_ranges: Optional[List[str]] = None
    demographics: Optional[List[str]] = None
    
    # Medical conditions
    cardiac_conditions: Optional[List[str]] = None
    hematologic_conditions: Optional[List[str]] = None
    genetic_markers: Optional[List[str]] = None
    
    # Data modalities
    data_types: Optional[List[str]] = None
    lab_parameters: Optional[List[str]] = None
    procedure_types: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    
    # Configuration metadata
    use_case_name: str = ""
    specialty_focus: Optional[List[str]] = None
    timeline_coverage: str = ""
    validation_rigor: str = ""

class ConfigurationMapper:
    """Maps frontend selections to EHR schema generation"""
    
    def __init__(self):
        self.cardiac_condition_mapping = {
            'Tetralogy of Fallot': {
                'icd10_codes': ['Q21.3'],
                'required_labs': ['hemoglobin', 'hematocrit', 'oxygen_saturation'],
                'required_procedures': ['cardiac_catheterization', 'echocardiogram'],
                'hemodynamic_requirements': ['ejection_fraction', 'pulmonary_pressure']
            },
            'Hypoplastic Left Heart Syndrome': {
                'icd10_codes': ['Q23.4'],
                'required_labs': ['bnt', 'troponin', 'lactate'],
                'required_procedures': ['norwood', 'glenn', 'fontan'],
                'hemodynamic_requirements': ['cardiac_output', 'central_venous_pressure']
            },
            'Iron Deficiency Anemia': {
                'icd10_codes': ['D50.9'],
                'required_labs': ['ferritin', 'iron', 'tibc', 'transferrin_saturation'],
                'medications': ['ferrous_sulfate', 'iron_infusion'],
                'monitoring_frequency': 'monthly'
            }
        }
        
        self.lab_parameter_mapping = {
            'Complete Blood Count (CBC)': {
                'loinc_codes': ['26464-8', '6690-2', '33747-0'],
                'components': ['wbc', 'rbc', 'hemoglobin', 'hematocrit', 'platelet_count'],
                'pediatric_ranges': True
            },
            'Ferritin & Iron Studies': {
                'loinc_codes': ['2276-4', '2498-4', '2500-7'],
                'components': ['ferritin', 'iron', 'tibc', 'transferrin_saturation'],
                'critical_for_conditions': ['iron_deficiency_anemia']
            },
            'PT/INR & aPTT': {
                'loinc_codes': ['5902-2', '6301-6', '14979-9'],
                'components': ['prothrombin_time', 'inr', 'ptt'],
                'critical_for_procedures': ['cardiac_surgery', 'anticoagulation']
            }
        }
        
        self.procedure_mapping = {
            'Cardiac Catheterization': {
                'cpt_codes': ['93454', '93455', '93456'],
                'generates_data': ['hemodynamic_measurements', 'angiography_results'],
                'duration_hours': [2, 4],
                'age_restrictions': 'pediatric_modified'
            },
            'Blood Transfusions': {
                'cpt_codes': ['36430', '36440'],
                'generates_data': ['pre_transfusion_labs', 'post_transfusion_monitoring'],
                'indication_mapping': ['severe_anemia', 'surgical_blood_loss']
            }
        }
    
    def map_frontend_config_to_schema(self, frontend_config: Dict[str, Any]) -> SyntheticDataConfiguration:
        """Convert frontend multi-select configuration to schema parameters"""
        
        config = SyntheticDataConfiguration()
        
        # Map population parameters
        if 'population_size' in frontend_config:
            size_mapping = {
                'Small Cohort (10-50 patients)': 50,
                'Medium Cohort (100-500 patients)': 500,
                'Large Cohort (1,000-5,000 patients)': 5000,
                'Enterprise Scale (10,000+ patients)': 10000,
                'Featured Demo Scale (N=10,000 Pediatric)': 10000
            }
            config.population_size = size_mapping.get(frontend_config['population_size'], 1000)
        
        # Map cardiac conditions to ICD-10 codes and required data
        if 'cardiac_conditions' in frontend_config:
            config.cardiac_conditions = frontend_config['cardiac_conditions']
        
        # Map hematologic conditions
        if 'hematologic_conditions' in frontend_config:
            config.hematologic_conditions = frontend_config['hematologic_conditions']
        
        # Map lab parameters to LOINC codes
        if 'lab_parameters' in frontend_config:
            config.lab_parameters = frontend_config['lab_parameters']
        
        # Map demographics
        if 'demographics' in frontend_config:
            config.demographics = frontend_config['demographics']
        
        # Map data types to generation modules
        if 'data_types' in frontend_config:
            config.data_types = frontend_config['data_types']
        
        return config
    
    def generate_patient_schema(self, config: SyntheticDataConfiguration, patient_index: int) -> Dict[str, Any]:
        """Generate complete patient schema based on configuration"""
        
        patient_schema = {
            'demographics': self._generate_demographics(config, patient_index),
            'conditions': self._generate_conditions(config),
            'lab_results': self._generate_lab_results(config),
            'medications': self._generate_medications(config),
            'procedures': self._generate_procedures(config),
            'clinical_notes': self._generate_clinical_notes(config),
            'hemodynamics': self._generate_hemodynamics(config),
            'audit_trail': self._generate_audit_trail(config, patient_index)
        }
        
        return patient_schema
    
    def _generate_demographics(self, config: SyntheticDataConfiguration, patient_index: int) -> Demographics:
        """Generate realistic demographics based on configuration"""
        demo = Demographics()
        
        # Apply age range selections
        if config.demographics and 'Age 0-5 years (Early Pediatric)' in config.demographics:
            demo.age_years = random.randint(0, 5)
            demo.age_months = demo.age_years * 12 + random.randint(0, 11)
        elif config.demographics and 'Age 6-12 years (Middle Pediatric)' in config.demographics:
            demo.age_years = random.randint(6, 12)
            demo.age_months = demo.age_years * 12 + random.randint(0, 11)
        
        # Apply demographic selections
        if config.demographics:
            if 'Oversample Black & Hispanic Patients' in config.demographics:
                demo.ethnicity = random.choice(['Hispanic or Latino', 'Not Hispanic or Latino'])
                demo.race_primary = random.choice(['Black or African American', 'Hispanic/Latino', 'White'])
            
            if 'Urban vs Rural (60/40 split)' in config.demographics:
                demo.city = random.choice(['Urban_City', 'Rural_Town'])
        
        return demo
    
    def _generate_conditions(self, config: SyntheticDataConfiguration) -> List[DiagnosisCode]:
        """Generate diagnosis codes based on selected conditions"""
        conditions = []
        
        if config.cardiac_conditions:
            for condition in config.cardiac_conditions:
                if condition in self.cardiac_condition_mapping:
                    mapping = self.cardiac_condition_mapping[condition]
                    for icd_code in mapping['icd10_codes']:
                        dx = DiagnosisCode()
                        dx.icd10_code = icd_code
                        dx.icd10_description = condition
                        dx.diagnosis_type = 'Primary'
                        dx.diagnosis_status = 'Active'
                        conditions.append(dx)
        
        if config.hematologic_conditions:
            for condition in config.hematologic_conditions:
                if condition in self.cardiac_condition_mapping:  # Extend mapping
                    mapping = self.cardiac_condition_mapping[condition]
                    for icd_code in mapping['icd10_codes']:
                        dx = DiagnosisCode()
                        dx.icd10_code = icd_code
                        dx.icd10_description = condition
                        dx.diagnosis_type = 'Secondary'
                        dx.diagnosis_status = 'Active'
                        conditions.append(dx)
        
        return conditions
    
    def _generate_lab_results(self, config: SyntheticDataConfiguration) -> List[LabResult]:
        """Generate lab results based on selected parameters"""
        lab_results = []
        
        if config.lab_parameters:
            for lab_param in config.lab_parameters:
                if lab_param in self.lab_parameter_mapping:
                    mapping = self.lab_parameter_mapping[lab_param]
                    for component in mapping['components']:
                        lab = LabResult()
                        lab.lab_name = component
                        lab.loinc_code = mapping['loinc_codes'][0]  # Use first LOINC code
                        
                        # Generate realistic values based on component
                        if component == 'hemoglobin':
                            if 'Iron Deficiency Anemia' in (config.hematologic_conditions or []):
                                lab.result_value = random.uniform(6.0, 9.0)  # Low for anemia
                                lab.abnormal_flag = 'Low'
                            else:
                                lab.result_value = random.uniform(12.0, 16.0)  # Normal range
                        elif component == 'ferritin':
                            if 'Iron Deficiency Anemia' in (config.hematologic_conditions or []):
                                lab.result_value = random.uniform(5.0, 15.0)  # Low for iron deficiency
                                lab.abnormal_flag = 'Low'
                            else:
                                lab.result_value = random.uniform(15.0, 200.0)  # Normal range
                        
                        lab.result_unit = self._get_unit_for_component(component)
                        lab_results.append(lab)
        
        return lab_results
    
    def _generate_medications(self, config: SyntheticDataConfiguration) -> List[Medication]:
        """Generate medications based on conditions and selections"""
        medications = []
        
        # Generate condition-specific medications
        if config.hematologic_conditions:
            if 'Iron Deficiency Anemia' in config.hematologic_conditions:
                iron_med = Medication()
                iron_med.generic_name = 'Ferrous Sulfate'
                iron_med.dosage_amount = 325.0
                iron_med.dosage_unit = 'mg'
                iron_med.frequency = 'BID'
                iron_med.indication = 'Iron Deficiency Anemia'
                medications.append(iron_med)
        
        return medications
    
    def _generate_procedures(self, config: SyntheticDataConfiguration) -> List[Dict[str, Any]]:
        """Generate procedures based on conditions and selections"""
        procedures = []
        
        if config.cardiac_conditions:
            if 'Tetralogy of Fallot' in config.cardiac_conditions:
                procedures.append({
                    'procedure_name': 'Cardiac Catheterization',
                    'cpt_code': '93454',
                    'indication': 'Tetralogy of Fallot evaluation'
                })
        
        return procedures
    
    def _generate_clinical_notes(self, config: SyntheticDataConfiguration) -> List[str]:
        """Generate realistic clinical notes based on configuration"""
        notes = []
        
        if config.cardiac_conditions and config.hematologic_conditions:
            notes.append(f"""
PROGRESS NOTE - Pediatric Cardiology
Patient presents for routine follow-up of {', '.join(config.cardiac_conditions or [])} 
with concurrent {', '.join(config.hematologic_conditions or [])}.

Current symptoms: Well-appearing child with stable cardiac status.
Recent labs show ongoing management needs for hematologic condition.
Plan: Continue current medications, repeat labs in 4 weeks.
            """.strip())
        
        return notes
    
    def _generate_hemodynamics(self, config: SyntheticDataConfiguration) -> Optional[HemodynamicData]:
        """Generate hemodynamic data for cardiac patients"""
        if not config.cardiac_conditions:
            return None
        
        hemo = HemodynamicData()
        
        # Generate realistic values based on cardiac conditions
        if 'Tetralogy of Fallot' in config.cardiac_conditions:
            hemo.ejection_fraction_percent = random.uniform(45.0, 65.0)
            hemo.heart_rate_bpm = random.uniform(80.0, 120.0)  # Pediatric range
            hemo.systolic_bp = random.uniform(90.0, 110.0)
        
        return hemo
    
    def _generate_audit_trail(self, config: SyntheticDataConfiguration, patient_index: int) -> AuditTrail:
        """Generate audit trail for compliance"""
        audit = AuditTrail()
        audit.operation_type = 'GENERATE'
        audit.record_type = 'SYNTHETIC_PATIENT'
        audit.record_id = f"PAT_{patient_index:06d}"
        audit.change_reason = f"Synthetic data generation for use case: {config.use_case_name}"
        
        return audit
    
    def _get_unit_for_component(self, component: str) -> str:
        """Get appropriate unit for lab component"""
        unit_mapping = {
            'hemoglobin': 'g/dL',
            'hematocrit': '%',
            'ferritin': 'ng/mL',
            'iron': 'μg/dL',
            'wbc': 'cells/μL',
            'platelet_count': 'cells/μL'
        }
        return unit_mapping.get(component, '')

# Export for use in API
__all__ = ['ConfigurationMapper', 'SyntheticDataConfiguration']