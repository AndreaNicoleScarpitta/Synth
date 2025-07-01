from .base_agent import BaseQAAgent
from typing import Dict, Any, List
import logging
from datetime import datetime

class QAFeedbackRouter(BaseQAAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"[{self.agent_name}] Routing QA feedback to next agents...")

        issues: List[Dict[str, Any]] = input_data.get("qa_flags", []) + input_data.get("issues", [])
        routing_table: Dict[str, str] = {
            "label_note_conflict": "FixRecommender",
            "statistical_outlier": "OutlierDetector",
            "bias_detected": "BiasAuditor",
            "missing_label": "LabelVerifier",
            "invalid_entry": "DataCuratorAgent",
            "low_confidence": "FixRecommender"
        }

        routes: List[Dict[str, Any]] = []
        for issue in issues:
            issue_type = issue.get("issue", "unknown").lower().replace(" ", "_")
            target_agent = routing_table.get(issue_type, "ManualReview")
            routes.append({
                "issue": issue_type,
                "routed_to": target_agent,
                "timestamp": datetime.utcnow().isoformat(),
                "confidence": issue.get("confidence", 0.5),
                "metadata": issue
            })

        output = {
            "routed_feedback": routes,
            "unresolved_issues_count": sum(1 for r in routes if r["routed_to"] == "ManualReview"),
            "timestamp": datetime.utcnow().isoformat()
        }

        return self.standard_response(
            output=output,
            log=f"[{self.agent_name}] Routed {len(routes)} issue(s), {output['unresolved_issues_count']} to manual review."
        )
