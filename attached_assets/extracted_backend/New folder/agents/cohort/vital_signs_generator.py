from typing import Dict, Any
import logging
import random
from utils.base_agent import BaseAgent

class VitalSignsGenerator(BaseAgent):
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "vitals": {
                "systolic_bp": (100, 160),
                "diastolic_bp": (60, 100),
                "heart_rate": (60, 110),
                "respiratory_rate": (12, 24),
                "temperature_c": (36.5, 38.0),
                "bmi": (18.5, 35.0)
            }
        }

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info("[VitalSignsGenerator] Generating vital signs...")

        # Optionally use demographics
        demographics = input_data.get("demographics", {})
        age = demographics.get("age", 40)
        sex = demographics.get("sex", "unknown")

        vitals = {
            "systolic_bp": random.randint(*self.config["vitals"]["systolic_bp"]),
            "diastolic_bp": random.randint(*self.config["vitals"]["diastolic_bp"]),
            "heart_rate": random.randint(*self.config["vitals"]["heart_rate"]),
            "respiratory_rate": random.randint(*self.config["vitals"]["respiratory_rate"]),
            "temperature_c": round(random.uniform(*self.config["vitals"]["temperature_c"]), 1),
            "bmi": round(random.uniform(*self.config["vitals"]["bmi"]), 1),
            "age_adjusted": age,
            "sex": sex
        }

        input_data["vital_signs"] = vitals

        return {
            "output": input_data,
            "log": f"Vital signs generated: {vitals}"
        }
