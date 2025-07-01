from .base_agent import BaseQAAgent
from typing import Dict, Any, List
from datetime import datetime
import logging
import uuid

class QAFHIRExporter(BaseQAAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"[{self.agent_name}] Exporting QA issues to FHIR format...")

        issues: List[Dict[str, Any]] = input_data.get("qa_flags", []) + input_data.get("issues", [])
        patient_id = input_data.get("patient_id", "unknown")

        fhir_issues = []

        for issue in issues:
            fhir_issues.append({
                "resourceType": "DetectedIssue",
                "id": str(uuid.uuid4()),
                "status": "final",
                "patient": {
                    "reference": f"Patient/{patient_id}"
                },
                "identifiedDateTime": datetime.utcnow().isoformat(),
                "severity": "high" if issue.get("confidence", 0.9) > 0.8 else "moderate",
                "code": {
                    "text": issue.get("issue", "Unspecified QA Issue")
                },
                "detail": issue.get("recommendation", "Needs review"),
                "extension": [
                    {
                        "url": "http://example.org/fhir/StructureDefinition/qa-confidence-score",
                        "valueDecimal": issue.get("confidence", 0.5)
                    }
                ]
            })

        output = {
            "fhir_resources": fhir_issues,
            "resource_count": len(fhir_issues),
            "export_timestamp": datetime.utcnow().isoformat()
        }

        return self.standard_response(
            output=output,
            log=f"[{self.agent_name}] Exported {len(fhir_issues)} DetectedIssue resources to FHIR."
        )
