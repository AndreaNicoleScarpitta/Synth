from typing import Dict, Any
import logging
from utils.base_agent import BaseAgent

class TimelineVisualizer(BaseAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info("[TimelineVisualizer] Creating human-readable summary...")

        timeline = input_data.get("timeline", [])
        if not timeline:
            return {
                "output": input_data,
                "log": "No timeline found in input_data. Skipping visualization."
            }

        summary = []
        for event in timeline:
            timestamp = event.get("timestamp", "unknown time")
            event_type = event.get("type", "unknown type")
            content = event.get("event", {})
            if isinstance(content, dict):
                detail = content.get("procedure_code") or content.get("value") or str(content)
            else:
                detail = str(content)

            summary.append(f"[{timestamp}] {event_type}: {detail}")

        input_data["timeline_summary"] = "\n".join(summary)

        return {
            "output": input_data,
            "log": f"TimelineVisualizer rendered {len(timeline)} events."
        }
