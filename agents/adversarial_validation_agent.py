"""
Adversarial Validation Agent for Synthetic EHR Quality Control
Implements configurable validation agents with tunable skepticism levels
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import numpy as np
import json
from utils.ollama_client import OllamaClient
from models.patient_data import PatientCohort, Patient

class ValidationAgent:
    """Base class for validation agents"""
    
    def __init__(self, name: str, ollama_client: OllamaClient, skepticism_level: float = 0.5):
        self.name = name
        self.ollama_client = ollama_client
        self.skepticism_level = max(0.0, min(1.0, skepticism_level))  # 0.0 = lenient, 1.0 = strict
        self.validation_history = []
    
    def validate(self, patient: Patient, context: str) -> Dict[str, Any]:
        """Abstract method for validation - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement validate method")
    
    def get_threshold(self, base_threshold: float) -> float:
        """Adjust validation threshold based on skepticism level"""
        # Higher skepticism = stricter thresholds
        adjustment = (self.skepticism_level - 0.5) * 0.4  # ±0.2 adjustment
        return max(0.1, min(0.9, base_threshold + adjustment))

class RealismAgent(ValidationAgent):
    """Validates medical realism using statistical profiles and clinical knowledge"""
    
    def __init__(self, ollama_client: OllamaClient, skepticism_level: float = 0.5):
        super().__init__("Realism Agent", ollama_client, skepticism_level)
        
        # Statistical profiles for realism validation
        self.age_condition_profiles = {
            'Diabetes Mellitus Type 2': {'peak_age_range': (45, 75), 'min_age': 25},
            'Hypertension': {'peak_age_range': (40, 80), 'min_age': 30},
            'Coronary Artery Disease': {'peak_age_range': (55, 85), 'min_age': 40},
            'COPD': {'peak_age_range': (60, 85), 'min_age': 40},
            'Osteoarthritis': {'peak_age_range': (50, 80), 'min_age': 35},
            'Depression': {'peak_age_range': (20, 60), 'min_age': 16},
            'Anxiety': {'peak_age_range': (18, 50), 'min_age': 16}
        }
        
        # Lab value realistic ranges
        self.lab_realistic_ranges = {
            'glucose': {'normal': (70, 180), 'diabetic': (126, 400), 'critical': (400, 600)},
            'creatinine': {'normal': (0.5, 1.3), 'elevated': (1.3, 3.0), 'critical': (3.0, 8.0)},
            'hemoglobin': {'low': (6, 12), 'normal': (12, 18), 'high': (18, 22)},
            'cholesterol': {'normal': (120, 240), 'high': (240, 400), 'extreme': (400, 600)}
        }
        
        # Medication-condition compatibility
        self.medication_contraindications = {
            'Metformin': ['Severe kidney disease', 'Liver disease'],
            'ACE inhibitors': ['Pregnancy', 'Hyperkalemia'],
            'NSAIDs': ['Kidney disease', 'Heart failure'],
            'Warfarin': ['Active bleeding', 'Recent surgery']
        }
    
    def validate(self, patient: Patient, context: str) -> Dict[str, Any]:
        """Validate patient realism across multiple dimensions"""
        
        validation_result = {
            'agent_name': self.name,
            'patient_id': patient.patient_id,
            'validation_time': datetime.now().isoformat(),
            'overall_score': 0.0,
            'passed': False,
            'findings': [],
            'warnings': [],
            'critical_issues': [],
            'skepticism_level': self.skepticism_level
        }
        
        scores = []
        
        # Age-condition realism check
        age_score = self._validate_age_condition_compatibility(patient)
        scores.append(age_score['score'])
        if age_score['issues']:
            validation_result['findings'].extend(age_score['issues'])
        
        # Lab value realism check
        lab_score = self._validate_lab_realism(patient)
        scores.append(lab_score['score'])
        if lab_score['issues']:
            validation_result['findings'].extend(lab_score['issues'])
        
        # Medication appropriateness
        med_score = self._validate_medication_realism(patient)
        scores.append(med_score['score'])
        if med_score['issues']:
            validation_result['findings'].extend(med_score['issues'])
        
        # Comorbidity patterns
        comorbidity_score = self._validate_comorbidity_patterns(patient)
        scores.append(comorbidity_score['score'])
        if comorbidity_score['issues']:
            validation_result['findings'].extend(comorbidity_score['issues'])
        
        # Clinical notes consistency (using LLM)
        notes_score = self._validate_clinical_notes_consistency(patient, context)
        scores.append(notes_score['score'])
        if notes_score['issues']:
            validation_result['findings'].extend(notes_score['issues'])
        
        # Calculate overall score
        validation_result['overall_score'] = np.mean(scores)
        
        # Apply skepticism-adjusted threshold
        pass_threshold = self.get_threshold(0.7)  # Base threshold of 0.7
        validation_result['passed'] = validation_result['overall_score'] >= pass_threshold
        validation_result['threshold_used'] = pass_threshold
        
        # Categorize findings by severity
        self._categorize_findings(validation_result)
        
        return validation_result
    
    def _validate_age_condition_compatibility(self, patient: Patient) -> Dict[str, Any]:
        """Check if patient's conditions are age-appropriate"""
        
        result = {'score': 1.0, 'issues': []}
        
        if not patient.age:
            result['score'] = 0.5
            result['issues'].append("Missing age information")
            return result
        
        age_penalties = 0
        total_conditions = len(patient.conditions)
        
        for condition in patient.conditions:
            if condition in self.age_condition_profiles:
                profile = self.age_condition_profiles[condition]
                
                if patient.age < profile['min_age']:
                    age_penalties += 1
                    result['issues'].append(f"{condition} very rare in age {patient.age} (min typical age: {profile['min_age']})")
                
                peak_min, peak_max = profile['peak_age_range']
                if not (peak_min <= patient.age <= peak_max):
                    # Minor penalty for being outside peak range
                    age_penalties += 0.3
                    if patient.age < peak_min:
                        result['issues'].append(f"{condition} uncommon in age {patient.age} (typical range: {peak_min}-{peak_max})")
        
        if total_conditions > 0:
            penalty_ratio = age_penalties / total_conditions
            result['score'] = max(0.0, 1.0 - penalty_ratio)
        
        return result
    
    def _validate_lab_realism(self, patient: Patient) -> Dict[str, Any]:
        """Validate lab values for clinical realism"""
        
        result = {'score': 1.0, 'issues': []}
        
        if not patient.lab_results:
            result['score'] = 0.8
            result['issues'].append("No lab results available for validation")
            return result
        
        total_labs = len(patient.lab_results)
        unrealistic_count = 0
        
        for lab_name, (value, unit) in patient.lab_results.items():
            lab_key = lab_name.lower()
            
            if lab_key in self.lab_realistic_ranges:
                ranges = self.lab_realistic_ranges[lab_key]
                
                # Check if value falls within any realistic range
                is_realistic = False
                range_info = ""
                
                for range_type, (min_val, max_val) in ranges.items():
                    if min_val <= value <= max_val:
                        is_realistic = True
                        range_info = range_type
                        break
                
                if not is_realistic:
                    unrealistic_count += 1
                    max_critical = max([r[1] for r in ranges.values()])
                    min_critical = min([r[0] for r in ranges.values()])
                    
                    if value > max_critical:
                        result['issues'].append(f"{lab_name}: {value} {unit} extremely high (max realistic: {max_critical})")
                    elif value < min_critical:
                        result['issues'].append(f"{lab_name}: {value} {unit} extremely low (min realistic: {min_critical})")
                
                # Check for condition-lab consistency
                if lab_key == 'glucose' and value >= 126:
                    if 'Diabetes Mellitus Type 2' not in patient.conditions and 'Diabetes Mellitus Type 1' not in patient.conditions:
                        result['issues'].append(f"Diabetic glucose level ({value}) without diabetes diagnosis")
                
                if lab_key == 'creatinine' and value >= 2.0:
                    kidney_conditions = ['Chronic Kidney Disease', 'Acute Kidney Injury', 'Renal Failure']
                    if not any(cond in patient.conditions for cond in kidney_conditions):
                        result['issues'].append(f"Elevated creatinine ({value}) without kidney disease diagnosis")
        
        if total_labs > 0:
            result['score'] = max(0.0, 1.0 - (unrealistic_count / total_labs))
        
        return result
    
    def _validate_medication_realism(self, patient: Patient) -> Dict[str, Any]:
        """Validate medication appropriateness and contraindications"""
        
        result = {'score': 1.0, 'issues': []}
        
        if not patient.medications:
            result['score'] = 0.9
            return result
        
        contraindication_violations = 0
        total_medications = len(patient.medications)
        
        for medication in patient.medications:
            if medication in self.medication_contraindications:
                contraindications = self.medication_contraindications[medication]
                
                for contraindication in contraindications:
                    # Check if patient has contraindicated condition
                    if any(contraindication.lower() in condition.lower() for condition in patient.conditions):
                        contraindication_violations += 1
                        result['issues'].append(f"{medication} contraindicated with {contraindication}")
            
            # Check age appropriateness
            if patient.age and patient.age < 18:
                adult_only_meds = ['Warfarin', 'ACE inhibitors', 'Statins']
                if any(med.lower() in medication.lower() for med in adult_only_meds):
                    contraindication_violations += 0.5
                    result['issues'].append(f"{medication} rarely prescribed to patients under 18")
        
        if total_medications > 0:
            penalty_ratio = contraindication_violations / total_medications
            result['score'] = max(0.0, 1.0 - penalty_ratio)
        
        return result
    
    def _validate_comorbidity_patterns(self, patient: Patient) -> Dict[str, Any]:
        """Validate realistic comorbidity patterns"""
        
        result = {'score': 1.0, 'issues': []}
        
        if len(patient.conditions) < 2:
            return result
        
        # Known realistic comorbidity clusters
        realistic_clusters = {
            'metabolic_syndrome': ['Diabetes Mellitus Type 2', 'Hypertension', 'Hyperlipidemia', 'Obesity'],
            'cardiovascular': ['Hypertension', 'Coronary Artery Disease', 'Heart Failure'],
            'respiratory': ['COPD', 'Asthma', 'Sleep Apnea'],
            'mental_health': ['Depression', 'Anxiety', 'PTSD']
        }
        
        # Check for unrealistic combinations
        unrealistic_combinations = [
            ('Diabetes Mellitus Type 1', 'Diabetes Mellitus Type 2'),  # Can't have both types
            ('Hypertension', 'Severe Hypotension'),  # Contradictory
            ('COPD', 'Asthma')  # Rarely co-occur in same patient
        ]
        
        violations = 0
        
        for combo in unrealistic_combinations:
            if all(cond in patient.conditions for cond in combo):
                violations += 1
                result['issues'].append(f"Unrealistic combination: {' + '.join(combo)}")
        
        # Bonus for realistic clusters
        cluster_bonus = 0
        for cluster_name, cluster_conditions in realistic_clusters.items():
            conditions_in_cluster = sum(1 for cond in patient.conditions if cond in cluster_conditions)
            if conditions_in_cluster >= 2:
                cluster_bonus += 0.1
        
        penalty = violations * 0.3
        bonus = min(0.2, cluster_bonus)
        result['score'] = max(0.0, min(1.0, 1.0 - penalty + bonus))
        
        return result
    
    def _validate_clinical_notes_consistency(self, patient: Patient, context: str) -> Dict[str, Any]:
        """Use LLM to validate clinical notes consistency"""
        
        result = {'score': 0.8, 'issues': []}  # Default score if no notes
        
        if not hasattr(patient, 'clinical_notes') or not patient.clinical_notes:
            return result
        
        # Combine all clinical information
        patient_summary = f"""
        Patient: {patient.age}yo {patient.gender}
        Conditions: {', '.join(patient.conditions)}
        Medications: {', '.join(patient.medications)}
        Lab Results: {', '.join([f"{lab}: {val} {unit}" for lab, (val, unit) in patient.lab_results.items()])}
        Clinical Notes: {' '.join(patient.clinical_notes)}
        Context: {context}
        """
        
        prompt = f"""
        Analyze this synthetic patient record for clinical consistency and realism:

        {patient_summary}

        Evaluate for:
        1. Consistency between diagnoses, medications, and lab values
        2. Realistic clinical presentation
        3. Appropriate clinical language and terminology
        4. Logical progression of care

        Rate realism from 0.0 to 1.0 and list any inconsistencies found.
        Respond in JSON format: {{"score": 0.85, "issues": ["inconsistency 1", "inconsistency 2"]}}
        """
        
        try:
            response = self.ollama_client.generate_text(prompt)
            
            # Parse JSON response
            if '{' in response and '}' in response:
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                json_str = response[json_start:json_end]
                
                parsed = json.loads(json_str)
                result['score'] = float(parsed.get('score', 0.8))
                result['issues'] = parsed.get('issues', [])
            
        except Exception as e:
            result['issues'].append(f"LLM validation error: {str(e)}")
        
        return result
    
    def _categorize_findings(self, validation_result: Dict[str, Any]):
        """Categorize findings by severity based on keywords"""
        
        for finding in validation_result['findings']:
            finding_lower = finding.lower()
            
            if any(word in finding_lower for word in ['extremely', 'contraindicated', 'unrealistic combination']):
                validation_result['critical_issues'].append(finding)
            elif any(word in finding_lower for word in ['uncommon', 'rare', 'elevated', 'without']):
                validation_result['warnings'].append(finding)

