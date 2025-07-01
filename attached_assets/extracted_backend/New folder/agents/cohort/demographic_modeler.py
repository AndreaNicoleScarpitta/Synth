from typing import Dict, Any
import random
import logging
from langchain_core.runnables import Runnable

class DemographicStratifier(Runnable):
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "age_distribution": [(0, 18), (19, 40), (41, 65), (66, 90)],
            "age_weights": [0.1, 0.35, 0.35, 0.2],
            "sex_distribution": ["male", "female"],
            "sex_weights": [0.49, 0.51],
            "race_distribution": ["White", "Black", "Asian", "Hispanic", "Other"],
            "race_weights": [0.6, 0.13, 0.06, 0.18, 0.03]
        }

    def invoke(self, input_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        logging.info("[DemographicStratifier] Sampling demographics...")

        # Sample age
        age_bucket = random.choices(
            self.config["age_distribution"],
            weights=self.config["age_weights"],
            k=1
        )[0]
        age = random.randint(age_bucket[0], age_bucket[1])

        # Sample sex and race
        sex = random.choices(self.config["sex_distribution"], weights=self.config["sex_weights"], k=1)[0]
        race = random.choices(self.config["race_distribution"], weights=self.config["race_weights"], k=1)[0]

        demographics = {
            "age": age,
            "sex": sex,
            "race": race
        }

        input_data["demographics"] = demographics

        return {
            "output": input_data,
            "log": f"Demographics assigned: {demographics}"
        }