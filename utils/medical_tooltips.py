"""
Medical Research Tooltips System
Provides contextual help for medical terminology throughout Synthetic Ascension platform
"""

import streamlit as st
from typing import Dict, List, Optional
import json

class MedicalTooltipManager:
    """Manages medical terminology tooltips with definitions and context"""
    
    def __init__(self):
        self.medical_terms = {
            # Cardiology Terms
            "hemodynamics": {
                "definition": "The study of blood flow and the forces involved in circulation",
                "context": "Critical for understanding cardiovascular function and surgical timing",
                "category": "Cardiology"
            },
            "ejection_fraction": {
                "definition": "Percentage of blood pumped out of the left ventricle with each heartbeat",
                "context": "Normal range is 50-70%; lower values indicate heart failure",
                "category": "Cardiology"
            },
            "pulmonary_hypertension": {
                "definition": "High blood pressure in the arteries of the lungs",
                "context": "Often requires specialized treatment and monitoring",
                "category": "Cardiology"
            },
            "ventricular_septal_defect": {
                "definition": "A hole in the wall separating the heart's two lower chambers",
                "context": "Most common congenital heart defect in children",
                "category": "Pediatric Cardiology"
            },
            
            # Research Methodology
            "real_world_evidence": {
                "definition": "Clinical evidence from analysis of real-world data (RWD)",
                "context": "Increasingly important for regulatory decisions and market access",
                "category": "Research"
            },
            "synthetic_cohort": {
                "definition": "Artificially generated patient populations that maintain statistical properties of real data",
                "context": "Enables privacy-preserving research at scale",
                "category": "Data Science"
            },
            "bias_detection": {
                "definition": "Systematic identification of unfair or skewed representations in data",
                "context": "Essential for ensuring AI fairness across demographics",
                "category": "AI/ML"
            },
            "clinical_validation": {
                "definition": "Process of confirming that synthetic data accurately represents real clinical patterns",
                "context": "Critical for regulatory acceptance and scientific validity",
                "category": "Validation"
            },
            
            # Regulatory & Compliance
            "fhir_r4": {
                "definition": "Fast Healthcare Interoperability Resources Release 4 standard",
                "context": "International standard for exchanging healthcare information electronically",
                "category": "Standards"
            },
            "cfr_part_11": {
                "definition": "FDA regulation defining criteria for electronic records and signatures",
                "context": "Required for pharmaceutical and medical device submissions",
                "category": "Regulatory"
            },
            "gdpr": {
                "definition": "General Data Protection Regulation - EU privacy law",
                "context": "Applies to any organization processing EU citizen data",
                "category": "Privacy"
            },
            "hipaa": {
                "definition": "Health Insurance Portability and Accountability Act",
                "context": "US law protecting patient health information privacy",
                "category": "Privacy"
            },
            
            # Pharmaceutical Terms
            "pharmacovigilance": {
                "definition": "Science of monitoring drug safety and preventing adverse effects",
                "context": "Critical throughout drug lifecycle from development to post-market",
                "category": "Pharma"
            },
            "adverse_event": {
                "definition": "Unfavorable medical occurrence associated with use of a drug",
                "context": "Must be systematically collected and reported to regulators",
                "category": "Safety"
            },
            "clinical_trial": {
                "definition": "Research study testing medical treatments in human volunteers",
                "context": "Gold standard for evaluating safety and efficacy",
                "category": "Research"
            },
            
            # Data Science & AI
            "machine_learning": {
                "definition": "AI technique enabling computers to learn patterns from data",
                "context": "Powers predictive analytics and automated insights",
                "category": "AI/ML"
            },
            "natural_language_processing": {
                "definition": "AI technology for understanding and processing human language",
                "context": "Enables extraction of insights from clinical notes and literature",
                "category": "AI/ML"
            },
            "statistical_significance": {
                "definition": "Probability that observed results are not due to chance",
                "context": "Typically requires p-value < 0.05 for medical research",
                "category": "Statistics"
            }
        }
    
    def get_tooltip_css(self) -> str:
        """Generate CSS for tooltip styling"""
        return """
        <style>
        .medical-tooltip {
            position: relative;
            display: inline-block;
            color: #6B4EFF;
            font-weight: 600;
            cursor: help;
            border-bottom: 1px dotted #6B4EFF;
            text-decoration: none;
        }
        
        .medical-tooltip:hover {
            color: #0A1F44;
        }
        
        .tooltip-content {
            visibility: hidden;
            width: 320px;
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            color: #374151;
            text-align: left;
            border-radius: 12px;
            padding: 16px;
            position: absolute;
            z-index: 1000;
            bottom: 125%;
            left: 50%;
            margin-left: -160px;
            opacity: 0;
            transition: opacity 0.3s ease-in-out;
            box-shadow: 0 8px 24px rgba(10, 31, 68, 0.15);
            border: 2px solid #e2e8f0;
        }
        
        .tooltip-content::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #f8fafc transparent transparent transparent;
        }
        
        .medical-tooltip:hover .tooltip-content {
            visibility: visible;
            opacity: 1;
        }
        
        .tooltip-definition {
            font-weight: 600;
            margin-bottom: 8px;
            color: #0A1F44;
            font-size: 14px;
        }
        
        .tooltip-context {
            font-size: 13px;
            line-height: 1.4;
            color: #6b7280;
            margin-bottom: 8px;
        }
        
        .tooltip-category {
            font-size: 11px;
            background: #6B4EFF;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            display: inline-block;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }
        </style>
        """
    
    def create_tooltip(self, term: str, display_text: Optional[str] = None) -> str:
        """Create HTML for a medical term tooltip"""
        if term.lower().replace(' ', '_') not in self.medical_terms:
            return display_text or term
        
        term_key = term.lower().replace(' ', '_')
        term_data = self.medical_terms[term_key]
        display = display_text or term
        
        return f"""
        <span class="medical-tooltip">
            {display}
            <div class="tooltip-content">
                <div class="tooltip-definition">{term_data['definition']}</div>
                <div class="tooltip-context">{term_data['context']}</div>
                <div class="tooltip-category">{term_data['category']}</div>
            </div>
        </span>
        """
    
    def wrap_medical_terms(self, text: str, terms_to_wrap: Optional[List[str]] = None) -> str:
        """Automatically wrap medical terms in text with tooltips"""
        if terms_to_wrap is None:
            terms_to_wrap = list(self.medical_terms.keys())
        
        wrapped_text = text
        for term_key in terms_to_wrap:
            if term_key in self.medical_terms:
                # Convert underscore format back to display format
                display_term = term_key.replace('_', ' ').title()
                tooltip_html = self.create_tooltip(term_key, display_term)
                
                # Replace exact matches (case insensitive)
                import re
                pattern = re.compile(re.escape(display_term), re.IGNORECASE)
                wrapped_text = pattern.sub(tooltip_html, wrapped_text, count=1)
        
        return wrapped_text
    
    def get_all_categories(self) -> List[str]:
        """Get all medical term categories"""
        categories = set()
        for term_data in self.medical_terms.values():
            categories.add(term_data['category'])
        return sorted(list(categories))
    
    def get_terms_by_category(self, category: str) -> Dict[str, Dict]:
        """Get all terms in a specific category"""
        return {
            term: data for term, data in self.medical_terms.items()
            if data['category'] == category
        }
    
    def add_custom_term(self, term: str, definition: str, context: str, category: str):
        """Add a custom medical term to the tooltip system"""
        term_key = term.lower().replace(' ', '_')
        self.medical_terms[term_key] = {
            "definition": definition,
            "context": context,
            "category": category
        }
    
    def search_terms(self, query: str) -> Dict[str, Dict]:
        """Search for medical terms matching query"""
        query_lower = query.lower()
        results = {}
        
        for term_key, term_data in self.medical_terms.items():
            if (query_lower in term_key.lower() or 
                query_lower in term_data['definition'].lower() or
                query_lower in term_data['context'].lower()):
                results[term_key] = term_data
        
        return results

# Global tooltip manager instance
tooltip_manager = MedicalTooltipManager()

def initialize_tooltips():
    """Initialize tooltip CSS in Streamlit"""
    st.markdown(tooltip_manager.get_tooltip_css(), unsafe_allow_html=True)

def medical_tooltip(term: str, display_text: Optional[str] = None) -> str:
    """Convenience function to create a medical tooltip"""
    return tooltip_manager.create_tooltip(term, display_text)

def wrap_medical_text(text: str, terms: Optional[List[str]] = None) -> str:
    """Convenience function to wrap medical terms in text"""
    return tooltip_manager.wrap_medical_terms(text, terms)