class RelevanceAgent(ValidationAgent):
    """Validates alignment between generated records and research context"""
    
    def __init__(self, ollama_client: OllamaClient, skepticism_level: float = 0.5):
        super().__init__("Relevance Agent", ollama_client, skepticism_level)
    
    def validate(self, patient: Patient, context: str) -> Dict[str, Any]:
        """Validate patient relevance to research context"""
        
        validation_result = {
            'agent_name': self.name,
            'patient_id': patient.patient_id,
            'validation_time': datetime.now().isoformat(),
            'overall_score': 0.0,
            'passed': False,
            'findings': [],
            'context_alignment': {},
            'skepticism_level': self.skepticism_level
        }
        
        # Extract key terms from context
        context_analysis = self._analyze_research_context(context)
        
        # Validate alignment across different dimensions
        scores = []
        
        # Condition relevance
        condition_score = self._validate_condition_relevance(patient, context_analysis)
        scores.append(condition_score['score'])
        validation_result['context_alignment']['conditions'] = condition_score
        
        # Demographic relevance
        demo_score = self._validate_demographic_relevance(patient, context_analysis)
        scores.append(demo_score['score'])
        validation_result['context_alignment']['demographics'] = demo_score
        
        # Clinical severity relevance
        severity_score = self._validate_severity_relevance(patient, context_analysis)
        scores.append(severity_score['score'])
        validation_result['context_alignment']['severity'] = severity_score
        
        # Overall relevance using LLM
        llm_score = self._validate_overall_relevance_llm(patient, context)
        scores.append(llm_score['score'])
        validation_result['context_alignment']['llm_assessment'] = llm_score
        
        # Calculate overall score
        validation_result['overall_score'] = np.mean(scores)
        
        # Apply skepticism-adjusted threshold
        pass_threshold = self.get_threshold(0.75)  # Base threshold of 0.75
        validation_result['passed'] = validation_result['overall_score'] >= pass_threshold
        validation_result['threshold_used'] = pass_threshold
        
        # Compile findings
        for dimension, result in validation_result['context_alignment'].items():
            if 'issues' in result:
                validation_result['findings'].extend(result['issues'])
        
        return validation_result
    
    def _analyze_research_context(self, context: str) -> Dict[str, Any]:
        """Extract key research parameters from context"""
        
        context_lower = context.lower()
        
        analysis = {
            'target_conditions': [],
            'target_demographics': {},
            'severity_indicators': [],
            'study_focus': []
        }
        
        # Extract conditions mentioned
        condition_keywords = {
            'diabetes': ['diabetes', 'diabetic', 'dm', 'hyperglycemia'],
            'hypertension': ['hypertension', 'high blood pressure', 'htn'],
            'renal': ['renal', 'kidney', 'nephropathy', 'ckd'],
            'cardiac': ['cardiac', 'heart', 'coronary', 'cardiovascular'],
            'autoimmune': ['autoimmune', 'inflammatory', 'lupus', 'arthritis']
        }
        
        for condition, keywords in condition_keywords.items():
            if any(keyword in context_lower for keyword in keywords):
                analysis['target_conditions'].append(condition)
        
        # Extract demographic info
        age_keywords = {
            'pediatric': ['pediatric', 'child', 'infant', 'adolescent'],
            'adult': ['adult', 'middle-aged'],
            'elderly': ['elderly', 'geriatric', 'senior', 'aged']
        }
        
        for age_group, keywords in age_keywords.items():
            if any(keyword in context_lower for keyword in keywords):
                analysis['target_demographics']['age_group'] = age_group
        
        # Extract gender if specified
        if 'female' in context_lower or 'women' in context_lower:
            analysis['target_demographics']['gender'] = 'female'
        elif 'male' in context_lower or 'men' in context_lower:
            analysis['target_demographics']['gender'] = 'male'
        
        # Extract severity indicators
        severity_terms = ['late-stage', 'advanced', 'severe', 'acute', 'chronic', 'early-stage', 'mild', 'moderate']
        for term in severity_terms:
            if term in context_lower:
                analysis['severity_indicators'].append(term)
        
        return analysis
    
    def _validate_condition_relevance(self, patient: Patient, context_analysis: Dict) -> Dict[str, Any]:
        """Validate patient conditions match research focus"""
        
        result = {'score': 1.0, 'issues': [], 'matched_conditions': []}
        
        target_conditions = context_analysis['target_conditions']
        
        if not target_conditions:
            result['score'] = 0.8  # Neutral score if no specific conditions mentioned
            return result
        
        patient_conditions_lower = [cond.lower() for cond in patient.conditions]
        matches = 0
        
        for target in target_conditions:
            condition_found = False
            
            if target == 'diabetes':
                if any('diabetes' in cond for cond in patient_conditions_lower):
                    matches += 1
                    condition_found = True
                    result['matched_conditions'].append('diabetes')
            
            elif target == 'hypertension':
                if any('hypertension' in cond for cond in patient_conditions_lower):
                    matches += 1
                    condition_found = True
                    result['matched_conditions'].append('hypertension')
            
            elif target == 'renal':
                renal_conditions = ['kidney', 'renal', 'nephropathy', 'ckd']
                if any(any(renal in cond for renal in renal_conditions) for cond in patient_conditions_lower):
                    matches += 1
                    condition_found = True
                    result['matched_conditions'].append('renal condition')
            
            elif target == 'cardiac':
                cardiac_conditions = ['coronary', 'heart', 'cardiac', 'cardiovascular']
                if any(any(cardiac in cond for cardiac in cardiac_conditions) for cond in patient_conditions_lower):
                    matches += 1
                    condition_found = True
                    result['matched_conditions'].append('cardiac condition')
            
            elif target == 'autoimmune':
                autoimmune_conditions = ['arthritis', 'lupus', 'inflammatory', 'autoimmune']
                if any(any(auto in cond for auto in autoimmune_conditions) for cond in patient_conditions_lower):
                    matches += 1
                    condition_found = True
                    result['matched_conditions'].append('autoimmune condition')
            
            if not condition_found:
                result['issues'].append(f"Missing expected condition type: {target}")
        
        # Calculate score based on matches
        if target_conditions:
            result['score'] = matches / len(target_conditions)
        
        return result
    
    def _validate_demographic_relevance(self, patient: Patient, context_analysis: Dict) -> Dict[str, Any]:
        """Validate patient demographics match research parameters"""
        
        result = {'score': 1.0, 'issues': []}
        
        target_demographics = context_analysis['target_demographics']
        
        if not target_demographics:
            return result
        
        # Validate age group
        if 'age_group' in target_demographics:
            target_age_group = target_demographics['age_group']
            patient_age_group = self._get_age_group(patient.age) if patient.age else None
            
            if patient_age_group != target_age_group:
                result['issues'].append(f"Age mismatch: expected {target_age_group}, got {patient_age_group}")
                result['score'] *= 0.7
        
        # Validate gender
        if 'gender' in target_demographics:
            target_gender = target_demographics['gender'].lower()
            patient_gender = patient.gender.lower() if patient.gender else None
            
            if patient_gender != target_gender:
                result['issues'].append(f"Gender mismatch: expected {target_gender}, got {patient_gender}")
                result['score'] *= 0.8
        
        return result
    
    def _validate_severity_relevance(self, patient: Patient, context_analysis: Dict) -> Dict[str, Any]:
        """Validate clinical severity matches research context"""
        
        result = {'score': 0.8, 'issues': []}  # Default neutral score
        
        severity_indicators = context_analysis['severity_indicators']
        
        if not severity_indicators:
            return result
        
        # Assess patient severity based on lab values and conditions
        patient_severity = self._assess_patient_severity(patient)
        
        # Map context severity to expected patient severity
        context_severity_mapping = {
            'late-stage': 'high',
            'advanced': 'high',
            'severe': 'high',
            'acute': 'moderate-high',
            'chronic': 'moderate',
            'early-stage': 'low',
            'mild': 'low',
            'moderate': 'moderate'
        }
        
        expected_severity_levels = set()
        for indicator in severity_indicators:
            if indicator in context_severity_mapping:
                expected_severity_levels.add(context_severity_mapping[indicator])
        
        if expected_severity_levels:
            if patient_severity not in expected_severity_levels:
                result['issues'].append(f"Severity mismatch: expected {list(expected_severity_levels)}, assessed as {patient_severity}")
                result['score'] = 0.4
            else:
                result['score'] = 1.0
        
        return result
    
    def _validate_overall_relevance_llm(self, patient: Patient, context: str) -> Dict[str, Any]:
        """Use LLM to assess overall relevance"""
        
        result = {'score': 0.8, 'issues': []}
        
        patient_summary = f"""
        Patient Profile:
        - Age: {patient.age}, Gender: {patient.gender}
        - Conditions: {', '.join(patient.conditions)}
        - Medications: {', '.join(patient.medications)}
        - Key Lab Values: {', '.join([f"{lab}: {val}" for lab, (val, unit) in list(patient.lab_results.items())[:5]])}
        """
        
        prompt = f"""
        Research Context: {context}
        
        {patient_summary}
        
        Assess how well this synthetic patient matches the research context. Consider:
        1. Relevance of conditions to research question
        2. Demographic alignment
        3. Clinical presentation appropriateness
        4. Overall utility for the stated research purpose
        
        Rate relevance from 0.0 to 1.0 and explain any misalignments.
        Respond in JSON format: {{"score": 0.85, "explanation": "reasoning here", "misalignments": ["issue 1", "issue 2"]}}
        """
        
        try:
            response = self.ollama_client.generate_text(prompt)
            
            if '{' in response and '}' in response:
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                json_str = response[json_start:json_end]
                
                parsed = json.loads(json_str)
                result['score'] = float(parsed.get('score', 0.8))
                result['explanation'] = parsed.get('explanation', '')
                result['issues'] = parsed.get('misalignments', [])
        
        except Exception as e:
            result['issues'].append(f"LLM relevance assessment error: {str(e)}")
        
        return result
    
    def _get_age_group(self, age: int) -> str:
        """Categorize age into groups"""
        if age < 18:
            return 'pediatric'
        elif age < 65:
            return 'adult'
        else:
            return 'elderly'
    
    def _assess_patient_severity(self, patient: Patient) -> str:
        """Assess overall patient severity based on conditions and lab values"""
        
        severity_score = 0
        
        # High-severity conditions
        high_severity_conditions = [
            'Heart Failure', 'Renal Failure', 'Advanced COPD', 'Metastatic Cancer',
            'Severe Depression', 'Acute Myocardial Infarction'
        ]
        
        moderate_severity_conditions = [
            'Diabetes Mellitus Type 2', 'Hypertension', 'Chronic Kidney Disease',
            'Coronary Artery Disease', 'COPD'
        ]
        
        for condition in patient.conditions:
            if any(severe in condition for severe in high_severity_conditions):
                severity_score += 3
            elif any(moderate in condition for moderate in moderate_severity_conditions):
                severity_score += 2
            else:
                severity_score += 1
        
        # Factor in lab value abnormalities
        for lab_name, (value, unit) in patient.lab_results.items():
            if lab_name.lower() == 'creatinine' and value > 3.0:
                severity_score += 2
            elif lab_name.lower() == 'glucose' and value > 300:
                severity_score += 2
            elif lab_name.lower() == 'hemoglobin' and value < 8.0:
                severity_score += 2
        
        # Medication count as complexity indicator
        if len(patient.medications) > 8:
            severity_score += 1
        
        # Categorize severity
        if severity_score >= 8:
            return 'high'
        elif severity_score >= 4:
            return 'moderate'
        else:
            return 'low'

