from typing import Dict, Any
import logging
import random
from langchain_core.runnables import Runnable

class MedicationPatternSuggester(Runnable):
    def __init__(self, llm=None, config: Dict[str, Any] = None):
        self.llm = llm
        self.config = config or {
            "condition_to_meds": {
                "CKD": ["lisinopril", "furosemide"],
                "Diabetes": ["metformin", "insulin glargine"],
                "Hypertension": ["amlodipine", "hydrochlorothiazide"],
                "COPD": ["albuterol", "tiotropium"],
                "CAD": ["atorvastatin", "aspirin"]
            },
            "max_meds_per_condition": 2
        }

    def invoke(self, input_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        logging.info("[MedicationPatternSuggester] Assigning medications...")

        conditions = input_data.get("conditions", [])
        prescribed_meds = []

        for condition in conditions:
            candidates = self.config["condition_to_meds"].get(condition, [])
            if candidates:
                meds = random.sample(
                    candidates,
                    k=min(len(candidates), self.config["max_meds_per_condition"])
                )
                prescribed_meds.extend(meds)

        # Deduplicate
        prescribed_meds = list(set(prescribed_meds))
        input_data["medications"] = prescribed_meds

        # Optional LLM validation
        if self.llm:
            try:
                prompt = f"Do the medications {prescribed_meds} make sense for a patient with {conditions}?"
                validation = self.llm.invoke(prompt)
                input_data["medication_validation"] = str(validation)
            except Exception as e:
                logging.warning(f"[MedicationPatternSuggester] LLM validation failed: {e}")
                input_data["medication_validation"] = "LLM validation failed"

        return {
            "output": input_data,
            "log": f"Medications assigned: {prescribed_meds}"
        }
