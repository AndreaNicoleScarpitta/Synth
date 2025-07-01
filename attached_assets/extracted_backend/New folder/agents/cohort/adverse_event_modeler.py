from typing import Dict, Any, List
import random
import logging
from utils.base_agent import BaseAgent

# Sample AE catalog (in practice, you may load this from a clinical dataset or JSON file)
ADVERSE_EVENT_CATALOG = [
    {"event": "Allergic reaction", "trigger": "medication"},
    {"event": "Procedure-related infection", "trigger": "procedure"},
    {"event": "Drug interaction", "trigger": "multiple_medications"},
    {"event": "Hypotension", "trigger": "comorbidity"},
    {"event": "Rash", "trigger": "medication"},
    {"event": "Respiratory distress", "trigger": "condition"},
    {"event": "Readmission", "trigger": "complex_case"}
]

class AdverseEventGenerator(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info("[AdverseEventGenerator] Modeling synthetic adverse events...")

        medications = input_data.get("medications", [])
        procedures = input_data.get("procedures", [])
        comorbidities = input_data.get("comorbidities", [])
        conditions = input_data.get("conditions", [])
        
        simulated_events: List[Dict[str, str]] = []

        for ae in ADVERSE_EVENT_CATALOG:
            trigger_type = ae["trigger"]

            if trigger_type == "medication" and medications and random.random() < 0.2:
                simulated_events.append({"event": ae["event"], "trigger": random.choice(medications)})

            elif trigger_type == "multiple_medications" and len(medications) > 2 and random.random() < 0.3:
                simulated_events.append({"event": ae["event"], "trigger": "polypharmacy"})

            elif trigger_type == "procedure" and procedures and random.random() < 0.2:
                simulated_events.append({"event": ae["event"], "trigger": random.choice(procedures)})

            elif trigger_type == "comorbidity" and comorbidities and random.random() < 0.15:
                simulated_events.append({"event": ae["event"], "trigger": random.choice(comorbidities)})

            elif trigger_type == "condition" and conditions and random.random() < 0.15:
                simulated_events.append({"event": ae["event"], "trigger": random.choice(conditions)})

            elif trigger_type == "complex_case" and len(comorbidities) + len(conditions) > 4:
                simulated_events.append({"event": ae["event"], "trigger": "clinical complexity"})

        input_data["adverse_events"] = simulated_events

        return {
            "output": input_data,
            "log": f"[AdverseEventGenerator] Generated {len(simulated_events)} adverse events."
        }
