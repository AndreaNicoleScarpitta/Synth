from .base_agent import BaseAgent
from datetime import datetime
import logging
from typing import Dict, Any, List

class MetaReasoner(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info("[MetaReasoner] Analyzing for conflicts across data sources...")

        # Pull multi-source evidence
        literature = input_data.get("literature_evidence", [])
        rwd = input_data.get("real_world_evidence", [])
        regulatory = input_data.get("regulatory_constraints", [])

        conflicts: List[Dict[str, Any]] = []
        missing_data_calls: List[str] = []

        # Example: check for drug use conflicts
        for lit in literature:
            lit_drug = lit.get("content", {}).get("recommended_drug", "").lower()
            for reg in regulatory:
                banned = reg.get("content", {}).get("banned_drugs", [])
                if isinstance(banned, list) and lit_drug in map(str.lower, banned):
                    conflicts.append({
                        "field": lit_drug,
                        "issue": "Conflict: Drug recommended in literature but banned by regulation",
                        "confidence": 0.85,
                        "source_ids": [lit.get("source_id"), reg.get("source_id")],
                        "recommendation": "Review country-specific regulatory status or substitute drug"
                    })

        # Optional: detect if key sources are missing entirely
        if not rwd:
            missing_data_calls.append("real_world_evidence")
        if not literature:
            missing_data_calls.append("literature_evidence")

        input_data["meta_analysis"] = {
            "conflicts": conflicts,
            "missing_data_calls": missing_data_calls,
            "research_rerun_required": len(conflicts) > 0,
            "timestamp": datetime.utcnow().isoformat()
        }

        return {
            "output": input_data,
            "log": f"[MetaReasoner] {len(conflicts)} conflicts found. Missing data: {missing_data_calls}"
        }
