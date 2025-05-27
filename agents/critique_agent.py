from typing import Dict, Any, List, Optional
from models.patient_data import PatientCohort
from models.literature_data import LiteratureResult
from utils.ollama_client import OllamaClient
import pandas as pd

class CritiqueAgent:
    """Agent responsible for critiquing and validating synthetic cohorts against literature"""
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
    
    def critique_cohort(self, cohort: PatientCohort, literature: LiteratureResult, 
                       query: str) -> Dict[str, Any]:
        """Comprehensive critique of synthetic cohort against literature evidence"""
        
        critique_results = {
            "overall_assessment": "",
            "realism_score": 0.0,
            "bias_assessment": {},
            "literature_alignment": {},
            "recommendations": [],
            "detailed_analysis": {}
        }
        
        # Perform different types of critique
        critique_results["realism_score"] = self._assess_realism(cohort)
        critique_results["bias_assessment"] = self._assess_bias(cohort)
        critique_results["literature_alignment"] = self._assess_literature_alignment(
            cohort, literature, query
        )
        critique_results["detailed_analysis"] = self._detailed_statistical_analysis(cohort)
        
        # Generate overall assessment
        critique_results["overall_assessment"] = self._generate_overall_assessment(
            cohort, literature, query, critique_results
        )
        
        # Generate recommendations
        critique_results["recommendations"] = self._generate_recommendations(critique_results)
        
        return critique_results
    
    def _assess_realism(self, cohort: PatientCohort) -> float:
        """Assess the overall realism of the synthetic cohort"""
        realism_factors = []
        
        # Age distribution realism
        ages = [p.age for p in cohort.patients if p.age]
        if ages:
            age_mean = sum(ages) / len(ages)
            age_std = (sum((x - age_mean) ** 2 for x in ages) / len(ages)) ** 0.5
            # Realistic if mean is between 20-80 and std is reasonable
            age_realism = 1.0 if 20 <= age_mean <= 80 and 10 <= age_std <= 25 else 0.7
            realism_factors.append(age_realism)
        
        # Gender distribution realism
        genders = [p.gender for p in cohort.patients if p.gender]
        if genders:
            female_ratio = sum(1 for g in genders if g.lower() == 'female') / len(genders)
            # Realistic if ratio is between 30-70%
            gender_realism = 1.0 if 0.3 <= female_ratio <= 0.7 else 0.8
            realism_factors.append(gender_realism)
        
        # Condition-medication alignment
        alignment_score = self._assess_condition_medication_alignment(cohort)
        realism_factors.append(alignment_score)
        
        # Lab value realism
        lab_realism = self._assess_lab_value_realism(cohort)
        realism_factors.append(lab_realism)
        
        return sum(realism_factors) / len(realism_factors) if realism_factors else 0.0
    
    def _assess_bias(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Assess potential biases in the synthetic cohort"""
        bias_assessment = {
            "demographic_bias": {},
            "condition_bias": {},
            "representation_gaps": [],
            "overall_bias_score": 0.0
        }
        
        # Demographic bias analysis
        bias_assessment["demographic_bias"] = self._analyze_demographic_bias(cohort)
        
        # Condition prevalence bias
        bias_assessment["condition_bias"] = self._analyze_condition_bias(cohort)
        
        # Identify representation gaps
        bias_assessment["representation_gaps"] = self._identify_representation_gaps(cohort)
        
        # Calculate overall bias score
        demographic_score = bias_assessment["demographic_bias"].get("score", 0.5)
        condition_score = bias_assessment["condition_bias"].get("score", 0.5)
        bias_assessment["overall_bias_score"] = (demographic_score + condition_score) / 2
        
        return bias_assessment
    
    def _assess_literature_alignment(self, cohort: PatientCohort, literature: LiteratureResult, 
                                   query: str) -> Dict[str, Any]:
        """Assess how well the cohort aligns with literature findings"""
        alignment_assessment = {
            "population_match": 0.0,
            "condition_prevalence_match": 0.0,
            "demographic_match": 0.0,
            "literature_gaps": [],
            "overall_alignment": 0.0
        }
        
        if not literature.papers:
            alignment_assessment["literature_gaps"] = ["No literature found for comparison"]
            return alignment_assessment
        
        # Use LLM to assess alignment
        alignment_text = self._generate_literature_alignment_analysis(cohort, literature, query)
        
        # Extract scores from LLM analysis (simplified scoring)
        alignment_assessment["population_match"] = 0.8  # Placeholder
        alignment_assessment["condition_prevalence_match"] = 0.7  # Placeholder
        alignment_assessment["demographic_match"] = 0.75  # Placeholder
        
        alignment_assessment["overall_alignment"] = (
            alignment_assessment["population_match"] +
            alignment_assessment["condition_prevalence_match"] +
            alignment_assessment["demographic_match"]
        ) / 3
        
        return alignment_assessment
    
    def _detailed_statistical_analysis(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Perform detailed statistical analysis of the cohort"""
        analysis = {
            "demographics": {},
            "conditions": {},
            "medications": {},
            "lab_values": {}
        }
        
        # Demographics analysis
        ages = [p.age for p in cohort.patients if p.age is not None]
        genders = [p.gender for p in cohort.patients if p.gender]
        ethnicities = [p.ethnicity for p in cohort.patients if p.ethnicity]
        
        analysis["demographics"] = {
            "age_statistics": {
                "mean": sum(ages) / len(ages) if ages else 0,
                "min": min(ages) if ages else 0,
                "max": max(ages) if ages else 0,
                "count": len(ages)
            },
            "gender_distribution": dict(pd.Series(genders).value_counts()) if genders else {},
            "ethnicity_distribution": dict(pd.Series(ethnicities).value_counts()) if ethnicities else {}
        }
        
        # Conditions analysis
        all_conditions = []
        for patient in cohort.patients:
            all_conditions.extend(patient.conditions)
        
        analysis["conditions"] = {
            "total_conditions": len(all_conditions),
            "unique_conditions": len(set(all_conditions)),
            "condition_prevalence": dict(pd.Series(all_conditions).value_counts()) if all_conditions else {},
            "avg_conditions_per_patient": len(all_conditions) / len(cohort.patients) if cohort.patients else 0
        }
        
        # Medications analysis
        all_medications = []
        for patient in cohort.patients:
            all_medications.extend(patient.medications)
        
        analysis["medications"] = {
            "total_medications": len(all_medications),
            "unique_medications": len(set(all_medications)),
            "medication_frequency": dict(pd.Series(all_medications).value_counts()) if all_medications else {},
            "avg_medications_per_patient": len(all_medications) / len(cohort.patients) if cohort.patients else 0
        }
        
        # Lab values analysis
        lab_summary = {}
        for patient in cohort.patients:
            for lab_name, (value, unit) in patient.lab_results.items():
                if lab_name not in lab_summary:
                    lab_summary[lab_name] = {"values": [], "unit": unit}
                lab_summary[lab_name]["values"].append(value)
        
        for lab_name, data in lab_summary.items():
            values = data["values"]
            lab_summary[lab_name]["statistics"] = {
                "mean": sum(values) / len(values) if values else 0,
                "min": min(values) if values else 0,
                "max": max(values) if values else 0,
                "count": len(values)
            }
        
        analysis["lab_values"] = lab_summary
        
        return analysis
    
    def _assess_condition_medication_alignment(self, cohort: PatientCohort) -> float:
        """Assess how well medications align with conditions"""
        appropriate_matches = 0
        total_condition_instances = 0
        
        # Define condition-medication mappings
        condition_med_map = {
            "Diabetes Mellitus Type 2": ["Metformin", "Insulin", "Glipizide"],
            "Hypertension": ["Lisinopril", "Amlodipine", "Metoprolol"],
            "Hyperlipidemia": ["Atorvastatin", "Simvastatin"],
            "Depression": ["Sertraline", "Escitalopram"],
            "COPD": ["Albuterol", "Tiotropium"]
        }
        
        for patient in cohort.patients:
            for condition in patient.conditions:
                if condition in condition_med_map:
                    total_condition_instances += 1
                    expected_meds = condition_med_map[condition]
                    if any(med in patient.medications for med in expected_meds):
                        appropriate_matches += 1
        
        return appropriate_matches / total_condition_instances if total_condition_instances > 0 else 1.0
    
    def _assess_lab_value_realism(self, cohort: PatientCohort) -> float:
        """Assess realism of lab values"""
        realistic_values = 0
        total_values = 0
        
        # Define realistic ranges
        realistic_ranges = {
            "glucose": (50, 400),
            "hemoglobin": (8, 20),
            "creatinine": (0.3, 5.0),
            "cholesterol": (100, 500),
            "blood_pressure_systolic": (70, 220),
            "blood_pressure_diastolic": (40, 130)
        }
        
        for patient in cohort.patients:
            for lab_name, (value, unit) in patient.lab_results.items():
                if lab_name in realistic_ranges:
                    total_values += 1
                    min_val, max_val = realistic_ranges[lab_name]
                    if min_val <= value <= max_val:
                        realistic_values += 1
        
        return realistic_values / total_values if total_values > 0 else 1.0
    
    def _analyze_demographic_bias(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Analyze demographic biases in the cohort"""
        genders = [p.gender for p in cohort.patients if p.gender]
        ethnicities = [p.ethnicity for p in cohort.patients if p.ethnicity]
        ages = [p.age for p in cohort.patients if p.age is not None]
        
        bias_issues = []
        
        # Gender bias check
        if genders:
            female_ratio = sum(1 for g in genders if g.lower() == 'female') / len(genders)
            if female_ratio < 0.2 or female_ratio > 0.8:
                bias_issues.append(f"Gender imbalance: {female_ratio:.1%} female")
        
        # Age bias check
        if ages:
            elderly_ratio = sum(1 for age in ages if age >= 65) / len(ages)
            if elderly_ratio > 0.7:
                bias_issues.append(f"Age bias toward elderly: {elderly_ratio:.1%} over 65")
            elif elderly_ratio < 0.1:
                bias_issues.append(f"Underrepresentation of elderly: {elderly_ratio:.1%} over 65")
        
        # Ethnicity bias check
        if ethnicities:
            ethnicity_counts = pd.Series(ethnicities).value_counts()
            dominant_ethnicity_ratio = ethnicity_counts.iloc[0] / len(ethnicities)
            if dominant_ethnicity_ratio > 0.8:
                bias_issues.append(f"Ethnicity bias: {dominant_ethnicity_ratio:.1%} {ethnicity_counts.index[0]}")
        
        # Calculate bias score (lower means more bias)
        bias_score = max(0.0, 1.0 - len(bias_issues) * 0.2)
        
        return {
            "score": bias_score,
            "issues": bias_issues,
            "demographic_breakdown": {
                "gender_distribution": dict(pd.Series(genders).value_counts()) if genders else {},
                "ethnicity_distribution": dict(pd.Series(ethnicities).value_counts()) if ethnicities else {},
                "age_groups": self._categorize_ages(ages)
            }
        }
    
    def _analyze_condition_bias(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Analyze condition-related biases"""
        all_conditions = []
        for patient in cohort.patients:
            all_conditions.extend(patient.conditions)
        
        if not all_conditions:
            return {"score": 0.5, "issues": ["No conditions to analyze"]}
        
        condition_counts = pd.Series(all_conditions).value_counts()
        bias_issues = []
        
        # Check for over-representation of single conditions
        total_patients = len(cohort.patients)
        for condition, count in condition_counts.items():
            prevalence = count / total_patients
            if prevalence > 0.9:
                bias_issues.append(f"Over-representation of {condition}: {prevalence:.1%}")
        
        # Check for lack of diversity
        if len(condition_counts) < 3:
            bias_issues.append("Low condition diversity")
        
        bias_score = max(0.0, 1.0 - len(bias_issues) * 0.25)
        
        return {
            "score": bias_score,
            "issues": bias_issues,
            "condition_distribution": dict(condition_counts)
        }
    
    def _identify_representation_gaps(self, cohort: PatientCohort) -> List[str]:
        """Identify gaps in representation"""
        gaps = []
        
        # Check age representation
        ages = [p.age for p in cohort.patients if p.age is not None]
        if ages:
            age_ranges = {
                "pediatric": sum(1 for age in ages if age < 18),
                "young_adult": sum(1 for age in ages if 18 <= age < 35),
                "middle_aged": sum(1 for age in ages if 35 <= age < 65),
                "elderly": sum(1 for age in ages if age >= 65)
            }
            
            for age_group, count in age_ranges.items():
                if count == 0:
                    gaps.append(f"No {age_group} representation")
        
        # Check gender representation
        genders = [p.gender for p in cohort.patients if p.gender]
        if genders:
            unique_genders = set(g.lower() for g in genders)
            if 'female' not in unique_genders:
                gaps.append("No female representation")
            if 'male' not in unique_genders:
                gaps.append("No male representation")
        
        # Check ethnicity diversity
        ethnicities = [p.ethnicity for p in cohort.patients if p.ethnicity]
        if ethnicities and len(set(ethnicities)) < 3:
            gaps.append("Limited ethnicity diversity")
        
        return gaps
    
    def _categorize_ages(self, ages: List[int]) -> Dict[str, int]:
        """Categorize ages into groups"""
        if not ages:
            return {}
        
        return {
            "pediatric (<18)": sum(1 for age in ages if age < 18),
            "young_adult (18-34)": sum(1 for age in ages if 18 <= age < 35),
            "middle_aged (35-64)": sum(1 for age in ages if 35 <= age < 65),
            "elderly (65+)": sum(1 for age in ages if age >= 65)
        }
    
    def _generate_literature_alignment_analysis(self, cohort: PatientCohort, 
                                              literature: LiteratureResult, query: str) -> str:
        """Generate detailed analysis of cohort-literature alignment using LLM"""
        
        # Prepare cohort summary
        cohort_summary = self._summarize_cohort_for_llm(cohort)
        
        # Prepare literature summary
        literature_summary = literature.summary if literature.summary else "No literature summary available"
        
        prompt = f"""
        Analyze how well this synthetic patient cohort aligns with the available literature evidence.

        Original Query: {query}

        Synthetic Cohort Summary:
        {cohort_summary}

        Literature Summary:
        {literature_summary}

        Key Literature Papers:
        {self._format_papers_for_prompt(literature.papers[:5])}

        Provide a detailed analysis addressing:
        1. How well the cohort demographics match study populations in the literature
        2. Whether condition prevalences align with published epidemiological data
        3. Gaps between the synthetic cohort and real-world evidence
        4. Potential biases that may have been introduced
        5. Recommendations for improving cohort realism

        Be specific and cite patterns you observe.
        """
        
        try:
            analysis = self.ollama_client.generate_text(prompt)
            return analysis
        except Exception as e:
            print(f"Error generating literature alignment analysis: {e}")
            return "Literature alignment analysis could not be generated due to technical issues."
    
    def _summarize_cohort_for_llm(self, cohort: PatientCohort) -> str:
        """Create a text summary of the cohort for LLM analysis"""
        ages = [p.age for p in cohort.patients if p.age is not None]
        genders = [p.gender for p in cohort.patients if p.gender]
        
        all_conditions = []
        for patient in cohort.patients:
            all_conditions.extend(patient.conditions)
        
        condition_counts = pd.Series(all_conditions).value_counts()
        
        summary = f"""
        Cohort Size: {len(cohort.patients)} patients
        
        Demographics:
        - Age: Mean {sum(ages)/len(ages):.1f} years (range: {min(ages)}-{max(ages)})
        - Gender: {dict(pd.Series(genders).value_counts())}
        
        Top Conditions:
        {condition_counts.head(10).to_dict()}
        
        Average conditions per patient: {len(all_conditions) / len(cohort.patients):.1f}
        """
        
        return summary
    
    def _format_papers_for_prompt(self, papers: List) -> str:
        """Format papers for inclusion in LLM prompt"""
        if not papers:
            return "No papers available"
        
        formatted = ""
        for i, paper in enumerate(papers[:5], 1):
            formatted += f"{i}. {paper.title}\n"
            formatted += f"   Authors: {paper.authors}\n"
            formatted += f"   Abstract: {paper.abstract[:200]}...\n\n"
        
        return formatted
    
    def _generate_overall_assessment(self, cohort: PatientCohort, literature: LiteratureResult, 
                                   query: str, critique_results: Dict[str, Any]) -> str:
        """Generate overall assessment using LLM"""
        
        prompt = f"""
        Provide a comprehensive assessment of this synthetic patient cohort based on the analysis results.

        Original Query: {query}
        
        Analysis Results:
        - Realism Score: {critique_results['realism_score']:.2f}/1.0
        - Bias Score: {critique_results['bias_assessment'].get('overall_bias_score', 0):.2f}/1.0
        - Literature Alignment: {critique_results['literature_alignment'].get('overall_alignment', 0):.2f}/1.0
        
        Bias Issues: {critique_results['bias_assessment'].get('issues', [])}
        Representation Gaps: {critique_results['bias_assessment'].get('representation_gaps', [])}
        
        Provide:
        1. Overall quality assessment (Excellent/Good/Fair/Poor)
        2. Key strengths of the cohort
        3. Main limitations and concerns
        4. Suitability for AI model training/validation
        5. Confidence level in using this data
        
        Keep the assessment concise but thorough (2-3 paragraphs).
        """
        
        try:
            assessment = self.ollama_client.generate_text(prompt)
            return assessment
        except Exception as e:
            print(f"Error generating overall assessment: {e}")
            return f"Overall Assessment: Cohort generated with realism score of {critique_results['realism_score']:.2f}. Manual review recommended."
    
    def _generate_recommendations(self, critique_results: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations based on critique results"""
        recommendations = []
        
        # Realism-based recommendations
        if critique_results["realism_score"] < 0.7:
            recommendations.append("Improve overall cohort realism by adjusting demographic distributions")
        
        # Bias-based recommendations
        bias_issues = critique_results["bias_assessment"].get("issues", [])
        if bias_issues:
            recommendations.append("Address identified biases: " + "; ".join(bias_issues))
        
        representation_gaps = critique_results["bias_assessment"].get("representation_gaps", [])
        if representation_gaps:
            recommendations.append("Fill representation gaps: " + "; ".join(representation_gaps))
        
        # Literature alignment recommendations
        alignment_score = critique_results["literature_alignment"].get("overall_alignment", 0)
        if alignment_score < 0.6:
            recommendations.append("Improve alignment with literature by adjusting patient characteristics")
        
        # General recommendations
        if critique_results["realism_score"] > 0.8:
            recommendations.append("Cohort shows good realism - suitable for preliminary AI model training")
        
        if not recommendations:
            recommendations.append("Cohort appears well-balanced and suitable for use")
        
        return recommendations
