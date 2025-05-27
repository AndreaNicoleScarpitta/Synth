"""
Multimodal EHR Generation Agent
Generates structured, unstructured, and multimodal synthetic EHR data
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
import json
import uuid
from utils.ollama_client import OllamaClient
from models.patient_data import Patient

class MultimodalEHRAgent:
    """Generates comprehensive multimodal EHR data from clinical contexts"""
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
        
        # Clinical note templates for different specialties
        self.note_templates = {
            'admission': {
                'sections': ['Chief Complaint', 'History of Present Illness', 'Past Medical History', 
                           'Medications', 'Physical Examination', 'Assessment and Plan'],
                'style': 'formal_clinical'
            },
            'progress': {
                'sections': ['Subjective', 'Objective', 'Assessment', 'Plan'],
                'style': 'concise_clinical'
            },
            'discharge': {
                'sections': ['Hospital Course', 'Discharge Medications', 'Follow-up Instructions', 
                           'Discharge Condition'],
                'style': 'comprehensive'
            },
            'consult': {
                'sections': ['Reason for Consultation', 'History', 'Examination', 'Recommendations'],
                'style': 'specialist_focused'
            }
        }
        
        # Imaging study templates
        self.imaging_templates = {
            'chest_xray': {
                'findings': ['heart size', 'lung fields', 'mediastinum', 'pleural spaces'],
                'common_abnormalities': ['cardiomegaly', 'pneumonia', 'pleural effusion', 'pneumothorax']
            },
            'ct_chest': {
                'findings': ['lungs', 'mediastinum', 'pleura', 'chest wall'],
                'common_abnormalities': ['pulmonary nodules', 'lymphadenopathy', 'consolidation']
            },
            'echocardiogram': {
                'findings': ['left ventricle', 'right ventricle', 'valves', 'pericardium'],
                'measurements': ['LVEF', 'wall thickness', 'chamber dimensions']
            },
            'mri_brain': {
                'findings': ['cerebral hemispheres', 'brainstem', 'cerebellum', 'ventricles'],
                'sequences': ['T1', 'T2', 'FLAIR', 'DWI']
            }
        }
        
        # Vital signs patterns
        self.vital_patterns = {
            'normal': {'hr': (60, 100), 'sbp': (90, 140), 'dbp': (60, 90), 'temp': (98.0, 100.4), 'rr': (12, 20), 'spo2': (95, 100)},
            'hypertensive': {'hr': (70, 110), 'sbp': (140, 180), 'dbp': (90, 110), 'temp': (98.0, 100.4), 'rr': (12, 22), 'spo2': (95, 100)},
            'septic': {'hr': (100, 140), 'sbp': (80, 120), 'dbp': (50, 80), 'temp': (100.5, 104.0), 'rr': (20, 30), 'spo2': (88, 96)},
            'respiratory_distress': {'hr': (90, 130), 'sbp': (100, 160), 'dbp': (60, 100), 'temp': (98.0, 101.0), 'rr': (24, 40), 'spo2': (85, 94)}
        }
    
    def generate_comprehensive_ehr(self, patient: Patient, clinical_context: str, 
                                 include_time_series: bool = True,
                                 include_imaging: bool = True,
                                 include_procedures: bool = True) -> Dict[str, Any]:
        """Generate comprehensive multimodal EHR data"""
        
        ehr_data = {
            'patient_id': patient.patient_id,
            'generation_timestamp': datetime.now().isoformat(),
            'clinical_context': clinical_context,
            'structured_data': {},
            'unstructured_data': {},
            'multimodal_data': {},
            'time_series_data': {},
            'metadata': {
                'generation_method': 'multimodal_llm',
                'data_types': [],
                'clinical_specialty': self._infer_specialty(clinical_context),
                'complexity_score': self._calculate_complexity_score(patient)
            }
        }
        
        # Generate structured data
        ehr_data['structured_data'] = self._generate_structured_data(patient, clinical_context)
        ehr_data['metadata']['data_types'].append('structured')
        
        # Generate unstructured clinical notes
        ehr_data['unstructured_data'] = self._generate_clinical_notes(patient, clinical_context)
        ehr_data['metadata']['data_types'].append('unstructured')
        
        # Generate time series data if requested
        if include_time_series:
            ehr_data['time_series_data'] = self._generate_time_series_data(patient, clinical_context)
            ehr_data['metadata']['data_types'].append('time_series')
        
        # Generate imaging and multimodal data if requested
        if include_imaging:
            ehr_data['multimodal_data']['imaging'] = self._generate_imaging_data(patient, clinical_context)
            ehr_data['metadata']['data_types'].append('imaging')
        
        # Generate procedure data if requested
        if include_procedures:
            ehr_data['multimodal_data']['procedures'] = self._generate_procedure_data(patient, clinical_context)
            ehr_data['metadata']['data_types'].append('procedures')
        
        return ehr_data
    
    def _generate_structured_data(self, patient: Patient, context: str) -> Dict[str, Any]:
        """Generate structured EHR components"""
        
        structured_data = {
            'demographics': {
                'age': patient.age,
                'gender': patient.gender,
                'ethnicity': patient.ethnicity,
                'marital_status': np.random.choice(['Single', 'Married', 'Divorced', 'Widowed']),
                'preferred_language': 'English',
                'insurance': np.random.choice(['Medicare', 'Medicaid', 'Private', 'Uninsured'])
            },
            'encounters': [],
            'diagnoses': [],
            'medications': [],
            'allergies': [],
            'social_history': {},
            'family_history': []
        }
        
        # Generate encounter data
        encounter_types = self._determine_encounter_types(context)
        for enc_type in encounter_types:
            encounter = self._generate_encounter(patient, enc_type, context)
            structured_data['encounters'].append(encounter)
        
        # Structure existing patient data
        for i, condition in enumerate(patient.conditions):
            diagnosis = {
                'icd10_code': self._get_icd10_code(condition),
                'diagnosis': condition,
                'onset_date': self._generate_onset_date(condition, patient.age),
                'status': np.random.choice(['Active', 'Chronic', 'Resolved'], p=[0.6, 0.3, 0.1]),
                'severity': np.random.choice(['Mild', 'Moderate', 'Severe'], p=[0.4, 0.4, 0.2])
            }
            structured_data['diagnoses'].append(diagnosis)
        
        # Structure medications with enhanced details
        for medication in patient.medications:
            med_data = {
                'medication': medication,
                'generic_name': self._get_generic_name(medication),
                'dosage': self._generate_dosage(medication),
                'frequency': self._generate_frequency(medication),
                'route': self._generate_route(medication),
                'start_date': self._generate_medication_start_date(),
                'prescriber': self._generate_prescriber(),
                'indication': self._match_medication_to_condition(medication, patient.conditions)
            }
            structured_data['medications'].append(med_data)
        
        # Generate allergies
        structured_data['allergies'] = self._generate_allergies(patient)
        
        # Generate social history
        structured_data['social_history'] = self._generate_social_history(patient, context)
        
        # Generate family history
        structured_data['family_history'] = self._generate_family_history(patient)
        
        return structured_data
    
    def _generate_clinical_notes(self, patient: Patient, context: str) -> Dict[str, Any]:
        """Generate unstructured clinical notes using LLM"""
        
        notes_data = {
            'admission_note': None,
            'progress_notes': [],
            'discharge_summary': None,
            'specialist_consults': [],
            'nursing_notes': [],
            'radiology_reports': []
        }
        
        # Generate admission note
        if any(word in context.lower() for word in ['admission', 'hospital', 'inpatient']):
            notes_data['admission_note'] = self._generate_admission_note(patient, context)
        
        # Generate progress notes
        num_progress_notes = np.random.randint(1, 4)
        for i in range(num_progress_notes):
            progress_note = self._generate_progress_note(patient, context, day=i+1)
            notes_data['progress_notes'].append(progress_note)
        
        # Generate discharge summary if appropriate
        if 'discharge' in context.lower() or np.random.random() > 0.7:
            notes_data['discharge_summary'] = self._generate_discharge_summary(patient, context)
        
        # Generate specialist consults based on conditions
        specialty_consults = self._determine_needed_consults(patient.conditions)
        for specialty in specialty_consults:
            consult_note = self._generate_consult_note(patient, specialty, context)
            notes_data['specialist_consults'].append(consult_note)
        
        return notes_data
    
    def _generate_time_series_data(self, patient: Patient, context: str) -> Dict[str, Any]:
        """Generate time series vital signs and lab trends"""
        
        # Determine time series pattern based on patient conditions
        pattern_type = self._determine_vital_pattern(patient.conditions)
        
        # Generate 72-hour time series (every 4 hours)
        time_points = 18
        start_time = datetime.now() - timedelta(hours=72)
        
        time_series = {
            'vital_signs': {
                'timestamps': [],
                'heart_rate': [],
                'blood_pressure_systolic': [],
                'blood_pressure_diastolic': [],
                'temperature': [],
                'respiratory_rate': [],
                'oxygen_saturation': []
            },
            'lab_trends': {},
            'intake_output': {
                'timestamps': [],
                'fluid_intake': [],
                'urine_output': []
            }
        }
        
        # Generate vital signs time series
        pattern = self.vital_patterns[pattern_type]
        
        for i in range(time_points):
            timestamp = start_time + timedelta(hours=i*4)
            time_series['vital_signs']['timestamps'].append(timestamp.isoformat())
            
            # Add realistic variation and trends
            time_factor = i / time_points  # 0 to 1 progression
            
            # Heart rate with realistic variation
            hr_base = np.random.uniform(*pattern['hr'])
            hr_variation = np.random.normal(0, 5)  # ±5 bpm variation
            time_series['vital_signs']['heart_rate'].append(max(40, min(200, hr_base + hr_variation)))
            
            # Blood pressure with gradual trends
            sbp_base = np.random.uniform(*pattern['sbp'])
            sbp_trend = self._apply_clinical_trend(sbp_base, time_factor, pattern_type, 'sbp')
            time_series['vital_signs']['blood_pressure_systolic'].append(max(60, min(250, sbp_trend)))
            
            dbp_base = np.random.uniform(*pattern['dbp'])
            dbp_trend = self._apply_clinical_trend(dbp_base, time_factor, pattern_type, 'dbp')
            time_series['vital_signs']['blood_pressure_diastolic'].append(max(30, min(150, dbp_trend)))
            
            # Temperature with fever patterns
            temp_base = np.random.uniform(*pattern['temp'])
            temp_variation = np.random.normal(0, 0.5)
            time_series['vital_signs']['temperature'].append(max(95.0, min(108.0, temp_base + temp_variation)))
            
            # Respiratory rate
            rr_base = np.random.uniform(*pattern['rr'])
            rr_variation = np.random.normal(0, 2)
            time_series['vital_signs']['respiratory_rate'].append(max(8, min(50, rr_base + rr_variation)))
            
            # Oxygen saturation
            spo2_base = np.random.uniform(*pattern['spo2'])
            spo2_variation = np.random.normal(0, 2)
            time_series['vital_signs']['oxygen_saturation'].append(max(70, min(100, spo2_base + spo2_variation)))
        
        # Generate lab trends for key values
        for lab_name, (value, unit) in patient.lab_results.items():
            if lab_name.lower() in ['glucose', 'creatinine', 'hemoglobin', 'wbc']:
                time_series['lab_trends'][lab_name] = self._generate_lab_trend(lab_name, value, time_points)
        
        return time_series
    
    def _generate_imaging_data(self, patient: Patient, context: str) -> Dict[str, Any]:
        """Generate imaging study data and reports"""
        
        imaging_data = {
            'studies_ordered': [],
            'reports': {},
            'image_metadata': {}
        }
        
        # Determine appropriate imaging based on conditions and context
        indicated_studies = self._determine_imaging_studies(patient.conditions, context)
        
        for study_type in indicated_studies:
            study_id = str(uuid.uuid4())
            
            # Generate study metadata
            study_metadata = {
                'study_id': study_id,
                'study_type': study_type,
                'modality': self._get_imaging_modality(study_type),
                'study_date': datetime.now().isoformat(),
                'ordering_physician': self._generate_physician_name(),
                'indication': self._get_imaging_indication(study_type, patient.conditions),
                'technique': self._get_imaging_technique(study_type),
                'contrast_used': np.random.choice([True, False], p=[0.3, 0.7])
            }
            
            imaging_data['studies_ordered'].append(study_metadata)
            
            # Generate radiology report
            report = self._generate_radiology_report(patient, study_type, context)
            imaging_data['reports'][study_id] = report
            
            # Generate image placeholders (would be actual images in real implementation)
            imaging_data['image_metadata'][study_id] = {
                'image_count': np.random.randint(10, 50),
                'image_format': 'DICOM',
                'image_series': self._generate_image_series_info(study_type),
                'file_size_mb': np.random.randint(50, 500)
            }
        
        return imaging_data
    
    def _generate_procedure_data(self, patient: Patient, context: str) -> Dict[str, Any]:
        """Generate procedure and intervention data"""
        
        procedure_data = {
            'procedures_performed': [],
            'procedure_notes': {},
            'complications': []
        }
        
        # Determine procedures based on conditions
        indicated_procedures = self._determine_procedures(patient.conditions, context)
        
        for procedure in indicated_procedures:
            procedure_id = str(uuid.uuid4())
            
            procedure_info = {
                'procedure_id': procedure_id,
                'procedure_name': procedure,
                'cpt_code': self._get_cpt_code(procedure),
                'procedure_date': datetime.now().isoformat(),
                'performing_physician': self._generate_physician_name(),
                'anesthesia_type': self._determine_anesthesia_type(procedure),
                'duration_minutes': self._estimate_procedure_duration(procedure),
                'location': self._determine_procedure_location(procedure)
            }
            
            procedure_data['procedures_performed'].append(procedure_info)
            
            # Generate procedure note
            procedure_note = self._generate_procedure_note(patient, procedure, context)
            procedure_data['procedure_notes'][procedure_id] = procedure_note
            
            # Potential complications (low probability)
            if np.random.random() < 0.1:  # 10% chance of minor complications
                complication = self._generate_procedure_complication(procedure)
                procedure_data['complications'].append({
                    'procedure_id': procedure_id,
                    'complication': complication,
                    'severity': 'Minor',
                    'management': f"Managed conservatively with monitoring"
                })
        
        return procedure_data
    
    # Helper methods for generating specific components
    def _infer_specialty(self, context: str) -> str:
        """Infer medical specialty from context"""
        context_lower = context.lower()
        
        specialty_keywords = {
            'cardiology': ['heart', 'cardiac', 'coronary', 'arrhythmia', 'chest pain'],
            'nephrology': ['kidney', 'renal', 'dialysis', 'creatinine'],
            'endocrinology': ['diabetes', 'thyroid', 'hormone', 'glucose'],
            'pulmonology': ['lung', 'respiratory', 'copd', 'asthma', 'breathing'],
            'rheumatology': ['arthritis', 'autoimmune', 'joint', 'inflammatory'],
            'psychiatry': ['depression', 'anxiety', 'mental health', 'psychiatric'],
            'emergency': ['emergency', 'urgent', 'acute', 'trauma']
        }
        
        for specialty, keywords in specialty_keywords.items():
            if any(keyword in context_lower for keyword in keywords):
                return specialty
        
        return 'internal_medicine'
    
    def _calculate_complexity_score(self, patient: Patient) -> float:
        """Calculate clinical complexity score"""
        score = 0.0
        
        # Condition complexity
        score += len(patient.conditions) * 0.2
        
        # Medication complexity
        score += len(patient.medications) * 0.1
        
        # Age factor
        if patient.age:
            if patient.age > 75:
                score += 0.3
            elif patient.age > 65:
                score += 0.2
        
        # Lab abnormalities
        abnormal_labs = 0
        for lab_name, (value, unit) in patient.lab_results.items():
            # Simple abnormality detection
            if lab_name.lower() == 'glucose' and (value < 70 or value > 140):
                abnormal_labs += 1
            elif lab_name.lower() == 'creatinine' and value > 1.3:
                abnormal_labs += 1
        
        score += abnormal_labs * 0.15
        
        return min(1.0, score)  # Cap at 1.0
    
    def _generate_admission_note(self, patient: Patient, context: str) -> Dict[str, Any]:
        """Generate detailed admission note using LLM"""
        
        patient_summary = f"""
        Patient: {patient.age}-year-old {patient.gender} {patient.ethnicity}
        Primary Conditions: {', '.join(patient.conditions[:3])}
        Current Medications: {', '.join(patient.medications[:5])}
        Key Lab Values: {', '.join([f"{lab}: {val} {unit}" for lab, (val, unit) in list(patient.lab_results.items())[:3]])}
        Clinical Context: {context}
        """
        
        prompt = f"""
        Generate a comprehensive hospital admission note for this patient:
        
        {patient_summary}
        
        Include the following sections:
        1. Chief Complaint
        2. History of Present Illness
        3. Past Medical History
        4. Current Medications
        5. Physical Examination
        6. Assessment and Plan
        
        Use authentic medical terminology and clinical reasoning. Make the note realistic and clinically coherent.
        """
        
        try:
            note_content = self.ollama_client.generate_text(prompt)
            return {
                'note_type': 'admission',
                'author': self._generate_physician_name(),
                'timestamp': datetime.now().isoformat(),
                'content': note_content,
                'sections': self.note_templates['admission']['sections']
            }
        except Exception as e:
            return {
                'note_type': 'admission',
                'author': 'Dr. System Generated',
                'timestamp': datetime.now().isoformat(),
                'content': f"Admission note generation error: {str(e)}",
                'sections': []
            }
    
    def _generate_progress_note(self, patient: Patient, context: str, day: int) -> Dict[str, Any]:
        """Generate daily progress note"""
        
        patient_summary = f"""
        Hospital Day {day} for {patient.age}-year-old {patient.gender}
        Conditions: {', '.join(patient.conditions)}
        Context: {context}
        """
        
        prompt = f"""
        Generate a concise daily progress note:
        
        {patient_summary}
        
        Use SOAP format:
        - Subjective: Patient's symptoms and concerns
        - Objective: Vital signs, physical exam, lab results
        - Assessment: Clinical interpretation
        - Plan: Treatment adjustments and next steps
        
        Keep it realistic and focused on day {day} of hospitalization.
        """
        
        try:
            note_content = self.ollama_client.generate_text(prompt)
            return {
                'note_type': 'progress',
                'hospital_day': day,
                'author': self._generate_physician_name(),
                'timestamp': (datetime.now() - timedelta(days=day-1)).isoformat(),
                'content': note_content
            }
        except Exception as e:
            return {
                'note_type': 'progress',
                'hospital_day': day,
                'author': 'Dr. System Generated',
                'timestamp': (datetime.now() - timedelta(days=day-1)).isoformat(),
                'content': f"Progress note generation error for day {day}: {str(e)}"
            }
    
    # Additional helper methods (abbreviated for space)
    def _generate_discharge_summary(self, patient: Patient, context: str) -> Dict[str, Any]:
        """Generate discharge summary"""
        # Implementation similar to other note generation methods
        return {
            'note_type': 'discharge',
            'author': self._generate_physician_name(),
            'timestamp': datetime.now().isoformat(),
            'content': f"Discharge summary for {patient.patient_id}",
            'discharge_medications': patient.medications,
            'follow_up_instructions': ['Follow up with primary care in 1-2 weeks']
        }
    
    def _generate_radiology_report(self, patient: Patient, study_type: str, context: str) -> Dict[str, Any]:
        """Generate radiology report"""
        
        template = self.imaging_templates.get(study_type, {})
        findings = template.get('findings', ['Normal study'])
        
        prompt = f"""
        Generate a radiology report for {study_type} in a {patient.age}-year-old {patient.gender} with {', '.join(patient.conditions[:2])}.
        
        Include:
        1. Technique/Method
        2. Findings for: {', '.join(findings)}
        3. Impression
        
        Make it clinically realistic and appropriate for the patient's conditions.
        """
        
        try:
            report_content = self.ollama_client.generate_text(prompt)
            return {
                'study_type': study_type,
                'radiologist': self._generate_physician_name('Radiologist'),
                'timestamp': datetime.now().isoformat(),
                'content': report_content,
                'findings_summary': findings
            }
        except Exception as e:
            return {
                'study_type': study_type,
                'radiologist': 'Dr. System Generated',
                'timestamp': datetime.now().isoformat(),
                'content': f"Radiology report generation error: {str(e)}",
                'findings_summary': []
            }
    
    # Utility methods
    def _generate_physician_name(self, specialty: str = None) -> str:
        """Generate realistic physician names"""
        first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'David', 'Elizabeth']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        
        name = f"Dr. {np.random.choice(first_names)} {np.random.choice(last_names)}"
        if specialty:
            name += f", {specialty}"
        
        return name
    
    def _get_icd10_code(self, condition: str) -> str:
        """Get ICD-10 code for condition"""
        icd10_mapping = {
            'Diabetes Mellitus Type 2': 'E11.9',
            'Hypertension': 'I10',
            'Coronary Artery Disease': 'I25.9',
            'COPD': 'J44.1',
            'Depression': 'F32.9',
            'Anxiety': 'F41.9'
        }
        return icd10_mapping.get(condition, 'Z99.9')  # Default unknown code
    
    def _determine_vital_pattern(self, conditions: List[str]) -> str:
        """Determine vital sign pattern based on conditions"""
        if any('sepsis' in cond.lower() or 'infection' in cond.lower() for cond in conditions):
            return 'septic'
        elif any('hypertension' in cond.lower() for cond in conditions):
            return 'hypertensive'
        elif any('copd' in cond.lower() or 'asthma' in cond.lower() for cond in conditions):
            return 'respiratory_distress'
        else:
            return 'normal'
    
    def _apply_clinical_trend(self, base_value: float, time_factor: float, pattern_type: str, vital_type: str) -> float:
        """Apply realistic clinical trends to vital signs"""
        if pattern_type == 'septic' and vital_type == 'sbp':
            # Septic patients may have decreasing blood pressure over time
            trend = -10 * time_factor
        elif pattern_type == 'hypertensive' and vital_type == 'sbp':
            # Hypertensive patients may show improvement with treatment
            trend = -5 * time_factor
        else:
            trend = 0
        
        return base_value + trend + np.random.normal(0, 3)
    
    def _generate_lab_trend(self, lab_name: str, initial_value: float, time_points: int) -> Dict[str, Any]:
        """Generate lab value trends over time"""
        timestamps = []
        values = []
        
        for i in range(time_points):
            timestamp = datetime.now() - timedelta(hours=72) + timedelta(hours=i*4)
            timestamps.append(timestamp.isoformat())
            
            # Apply realistic lab trends
            if lab_name.lower() == 'glucose':
                # Glucose may fluctuate throughout the day
                daily_cycle = 20 * np.sin(2 * np.pi * i / 6)  # 6 measurements per day
                variation = np.random.normal(0, 15)
                value = initial_value + daily_cycle + variation
            else:
                # General trend with small variations
                trend = np.random.normal(0, initial_value * 0.05)  # 5% variation
                value = initial_value + trend
            
            values.append(max(0, value))  # Ensure positive values
        
        return {
            'timestamps': timestamps,
            'values': values,
            'unit': 'mg/dL' if lab_name.lower() == 'glucose' else 'various'
        }
    
    def _determine_imaging_studies(self, conditions: List[str], context: str) -> List[str]:
        """Determine appropriate imaging studies"""
        studies = []
        
        for condition in conditions:
            if 'heart' in condition.lower() or 'cardiac' in condition.lower():
                studies.extend(['chest_xray', 'echocardiogram'])
            elif 'lung' in condition.lower() or 'copd' in condition.lower():
                studies.extend(['chest_xray', 'ct_chest'])
            elif 'stroke' in condition.lower() or 'neurologic' in condition.lower():
                studies.append('mri_brain')
        
        # Remove duplicates and limit
        return list(set(studies))[:3]
    
    def _determine_procedures(self, conditions: List[str], context: str) -> List[str]:
        """Determine indicated procedures"""
        procedures = []
        
        for condition in conditions:
            if 'diabetes' in condition.lower():
                procedures.append('Glucose monitoring setup')
            elif 'heart' in condition.lower():
                procedures.append('Cardiac catheterization')
            elif 'kidney' in condition.lower():
                procedures.append('Renal biopsy')
        
        return procedures
    
    def _get_imaging_modality(self, study_type: str) -> str:
        """Get imaging modality for study type"""
        modality_mapping = {
            'chest_xray': 'X-Ray',
            'ct_chest': 'CT',
            'echocardiogram': 'Ultrasound',
            'mri_brain': 'MRI'
        }
        return modality_mapping.get(study_type, 'Unknown')
    
    def _generate_encounter(self, patient: Patient, encounter_type: str, context: str) -> Dict[str, Any]:
        """Generate encounter data"""
        return {
            'encounter_id': str(uuid.uuid4()),
            'encounter_type': encounter_type,
            'encounter_date': datetime.now().isoformat(),
            'department': self._get_department_for_encounter(encounter_type),
            'attending_physician': self._generate_physician_name(),
            'chief_complaint': self._generate_chief_complaint(patient.conditions, context),
            'length_of_stay': self._estimate_length_of_stay(encounter_type, patient.conditions)
        }
    
    def _get_department_for_encounter(self, encounter_type: str) -> str:
        """Get appropriate department"""
        dept_mapping = {
            'inpatient': 'Internal Medicine',
            'outpatient': 'Primary Care',
            'emergency': 'Emergency Department',
            'surgical': 'Surgery'
        }
        return dept_mapping.get(encounter_type, 'General Medicine')
    
    def _generate_chief_complaint(self, conditions: List[str], context: str) -> str:
        """Generate realistic chief complaint"""
        if conditions:
            primary_condition = conditions[0]
            if 'diabetes' in primary_condition.lower():
                return "Elevated blood sugar and fatigue"
            elif 'hypertension' in primary_condition.lower():
                return "Headache and elevated blood pressure"
            elif 'heart' in primary_condition.lower():
                return "Chest pain and shortness of breath"
        
        return "General medical evaluation"
    
    def _determine_encounter_types(self, context: str) -> List[str]:
        """Determine encounter types based on context"""
        context_lower = context.lower()
        
        if 'emergency' in context_lower:
            return ['emergency']
        elif 'hospital' in context_lower or 'admission' in context_lower:
            return ['inpatient']
        elif 'surgery' in context_lower or 'procedure' in context_lower:
            return ['surgical']
        else:
            return ['outpatient']
    
    # Additional utility methods would continue here...
    def _generate_social_history(self, patient: Patient, context: str) -> Dict[str, Any]:
        """Generate social history"""
        return {
            'smoking_status': np.random.choice(['Never', 'Former', 'Current'], p=[0.6, 0.3, 0.1]),
            'alcohol_use': np.random.choice(['None', 'Occasional', 'Regular'], p=[0.4, 0.4, 0.2]),
            'occupation': np.random.choice(['Retired', 'Healthcare', 'Education', 'Business', 'Other']),
            'exercise': np.random.choice(['Sedentary', 'Light', 'Moderate', 'Active'], p=[0.3, 0.3, 0.3, 0.1])
        }
    
    def _generate_family_history(self, patient: Patient) -> List[Dict[str, Any]]:
        """Generate family history"""
        family_conditions = ['Diabetes', 'Hypertension', 'Heart Disease', 'Cancer']
        family_history = []
        
        for condition in family_conditions:
            if np.random.random() < 0.3:  # 30% chance each condition is in family history
                family_history.append({
                    'condition': condition,
                    'relationship': np.random.choice(['Mother', 'Father', 'Sibling', 'Grandparent']),
                    'age_of_onset': np.random.randint(40, 80)
                })
        
        return family_history