from agents.reporting.base_agent import BaseReportingAgent
from typing import Dict, Any

class ReportOrchestrator(BaseReportingAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gathers reporting outputs and assembles the final synthetic data report.
        Organizes sections for audit, summary, trust, regulatory, lineage, format, and any extras.
        """
        report = {
            "report_generated_by": "ReportOrchestrator",
            "timestamp": input_data.get("timestamp"),
            "sections": {}
        }

        for key, value in input_data.items():
            key_lower = key.lower()
            if key_lower.startswith("audit"):
                report["sections"]["audit_log"] = value
            elif "summary" in key_lower:
                report["sections"]["summary"] = value
            elif "trust" in key_lower:
                report["sections"]["trust"] = value
            elif "regulatory" in key_lower:
                report["sections"]["regulatory"] = value
            elif "lineage" in key_lower:
                report["sections"]["lineage"] = value
            elif "format" in key_lower:
                report["sections"]["formatted_output"] = value
            elif "fhir" in key_lower:
                report["sections"]["fhir_bundle"] = value
            elif "csv" in key_lower:
                report["sections"]["csv_export"] = value
            else:
                # Capture any extras under "other"
                report["sections"].setdefault("other", {})[key] = value

        log = (
            f"ReportOrchestrator: Assembled report with {len(report['sections'])} sections "
            f"at {report['timestamp'] or 'unknown timestamp'}."
        )

        return self.standard_response(
            output={"synthetic_data_report": report},
            log=log
        )
