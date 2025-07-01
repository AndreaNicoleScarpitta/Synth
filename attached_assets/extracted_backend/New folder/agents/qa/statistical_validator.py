from utils.base_agent import BaseAgent
from typing import Dict, Any, List
from statistics import mean, stdev
from datetime import datetime


class StatisticalValidator(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        patients: List[Dict[str, Any]] = input_data.get("patients", [])
        age_values = []
        encounter_counts = []
        flags = []

        for idx, patient in enumerate(patients):
            demographics = patient.get("demographics", {})
            encounters = patient.get("encounters", [])

            # Validate age
            age = demographics.get("age")
            if isinstance(age, (int, float, str)) and str(age).isdigit():
                age_values.append(int(age))
            else:
                flags.append({
                    "patient_index": idx,
                    "issue": "Invalid or missing age",
                    "field": "demographics.age"
                })

            # Validate encounters
            if isinstance(encounters, list):
                encounter_counts.append(len(encounters))
            else:
                flags.append({
                    "patient_index": idx,
                    "issue": "Invalid or missing encounter list",
                    "field": "encounters"
                })

        # Compute stats
        age_summary = {
            "count": len(age_values),
            "min": min(age_values) if age_values else None,
            "max": max(age_values) if age_values else None,
            "mean": mean(age_values) if len(age_values) > 1 else None,
            "stdev": stdev(age_values) if len(age_values) > 2 else None
        }

        encounter_summary = {
            "count": len(encounter_counts),
            "min": min(encounter_counts) if encounter_counts else None,
            "max": max(encounter_counts) if encounter_counts else None,
            "mean": mean(encounter_counts) if len(encounter_counts) > 1 else None,
            "stdev": stdev(encounter_counts) if len(encounter_counts) > 2 else None
        }

        return {
            "valid": len(flags) == 0,
            "summary": {
                "age": age_summary,
                "encounters_per_patient": encounter_summary
            },
            "flags": flags,
            "timestamp": datetime.utcnow().isoformat()
        }