class AdversarialValidationOrchestrator:
    """Orchestrates multiple validation agents with configurable parameters"""
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
        self.validation_agents = {}
        self.validation_history = []
        
        # Initialize default agents
        self.add_agent('realism', RealismAgent(ollama_client))
        self.add_agent('relevance', RelevanceAgent(ollama_client))
    
    def add_agent(self, agent_id: str, agent: ValidationAgent):
        """Add a validation agent to the orchestrator"""
        self.validation_agents[agent_id] = agent
    
    def configure_agent_skepticism(self, agent_id: str, skepticism_level: float):
        """Configure the skepticism level for a specific agent"""
        if agent_id in self.validation_agents:
            self.validation_agents[agent_id].skepticism_level = max(0.0, min(1.0, skepticism_level))
    
    def validate_patient(self, patient: Patient, context: str, required_agents: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run patient through all or specified validation agents"""
        
        agents_to_run = required_agents or list(self.validation_agents.keys())
        
        validation_session = {
            'patient_id': patient.patient_id,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'agent_results': {},
            'overall_result': {
                'passed': True,
                'overall_score': 0.0,
                'critical_failures': [],
                'warnings': [],
                'agent_scores': {}
            }
        }
        
        agent_scores = []
        
        for agent_id in agents_to_run:
            if agent_id in self.validation_agents:
                agent = self.validation_agents[agent_id]
                
                # Run validation
                result = agent.validate(patient, context)
                validation_session['agent_results'][agent_id] = result
                
                # Track scores
                agent_scores.append(result['overall_score'])
                validation_session['overall_result']['agent_scores'][agent_id] = result['overall_score']
                
                # Check if agent failed patient
                if not result['passed']:
                    validation_session['overall_result']['passed'] = False
                    
                    if 'critical_issues' in result and result['critical_issues']:
                        validation_session['overall_result']['critical_failures'].extend(result['critical_issues'])
                    
                    if 'warnings' in result and result['warnings']:
                        validation_session['overall_result']['warnings'].extend(result['warnings'])
        
        # Calculate overall score
        if agent_scores:
            validation_session['overall_result']['overall_score'] = np.mean(agent_scores)
        
        # Store validation history
        self.validation_history.append(validation_session)
        
        return validation_session
    
    def validate_cohort(self, cohort: PatientCohort, context: str) -> Dict[str, Any]:
        """Validate entire patient cohort"""
        
        cohort_validation = {
            'cohort_id': getattr(cohort, 'cohort_id', 'unknown'),
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'patient_validations': {},
            'summary': {
                'total_patients': len(cohort.patients),
                'passed_patients': 0,
                'failed_patients': 0,
                'average_score': 0.0,
                'agent_performance': {},
                'common_issues': []
            }
        }
        
        all_scores = []
        all_issues = []
        
        for patient in cohort.patients:
            patient_validation = self.validate_patient(patient, context)
            cohort_validation['patient_validations'][patient.patient_id] = patient_validation
            
            # Update summary statistics
            if patient_validation['overall_result']['passed']:
                cohort_validation['summary']['passed_patients'] += 1
            else:
                cohort_validation['summary']['failed_patients'] += 1
            
            all_scores.append(patient_validation['overall_result']['overall_score'])
            
            # Collect issues for analysis
            for agent_result in patient_validation['agent_results'].values():
                if 'findings' in agent_result:
                    all_issues.extend(agent_result['findings'])
        
        # Calculate summary statistics
        if all_scores:
            cohort_validation['summary']['average_score'] = np.mean(all_scores)
        
        # Analyze common issues
        issue_counts = {}
        for issue in all_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        # Get top 5 most common issues
        sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
        cohort_validation['summary']['common_issues'] = sorted_issues[:5]
        
        # Agent performance summary
        for agent_id in self.validation_agents.keys():
            agent_scores = []
            for patient_validation in cohort_validation['patient_validations'].values():
                if agent_id in patient_validation['agent_results']:
                    agent_scores.append(patient_validation['agent_results'][agent_id]['overall_score'])
            
            if agent_scores:
                cohort_validation['summary']['agent_performance'][agent_id] = {
                    'average_score': np.mean(agent_scores),
                    'pass_rate': sum(1 for score in agent_scores if score >= 0.7) / len(agent_scores)
                }
        
        return cohort_validation
    
    def get_validation_statistics(self) -> Dict[str, Any]:
        """Get overall validation statistics"""
        
        if not self.validation_history:
            return {'message': 'No validation history available'}
        
        total_validations = len(self.validation_history)
        passed_validations = sum(1 for v in self.validation_history if v['overall_result']['passed'])
        
        all_scores = [v['overall_result']['overall_score'] for v in self.validation_history]
        
        stats = {
            'total_validations': total_validations,
            'pass_rate': passed_validations / total_validations,
            'average_score': np.mean(all_scores),
            'score_std': np.std(all_scores),
            'agent_statistics': {}
        }
        
        # Per-agent statistics
        for agent_id in self.validation_agents.keys():
            agent_scores = []
            agent_passes = 0
            
            for validation in self.validation_history:
                if agent_id in validation['agent_results']:
                    result = validation['agent_results'][agent_id]
                    agent_scores.append(result['overall_score'])
                    if result['passed']:
                        agent_passes += 1
            
            if agent_scores:
                stats['agent_statistics'][agent_id] = {
                    'average_score': np.mean(agent_scores),
                    'pass_rate': agent_passes / len(agent_scores),
                    'skepticism_level': self.validation_agents[agent_id].skepticism_level
                }
        
        return stats