from qa.base_agent import BaseQAAgent
from typing import Dict, Any, List
import logging

class LabelVerifier(BaseQAAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"[{self.agent_name}] Verifying label-to-note alignment...")

        labels = input_data.get("labels", [])
        notes = input_data.get("clinical_notes", [])
        conditions = input_data.get("conditions", [])

        label_flags: List[Dict[str, Any]] = []

        for label in labels:
            label_text = label.lower()
            # Check for absence in clinical notes
            if all(label_text not in note.lower() for note in notes):
                label_flags.append({
                    "label": label,
                    "issue": "Label not reflected in clinical notes",
                    "confidence": 0.8
                })

            # Optional: also check if conditions are unmentioned
            if label_text not in [c.lower() for c in conditions]:
                label_flags.append({
                    "label": label,
                    "issue": "Label missing from structured conditions",
                    "confidence": 0.75
                })

        input_data["label_verification"] = {
            "issues": label_flags,
            "summary": f"{len(label_flags)} label conflict(s) found"
        }

        # Optional: append to global qa_flags for orchestration
        if "qa_flags" not in input_data:
            input_data["qa_flags"] = []
        input_data["qa_flags"].extend(label_flags)

        return self.standard_response(
            output=input_data,
            log=f"{self.agent_name} found {len(label_flags)} label inconsistency issue(s)."
        )
