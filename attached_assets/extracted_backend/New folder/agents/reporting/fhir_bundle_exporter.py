from utils.base_agent import BaseAgent
from typing import Dict, Any, List
from datetime import datetime
import uuid

class FHIRBundleExporter(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        patients: List[Dict[str, Any]] = input_data.get("patients", [])
        bundle_entries = []

        for p in patients:
            patient_id = p.get("id", str(uuid.uuid4()))
            demographics = p.get("demographics", {})
            resource = {
                "resourceType": "Patient",
                "id": patient_id,
                "gender": demographics.get("gender", None),
                "birthDate": demographics.get("birthDate", None),
                "extension": [
                    {
                        "url": "http://syntheticascension.org/fhir/StructureDefinition/age",
                        "valueInteger": demographics.get("age", None)
                    }
                ]
            }
            bundle_entries.append({"resource": resource})

            # Export encounters (if present)
            for enc in p.get("encounters", []):
                enc_id = enc.get("id", str(uuid.uuid4()))
                bundle_entries.append({
                    "resource": {
                        "resourceType": "Encounter",
                        "id": enc_id,
                        "subject": {"reference": f"Patient/{patient_id}"},
                        "period": {"start": enc.get("start", None)},
                        "type": [{"text": enc.get("type", None)}],
                        "location": [{"location": enc.get("location", None)}]
                    }
                })

        bundle = {
            "resourceType": "Bundle",
            "type": "collection",
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "entry": bundle_entries
        }

        return self.standard_response(
            output={"fhir_bundle": bundle, "entry_count": len(bundle_entries)},
            log=f"FHIRBundleExporter: Exported {len(bundle_entries)} resources to FHIR Bundle."
        )
