from qa.base_agent import BaseQAAgent
from typing import Dict, Any, List
import logging
import numpy as np

class OutlierDetector(BaseQAAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"[{self.agent_name}] Detecting statistical outliers...")

        outlier_flags: List[Dict[str, Any]] = []

        # Pull from structured inputs
        labs = input_data.get("labs", [])
        vitals = input_data.get("vitals", [])
        age_values = [p.get("age") for p in input_data.get("patients", []) if isinstance(p.get("age"), (int, float))]

        def detect(field_name: str, values: List[float], threshold: float = 2.5):
            if len(values) < 2:
                return []
            mean = np.mean(values)
            std = np.std(values)
            return [
                {
                    "field": field_name,
                    "value": val,
                    "issue": "Statistical outlier",
                    "z_score": round((val - mean) / std, 2),
                    "confidence": 0.9
                }
                for val in values if abs((val - mean) / std) > threshold
            ]

        # Age-based outliers
        outlier_flags.extend(detect("age", age_values))

        # Lab value outliers
        for lab in labs:
            if isinstance(lab.get("value"), (int, float)):
                field = f"lab:{lab.get('name', 'unknown')}"
                outlier_flags.extend(detect(field, [lab["value"]]))

        # Vitals outliers
        for vital in vitals:
            for k, v in vital.items():
                if isinstance(v, (int, float)):
                    field = f"vital:{k}"
                    outlier_flags.extend(detect(field, [v]))

        input_data["outlier_detection"] = {
            "issues": outlier_flags,
            "summary": f"{len(outlier_flags)} potential outlier(s) detected"
        }

        if "qa_flags" not in input_data:
            input_data["qa_flags"] = []
        input_data["qa_flags"].extend(outlier_flags)

        return self.standard_response(
            output=input_data,
            log=f"{self.agent_name} found {len(outlier_flags)} statistical outlier(s)."
        )
