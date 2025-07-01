from agents.reporting.base_agent import BaseReportingAgent
from typing import Dict, Any
from datetime import datetime

class FormatOutputReconstructor(BaseReportingAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reconstructs or post-processes output for export/presentation.
        Example: Normalizes field names, restores nested structure, fixes types, etc.
        """
        records = input_data.get("records", [])
        # Example: convert all keys to snake_case and ensure all dict values are serializable (stubbed here)
        formatted_records = [
            {str(k).lower().replace(" ", "_"): v for k, v in record.items()}
            for record in records
        ] if records else []

        output = {
            "formatted_output": formatted_records,
            "record_count": len(formatted_records),
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat()
        }
        log = f"FormatOutputReconstructor: Formatted {len(formatted_records)} records."

        return self.standard_response(
            output=output,
            log=log
        )
