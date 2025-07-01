from typing import Dict, Any
import logging
from utils.base_agent import BaseAgent

class NarrativeValidator(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info("[NarrativeValidator] Validating clinical notes...")

        notes = input_data.get("clinical_notes", [])
        validated_notes = []
        issues = []

        for idx, note in enumerate(notes):
            note_str = str(note).strip()
            note_result = {
                "original": note_str,
                "is_valid": True,
                "issues": []
            }

            # Example heuristics — replace with real medical QA later
            if len(note_str) < 30:
                note_result["is_valid"] = False
                note_result["issues"].append("Too short — possible placeholder or hallucination")

            if any(term in note_str.lower() for term in ["asdf", "lorem ipsum", "???"]):
                note_result["is_valid"] = False
                note_result["issues"].append("Placeholder or invalid characters detected")

            # More checks: terminology, structure, dates, hallucinations...
            # TODO: Add integration with medical LLM or ontology validator

            if not note_result["is_valid"]:
                issues.append(note_result)

            validated_notes.append(note_result)

        input_data["validated_clinical_notes"] = validated_notes
        input_data["note_validation_issues"] = issues

        return {
            "output": input_data,
            "log": f"[NarrativeValidator] Validation complete. {len(issues)} issue(s) found."
        }
