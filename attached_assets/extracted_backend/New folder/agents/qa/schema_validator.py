from .base_agent import BaseQAAgent
from typing import Dict, Any, List, Union
from datetime import datetime


class SchemaValidator(BaseQAAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        patients: List[Dict[str, Any]] = input_data.get("patients", [])
        required_fields = {
            "demographics": {
                "age": int,
                "gender": str
            },
            "encounters": list  # At least one encounter per patient
        }

        missing_fields: List[Dict[str, Union[str, int]]] = []
        invalid_types: List[Dict[str, Union[str, int, str]]] = []

        for idx, patient in enumerate(patients):
            for section, fields in required_fields.items():
                section_data = patient.get(section)

                if section_data is None:
                    missing_fields.append({
                        "patient_index": idx,
                        "field": section
                    })
                    continue

                if isinstance(fields, dict):
                    for subfield, expected_type in fields.items():
                        value = section_data.get(subfield)
                        if value is None:
                            missing_fields.append({
                                "patient_index": idx,
                                "field": f"{section}.{subfield}"
                            })
                        elif not isinstance(value, expected_type):
                            invalid_types.append({
                                "patient_index": idx,
                                "field": f"{section}.{subfield}",
                                "expected": expected_type.__name__,
                                "received": type(value).__name__
                            })
                elif isinstance(fields, type) and not isinstance(section_data, fields):
                    invalid_types.append({
                        "patient_index": idx,
                        "field": section,
                        "expected": fields.__name__,
                        "received": type(section_data).__name__
                    })

        valid = len(missing_fields) == 0 and len(invalid_types) == 0

        return {
            "valid": valid,
            "missing_fields": missing_fields,
            "invalid_types": invalid_types,
            "timestamp": datetime.utcnow().isoformat()
        }
