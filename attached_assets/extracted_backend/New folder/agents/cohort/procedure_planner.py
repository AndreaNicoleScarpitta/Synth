from typing import Dict, Any
import logging
import random
from utils.base_agent import BaseAgent

class ProcedureGenerator(BaseAgent):
    def __init__(self, llm=None, config: Dict[str, Any] = None):
        self.llm = llm
        self.config = config or {
            "condition_to_procedures": {
                "CKD": ["CPT:90935 - Hemodialysis"],
                "Diabetes": ["CPT:82947 - Glucose Test"],
                "Hypertension": ["CPT:93784 - BP Monitoring"],
                "COPD": ["CPT:94010 - Spirometry"],
                "CAD": ["CPT:92928 - Coronary stent"]
            },
            "max_procs_per_condition": 1,
            "link_to_encounters": True
        }

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info("[ProcedureGenerator] Assigning procedures...")

        conditions = input_data.get("conditions", [])
        procedures = []
        encounters = input_data.get("encounters", [])

        for cond in conditions:
            candidates = self.config["condition_to_procedures"].get(cond, [])
            if candidates:
                selected = random.sample(
                    candidates,
                    k=min(len(candidates), self.config["max_procs_per_condition"])
                )
                procedures.extend(selected)

        procedure_events = []
        for i, proc in enumerate(procedures):
            linked_encounter = random.choice(encounters)["visit_id"] if encounters else f"encounter-{i+1}"
            procedure_events.append({
                "procedure_code": proc,
                "linked_encounter": linked_encounter,
                "condition": conditions[i % len(conditions)] if conditions else None
            })

        input_data["procedures"] = procedure_events

        # Optional LLM validation
        if self.llm:
            try:
                summary = ", ".join([p['procedure_code'] for p in procedure_events])
                prompt = f"Do these procedures make sense for a patient with {conditions}? {summary}"
                validation = self.llm.invoke(prompt)
                input_data["procedure_validation"] = str(validation)
            except Exception as e:
                logging.warning(f"[ProcedureGenerator] LLM validation failed: {e}")
                input_data["procedure_validation"] = "LLM validation failed"

        return {
            "output": input_data,
            "log": f"Procedures assigned: {[p['procedure_code'] for p in procedure_events]}"
        }
