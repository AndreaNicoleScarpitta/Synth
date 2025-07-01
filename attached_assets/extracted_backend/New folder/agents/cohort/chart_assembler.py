from typing import Dict, Any
import logging
from utils.base_agent import BaseAgent

class ChartAssembler(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info("[ChartAssembler] Assembling full patient chart...")

        # Create a top-level chart dictionary
        chart = {
            "demographics": input_data.get("demographics", {}),
            "conditions": input_data.get("conditions", []),
            "phenotypes": input_data.get("phenotypes", []),
            "comorbidities": input_data.get("comorbidities", []),
            "procedures": input_data.get("procedures", []),
            "medications": input_data.get("medications", []),
            "lab_results": input_data.get("lab_results", []),
            "vital_signs": input_data.get("vital_signs", {}),
            "notes": input_data.get("clinical_notes", []),
            "adverse_events": input_data.get("adverse_events", []),
            "temporal_dynamics": input_data.get("temporal_dynamics", {}),
            "timeline": input_data.get("timeline", {}),
            "chart_summary": "Synthetic chart assembled successfully."
        }

        input_data["synthetic_chart"] = chart

        return {
            "output": input_data,
            "log": "[ChartAssembler] Chart successfully assembled."
        }
