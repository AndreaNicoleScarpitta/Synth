from .base_agent import BaseQAAgent
from typing import Dict, Any, List
import logging

class PatientScorecard(BaseQAAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"[{self.agent_name}] Generating patient-level QA scorecard...")

        patient_id = input_data.get("patient_id", "unknown")
        demographics = input_data.get("demographics", {})
        labels = input_data.get("labels", [])
        qa_flags = input_data.get("qa_flags", [])

        score = 1.0
        deductions = []

        # Deduct for missing demographics
        for field in ["age", "gender"]:
            if field not in demographics:
                deductions.append({
                    "field": field,
                    "issue": "Missing demographic info",
                    "deduction": 0.1
                })
                score -= 0.1

        # Deduct for label-note mismatches
        for flag in qa_flags:
            if flag.get("issue", "").lower() in ["label_note_conflict", "statistical outlier"]:
                deductions.append({
                    "field": flag.get("field", "unknown"),
                    "issue": flag.get("issue"),
                    "deduction": 0.05
                })
                score -= 0.05

        # Deduct for too few labels
        if isinstance(labels, list) and len(labels) < 2:
            deductions.append({
                "field": "labels",
                "issue": "Too few labeled outputs",
                "deduction": 0.05
            })
            score -= 0.05

        score = max(0.0, round(score, 2))

        output = {
            "patient_id": patient_id,
            "score": score,
            "deductions": deductions
        }

        return self.standard_response(
            output=output,
            log=f"[{self.agent_name}] Scorecard generated with score: {score}"
        )
