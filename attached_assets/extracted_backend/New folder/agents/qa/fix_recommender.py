from qa.base_agent import BaseQAAgent
from typing import Dict, Any, List
import logging

class FixRecommender(BaseQAAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"[{self.agent_name}] Analyzing QA flags for fix recommendations...")

        qa_flags: List[Dict[str, Any]] = input_data.get("qa_flags", [])
        bias_audit = input_data.get("bias_audit", {}).get("bias_summary", {})
        schema_issues = input_data.get("schema_validation", {}).get("issues", [])

        fix_recs: List[Dict[str, str]] = []

        for issue in qa_flags:
            if "label" in issue.get("issue", ""):
                fix_recs.append({
                    "issue": issue["issue"],
                    "suggestion": "Regenerate label or verify label mapping logic."
                })

        if bias_audit:
            if "Underrepresentation of seniors" in bias_audit.get("flags", []):
                fix_recs.append({
                    "issue": "Age bias",
                    "suggestion": "Augment synthetic cohort with more 65+ patients."
                })

        for s in schema_issues:
            fix_recs.append({
                "issue": f"Schema: {s}",
                "suggestion": "Ensure required fields are generated before final export."
            })

        input_data["fix_recommendations"] = fix_recs

        return self.standard_response(
            output=input_data,
            log=f"{self.agent_name} generated {len(fix_recs)} fix suggestion(s)."
        )
