from utils.base_agent import BaseAgent
from typing import Dict, Any, List
from collections import Counter
from datetime import datetime

class CohortSummary(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        patients: List[Dict[str, Any]] = input_data.get("patients", [])
        demographics = [p.get("demographics", {}) for p in patients]
        condition_lists = [p.get("conditions", []) for p in patients]

        gender_counts = Counter(d.get("gender", "unknown") for d in demographics)
        age_values = [int(d.get("age", -1)) for d in demographics if "age" in d and isinstance(d.get("age"), (int, float, str)) and str(d.get("age")).isdigit()]
        condition_counts = Counter(cond for cond_list in condition_lists for cond in cond_list)

        output = {
            "patient_count": len(patients),
            "gender_distribution": dict(gender_counts),
            "age_stats": {
                "min": min(age_values) if age_values else None,
                "max": max(age_values) if age_values else None,
                "mean": round(sum(age_values) / len(age_values), 2) if age_values else None
            },
            "top_conditions": dict(condition_counts.most_common(5)),
            "timestamp": datetime.utcnow().isoformat()
        }

        log = (
            f"CohortSummary: {len(patients)} patients | "
            f"Genders: {dict(gender_counts)} | "
            f"Age mean: {output['age_stats']['mean']} | "
            f"Top conditions: {list(output['top_conditions'].keys())}"
        )

        return self.standard_response(
            output={"cohort_summary": output},
            log=log
        )
