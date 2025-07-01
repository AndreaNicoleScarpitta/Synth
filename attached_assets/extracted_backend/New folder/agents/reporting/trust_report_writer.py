from agents.reporting.base_agent import BaseReportingAgent
from typing import Dict, Any

class TrustNarrative(BaseReportingAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Aggregate QA, schema, bias, and provenance flags
        flags = input_data.get("flags", [])
        patient_score = input_data.get("scorecard", {}).get("score", None)
        status = "high" if patient_score and patient_score > 0.8 and not flags else "moderate" if patient_score and patient_score > 0.6 else "low"
        flag_descriptions = [f"{f.get('field', 'unknown')}: {f.get('issue', 'issue')}" for f in flags]

        narrative = (
            f"Trust in this dataset is assessed as {status.upper()}."
            f"{' No major issues detected.' if not flags else ' Issues flagged: ' + '; '.join(flag_descriptions)}"
        )
        output = {
            "trust_narrative": narrative,
            "status": status,
            "flag_count": len(flags),
            "score": patient_score
        }
        log = f"TrustNarrative: Status {status.upper()}, {len(flags)} flag(s)."
        return self.standard_response(output=output, log=log)
class TrustReportWriter(BaseReportingAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Aggregate scores and flags from multiple QA/reporting outputs
        trust_metrics = input_data.get("trust_metrics", {})
        narrative = input_data.get("trust_narrative", "")
        scorecard = input_data.get("scorecard", {})
        additional_flags = input_data.get("flags", [])

        output = {
            "trust_report": {
                "overall_score": trust_metrics.get("overall_score", scorecard.get("score")),
                "trust_narrative": narrative if narrative else "No narrative provided.",
                "flag_count": trust_metrics.get("flag_count", len(additional_flags)),
                "details": {
                    "trust_metrics": trust_metrics,
                    "scorecard": scorecard,
                    "flags": additional_flags,
                }
            }
        }
        log = (
            f"TrustReportWriter: Score {output['trust_report']['overall_score']}, "
            f"{output['trust_report']['flag_count']} flag(s)."
        )
        return self.standard_response(output=output, log=log)