from utils.base_agent import BaseAgent
from datetime import datetime
from typing import Dict, Any, List


class RealismChecker(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        patients: List[Dict[str, Any]] = input_data.get("patients", [])
        realism_scores: List[Dict[str, Any]] = []
        flags: List[Dict[str, Any]] = []

        for patient in patients:
            demographics = patient.get("demographics", {})
            encounters = patient.get("encounters", [])

            age = int(demographics.get("age", -1))
            gender = demographics.get("gender", "unknown")
            realism_score = 1.0  # Start with a perfect score

            # Rule: Check plausible age range
            if age < 0 or age > 120:
                realism_score -= 0.3
                flags.append({
                    "patient_id": patient.get("id", "unknown"),
                    "issue": f"Unrealistic age: {age}",
                    "field": "demographics.age",
                    "confidence": 0.9
                })

            # Rule: Ensure at least one encounter
            if not encounters:
                realism_score -= 0.2
                flags.append({
                    "patient_id": patient.get("id", "unknown"),
                    "issue": "Missing encounters",
                    "field": "encounters",
                    "confidence": 0.85
                })

            realism_scores.append({
                "patient_id": patient.get("id", "unknown"),
                "realism_score": round(realism_score, 2)
            })

        output = {
            "timestamp": datetime.utcnow().isoformat(),
            "realism_scores": realism_scores,
            "flags": flags,
            "average_score": round(
                sum(r["realism_score"] for r in realism_scores) / len(realism_scores),
                2
            ) if realism_scores else None
        }

        log = f"[RealismChecker] Evaluated {len(patients)} patient(s), flagged {len(flags)} potential issue(s)."

        return {
            "output": output,
            "log": log
        }
