from agents.research.base_agent import BaseAgent
from typing import Dict, Any
import logging
from datetime import datetime
from collections import Counter

class DatasetProfileAgent(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info("[DatasetProfileAgent] Profiling dataset...")

        # Stubbed example dataset — in production, this could come from a Bronze/Silver FHIR table or JSONL
        dataset = input_data.get("existing_patients", [
            {"age": 67, "gender": "female", "conditions": ["E11.9", "I10"]},
            {"age": 72, "gender": "male", "conditions": ["N18.4", "E11.9"]},
            {"age": 59, "gender": "female", "conditions": ["E11.9"]},
            {"age": 88, "gender": "male", "conditions": ["I10", "N18.9"]}
        ])

        total = len(dataset)
        ages = [entry["age"] for entry in dataset]
        genders = [entry["gender"] for entry in dataset]
        conditions = [code for entry in dataset for code in entry["conditions"]]

        stats = {
            "total_patients": total,
            "age_distribution": {
                "min": min(ages),
                "max": max(ages),
                "avg": sum(ages) / total
            },
            "gender_counts": dict(Counter(genders)),
            "top_conditions": dict(Counter(conditions).most_common(5)),
            "timestamp": datetime.utcnow().isoformat()
        }

        input_data["dataset_profile"] = stats

        return {
            "output": input_data,
            "log": f"[DatasetProfileAgent] Profiled dataset with {total} patients."
        }
