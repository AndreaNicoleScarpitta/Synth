from typing import Dict, Any
import logging
import random
from utils.base_agent import BaseAgent

class LabGenerator(BaseAgent):
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "condition_to_labs": {
                "CKD": [
                    {"loinc": "2160-0", "name": "Creatinine", "range": (2.0, 6.0), "unit": "mg/dL"},
                    {"loinc": "2951-2", "name": "BUN", "range": (20, 80), "unit": "mg/dL"}
                ],
                "Diabetes": [
                    {"loinc": "4548-4", "name": "HbA1c", "range": (6.5, 12.0), "unit": "%"},
                    {"loinc": "2345-7", "name": "Glucose", "range": (120, 300), "unit": "mg/dL"}
                ],
                "Hypertension": [
                    {"loinc": "3094-0", "name": "Sodium", "range": (135, 150), "unit": "mmol/L"}
                ]
            },
            "default_labs": [
                {"loinc": "718-7", "name": "WBC", "range": (4.0, 11.0), "unit": "10^9/L"},
                {"loinc": "2823-3", "name": "Cholesterol", "range": (150, 240), "unit": "mg/dL"}
            ]
        }

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info("[LabGenerator] Generating lab values...")

        conditions = input_data.get("conditions", [])
        generated_labs = []

        # Add condition-specific labs
        for condition in conditions:
            labs = self.config["condition_to_labs"].get(condition, [])
            for lab in labs:
                value = round(random.uniform(*lab["range"]), 2)
                generated_labs.append({
                    "loinc": lab["loinc"],
                    "name": lab["name"],
                    "value": value,
                    "unit": lab["unit"],
                    "related_condition": condition
                })

        # Add some general labs regardless of condition
        for lab in self.config["default_labs"]:
            value = round(random.uniform(*lab["range"]), 2)
            generated_labs.append({
                "loinc": lab["loinc"],
                "name": lab["name"],
                "value": value,
                "unit": lab["unit"]
            })

        input_data["lab_results"] = generated_labs

        return {
            "output": input_data,
            "log": f"LabGenerator assigned {len(generated_labs)} lab values."
        }
