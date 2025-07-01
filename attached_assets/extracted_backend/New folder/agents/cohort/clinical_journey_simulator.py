from typing import Dict, Any
import logging
import random
from datetime import timedelta, datetime
from langchain_core.runnables import Runnable

class ClinicalJourneyBuilder(Runnable):
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "min_visits": 2,
            "max_visits": 6,
            "visit_types": ["primary_care", "specialist", "ER", "inpatient"],
            "visit_weights": [0.4, 0.3, 0.2, 0.1],
            "start_date_range_days": 180  # range prior to today to begin visit sequence
        }

    def invoke(self, input_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        logging.info("[ClinicalJourneyBuilder] Constructing encounter timeline...")

        visit_count = random.randint(self.config["min_visits"], self.config["max_visits"])
        today = datetime.today()
        first_visit_date = today - timedelta(days=random.randint(0, self.config["start_date_range_days"]))

        visits = []
        for i in range(visit_count):
            visit_date = first_visit_date + timedelta(days=random.randint(14, 90) * i)
            visit_type = random.choices(
                self.config["visit_types"], weights=self.config["visit_weights"], k=1
            )[0]
            visit = {
                "date": visit_date.strftime("%Y-%m-%d"),
                "type": visit_type,
                "visit_id": f"encounter-{i+1}",
                "conditions": random.sample(input_data.get("conditions", []), k=1)
            }
            visits.append(visit)

        input_data["encounters"] = visits

        return {
            "output": input_data,
            "log": f"{len(visits)} encounters generated starting on {first_visit_date.date()}"
        }