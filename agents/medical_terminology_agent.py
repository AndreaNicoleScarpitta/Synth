from typing import Dict, List, Any, Optional, Tuple
from utils.ollama_client import OllamaClient
import re

class MedicalTerminologyAgent:
    """Agent for validating and understanding medical terminology"""
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
        
        # Comprehensive medical terminology dictionaries
        self.medical_conditions = {
            'cardiovascular': {
                'Hypertension': {
                    'definition': 'Persistent high blood pressure (≥140/90 mmHg)',
                    'icd10': 'I10',
                    'prevalence': 0.45,
                    'common_medications': ['ACE inhibitors', 'ARBs', 'Diuretics', 'Beta-blockers'],
                    'lab_markers': ['Blood pressure', 'Creatinine', 'Potassium'],
                    'comorbidities': ['Diabetes', 'Hyperlipidemia', 'Coronary Artery Disease']
                },
                'Coronary Artery Disease': {
                    'definition': 'Narrowing of coronary arteries due to atherosclerosis',
                    'icd10': 'I25.9',
                    'prevalence': 0.06,
                    'common_medications': ['Statins', 'Antiplatelet agents', 'Beta-blockers'],
                    'lab_markers': ['Troponins', 'CK-MB', 'Cholesterol panel'],
                    'comorbidities': ['Hypertension', 'Diabetes', 'Hyperlipidemia']
                },
                'Heart Failure': {
                    'definition': 'Inability of heart to pump blood effectively',
                    'icd10': 'I50.9',
                    'prevalence': 0.02,
                    'common_medications': ['ACE inhibitors', 'Diuretics', 'Beta-blockers'],
                    'lab_markers': ['BNP', 'NT-proBNP', 'Creatinine'],
                    'comorbidities': ['Hypertension', 'Coronary Artery Disease', 'Diabetes']
                }
            },
            'endocrine': {
                'Diabetes Mellitus Type 2': {
                    'definition': 'Insulin resistance and relative insulin deficiency',
                    'icd10': 'E11',
                    'prevalence': 0.11,
                    'common_medications': ['Metformin', 'Insulin', 'Sulfonylureas', 'GLP-1 agonists'],
                    'lab_markers': ['HbA1c', 'Fasting glucose', 'Random glucose'],
                    'comorbidities': ['Hypertension', 'Hyperlipidemia', 'Nephropathy', 'Retinopathy']
                },
                'Hypothyroidism': {
                    'definition': 'Underactive thyroid gland producing insufficient thyroid hormone',
                    'icd10': 'E03.9',
                    'prevalence': 0.05,
                    'common_medications': ['Levothyroxine', 'Liothyronine'],
                    'lab_markers': ['TSH', 'Free T4', 'Free T3'],
                    'comorbidities': ['Depression', 'Hyperlipidemia', 'Heart Disease']
                }
            },
            'respiratory': {
                'COPD': {
                    'definition': 'Chronic Obstructive Pulmonary Disease - progressive airflow limitation',
                    'icd10': 'J44.1',
                    'prevalence': 0.04,
                    'common_medications': ['Bronchodilators', 'Corticosteroids', 'Oxygen therapy'],
                    'lab_markers': ['ABG', 'Alpha-1 antitrypsin', 'CBC'],
                    'comorbidities': ['Cardiovascular disease', 'Depression', 'Osteoporosis']
                },
                'Asthma': {
                    'definition': 'Chronic inflammatory disorder of airways with reversible obstruction',
                    'icd10': 'J45.9',
                    'prevalence': 0.08,
                    'common_medications': ['Inhaled corticosteroids', 'Beta-2 agonists', 'Leukotriene modifiers'],
                    'lab_markers': ['IgE', 'Eosinophil count', 'Peak flow'],
                    'comorbidities': ['Allergic rhinitis', 'Eczema', 'GERD']
                }
            },
            'psychiatric': {
                'Depression': {
                    'definition': 'Major depressive disorder with persistent sad mood and anhedonia',
                    'icd10': 'F32.9',
                    'prevalence': 0.08,
                    'common_medications': ['SSRIs', 'SNRIs', 'Tricyclic antidepressants'],
                    'lab_markers': ['Thyroid function', 'B12', 'Folate'],
                    'comorbidities': ['Anxiety', 'Substance abuse', 'Chronic pain']
                },
                'Anxiety': {
                    'definition': 'Excessive worry and fear interfering with daily activities',
                    'icd10': 'F41.9',
                    'prevalence': 0.18,
                    'common_medications': ['SSRIs', 'Benzodiazepines', 'Buspirone'],
                    'lab_markers': ['Thyroid function', 'Cortisol', 'Drug screening'],
                    'comorbidities': ['Depression', 'Substance abuse', 'PTSD']
                }
            },
            'metabolic': {
                'Hyperlipidemia': {
                    'definition': 'Elevated cholesterol and/or triglycerides in blood',
                    'icd10': 'E78.5',
                    'prevalence': 0.38,
                    'common_medications': ['Statins', 'Fibrates', 'Ezetimibe'],
                    'lab_markers': ['Total cholesterol', 'LDL', 'HDL', 'Triglycerides'],
                    'comorbidities': ['Coronary Artery Disease', 'Diabetes', 'Hypertension']
                },
                'Obesity': {
                    'definition': 'Excessive body fat accumulation (BMI ≥30 kg/m²)',
                    'icd10': 'E66.9',
                    'prevalence': 0.36,
                    'common_medications': ['Orlistat', 'Phentermine', 'GLP-1 agonists'],
                    'lab_markers': ['BMI', 'Waist circumference', 'Metabolic panel'],
                    'comorbidities': ['Diabetes', 'Hypertension', 'Sleep apnea']
                }
            },
            'renal': {
                'Chronic Kidney Disease': {
                    'definition': 'Progressive loss of kidney function over ≥3 months',
                    'icd10': 'N18.9',
                    'prevalence': 0.15,
                    'common_medications': ['ACE inhibitors', 'Phosphate binders', 'EPO'],
                    'lab_markers': ['Creatinine', 'eGFR', 'Proteinuria', 'BUN'],
                    'comorbidities': ['Diabetes', 'Hypertension', 'Anemia']
                }
            },
            'musculoskeletal': {
                'Osteoarthritis': {
                    'definition': 'Degenerative joint disease with cartilage breakdown',
                    'icd10': 'M19.9',
                    'prevalence': 0.22,
                    'common_medications': ['NSAIDs', 'Acetaminophen', 'Topical analgesics'],
                    'lab_markers': ['ESR', 'CRP', 'Joint fluid analysis'],
                    'comorbidities': ['Obesity', 'Depression', 'Chronic pain']
                },
                'Rheumatoid Arthritis': {
                    'definition': 'Autoimmune inflammatory arthritis affecting multiple joints',
                    'icd10': 'M06.9',
                    'prevalence': 0.01,
                    'common_medications': ['DMARDs', 'Biologics', 'Corticosteroids'],
                    'lab_markers': ['RF', 'Anti-CCP', 'ESR', 'CRP'],
                    'comorbidities': ['Cardiovascular disease', 'Osteoporosis', 'Depression']
                }
            }
        }
        
        # Laboratory test reference ranges and clinical significance
        self.lab_tests = {
            'glucose': {
                'normal_range': (70, 99),
                'prediabetic_range': (100, 125),
                'diabetic_range': (126, 400),
                'unit': 'mg/dL',
                'clinical_significance': 'Glucose metabolism, diabetes screening',
                'related_conditions': ['Diabetes', 'Metabolic syndrome', 'Hypoglycemia']
            },
            'hemoglobin': {
                'normal_range_male': (13.8, 17.2),
                'normal_range_female': (12.1, 15.1),
                'unit': 'g/dL',
                'clinical_significance': 'Oxygen carrying capacity, anemia detection',
                'related_conditions': ['Anemia', 'Polycythemia', 'Chronic disease']
            },
            'creatinine': {
                'normal_range_male': (0.74, 1.35),
                'normal_range_female': (0.59, 1.04),
                'unit': 'mg/dL',
                'clinical_significance': 'Kidney function assessment',
                'related_conditions': ['Chronic Kidney Disease', 'Acute kidney injury']
            },
            'cholesterol_total': {
                'desirable': (0, 200),
                'borderline_high': (200, 239),
                'high': (240, 500),
                'unit': 'mg/dL',
                'clinical_significance': 'Cardiovascular risk assessment',
                'related_conditions': ['Hyperlipidemia', 'Coronary Artery Disease']
            },
            'ldl_cholesterol': {
                'optimal': (0, 100),
                'near_optimal': (100, 129),
                'borderline_high': (130, 159),
                'high': (160, 189),
                'very_high': (190, 400),
                'unit': 'mg/dL',
                'clinical_significance': 'Atherogenic lipoprotein, cardiovascular risk',
                'related_conditions': ['Atherosclerosis', 'Coronary Artery Disease']
            },
            'hdl_cholesterol': {
                'low_male': (0, 40),
                'low_female': (0, 50),
                'normal': (40, 100),
                'unit': 'mg/dL',
                'clinical_significance': 'Protective lipoprotein, cardiovascular risk',
                'related_conditions': ['Metabolic syndrome', 'Low HDL syndrome']
            },
            'hba1c': {
                'normal': (4.0, 5.6),
                'prediabetic': (5.7, 6.4),
                'diabetic': (6.5, 15.0),
                'unit': '%',
                'clinical_significance': '3-month average glucose, diabetes monitoring',
                'related_conditions': ['Diabetes', 'Prediabetes', 'Metabolic syndrome']
            },
            'tsh': {
                'normal': (0.4, 4.0),
                'unit': 'mIU/L',
                'clinical_significance': 'Thyroid function assessment',
                'related_conditions': ['Hypothyroidism', 'Hyperthyroidism']
            },
            'blood_pressure_systolic': {
                'normal': (90, 120),
                'elevated': (120, 129),
                'stage1_hypertension': (130, 139),
                'stage2_hypertension': (140, 180),
                'hypertensive_crisis': (180, 220),
                'unit': 'mmHg',
                'clinical_significance': 'Cardiovascular pressure during systole',
                'related_conditions': ['Hypertension', 'Cardiovascular disease']
            },
            'blood_pressure_diastolic': {
                'normal': (60, 80),
                'stage1_hypertension': (80, 89),
                'stage2_hypertension': (90, 120),
                'unit': 'mmHg',
                'clinical_significance': 'Cardiovascular pressure during diastole',
                'related_conditions': ['Hypertension', 'Cardiovascular disease']
            }
        }
        
        # Medication classifications and mechanisms
        self.medications = {
            'antihypertensives': {
                'ace_inhibitors': {
                    'examples': ['Lisinopril', 'Enalapril', 'Captopril'],
                    'mechanism': 'Inhibits ACE enzyme, reduces angiotensin II formation',
                    'indications': ['Hypertension', 'Heart failure', 'Diabetic nephropathy'],
                    'contraindications': ['Pregnancy', 'Bilateral renal artery stenosis'],
                    'side_effects': ['Dry cough', 'Hyperkalemia', 'Angioedema']
                },
                'arbs': {
                    'examples': ['Losartan', 'Valsartan', 'Olmesartan'],
                    'mechanism': 'Blocks angiotensin II receptors',
                    'indications': ['Hypertension', 'Heart failure', 'Diabetic nephropathy'],
                    'contraindications': ['Pregnancy', 'Bilateral renal artery stenosis'],
                    'side_effects': ['Hyperkalemia', 'Dizziness', 'Fatigue']
                },
                'beta_blockers': {
                    'examples': ['Metoprolol', 'Propranolol', 'Atenolol'],
                    'mechanism': 'Blocks beta-adrenergic receptors',
                    'indications': ['Hypertension', 'Angina', 'Heart failure', 'Arrhythmias'],
                    'contraindications': ['Severe asthma', 'Heart block', 'Severe bradycardia'],
                    'side_effects': ['Bradycardia', 'Fatigue', 'Cold extremities']
                },
                'calcium_channel_blockers': {
                    'examples': ['Amlodipine', 'Nifedipine', 'Verapamil'],
                    'mechanism': 'Blocks calcium channels in vascular smooth muscle',
                    'indications': ['Hypertension', 'Angina', 'Arrhythmias'],
                    'contraindications': ['Severe heart failure', 'Cardiogenic shock'],
                    'side_effects': ['Peripheral edema', 'Flushing', 'Constipation']
                },
                'diuretics': {
                    'examples': ['Hydrochlorothiazide', 'Furosemide', 'Spironolactone'],
                    'mechanism': 'Increases sodium and water excretion',
                    'indications': ['Hypertension', 'Heart failure', 'Edema'],
                    'contraindications': ['Anuria', 'Severe electrolyte imbalance'],
                    'side_effects': ['Hyponatremia', 'Hypokalemia', 'Dehydration']
                }
            },
            'antidiabetic': {
                'metformin': {
                    'examples': ['Metformin', 'Glucophage'],
                    'mechanism': 'Decreases hepatic glucose production, increases insulin sensitivity',
                    'indications': ['Type 2 diabetes', 'Prediabetes', 'PCOS'],
                    'contraindications': ['Severe kidney disease', 'Metabolic acidosis'],
                    'side_effects': ['GI upset', 'Lactic acidosis (rare)', 'B12 deficiency']
                },
                'sulfonylureas': {
                    'examples': ['Glipizide', 'Glyburide', 'Glimepiride'],
                    'mechanism': 'Stimulates insulin release from pancreatic beta cells',
                    'indications': ['Type 2 diabetes'],
                    'contraindications': ['Type 1 diabetes', 'Diabetic ketoacidosis'],
                    'side_effects': ['Hypoglycemia', 'Weight gain', 'Skin reactions']
                },
                'insulin': {
                    'examples': ['Regular insulin', 'NPH', 'Glargine', 'Aspart'],
                    'mechanism': 'Replaces or supplements endogenous insulin',
                    'indications': ['Type 1 diabetes', 'Type 2 diabetes', 'DKA'],
                    'contraindications': ['Hypoglycemia'],
                    'side_effects': ['Hypoglycemia', 'Weight gain', 'Lipodystrophy']
                }
            },
            'lipid_lowering': {
                'statins': {
                    'examples': ['Atorvastatin', 'Simvastatin', 'Rosuvastatin'],
                    'mechanism': 'Inhibits HMG-CoA reductase, reduces cholesterol synthesis',
                    'indications': ['Hyperlipidemia', 'Cardiovascular disease prevention'],
                    'contraindications': ['Active liver disease', 'Pregnancy'],
                    'side_effects': ['Myalgia', 'Elevated liver enzymes', 'Rhabdomyolysis (rare)']
                }
            },
            'antidepressants': {
                'ssris': {
                    'examples': ['Sertraline', 'Fluoxetine', 'Escitalopram'],
                    'mechanism': 'Selective serotonin reuptake inhibition',
                    'indications': ['Depression', 'Anxiety disorders', 'PTSD', 'OCD'],
                    'contraindications': ['MAO inhibitor use', 'Severe liver disease'],
                    'side_effects': ['Nausea', 'Sexual dysfunction', 'Weight changes']
                }
            }
        }
    
    def validate_medical_terminology(self, text: str) -> Dict[str, Any]:
        """Validate medical terminology in text using knowledge base and LLM"""
        
        validation_results = {
            'recognized_conditions': [],
            'recognized_medications': [],
            'recognized_lab_tests': [],
            'potential_errors': [],
            'terminology_score': 0.0,
            'suggestions': []
        }
        
        # Extract and validate conditions
        conditions_found = self._extract_conditions(text)
        validation_results['recognized_conditions'] = conditions_found
        
        # Extract and validate medications
        medications_found = self._extract_medications(text)
        validation_results['recognized_medications'] = medications_found
        
        # Extract and validate lab tests
        lab_tests_found = self._extract_lab_tests(text)
        validation_results['recognized_lab_tests'] = lab_tests_found
        
        # Use LLM for additional validation
        llm_validation = self._llm_terminology_validation(text)
        validation_results.update(llm_validation)
        
        # Calculate terminology score
        validation_results['terminology_score'] = self._calculate_terminology_score(validation_results)
        
        return validation_results
    
    def explain_medical_term(self, term: str) -> Dict[str, Any]:
        """Provide comprehensive explanation of a medical term"""
        
        explanation = {
            'term': term,
            'found_in_knowledge_base': False,
            'definition': '',
            'category': '',
            'clinical_details': {},
            'llm_explanation': ''
        }
        
        # Search in conditions
        for category, conditions in self.medical_conditions.items():
            if term in conditions:
                explanation['found_in_knowledge_base'] = True
                explanation['definition'] = conditions[term]['definition']
                explanation['category'] = f"Medical Condition - {category.title()}"
                explanation['clinical_details'] = conditions[term]
                break
        
        # Search in lab tests
        if not explanation['found_in_knowledge_base'] and term.lower() in self.lab_tests:
            lab_info = self.lab_tests[term.lower()]
            explanation['found_in_knowledge_base'] = True
            explanation['definition'] = lab_info['clinical_significance']
            explanation['category'] = "Laboratory Test"
            explanation['clinical_details'] = lab_info
        
        # Search in medications
        if not explanation['found_in_knowledge_base']:
            for med_category, med_classes in self.medications.items():
                for med_class, med_info in med_classes.items():
                    if term in med_info.get('examples', []):
                        explanation['found_in_knowledge_base'] = True
                        explanation['definition'] = med_info['mechanism']
                        explanation['category'] = f"Medication - {med_category.replace('_', ' ').title()}"
                        explanation['clinical_details'] = med_info
                        break
                if explanation['found_in_knowledge_base']:
                    break
        
        # Use LLM for additional explanation
        explanation['llm_explanation'] = self._get_llm_explanation(term)
        
        return explanation
    
    def validate_condition_medication_pairing(self, condition: str, medication: str) -> Dict[str, Any]:
        """Validate if a medication is appropriate for a condition"""
        
        validation = {
            'condition': condition,
            'medication': medication,
            'is_appropriate': False,
            'confidence': 0.0,
            'reasoning': '',
            'alternative_medications': [],
            'contraindications': []
        }
        
        # Check in knowledge base
        condition_info = self._find_condition_info(condition)
        medication_info = self._find_medication_info(medication)
        
        if condition_info and medication_info:
            # Check if medication is commonly used for condition
            common_meds = condition_info.get('common_medications', [])
            
            # Check for direct match or class match
            for med_class in common_meds:
                if (medication in med_class or 
                    any(medication in med_info.get('examples', []) 
                        for med_info in self._get_medication_class_info(med_class))):
                    validation['is_appropriate'] = True
                    validation['confidence'] = 0.9
                    validation['reasoning'] = f"{medication} is commonly prescribed for {condition}"
                    break
        
        # Use LLM for additional validation
        llm_validation = self._llm_validate_pairing(condition, medication)
        if not validation['is_appropriate'] and llm_validation.get('is_appropriate'):
            validation.update(llm_validation)
        
        # Get alternative medications
        if condition_info:
            validation['alternative_medications'] = condition_info.get('common_medications', [])
        
        return validation
    
    def assess_lab_value_clinical_significance(self, lab_name: str, value: float, 
                                             patient_conditions: List[str]) -> Dict[str, Any]:
        """Assess clinical significance of lab value given patient conditions"""
        
        assessment = {
            'lab_name': lab_name,
            'value': value,
            'reference_range': {},
            'interpretation': '',
            'clinical_significance': '',
            'related_conditions': [],
            'follow_up_recommendations': []
        }
        
        # Get lab test info
        lab_info = self.lab_tests.get(lab_name.lower(), {})
        
        if lab_info:
            assessment['reference_range'] = lab_info
            assessment['clinical_significance'] = lab_info.get('clinical_significance', '')
            assessment['related_conditions'] = lab_info.get('related_conditions', [])
            
            # Interpret value
            assessment['interpretation'] = self._interpret_lab_value(lab_name, value, lab_info)
            
            # Assess in context of patient conditions
            context_assessment = self._assess_lab_in_context(lab_name, value, patient_conditions)
            assessment.update(context_assessment)
        
        # Get LLM interpretation
        llm_interpretation = self._get_llm_lab_interpretation(lab_name, value, patient_conditions)
        assessment['llm_interpretation'] = llm_interpretation
        
        return assessment
    
    def generate_medical_insights(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate medical insights from patient data using medical knowledge"""
        
        insights = {
            'condition_patterns': [],
            'medication_appropriateness': {},
            'lab_value_concerns': [],
            'potential_drug_interactions': [],
            'follow_up_recommendations': [],
            'risk_factors': []
        }
        
        conditions = patient_data.get('conditions', [])
        medications = patient_data.get('medications', [])
        lab_results = patient_data.get('lab_results', {})
        age = patient_data.get('age')
        gender = patient_data.get('gender')
        
        # Analyze condition patterns
        insights['condition_patterns'] = self._analyze_condition_patterns(conditions)
        
        # Assess medication appropriateness
        for medication in medications:
            for condition in conditions:
                pairing = self.validate_condition_medication_pairing(condition, medication)
                insights['medication_appropriateness'][f"{condition}_{medication}"] = pairing
        
        # Assess lab values
        for lab_name, (value, unit) in lab_results.items():
            lab_assessment = self.assess_lab_value_clinical_significance(lab_name, value, conditions)
            if 'abnormal' in lab_assessment.get('interpretation', '').lower():
                insights['lab_value_concerns'].append(lab_assessment)
        
        # Generate comprehensive insights using LLM
        llm_insights = self._generate_llm_insights(patient_data)
        insights['llm_generated_insights'] = llm_insights
        
        return insights
    
    # Helper methods
    def _extract_conditions(self, text: str) -> List[Dict[str, Any]]:
        """Extract recognized medical conditions from text"""
        recognized_conditions = []
        text_lower = text.lower()
        
        for category, conditions in self.medical_conditions.items():
            for condition_name, condition_info in conditions.items():
                if condition_name.lower() in text_lower:
                    recognized_conditions.append({
                        'name': condition_name,
                        'category': category,
                        'confidence': 0.9,
                        'definition': condition_info['definition']
                    })
        
        return recognized_conditions
    
    def _extract_medications(self, text: str) -> List[Dict[str, Any]]:
        """Extract recognized medications from text"""
        recognized_medications = []
        text_lower = text.lower()
        
        for med_category, med_classes in self.medications.items():
            for med_class, med_info in med_classes.items():
                for example in med_info.get('examples', []):
                    if example.lower() in text_lower:
                        recognized_medications.append({
                            'name': example,
                            'category': med_category,
                            'class': med_class,
                            'confidence': 0.9,
                            'mechanism': med_info['mechanism']
                        })
        
        return recognized_medications
    
    def _extract_lab_tests(self, text: str) -> List[Dict[str, Any]]:
        """Extract recognized lab tests from text"""
        recognized_labs = []
        text_lower = text.lower()
        
        for lab_name, lab_info in self.lab_tests.items():
            if lab_name.lower() in text_lower:
                recognized_labs.append({
                    'name': lab_name,
                    'confidence': 0.9,
                    'clinical_significance': lab_info['clinical_significance']
                })
        
        return recognized_labs
    
    def _llm_terminology_validation(self, text: str) -> Dict[str, Any]:
        """Use LLM to validate medical terminology"""
        
        prompt = f"""
        Review this medical text for terminology accuracy and appropriateness:
        
        {text}
        
        Identify:
        1. Any medical terms that seem incorrect or inappropriate
        2. Missing medical terms that should be included
        3. Terminology that needs clarification
        4. Overall medical accuracy assessment
        
        Respond with specific findings and suggestions for improvement.
        """
        
        try:
            response = self.ollama_client.generate_text(prompt)
            return {
                'llm_validation': response,
                'potential_errors': self._parse_llm_errors(response),
                'suggestions': self._parse_llm_suggestions(response)
            }
        except Exception as e:
            return {
                'llm_validation': f"Error in LLM validation: {e}",
                'potential_errors': [],
                'suggestions': []
            }
    
    def _calculate_terminology_score(self, validation_results: Dict[str, Any]) -> float:
        """Calculate overall terminology accuracy score"""
        
        recognized_terms = (len(validation_results['recognized_conditions']) + 
                          len(validation_results['recognized_medications']) + 
                          len(validation_results['recognized_lab_tests']))
        
        potential_errors = len(validation_results['potential_errors'])
        
        # Base score on recognition and subtract for errors
        base_score = min(recognized_terms * 0.1, 0.8)
        error_penalty = potential_errors * 0.1
        
        final_score = max(0.0, min(1.0, base_score - error_penalty))
        
        return final_score
    
    def _get_llm_explanation(self, term: str) -> str:
        """Get LLM explanation of medical term"""
        
        prompt = f"""
        Provide a comprehensive medical explanation of the term: {term}
        
        Include:
        1. Definition in clear, medical language
        2. Clinical significance
        3. Common symptoms or manifestations
        4. Typical treatments or management
        5. Related conditions or complications
        
        Focus on accuracy and clinical relevance.
        """
        
        try:
            return self.ollama_client.generate_text(prompt)
        except Exception as e:
            return f"Error generating explanation: {e}"
    
    def _find_condition_info(self, condition: str) -> Optional[Dict[str, Any]]:
        """Find condition information in knowledge base"""
        for category, conditions in self.medical_conditions.items():
            if condition in conditions:
                return conditions[condition]
        return None
    
    def _find_medication_info(self, medication: str) -> Optional[Dict[str, Any]]:
        """Find medication information in knowledge base"""
        for med_category, med_classes in self.medications.items():
            for med_class, med_info in med_classes.items():
                if medication in med_info.get('examples', []):
                    return med_info
        return None
    
    def _get_medication_class_info(self, med_class: str) -> List[Dict[str, Any]]:
        """Get medication class information"""
        class_info = []
        for med_category, med_classes in self.medications.items():
            for class_name, med_info in med_classes.items():
                if med_class.lower() in class_name.lower() or med_class.lower() in med_info.get('examples', []):
                    class_info.append(med_info)
        return class_info
    
    def _llm_validate_pairing(self, condition: str, medication: str) -> Dict[str, Any]:
        """Use LLM to validate condition-medication pairing"""
        
        prompt = f"""
        Evaluate if {medication} is an appropriate medication for treating {condition}.
        
        Consider:
        1. Standard treatment guidelines
        2. Mechanism of action
        3. Clinical evidence
        4. Safety profile
        5. Contraindications
        
        Respond with:
        - Is this pairing appropriate? (Yes/No)
        - Confidence level (0.0-1.0)
        - Clinical reasoning
        - Any concerns or contraindications
        """
        
        try:
            response = self.ollama_client.generate_text(prompt)
            
            # Parse LLM response (simplified)
            is_appropriate = 'yes' in response.lower() and 'appropriate' in response.lower()
            
            return {
                'is_appropriate': is_appropriate,
                'confidence': 0.7,  # Default confidence for LLM
                'reasoning': response,
                'source': 'llm_analysis'
            }
        except Exception as e:
            return {
                'is_appropriate': False,
                'confidence': 0.0,
                'reasoning': f"Error in LLM analysis: {e}",
                'source': 'error'
            }
    
    def _interpret_lab_value(self, lab_name: str, value: float, lab_info: Dict[str, Any]) -> str:
        """Interpret lab value against reference ranges"""
        
        interpretation = "Normal"
        
        # Check different range types
        if 'normal_range' in lab_info:
            normal_min, normal_max = lab_info['normal_range']
            if value < normal_min:
                interpretation = "Below normal range"
            elif value > normal_max:
                interpretation = "Above normal range"
        
        # Check condition-specific ranges
        elif 'desirable' in lab_info:
            if value <= lab_info['desirable'][1]:
                interpretation = "Desirable"
            elif 'borderline_high' in lab_info and value <= lab_info['borderline_high'][1]:
                interpretation = "Borderline high"
            elif 'high' in lab_info:
                interpretation = "High"
        
        # Check diabetic ranges for glucose
        elif lab_name.lower() == 'glucose':
            if 'diabetic_range' in lab_info and value >= lab_info['diabetic_range'][0]:
                interpretation = "Diabetic range"
            elif 'prediabetic_range' in lab_info and value >= lab_info['prediabetic_range'][0]:
                interpretation = "Prediabetic range"
        
        return interpretation
    
    def _assess_lab_in_context(self, lab_name: str, value: float, conditions: List[str]) -> Dict[str, Any]:
        """Assess lab value in context of patient conditions"""
        
        context_assessment = {
            'expected_for_conditions': [],
            'unexpected_for_conditions': [],
            'monitoring_recommendations': []
        }
        
        # Check if abnormal value is expected given conditions
        for condition in conditions:
            condition_info = self._find_condition_info(condition)
            if condition_info:
                lab_markers = condition_info.get('lab_markers', [])
                if lab_name in [marker.lower() for marker in lab_markers]:
                    context_assessment['expected_for_conditions'].append(condition)
        
        # Generate monitoring recommendations
        if 'abnormal' in self._interpret_lab_value(lab_name, value, self.lab_tests.get(lab_name.lower(), {})).lower():
            context_assessment['monitoring_recommendations'].append(f"Monitor {lab_name} closely")
            
            # Condition-specific recommendations
            for condition in conditions:
                if condition == 'Diabetes Mellitus Type 2' and lab_name.lower() in ['glucose', 'hba1c']:
                    context_assessment['monitoring_recommendations'].append("Consider diabetes management adjustment")
                elif condition == 'Hypertension' and 'blood_pressure' in lab_name.lower():
                    context_assessment['monitoring_recommendations'].append("Consider hypertension management review")
        
        return context_assessment
    
    def _get_llm_lab_interpretation(self, lab_name: str, value: float, conditions: List[str]) -> str:
        """Get LLM interpretation of lab value"""
        
        conditions_str = ', '.join(conditions) if conditions else 'None'
        
        prompt = f"""
        Interpret this laboratory result:
        
        Test: {lab_name}
        Value: {value}
        Patient conditions: {conditions_str}
        
        Provide:
        1. Clinical interpretation of the value
        2. Significance given patient's conditions
        3. Possible causes for abnormal values
        4. Recommended follow-up actions
        
        Focus on clinical relevance and actionable insights.
        """
        
        try:
            return self.ollama_client.generate_text(prompt)
        except Exception as e:
            return f"Error generating interpretation: {e}"
    
    def _analyze_condition_patterns(self, conditions: List[str]) -> List[Dict[str, Any]]:
        """Analyze patterns in patient conditions"""
        
        patterns = []
        
        # Check for common comorbidity patterns
        diabetes_related = ['Diabetes Mellitus Type 2', 'Hypertension', 'Hyperlipidemia']
        cardiovascular_cluster = ['Hypertension', 'Coronary Artery Disease', 'Hyperlipidemia']
        metabolic_syndrome = ['Diabetes Mellitus Type 2', 'Hypertension', 'Obesity', 'Hyperlipidemia']
        
        pattern_sets = [
            ('Diabetes-related complications', diabetes_related),
            ('Cardiovascular risk cluster', cardiovascular_cluster),
            ('Metabolic syndrome components', metabolic_syndrome)
        ]
        
        for pattern_name, pattern_conditions in pattern_sets:
            matches = [cond for cond in conditions if cond in pattern_conditions]
            if len(matches) >= 2:
                patterns.append({
                    'pattern_name': pattern_name,
                    'matching_conditions': matches,
                    'completeness': len(matches) / len(pattern_conditions),
                    'clinical_significance': f"Patient shows {len(matches)}/{len(pattern_conditions)} components of {pattern_name}"
                })
        
        return patterns
    
    def _generate_llm_insights(self, patient_data: Dict[str, Any]) -> str:
        """Generate comprehensive medical insights using LLM"""
        
        conditions = ', '.join(patient_data.get('conditions', []))
        medications = ', '.join(patient_data.get('medications', []))
        lab_results = ', '.join([f"{lab}: {value} {unit}" 
                               for lab, (value, unit) in patient_data.get('lab_results', {}).items()])
        
        prompt = f"""
        Analyze this patient's medical profile and provide clinical insights:
        
        Age: {patient_data.get('age', 'Unknown')}
        Gender: {patient_data.get('gender', 'Unknown')}
        Conditions: {conditions or 'None listed'}
        Medications: {medications or 'None listed'}
        Lab Results: {lab_results or 'None available'}
        
        Provide insights on:
        1. Overall health status and risk factors
        2. Condition management appropriateness
        3. Potential drug interactions or concerns
        4. Missing or recommended screenings
        5. Lifestyle or treatment modifications
        
        Focus on clinically relevant observations and actionable recommendations.
        """
        
        try:
            return self.ollama_client.generate_text(prompt)
        except Exception as e:
            return f"Error generating insights: {e}"
    
    def _parse_llm_errors(self, response: str) -> List[str]:
        """Parse potential errors from LLM response"""
        errors = []
        
        # Simple parsing - look for error indicators
        error_indicators = ['error', 'incorrect', 'inappropriate', 'wrong', 'mistake']
        
        lines = response.split('\n')
        for line in lines:
            if any(indicator in line.lower() for indicator in error_indicators):
                errors.append(line.strip())
        
        return errors
    
    def _parse_llm_suggestions(self, response: str) -> List[str]:
        """Parse suggestions from LLM response"""
        suggestions = []
        
        # Simple parsing - look for suggestion indicators
        suggestion_indicators = ['suggest', 'recommend', 'consider', 'should', 'could']
        
        lines = response.split('\n')
        for line in lines:
            if any(indicator in line.lower() for indicator in suggestion_indicators):
                suggestions.append(line.strip())
        
        return suggestions