from qa.base_agent import BaseQAAgent
from typing import Dict, Any
import logging
from collections import Counter

class BiasAuditor(BaseQAAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"[{self.agent_name}] Checking for representational bias...")

        patients = input_data.get("patients", [])
        if not patients:
            return self.fallback("No patient data provided.")

        demographics = [p.get("demographics", {}) for p in patients]

        gender_counts = Counter(d.get("gender", "unknown") for d in demographics)
        age_bins = Counter(self._age_bucket(d.get("age", 0)) for d in demographics)
        region_counts = Counter(d.get("region", "unspecified") for d in demographics)

        total = len(demographics)
        bias_flags = []

        if "female" in gender_counts and gender_counts["female"] / total < 0.25:
            bias_flags.append("Low female representation")

        if age_bins.get("65+", 0) / total < 0.1:
            bias_flags.append("Underrepresentation of seniors")

        output = {
            "bias_summary": {
                "gender_counts": gender_counts,
                "age_distribution": age_bins,
                "region_distribution": region_counts,
                "flags": bias_flags
            }
        }

        input_data["bias_audit"] = output

        return self.standard_response(
            output=input_data,
            log=f"BiasAuditor flagged {len(bias_flags)} potential bias issue(s)."
        )

    def _age_bucket(self, age: Any) -> str:
        try:
            age = int(age)
            if age < 18:
                return "<18"
            elif age < 30:
                return "18–29"
            elif age < 45:
                return "30–44"
            elif age < 65:
                return "45–64"
            else:
                return "65+"
        except:
            return "unknown"
