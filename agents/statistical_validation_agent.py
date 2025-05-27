import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from models.patient_data import PatientCohort
from models.literature_data import LiteratureResult
from utils.ollama_client import OllamaClient

class StatisticalValidationAgent:
    """Agent for comprehensive statistical validation of synthetic medical data"""
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
        
        # Medical reference ranges and normal distributions
        self.medical_references = {
            'age': {'mean': 45, 'std': 20, 'min': 0, 'max': 100},
            'glucose': {'mean': 100, 'std': 15, 'min': 70, 'max': 200, 'unit': 'mg/dL'},
            'hemoglobin': {'mean': 14, 'std': 2, 'min': 10, 'max': 18, 'unit': 'g/dL'},
            'creatinine': {'mean': 1.0, 'std': 0.3, 'min': 0.5, 'max': 3.0, 'unit': 'mg/dL'},
            'cholesterol': {'mean': 200, 'std': 40, 'min': 120, 'max': 350, 'unit': 'mg/dL'},
            'blood_pressure_systolic': {'mean': 120, 'std': 20, 'min': 80, 'max': 200, 'unit': 'mmHg'},
            'blood_pressure_diastolic': {'mean': 80, 'std': 10, 'min': 50, 'max': 120, 'unit': 'mmHg'},
            'heart_rate': {'mean': 75, 'std': 15, 'min': 50, 'max': 120, 'unit': 'bpm'},
            'bmi': {'mean': 25, 'std': 5, 'min': 15, 'max': 45, 'unit': 'kg/m²'}
        }
        
        # Disease prevalence rates (per 100,000 population)
        self.disease_prevalence = {
            'Hypertension': 0.45,
            'Diabetes Mellitus Type 2': 0.11,
            'Hyperlipidemia': 0.38,
            'Coronary Artery Disease': 0.06,
            'COPD': 0.04,
            'Depression': 0.08,
            'Anxiety': 0.18,
            'Osteoarthritis': 0.22,
            'Hypothyroidism': 0.05,
            'Chronic Kidney Disease': 0.15
        }
        
        # Age-specific disease adjustments
        self.age_disease_multipliers = {
            'elderly': {'Hypertension': 2.5, 'Diabetes Mellitus Type 2': 2.0, 'Coronary Artery Disease': 4.0},
            'middle_aged': {'Hypertension': 1.5, 'Diabetes Mellitus Type 2': 1.3},
            'young_adult': {'Depression': 1.5, 'Anxiety': 2.0}
        }
    
    def comprehensive_validation(self, cohort: PatientCohort, literature: Optional[LiteratureResult] = None) -> Dict[str, Any]:
        """Perform comprehensive statistical validation of synthetic cohort"""
        
        validation_results = {
            'demographic_analysis': self.analyze_demographics(cohort),
            'clinical_validity': self.assess_clinical_validity(cohort),
            'distribution_analysis': self.analyze_distributions(cohort),
            'correlation_analysis': self.analyze_correlations(cohort),
            'outlier_detection': self.detect_outliers(cohort),
            'clustering_analysis': self.perform_clustering_analysis(cohort),
            'literature_consistency': self.assess_literature_consistency(cohort, literature),
            'medical_plausibility': self.assess_medical_plausibility(cohort),
            'statistical_summary': {},
            'recommendations': [],
            'overall_quality_score': 0.0,
            'validation_timestamp': datetime.now().isoformat()
        }
        
        # Calculate overall quality score
        validation_results['overall_quality_score'] = self._calculate_overall_quality(validation_results)
        
        # Generate recommendations
        validation_results['recommendations'] = self._generate_recommendations(validation_results)
        
        # Create statistical summary
        validation_results['statistical_summary'] = self._create_statistical_summary(cohort)
        
        return validation_results
    
    def analyze_demographics(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Analyze demographic distributions and patterns"""
        if not cohort.patients:
            return {'error': 'No patients in cohort'}
        
        # Extract demographic data
        ages = [p.age for p in cohort.patients if p.age is not None]
        genders = [p.gender for p in cohort.patients if p.gender]
        ethnicities = [p.ethnicity for p in cohort.patients if p.ethnicity]
        
        analysis = {
            'age_analysis': {},
            'gender_analysis': {},
            'ethnicity_analysis': {},
            'demographic_validity_score': 0.0
        }
        
        # Age analysis
        if ages:
            age_stats = {
                'mean': np.mean(ages),
                'median': np.median(ages),
                'std': np.std(ages),
                'min': np.min(ages),
                'max': np.max(ages),
                'q25': np.percentile(ages, 25),
                'q75': np.percentile(ages, 75),
                'skewness': stats.skew(ages),
                'kurtosis': stats.kurtosis(ages)
            }
            
            # Test for normality
            normality_test = stats.shapiro(ages) if len(ages) < 5000 else stats.kstest(ages, 'norm')
            age_stats['normality_p_value'] = normality_test.pvalue
            age_stats['is_normal'] = normality_test.pvalue > 0.05
            
            # Age group distribution
            age_groups = self._categorize_ages(ages)
            age_stats['age_group_distribution'] = age_groups
            
            analysis['age_analysis'] = age_stats
        
        # Gender analysis
        if genders:
            gender_counts = pd.Series(genders).value_counts()
            total_patients = len(genders)
            
            gender_analysis = {
                'distribution': dict(gender_counts),
                'proportions': dict(gender_counts / total_patients),
                'balance_score': self._calculate_gender_balance_score(gender_counts),
                'chi_square_test': self._perform_gender_chi_square(gender_counts)
            }
            
            analysis['gender_analysis'] = gender_analysis
        
        # Ethnicity analysis
        if ethnicities:
            ethnicity_counts = pd.Series(ethnicities).value_counts()
            total_patients = len(ethnicities)
            
            ethnicity_analysis = {
                'distribution': dict(ethnicity_counts),
                'proportions': dict(ethnicity_counts / total_patients),
                'diversity_index': self._calculate_diversity_index(ethnicity_counts),
                'representation_gaps': self._identify_ethnicity_gaps(ethnicity_counts)
            }
            
            analysis['ethnicity_analysis'] = ethnicity_analysis
        
        # Calculate overall demographic validity score
        analysis['demographic_validity_score'] = self._calculate_demographic_validity_score(analysis)
        
        return analysis
    
    def assess_clinical_validity(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Assess clinical validity of patient data"""
        
        validity_analysis = {
            'lab_value_validity': {},
            'medication_appropriateness': {},
            'comorbidity_patterns': {},
            'clinical_consistency_score': 0.0
        }
        
        # Analyze lab values
        all_lab_data = {}
        for patient in cohort.patients:
            for lab_name, (value, unit) in patient.lab_results.items():
                if lab_name not in all_lab_data:
                    all_lab_data[lab_name] = []
                all_lab_data[lab_name].append(value)
        
        lab_validity = {}
        for lab_name, values in all_lab_data.items():
            if lab_name in self.medical_references:
                ref = self.medical_references[lab_name]
                
                lab_stats = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'within_normal_range': sum(1 for v in values if ref['min'] <= v <= ref['max']) / len(values),
                    'outliers': sum(1 for v in values if v < ref['min'] or v > ref['max']),
                    'z_scores': [(v - ref['mean']) / ref['std'] for v in values],
                    'clinical_plausibility': self._assess_lab_plausibility(lab_name, values)
                }
                
                lab_validity[lab_name] = lab_stats
        
        validity_analysis['lab_value_validity'] = lab_validity
        
        # Analyze medication appropriateness
        medication_analysis = self._analyze_medication_patterns(cohort)
        validity_analysis['medication_appropriateness'] = medication_analysis
        
        # Analyze comorbidity patterns
        comorbidity_analysis = self._analyze_comorbidity_patterns(cohort)
        validity_analysis['comorbidity_patterns'] = comorbidity_analysis
        
        # Calculate clinical consistency score
        validity_analysis['clinical_consistency_score'] = self._calculate_clinical_consistency_score(validity_analysis)
        
        return validity_analysis
    
    def analyze_distributions(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Analyze statistical distributions of key variables"""
        
        distribution_analysis = {
            'age_distribution': {},
            'lab_distributions': {},
            'disease_prevalence_analysis': {},
            'distribution_quality_score': 0.0
        }
        
        # Age distribution analysis
        ages = [p.age for p in cohort.patients if p.age is not None]
        if ages:
            age_dist = self._analyze_single_distribution(ages, 'age')
            distribution_analysis['age_distribution'] = age_dist
        
        # Lab value distributions
        lab_distributions = {}
        for patient in cohort.patients:
            for lab_name, (value, unit) in patient.lab_results.items():
                if lab_name not in lab_distributions:
                    lab_distributions[lab_name] = []
                lab_distributions[lab_name].append(value)
        
        for lab_name, values in lab_distributions.items():
            if len(values) > 10:  # Minimum sample size for distribution analysis
                lab_dist = self._analyze_single_distribution(values, lab_name)
                distribution_analysis['lab_distributions'][lab_name] = lab_dist
        
        # Disease prevalence analysis
        disease_analysis = self._analyze_disease_prevalence(cohort)
        distribution_analysis['disease_prevalence_analysis'] = disease_analysis
        
        # Calculate distribution quality score
        distribution_analysis['distribution_quality_score'] = self._calculate_distribution_quality_score(distribution_analysis)
        
        return distribution_analysis
    
    def analyze_correlations(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Analyze correlations between variables"""
        
        # Create correlation matrix
        correlation_data = []
        
        for patient in cohort.patients:
            patient_data = {'age': patient.age}
            
            # Add lab results
            for lab_name, (value, unit) in patient.lab_results.items():
                patient_data[lab_name] = value
            
            # Add condition counts
            patient_data['condition_count'] = len(patient.conditions)
            patient_data['medication_count'] = len(patient.medications)
            
            correlation_data.append(patient_data)
        
        if not correlation_data:
            return {'error': 'No data available for correlation analysis'}
        
        df = pd.DataFrame(correlation_data)
        
        # Calculate correlation matrix
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return {'error': 'Insufficient numeric variables for correlation analysis'}
        
        correlation_matrix = df[numeric_cols].corr()
        
        # Identify significant correlations
        significant_correlations = self._find_significant_correlations(correlation_matrix)
        
        # Medical correlation validation
        medical_correlations = self._validate_medical_correlations(correlation_matrix)
        
        return {
            'correlation_matrix': correlation_matrix.to_dict(),
            'significant_correlations': significant_correlations,
            'medical_correlation_validity': medical_correlations,
            'correlation_insights': self._generate_correlation_insights(correlation_matrix)
        }
    
    def detect_outliers(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Detect outliers in patient data using multiple methods"""
        
        outlier_analysis = {
            'statistical_outliers': {},
            'clinical_outliers': {},
            'isolation_forest_outliers': [],
            'outlier_summary': {}
        }
        
        # Statistical outlier detection (Z-score and IQR methods)
        for patient in cohort.patients:
            patient_outliers = {}
            
            # Check age outliers
            if patient.age is not None:
                age_z_score = abs((patient.age - 45) / 20)  # Using population mean/std
                if age_z_score > 3:
                    patient_outliers['age'] = {'value': patient.age, 'z_score': age_z_score, 'type': 'statistical'}
            
            # Check lab value outliers
            for lab_name, (value, unit) in patient.lab_results.items():
                if lab_name in self.medical_references:
                    ref = self.medical_references[lab_name]
                    z_score = abs((value - ref['mean']) / ref['std'])
                    
                    if z_score > 3 or value < ref['min'] or value > ref['max']:
                        patient_outliers[lab_name] = {
                            'value': value,
                            'z_score': z_score,
                            'reference_range': f"{ref['min']}-{ref['max']} {ref.get('unit', '')}",
                            'type': 'clinical' if (value < ref['min'] or value > ref['max']) else 'statistical'
                        }
            
            if patient_outliers:
                outlier_analysis['statistical_outliers'][patient.patient_id] = patient_outliers
        
        # Isolation Forest for multivariate outlier detection
        numeric_data = self._prepare_numeric_data_for_outlier_detection(cohort)
        if len(numeric_data) > 10:
            isolation_outliers = self._detect_isolation_forest_outliers(numeric_data, cohort)
            outlier_analysis['isolation_forest_outliers'] = isolation_outliers
        
        # Summarize outlier findings
        outlier_analysis['outlier_summary'] = self._summarize_outliers(outlier_analysis)
        
        return outlier_analysis
    
    def perform_clustering_analysis(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Perform clustering analysis to identify patient subgroups"""
        
        # Prepare data for clustering
        clustering_data = self._prepare_clustering_data(cohort)
        
        if len(clustering_data) < 10:
            return {'error': 'Insufficient data for clustering analysis'}
        
        # Standardize data
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(clustering_data)
        
        # Determine optimal number of clusters
        optimal_clusters = self._find_optimal_clusters(scaled_data)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(scaled_data)
        
        # Calculate silhouette score
        silhouette_avg = silhouette_score(scaled_data, cluster_labels)
        
        # Analyze cluster characteristics
        cluster_analysis = self._analyze_clusters(cohort, cluster_labels, clustering_data.columns)
        
        # PCA for dimensionality reduction and visualization
        pca = PCA(n_components=2)
        pca_data = pca.fit_transform(scaled_data)
        
        return {
            'optimal_clusters': optimal_clusters,
            'silhouette_score': silhouette_avg,
            'cluster_assignments': cluster_labels.tolist(),
            'cluster_characteristics': cluster_analysis,
            'pca_variance_ratio': pca.explained_variance_ratio_.tolist(),
            'clustering_quality': 'good' if silhouette_avg > 0.5 else 'moderate' if silhouette_avg > 0.3 else 'poor'
        }
    
    def assess_literature_consistency(self, cohort: PatientCohort, literature: Optional[LiteratureResult]) -> Dict[str, Any]:
        """Assess consistency between synthetic cohort and literature findings"""
        
        if not literature or not literature.papers:
            return {'error': 'No literature available for consistency analysis'}
        
        # Extract population characteristics from literature using LLM
        literature_characteristics = self._extract_literature_characteristics(literature)
        
        # Compare cohort to literature characteristics
        consistency_analysis = {
            'population_match': self._compare_population_characteristics(cohort, literature_characteristics),
            'prevalence_match': self._compare_disease_prevalence(cohort, literature_characteristics),
            'demographic_match': self._compare_demographics(cohort, literature_characteristics),
            'consistency_score': 0.0,
            'literature_gaps': []
        }
        
        # Calculate overall consistency score
        consistency_analysis['consistency_score'] = self._calculate_literature_consistency_score(consistency_analysis)
        
        return consistency_analysis
    
    def assess_medical_plausibility(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Assess medical plausibility using domain knowledge and LLM"""
        
        plausibility_analysis = {
            'condition_medication_alignment': {},
            'age_condition_appropriateness': {},
            'lab_condition_consistency': {},
            'medical_logic_violations': [],
            'plausibility_score': 0.0
        }
        
        # Analyze condition-medication alignment
        plausibility_analysis['condition_medication_alignment'] = self._assess_condition_medication_alignment(cohort)
        
        # Analyze age-condition appropriateness
        plausibility_analysis['age_condition_appropriateness'] = self._assess_age_condition_appropriateness(cohort)
        
        # Analyze lab-condition consistency
        plausibility_analysis['lab_condition_consistency'] = self._assess_lab_condition_consistency(cohort)
        
        # Use LLM to identify medical logic violations
        plausibility_analysis['medical_logic_violations'] = self._identify_medical_logic_violations(cohort)
        
        # Calculate overall plausibility score
        plausibility_analysis['plausibility_score'] = self._calculate_medical_plausibility_score(plausibility_analysis)
        
        return plausibility_analysis
    
    def _calculate_overall_quality(self, validation_results: Dict[str, Any]) -> float:
        """Calculate overall quality score from all validation components"""
        scores = []
        
        if 'demographic_analysis' in validation_results:
            scores.append(validation_results['demographic_analysis'].get('demographic_validity_score', 0.5))
        
        if 'clinical_validity' in validation_results:
            scores.append(validation_results['clinical_validity'].get('clinical_consistency_score', 0.5))
        
        if 'distribution_analysis' in validation_results:
            scores.append(validation_results['distribution_analysis'].get('distribution_quality_score', 0.5))
        
        if 'literature_consistency' in validation_results:
            scores.append(validation_results['literature_consistency'].get('consistency_score', 0.5))
        
        if 'medical_plausibility' in validation_results:
            scores.append(validation_results['medical_plausibility'].get('plausibility_score', 0.5))
        
        return np.mean(scores) if scores else 0.5
    
    def _generate_recommendations(self, validation_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        overall_score = validation_results.get('overall_quality_score', 0.5)
        
        if overall_score < 0.6:
            recommendations.append("Overall data quality is below acceptable threshold. Consider regenerating cohort with adjusted parameters.")
        
        # Demographic recommendations
        demo_analysis = validation_results.get('demographic_analysis', {})
        if demo_analysis.get('demographic_validity_score', 0.5) < 0.7:
            recommendations.append("Improve demographic distribution balance, particularly age and gender representation.")
        
        # Clinical recommendations
        clinical_analysis = validation_results.get('clinical_validity', {})
        if clinical_analysis.get('clinical_consistency_score', 0.5) < 0.7:
            recommendations.append("Review clinical data consistency, particularly lab values and medication appropriateness.")
        
        # Distribution recommendations
        dist_analysis = validation_results.get('distribution_analysis', {})
        if dist_analysis.get('distribution_quality_score', 0.5) < 0.7:
            recommendations.append("Adjust statistical distributions to better match expected medical patterns.")
        
        # Medical plausibility recommendations
        med_analysis = validation_results.get('medical_plausibility', {})
        if med_analysis.get('plausibility_score', 0.5) < 0.7:
            recommendations.append("Improve medical plausibility by better aligning conditions, medications, and lab values.")
        
        return recommendations
    
    def _create_statistical_summary(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Create comprehensive statistical summary"""
        if not cohort.patients:
            return {}
        
        summary = {
            'cohort_size': len(cohort.patients),
            'data_completeness': {},
            'key_statistics': {},
            'data_quality_metrics': {}
        }
        
        # Data completeness
        total_patients = len(cohort.patients)
        summary['data_completeness'] = {
            'age_completeness': sum(1 for p in cohort.patients if p.age is not None) / total_patients,
            'gender_completeness': sum(1 for p in cohort.patients if p.gender) / total_patients,
            'ethnicity_completeness': sum(1 for p in cohort.patients if p.ethnicity) / total_patients,
            'conditions_completeness': sum(1 for p in cohort.patients if p.conditions) / total_patients,
            'medications_completeness': sum(1 for p in cohort.patients if p.medications) / total_patients,
            'lab_results_completeness': sum(1 for p in cohort.patients if p.lab_results) / total_patients
        }
        
        # Key statistics
        ages = [p.age for p in cohort.patients if p.age is not None]
        if ages:
            summary['key_statistics']['age'] = {
                'mean': np.mean(ages),
                'median': np.median(ages),
                'std': np.std(ages),
                'range': [np.min(ages), np.max(ages)]
            }
        
        # Condition statistics
        all_conditions = []
        for patient in cohort.patients:
            all_conditions.extend(patient.conditions)
        
        if all_conditions:
            condition_counts = pd.Series(all_conditions).value_counts()
            summary['key_statistics']['top_conditions'] = dict(condition_counts.head(10))
            summary['key_statistics']['total_unique_conditions'] = len(condition_counts)
            summary['key_statistics']['avg_conditions_per_patient'] = len(all_conditions) / total_patients
        
        return summary
    
    # Helper methods for specific analyses
    def _categorize_ages(self, ages: List[int]) -> Dict[str, int]:
        """Categorize ages into standard groups"""
        categories = {
            'pediatric (<18)': sum(1 for age in ages if age < 18),
            'young_adult (18-34)': sum(1 for age in ages if 18 <= age < 35),
            'middle_aged (35-64)': sum(1 for age in ages if 35 <= age < 65),
            'elderly (65+)': sum(1 for age in ages if age >= 65)
        }
        return categories
    
    def _calculate_gender_balance_score(self, gender_counts: pd.Series) -> float:
        """Calculate gender balance score (higher is more balanced)"""
        if len(gender_counts) < 2:
            return 0.0
        
        total = gender_counts.sum()
        proportions = gender_counts / total
        
        # Calculate entropy-based balance score
        entropy = -sum(p * np.log2(p) for p in proportions if p > 0)
        max_entropy = np.log2(len(gender_counts))
        
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    def _perform_gender_chi_square(self, gender_counts: pd.Series) -> Dict[str, float]:
        """Perform chi-square test for gender distribution"""
        if len(gender_counts) < 2:
            return {'statistic': 0.0, 'p_value': 1.0}
        
        expected = [gender_counts.sum() / len(gender_counts)] * len(gender_counts)
        chi2_stat, p_value = stats.chisquare(gender_counts.values, expected)
        
        return {'statistic': chi2_stat, 'p_value': p_value}
    
    def _calculate_diversity_index(self, counts: pd.Series) -> float:
        """Calculate Shannon diversity index"""
        total = counts.sum()
        proportions = counts / total
        
        shannon_index = -sum(p * np.log(p) for p in proportions if p > 0)
        return shannon_index
    
    def _identify_ethnicity_gaps(self, ethnicity_counts: pd.Series) -> List[str]:
        """Identify potential gaps in ethnicity representation"""
        gaps = []
        total = ethnicity_counts.sum()
        
        # Expected major ethnic groups
        expected_groups = ['White', 'Black or African American', 'Asian', 'Hispanic or Latino']
        
        for group in expected_groups:
            if group not in ethnicity_counts.index:
                gaps.append(f"Missing representation: {group}")
            elif ethnicity_counts[group] / total < 0.05:
                gaps.append(f"Underrepresented: {group} ({ethnicity_counts[group]/total:.1%})")
        
        return gaps
    
    def _calculate_demographic_validity_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall demographic validity score"""
        scores = []
        
        # Age distribution score
        if 'age_analysis' in analysis and analysis['age_analysis']:
            age_stats = analysis['age_analysis']
            # Check if age distribution is reasonable
            if 20 <= age_stats.get('mean', 0) <= 80 and 10 <= age_stats.get('std', 0) <= 30:
                scores.append(0.8)
            else:
                scores.append(0.4)
        
        # Gender balance score
        if 'gender_analysis' in analysis and analysis['gender_analysis']:
            balance_score = analysis['gender_analysis'].get('balance_score', 0.5)
            scores.append(balance_score)
        
        # Ethnicity diversity score
        if 'ethnicity_analysis' in analysis and analysis['ethnicity_analysis']:
            diversity_index = analysis['ethnicity_analysis'].get('diversity_index', 0)
            # Normalize diversity index to 0-1 scale
            normalized_diversity = min(diversity_index / 2.0, 1.0)
            scores.append(normalized_diversity)
        
        return np.mean(scores) if scores else 0.5
    
    def _assess_lab_plausibility(self, lab_name: str, values: List[float]) -> float:
        """Assess clinical plausibility of lab values"""
        if lab_name not in self.medical_references:
            return 0.5
        
        ref = self.medical_references[lab_name]
        
        # Check percentage within normal range
        within_normal = sum(1 for v in values if ref['min'] <= v <= ref['max']) / len(values)
        
        # Check for extreme outliers
        extreme_outliers = sum(1 for v in values if v < ref['min'] * 0.5 or v > ref['max'] * 2) / len(values)
        
        # Calculate plausibility score
        plausibility = within_normal * 0.7 + (1 - extreme_outliers) * 0.3
        
        return plausibility
    
    def _analyze_medication_patterns(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Analyze medication prescription patterns"""
        medication_analysis = {
            'condition_medication_matches': 0,
            'total_condition_instances': 0,
            'appropriateness_score': 0.0,
            'common_medications': {},
            'polypharmacy_analysis': {}
        }
        
        # Expected medications for conditions
        condition_medications = {
            'Hypertension': ['Lisinopril', 'Amlodipine', 'Metoprolol', 'Losartan', 'Hydrochlorothiazide'],
            'Diabetes Mellitus Type 2': ['Metformin', 'Insulin', 'Glipizide', 'Sitagliptin'],
            'Hyperlipidemia': ['Atorvastatin', 'Simvastatin', 'Rosuvastatin'],
            'Depression': ['Sertraline', 'Escitalopram', 'Fluoxetine', 'Venlafaxine'],
            'COPD': ['Albuterol', 'Tiotropium', 'Budesonide', 'Prednisone'],
            'Coronary Artery Disease': ['Aspirin', 'Clopidogrel', 'Atorvastatin', 'Metoprolol']
        }
        
        matches = 0
        total_instances = 0
        
        for patient in cohort.patients:
            for condition in patient.conditions:
                if condition in condition_medications:
                    total_instances += 1
                    expected_meds = condition_medications[condition]
                    if any(med in patient.medications for med in expected_meds):
                        matches += 1
        
        medication_analysis['condition_medication_matches'] = matches
        medication_analysis['total_condition_instances'] = total_instances
        medication_analysis['appropriateness_score'] = matches / total_instances if total_instances > 0 else 0.0
        
        # Analyze polypharmacy (multiple medications)
        med_counts = [len(p.medications) for p in cohort.patients]
        polypharmacy_count = sum(1 for count in med_counts if count >= 5)
        
        medication_analysis['polypharmacy_analysis'] = {
            'patients_with_polypharmacy': polypharmacy_count,
            'polypharmacy_rate': polypharmacy_count / len(cohort.patients),
            'avg_medications_per_patient': np.mean(med_counts) if med_counts else 0,
            'max_medications': max(med_counts) if med_counts else 0
        }
        
        return medication_analysis
    
    def _analyze_comorbidity_patterns(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Analyze patterns of comorbid conditions"""
        comorbidity_analysis = {
            'common_combinations': {},
            'comorbidity_rates': {},
            'medical_plausibility': {}
        }
        
        # Known medical comorbidity patterns
        known_comorbidities = {
            'Diabetes Mellitus Type 2': ['Hypertension', 'Hyperlipidemia', 'Coronary Artery Disease'],
            'Hypertension': ['Diabetes Mellitus Type 2', 'Hyperlipidemia', 'Coronary Artery Disease'],
            'COPD': ['Coronary Artery Disease', 'Depression', 'Osteoporosis'],
            'Depression': ['Anxiety', 'Chronic Pain', 'Diabetes Mellitus Type 2']
        }
        
        # Analyze actual comorbidity patterns in cohort
        for primary_condition, expected_comorbidities in known_comorbidities.items():
            patients_with_primary = [p for p in cohort.patients if primary_condition in p.conditions]
            
            if patients_with_primary:
                comorbidity_rates = {}
                for comorbidity in expected_comorbidities:
                    count = sum(1 for p in patients_with_primary if comorbidity in p.conditions)
                    rate = count / len(patients_with_primary)
                    comorbidity_rates[comorbidity] = rate
                
                comorbidity_analysis['comorbidity_rates'][primary_condition] = comorbidity_rates
        
        return comorbidity_analysis
    
    def _calculate_clinical_consistency_score(self, validity_analysis: Dict[str, Any]) -> float:
        """Calculate overall clinical consistency score"""
        scores = []
        
        # Lab value validity score
        lab_validity = validity_analysis.get('lab_value_validity', {})
        if lab_validity:
            lab_scores = []
            for lab_name, stats in lab_validity.items():
                within_range = stats.get('within_normal_range', 0.5)
                plausibility = stats.get('clinical_plausibility', 0.5)
                lab_scores.append((within_range + plausibility) / 2)
            
            if lab_scores:
                scores.append(np.mean(lab_scores))
        
        # Medication appropriateness score
        med_analysis = validity_analysis.get('medication_appropriateness', {})
        if med_analysis:
            appropriateness = med_analysis.get('appropriateness_score', 0.5)
            scores.append(appropriateness)
        
        return np.mean(scores) if scores else 0.5
    
    def _analyze_single_distribution(self, values: List[float], variable_name: str) -> Dict[str, Any]:
        """Analyze statistical distribution of a single variable"""
        if len(values) < 5:
            return {'error': 'Insufficient data for distribution analysis'}
        
        values_array = np.array(values)
        
        distribution_stats = {
            'mean': np.mean(values_array),
            'median': np.median(values_array),
            'std': np.std(values_array),
            'variance': np.var(values_array),
            'skewness': stats.skew(values_array),
            'kurtosis': stats.kurtosis(values_array),
            'min': np.min(values_array),
            'max': np.max(values_array),
            'range': np.max(values_array) - np.min(values_array),
            'q25': np.percentile(values_array, 25),
            'q75': np.percentile(values_array, 75),
            'iqr': np.percentile(values_array, 75) - np.percentile(values_array, 25)
        }
        
        # Test for normality
        if len(values) < 5000:
            normality_stat, normality_p = stats.shapiro(values_array)
        else:
            normality_stat, normality_p = stats.kstest(values_array, 'norm')
        
        distribution_stats['normality_test'] = {
            'statistic': normality_stat,
            'p_value': normality_p,
            'is_normal': normality_p > 0.05
        }
        
        # Compare to expected medical distribution if available
        if variable_name in self.medical_references:
            ref = self.medical_references[variable_name]
            distribution_stats['medical_comparison'] = {
                'expected_mean': ref['mean'],
                'expected_std': ref['std'],
                'mean_difference': abs(distribution_stats['mean'] - ref['mean']),
                'std_difference': abs(distribution_stats['std'] - ref['std']),
                'within_expected_range': ref['min'] <= distribution_stats['mean'] <= ref['max']
            }
        
        return distribution_stats
    
    def _analyze_disease_prevalence(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Analyze disease prevalence compared to population norms"""
        total_patients = len(cohort.patients)
        if total_patients == 0:
            return {'error': 'No patients in cohort'}
        
        prevalence_analysis = {}
        
        # Count conditions
        condition_counts = {}
        for patient in cohort.patients:
            for condition in patient.conditions:
                condition_counts[condition] = condition_counts.get(condition, 0) + 1
        
        # Compare to expected prevalence
        for condition, count in condition_counts.items():
            observed_prevalence = count / total_patients
            
            analysis = {
                'observed_count': count,
                'observed_prevalence': observed_prevalence,
                'expected_prevalence': self.disease_prevalence.get(condition, 0.1),
                'prevalence_ratio': None,
                'assessment': 'unknown'
            }
            
            if condition in self.disease_prevalence:
                expected = self.disease_prevalence[condition]
                analysis['prevalence_ratio'] = observed_prevalence / expected
                
                if 0.5 <= analysis['prevalence_ratio'] <= 2.0:
                    analysis['assessment'] = 'appropriate'
                elif analysis['prevalence_ratio'] < 0.5:
                    analysis['assessment'] = 'underrepresented'
                else:
                    analysis['assessment'] = 'overrepresented'
            
            prevalence_analysis[condition] = analysis
        
        return prevalence_analysis
    
    def _calculate_distribution_quality_score(self, distribution_analysis: Dict[str, Any]) -> float:
        """Calculate overall distribution quality score"""
        scores = []
        
        # Age distribution quality
        age_dist = distribution_analysis.get('age_distribution', {})
        if age_dist and 'medical_comparison' in age_dist:
            med_comp = age_dist['medical_comparison']
            if med_comp['within_expected_range'] and med_comp['mean_difference'] < 10:
                scores.append(0.8)
            else:
                scores.append(0.4)
        
        # Lab distribution quality
        lab_dists = distribution_analysis.get('lab_distributions', {})
        if lab_dists:
            lab_scores = []
            for lab_name, lab_dist in lab_dists.items():
                if 'medical_comparison' in lab_dist:
                    med_comp = lab_dist['medical_comparison']
                    if med_comp['within_expected_range']:
                        lab_scores.append(0.8)
                    else:
                        lab_scores.append(0.4)
            
            if lab_scores:
                scores.append(np.mean(lab_scores))
        
        # Disease prevalence quality
        disease_analysis = distribution_analysis.get('disease_prevalence_analysis', {})
        if disease_analysis:
            appropriate_count = sum(1 for analysis in disease_analysis.values() 
                                  if analysis.get('assessment') == 'appropriate')
            total_diseases = len(disease_analysis)
            if total_diseases > 0:
                scores.append(appropriate_count / total_diseases)
        
        return np.mean(scores) if scores else 0.5
    
    def _find_significant_correlations(self, correlation_matrix: pd.DataFrame, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Find statistically significant correlations"""
        significant_correlations = []
        
        for i in range(len(correlation_matrix.columns)):
            for j in range(i + 1, len(correlation_matrix.columns)):
                var1 = correlation_matrix.columns[i]
                var2 = correlation_matrix.columns[j]
                correlation = correlation_matrix.iloc[i, j]
                
                if abs(correlation) >= threshold and not np.isnan(correlation):
                    significant_correlations.append({
                        'variable1': var1,
                        'variable2': var2,
                        'correlation': correlation,
                        'strength': 'strong' if abs(correlation) >= 0.7 else 'moderate',
                        'direction': 'positive' if correlation > 0 else 'negative'
                    })
        
        return sorted(significant_correlations, key=lambda x: abs(x['correlation']), reverse=True)
    
    def _validate_medical_correlations(self, correlation_matrix: pd.DataFrame) -> Dict[str, Any]:
        """Validate medically expected correlations"""
        expected_correlations = {
            ('age', 'blood_pressure_systolic'): 'positive',
            ('glucose', 'hemoglobin'): 'negative',
            ('cholesterol', 'blood_pressure_systolic'): 'positive',
            ('age', 'condition_count'): 'positive'
        }
        
        validation_results = {}
        
        for (var1, var2), expected_direction in expected_correlations.items():
            if var1 in correlation_matrix.columns and var2 in correlation_matrix.columns:
                observed_corr = correlation_matrix.loc[var1, var2]
                
                if not np.isnan(observed_corr):
                    observed_direction = 'positive' if observed_corr > 0 else 'negative'
                    
                    validation_results[f"{var1}_vs_{var2}"] = {
                        'expected_direction': expected_direction,
                        'observed_direction': observed_direction,
                        'observed_correlation': observed_corr,
                        'matches_expectation': expected_direction == observed_direction,
                        'strength': abs(observed_corr)
                    }
        
        return validation_results
    
    def _generate_correlation_insights(self, correlation_matrix: pd.DataFrame) -> List[str]:
        """Generate insights from correlation analysis"""
        insights = []
        
        # Find strongest correlations
        strong_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i + 1, len(correlation_matrix.columns)):
                corr = correlation_matrix.iloc[i, j]
                if abs(corr) >= 0.7 and not np.isnan(corr):
                    var1 = correlation_matrix.columns[i]
                    var2 = correlation_matrix.columns[j]
                    strong_correlations.append((var1, var2, corr))
        
        if strong_correlations:
            insights.append(f"Found {len(strong_correlations)} strong correlations (|r| >= 0.7)")
            
            for var1, var2, corr in strong_correlations[:3]:  # Top 3
                direction = "positively" if corr > 0 else "negatively"
                insights.append(f"{var1} and {var2} are strongly {direction} correlated (r = {corr:.3f})")
        
        return insights
    
    def _prepare_numeric_data_for_outlier_detection(self, cohort: PatientCohort) -> pd.DataFrame:
        """Prepare numeric data for outlier detection"""
        data_rows = []
        
        for patient in cohort.patients:
            row = {'patient_id': patient.patient_id}
            
            if patient.age is not None:
                row['age'] = patient.age
            
            # Add lab results
            for lab_name, (value, unit) in patient.lab_results.items():
                row[lab_name] = value
            
            # Add counts
            row['condition_count'] = len(patient.conditions)
            row['medication_count'] = len(patient.medications)
            
            data_rows.append(row)
        
        df = pd.DataFrame(data_rows)
        
        # Select only numeric columns (excluding patient_id)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        return df[numeric_cols]
    
    def _detect_isolation_forest_outliers(self, numeric_data: pd.DataFrame, cohort: PatientCohort) -> List[Dict[str, Any]]:
        """Detect multivariate outliers using Isolation Forest"""
        if len(numeric_data) < 10:
            return []
        
        # Standardize data
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_data)
        
        # Apply Isolation Forest
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        outlier_labels = iso_forest.fit_predict(scaled_data)
        
        outliers = []
        for i, is_outlier in enumerate(outlier_labels):
            if is_outlier == -1:  # -1 indicates outlier
                patient = cohort.patients[i]
                outlier_score = iso_forest.score_samples([scaled_data[i]])[0]
                
                outliers.append({
                    'patient_id': patient.patient_id,
                    'outlier_score': outlier_score,
                    'features': dict(zip(numeric_data.columns, numeric_data.iloc[i]))
                })
        
        return sorted(outliers, key=lambda x: x['outlier_score'])
    
    def _summarize_outliers(self, outlier_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize outlier detection results"""
        summary = {
            'total_statistical_outliers': len(outlier_analysis.get('statistical_outliers', {})),
            'total_isolation_outliers': len(outlier_analysis.get('isolation_forest_outliers', [])),
            'most_common_outlier_types': {},
            'outlier_percentage': 0.0
        }
        
        # Count outlier types
        outlier_types = {}
        for patient_outliers in outlier_analysis.get('statistical_outliers', {}).values():
            for feature, outlier_info in patient_outliers.items():
                outlier_type = outlier_info.get('type', 'unknown')
                outlier_types[outlier_type] = outlier_types.get(outlier_type, 0) + 1
        
        summary['most_common_outlier_types'] = outlier_types
        
        return summary
    
    def _prepare_clustering_data(self, cohort: PatientCohort) -> pd.DataFrame:
        """Prepare data for clustering analysis"""
        data_rows = []
        
        for patient in cohort.patients:
            row = {}
            
            # Demographics
            if patient.age is not None:
                row['age'] = patient.age
            
            # Lab results
            for lab_name, (value, unit) in patient.lab_results.items():
                row[lab_name] = value
            
            # Condition and medication counts
            row['condition_count'] = len(patient.conditions)
            row['medication_count'] = len(patient.medications)
            
            # Binary indicators for common conditions
            common_conditions = ['Hypertension', 'Diabetes Mellitus Type 2', 'Hyperlipidemia', 
                               'Depression', 'COPD', 'Coronary Artery Disease']
            for condition in common_conditions:
                row[f'has_{condition.lower().replace(" ", "_")}'] = int(condition in patient.conditions)
            
            data_rows.append(row)
        
        df = pd.DataFrame(data_rows)
        
        # Fill missing values with median for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col].fillna(df[col].median(), inplace=True)
        
        return df
    
    def _find_optimal_clusters(self, data: np.ndarray, max_clusters: int = 10) -> int:
        """Find optimal number of clusters using elbow method"""
        if len(data) < 10:
            return 2
        
        max_clusters = min(max_clusters, len(data) // 2)
        inertias = []
        
        for k in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(data)
            inertias.append(kmeans.inertia_)
        
        # Find elbow using second derivative
        if len(inertias) >= 3:
            diffs = np.diff(inertias)
            second_diffs = np.diff(diffs)
            optimal_k = np.argmax(second_diffs) + 2  # +2 because we started from k=2
        else:
            optimal_k = 3  # Default
        
        return min(optimal_k, max_clusters)
    
    def _analyze_clusters(self, cohort: PatientCohort, cluster_labels: np.ndarray, feature_names: List[str]) -> Dict[str, Any]:
        """Analyze characteristics of each cluster"""
        cluster_analysis = {}
        unique_clusters = np.unique(cluster_labels)
        
        for cluster_id in unique_clusters:
            cluster_patients = [cohort.patients[i] for i, label in enumerate(cluster_labels) if label == cluster_id]
            
            # Basic statistics
            cluster_size = len(cluster_patients)
            ages = [p.age for p in cluster_patients if p.age is not None]
            
            cluster_info = {
                'size': cluster_size,
                'percentage': cluster_size / len(cohort.patients),
                'age_stats': {
                    'mean': np.mean(ages) if ages else None,
                    'std': np.std(ages) if ages else None,
                    'range': [np.min(ages), np.max(ages)] if ages else None
                },
                'common_conditions': {},
                'common_medications': {}
            }
            
            # Most common conditions in cluster
            all_conditions = []
            for patient in cluster_patients:
                all_conditions.extend(patient.conditions)
            
            if all_conditions:
                condition_counts = pd.Series(all_conditions).value_counts()
                cluster_info['common_conditions'] = dict(condition_counts.head(5))
            
            # Most common medications in cluster
            all_medications = []
            for patient in cluster_patients:
                all_medications.extend(patient.medications)
            
            if all_medications:
                medication_counts = pd.Series(all_medications).value_counts()
                cluster_info['common_medications'] = dict(medication_counts.head(5))
            
            cluster_analysis[f'cluster_{cluster_id}'] = cluster_info
        
        return cluster_analysis
    
    def _extract_literature_characteristics(self, literature: LiteratureResult) -> Dict[str, Any]:
        """Extract population characteristics from literature using LLM"""
        if not literature.papers:
            return {}
        
        # Combine abstracts from top papers
        abstracts_text = ""
        for paper in literature.papers[:5]:  # Use top 5 papers
            abstracts_text += f"Paper: {paper.title}\nAbstract: {paper.abstract}\n\n"
        
        prompt = f"""
        Extract population characteristics from these medical research papers:

        {abstracts_text}

        Extract and format as key-value pairs:
        - Sample sizes mentioned
        - Age ranges and demographics
        - Gender distributions
        - Disease prevalence rates
        - Common comorbidities
        - Treatment patterns

        Focus on quantitative data that can be compared to synthetic patient cohorts.
        """
        
        try:
            response = self.ollama_client.generate_text(prompt)
            # Parse response into structured data (simplified)
            return {'llm_extracted_characteristics': response}
        except Exception as e:
            print(f"Error extracting literature characteristics: {e}")
            return {}
    
    def _compare_population_characteristics(self, cohort: PatientCohort, literature_chars: Dict[str, Any]) -> Dict[str, Any]:
        """Compare cohort population characteristics to literature"""
        # This is a simplified implementation
        # In practice, you'd parse the LLM response and do detailed comparisons
        
        cohort_stats = {
            'sample_size': len(cohort.patients),
            'avg_age': np.mean([p.age for p in cohort.patients if p.age is not None]),
            'gender_distribution': {}
        }
        
        genders = [p.gender for p in cohort.patients if p.gender]
        if genders:
            gender_counts = pd.Series(genders).value_counts()
            cohort_stats['gender_distribution'] = dict(gender_counts / len(genders))
        
        return {
            'cohort_characteristics': cohort_stats,
            'literature_characteristics': literature_chars,
            'comparison_score': 0.7  # Placeholder - would implement detailed comparison
        }
    
    def _compare_disease_prevalence(self, cohort: PatientCohort, literature_chars: Dict[str, Any]) -> Dict[str, Any]:
        """Compare disease prevalence between cohort and literature"""
        # Extract disease prevalence from cohort
        total_patients = len(cohort.patients)
        condition_counts = {}
        
        for patient in cohort.patients:
            for condition in patient.conditions:
                condition_counts[condition] = condition_counts.get(condition, 0) + 1
        
        cohort_prevalence = {condition: count/total_patients 
                           for condition, count in condition_counts.items()}
        
        return {
            'cohort_prevalence': cohort_prevalence,
            'literature_mentions': literature_chars.get('disease_prevalence', {}),
            'prevalence_comparison_score': 0.6  # Placeholder
        }
    
    def _compare_demographics(self, cohort: PatientCohort, literature_chars: Dict[str, Any]) -> Dict[str, Any]:
        """Compare demographic characteristics"""
        ages = [p.age for p in cohort.patients if p.age is not None]
        genders = [p.gender for p in cohort.patients if p.gender]
        
        cohort_demographics = {
            'age_mean': np.mean(ages) if ages else None,
            'age_std': np.std(ages) if ages else None,
            'gender_distribution': dict(pd.Series(genders).value_counts() / len(genders)) if genders else {}
        }
        
        return {
            'cohort_demographics': cohort_demographics,
            'literature_demographics': literature_chars.get('demographics', {}),
            'demographic_alignment_score': 0.75  # Placeholder
        }
    
    def _calculate_literature_consistency_score(self, consistency_analysis: Dict[str, Any]) -> float:
        """Calculate overall literature consistency score"""
        scores = []
        
        population_match = consistency_analysis.get('population_match', {})
        if 'comparison_score' in population_match:
            scores.append(population_match['comparison_score'])
        
        prevalence_match = consistency_analysis.get('prevalence_match', {})
        if 'prevalence_comparison_score' in prevalence_match:
            scores.append(prevalence_match['prevalence_comparison_score'])
        
        demographic_match = consistency_analysis.get('demographic_match', {})
        if 'demographic_alignment_score' in demographic_match:
            scores.append(demographic_match['demographic_alignment_score'])
        
        return np.mean(scores) if scores else 0.5
    
    def _assess_condition_medication_alignment(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Assess alignment between conditions and medications"""
        # Medical condition-medication mappings based on clinical guidelines
        condition_medications = {
            'Hypertension': ['Lisinopril', 'Amlodipine', 'Metoprolol', 'Losartan', 'Hydrochlorothiazide'],
            'Diabetes Mellitus Type 2': ['Metformin', 'Insulin', 'Glipizide', 'Sitagliptin', 'Glargine'],
            'Hyperlipidemia': ['Atorvastatin', 'Simvastatin', 'Rosuvastatin', 'Pravastatin'],
            'Depression': ['Sertraline', 'Escitalopram', 'Fluoxetine', 'Venlafaxine', 'Bupropion'],
            'COPD': ['Albuterol', 'Tiotropium', 'Budesonide', 'Prednisone', 'Formoterol'],
            'Coronary Artery Disease': ['Aspirin', 'Clopidogrel', 'Atorvastatin', 'Metoprolol', 'Nitroglycerin'],
            'Anxiety': ['Sertraline', 'Escitalopram', 'Lorazepam', 'Alprazolam', 'Buspirone']
        }
        
        alignment_results = {}
        total_matches = 0
        total_conditions = 0
        
        for condition, expected_meds in condition_medications.items():
            patients_with_condition = [p for p in cohort.patients if condition in p.conditions]
            
            if patients_with_condition:
                condition_analysis = {
                    'patient_count': len(patients_with_condition),
                    'patients_with_appropriate_medication': 0,
                    'common_medications_prescribed': {},
                    'alignment_score': 0.0
                }
                
                matches = 0
                all_meds_for_condition = []
                
                for patient in patients_with_condition:
                    patient_meds = patient.medications
                    all_meds_for_condition.extend(patient_meds)
                    
                    # Check if patient has at least one appropriate medication
                    if any(med in expected_meds for med in patient_meds):
                        matches += 1
                
                condition_analysis['patients_with_appropriate_medication'] = matches
                condition_analysis['alignment_score'] = matches / len(patients_with_condition)
                
                # Count medication frequencies
                if all_meds_for_condition:
                    med_counts = pd.Series(all_meds_for_condition).value_counts()
                    condition_analysis['common_medications_prescribed'] = dict(med_counts.head(5))
                
                alignment_results[condition] = condition_analysis
                total_matches += matches
                total_conditions += len(patients_with_condition)
        
        overall_alignment = total_matches / total_conditions if total_conditions > 0 else 0.0
        
        return {
            'condition_specific_alignment': alignment_results,
            'overall_alignment_score': overall_alignment,
            'total_condition_instances': total_conditions,
            'total_appropriate_prescriptions': total_matches
        }
    
    def _assess_age_condition_appropriateness(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Assess if conditions are age-appropriate"""
        age_condition_patterns = {
            'pediatric': {
                'common': ['Asthma', 'ADHD', 'Autism Spectrum Disorder'],
                'rare': ['Coronary Artery Disease', 'Osteoarthritis', 'Alzheimer Disease']
            },
            'young_adult': {
                'common': ['Depression', 'Anxiety', 'Asthma'],
                'rare': ['Coronary Artery Disease', 'Osteoarthritis', 'Dementia']
            },
            'middle_aged': {
                'common': ['Hypertension', 'Diabetes Mellitus Type 2', 'Hyperlipidemia'],
                'rare': ['ADHD', 'Childhood conditions']
            },
            'elderly': {
                'common': ['Hypertension', 'Diabetes Mellitus Type 2', 'Coronary Artery Disease', 
                          'Osteoarthritis', 'COPD'],
                'rare': ['ADHD', 'Autism Spectrum Disorder']
            }
        }
        
        appropriateness_results = {}
        
        for patient in cohort.patients:
            if patient.age is None:
                continue
                
            age_group = self._get_age_group(patient.age)
            patient_analysis = {
                'age': patient.age,
                'age_group': age_group,
                'conditions': patient.conditions,
                'appropriate_conditions': [],
                'questionable_conditions': [],
                'appropriateness_score': 0.0
            }
            
            if age_group in age_condition_patterns:
                patterns = age_condition_patterns[age_group]
                
                for condition in patient.conditions:
                    if condition in patterns.get('common', []):
                        patient_analysis['appropriate_conditions'].append(condition)
                    elif condition in patterns.get('rare', []):
                        patient_analysis['questionable_conditions'].append(condition)
                    else:
                        # Neutral - neither clearly appropriate nor inappropriate
                        patient_analysis['appropriate_conditions'].append(condition)
                
                total_conditions = len(patient.conditions)
                appropriate_count = len(patient_analysis['appropriate_conditions'])
                patient_analysis['appropriateness_score'] = appropriate_count / total_conditions if total_conditions > 0 else 1.0
            
            appropriateness_results[patient.patient_id] = patient_analysis
        
        # Calculate overall appropriateness
        scores = [analysis['appropriateness_score'] for analysis in appropriateness_results.values()]
        overall_score = np.mean(scores) if scores else 0.5
        
        return {
            'patient_specific_analysis': appropriateness_results,
            'overall_appropriateness_score': overall_score,
            'age_group_summary': self._summarize_age_condition_patterns(appropriateness_results)
        }
    
    def _assess_lab_condition_consistency(self, cohort: PatientCohort) -> Dict[str, Any]:
        """Assess consistency between lab values and conditions"""
        lab_condition_expectations = {
            'Diabetes Mellitus Type 2': {
                'glucose': {'expected_range': (126, 300), 'direction': 'high'},
                'hemoglobin': {'expected_range': (10, 16), 'direction': 'normal_to_low'}
            },
            'Hypertension': {
                'blood_pressure_systolic': {'expected_range': (140, 200), 'direction': 'high'},
                'blood_pressure_diastolic': {'expected_range': (90, 120), 'direction': 'high'}
            },
            'Hyperlipidemia': {
                'cholesterol': {'expected_range': (200, 400), 'direction': 'high'}
            },
            'Chronic Kidney Disease': {
                'creatinine': {'expected_range': (1.5, 5.0), 'direction': 'high'}
            }
        }
        
        consistency_results = {}
        total_consistent = 0
        total_lab_condition_pairs = 0
        
        for patient in cohort.patients:
            patient_consistency = {}
            
            for condition in patient.conditions:
                if condition in lab_condition_expectations:
                    expected_labs = lab_condition_expectations[condition]
                    
                    for lab_name, expectations in expected_labs.items():
                        if lab_name in patient.lab_results:
                            lab_value, unit = patient.lab_results[lab_name]
                            expected_range = expectations['expected_range']
                            
                            is_consistent = expected_range[0] <= lab_value <= expected_range[1]
                            
                            patient_consistency[f"{condition}_{lab_name}"] = {
                                'lab_value': lab_value,
                                'expected_range': expected_range,
                                'is_consistent': is_consistent,
                                'expectation': expectations['direction']
                            }
                            
                            total_lab_condition_pairs += 1
                            if is_consistent:
                                total_consistent += 1
            
            if patient_consistency:
                consistency_results[patient.patient_id] = patient_consistency
        
        overall_consistency = total_consistent / total_lab_condition_pairs if total_lab_condition_pairs > 0 else 0.5
        
        return {
            'patient_specific_consistency': consistency_results,
            'overall_consistency_score': overall_consistency,
            'total_lab_condition_pairs': total_lab_condition_pairs,
            'consistent_pairs': total_consistent
        }
    
    def _identify_medical_logic_violations(self, cohort: PatientCohort) -> List[Dict[str, Any]]:
        """Use LLM to identify medical logic violations"""
        violations = []
        
        # Sample a few patients for detailed LLM analysis
        sample_patients = cohort.patients[:5] if len(cohort.patients) > 5 else cohort.patients
        
        for patient in sample_patients:
            # Create patient summary for LLM
            patient_summary = f"""
            Patient ID: {patient.patient_id}
            Age: {patient.age}
            Gender: {patient.gender}
            Conditions: {', '.join(patient.conditions)}
            Medications: {', '.join(patient.medications)}
            Lab Results: {', '.join([f"{lab}: {value} {unit}" for lab, (value, unit) in patient.lab_results.items()])}
            """
            
            prompt = f"""
            Review this synthetic patient data for medical logic violations or implausible combinations:
            
            {patient_summary}
            
            Identify any issues such as:
            1. Inappropriate medications for age
            2. Conflicting medications
            3. Lab values inconsistent with conditions
            4. Missing expected treatments
            5. Implausible condition combinations
            
            Respond with specific violations found, or "No violations detected" if the patient data is medically plausible.
            """
            
            try:
                response = self.ollama_client.generate_text(prompt)
                
                if "No violations detected" not in response:
                    violations.append({
                        'patient_id': patient.patient_id,
                        'violations': response.strip(),
                        'severity': 'moderate'  # Could be enhanced to classify severity
                    })
                    
            except Exception as e:
                print(f"Error analyzing patient {patient.patient_id}: {e}")
        
        return violations
    
    def _calculate_medical_plausibility_score(self, plausibility_analysis: Dict[str, Any]) -> float:
        """Calculate overall medical plausibility score"""
        scores = []
        
        # Condition-medication alignment score
        alignment = plausibility_analysis.get('condition_medication_alignment', {})
        if 'overall_alignment_score' in alignment:
            scores.append(alignment['overall_alignment_score'])
        
        # Age-condition appropriateness score
        age_appropriateness = plausibility_analysis.get('age_condition_appropriateness', {})
        if 'overall_appropriateness_score' in age_appropriateness:
            scores.append(age_appropriateness['overall_appropriateness_score'])
        
        # Lab-condition consistency score
        lab_consistency = plausibility_analysis.get('lab_condition_consistency', {})
        if 'overall_consistency_score' in lab_consistency:
            scores.append(lab_consistency['overall_consistency_score'])
        
        # Medical logic violations penalty
        violations = plausibility_analysis.get('medical_logic_violations', [])
        violation_penalty = len(violations) * 0.1  # 10% penalty per violation
        
        base_score = np.mean(scores) if scores else 0.5
        final_score = max(0.0, base_score - violation_penalty)
        
        return final_score
    
    def _get_age_group(self, age: int) -> str:
        """Get age group for a given age"""
        if age < 18:
            return 'pediatric'
        elif 18 <= age < 35:
            return 'young_adult'
        elif 35 <= age < 65:
            return 'middle_aged'
        else:
            return 'elderly'
    
    def _summarize_age_condition_patterns(self, appropriateness_results: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize age-condition patterns across the cohort"""
        age_group_summary = {}
        
        for analysis in appropriateness_results.values():
            age_group = analysis['age_group']
            
            if age_group not in age_group_summary:
                age_group_summary[age_group] = {
                    'patient_count': 0,
                    'avg_appropriateness_score': 0.0,
                    'common_conditions': {},
                    'questionable_conditions': {}
                }
            
            summary = age_group_summary[age_group]
            summary['patient_count'] += 1
            summary['avg_appropriateness_score'] += analysis['appropriateness_score']
            
            # Count conditions
            for condition in analysis['appropriate_conditions']:
                summary['common_conditions'][condition] = summary['common_conditions'].get(condition, 0) + 1
            
            for condition in analysis['questionable_conditions']:
                summary['questionable_conditions'][condition] = summary['questionable_conditions'].get(condition, 0) + 1
        
        # Calculate averages
        for age_group, summary in age_group_summary.items():
            if summary['patient_count'] > 0:
                summary['avg_appropriateness_score'] /= summary['patient_count']
        
        return age_group_summary