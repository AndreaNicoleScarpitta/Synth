from .bias_auditor import BiasAuditor
from .label_verifier import LabelVerifier
from .outlier_detector import OutlierDetector
from .patient_scorecard import PatientScorecard
from .realism_checker import RealismChecker
from .schema_validator import SchemaValidator
from .statistical_validator import StatisticalValidator
from .fix_recommender import FixRecommender
from .qa_feedback_router import QAFeedbackRouter
from .qa_fhir_exporter import QAFHIRExporter
from .qa_langchain_probe import QALangchainProbe

class QAOrchestrator:
    def __init__(self):
        self.agents = {
            "bias_auditor": BiasAuditor(),
            "label_verifier": LabelVerifier(),
            "outlier_detector": OutlierDetector(),
            "realism_checker": RealismChecker(),
            "schema_validator": SchemaValidator(),
            "statistical_validator": StatisticalValidator(),
            "fix_recommender": FixRecommender(),
            "patient_scorecard": PatientScorecard(),
            "feedback_router": QAFeedbackRouter(),
            "fhir_exporter": QAFHIRExporter(),
            "langchain_probe": QALangchainProbe()
        }

    def run_all(self, input_data: dict) -> dict:
        results = {}
        for name, agent in self.agents.items():
            try:
                results[name] = agent.run(input_data)
            except Exception as e:
                results[name] = {
                    "error": str(e),
                    "log": f"{name} failed to execute"
                }

        return results
