from agents.reporting.base_agent import BaseReportingAgent
from typing import Dict, Any

class TrustScoreExplainer(BaseReportingAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Explains the computation of trust/confidence scores for the synthetic dataset.
        Draws on flags, QA scores, and any scoring rubric provided in input_data.
        """
        scorecard = input_data.get("scorecard", {})
        trust_metrics = input_data.get("trust_metrics", {})
        overall_score = trust_metrics.get("overall_score", scorecard.get("score", None))
        flag_count = trust_metrics.get("flag_count", len(input_data.get("flags", [])))
        rubric = input_data.get("trust_rubric", "QA results, label verification, bias audit, and schema validation.")

        # Generate a simple explanation
        if overall_score is not None:
            if overall_score > 0.85 and flag_count == 0:
                status = "excellent"
            elif overall_score > 0.7:
                status = "good"
            elif overall_score > 0.5:
                status = "moderate"
            else:
                status = "poor"
            explanation = (
                f"Trust score ({overall_score:.2f}) is considered {status.upper()} based on "
                f"the scoring rubric: {rubric}. Flag count: {flag_count}."
            )
        else:
            status = "unknown"
            explanation = (
                "No valid trust score found. Trust score is typically computed from cohort scorecard, QA results, "
                "and weighted penalties for major issues."
            )

        output = {
            "trust_score_explanation": {
                "status": status,
                "confidence_score": overall_score,
                "explanation": explanation,
                "generated_by": "TrustScoreExplainer"
            }
        }
        log = f"TrustScoreExplainer: Status={status.upper()}, Score={overall_score}, Flags={flag_count}"
        return self.standard_response(output=output, log=log)
