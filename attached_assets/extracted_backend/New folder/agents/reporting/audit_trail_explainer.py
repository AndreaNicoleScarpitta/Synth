from utils.base_agent import BaseAgent
from typing import Dict, Any, List
from datetime import datetime

class AuditTrailExplainer(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        audit_trail: List[Dict[str, Any]] = input_data.get("audit_trail", [])
        logs: List[str] = []

        if not audit_trail:
            return self.standard_response(
                output={"audit_explanation": []},
                log="No audit trail found in input data."
            )

        # Order by timestamp if present
        explanation: List[str] = []
        for entry in sorted(audit_trail, key=lambda x: x.get("timestamp", "")):
            who = entry.get("agent", "Unknown Agent")
            when = entry.get("timestamp", "Unknown Time")
            what = entry.get("action", "Performed unknown action")
            details = entry.get("details", "")
            line = f"[{when}] {who}: {what}. {details}"
            explanation.append(line)
            logs.append(f"Explained: {line}")

        output = {
            "audit_explanation": explanation,
            "entry_count": len(explanation),
            "last_event": explanation[-1] if explanation else None,
            "timestamp": datetime.utcnow().isoformat()
        }

        return self.standard_response(
            output=output,
            log=f"AuditTrailExplainer processed {len(explanation)} entries."
        )
