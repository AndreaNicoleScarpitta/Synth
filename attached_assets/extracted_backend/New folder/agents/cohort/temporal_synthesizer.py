from typing import Dict, Any, List
import logging
import random
from datetime import datetime, timedelta
from utils.base_agent import BaseAgent

class TemporalDynamics(BaseAgent):
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "start_date": "2020-01-01",
            "event_gap_days": (10, 60),
            "include_timeline": True
        }

    def _random_date(self, start: datetime, min_days: int, max_days: int) -> datetime:
        delta = timedelta(days=random.randint(min_days, max_days))
        return start + delta

    def _assign_dates(self, events: List[Dict[str, Any]], start: datetime) -> List[Dict[str, Any]]:
        dated_events = []
        for i, event in enumerate(events):
            event_date = self._random_date(start, *self.config["event_gap_days"])
            start = event_date  # update reference
            event["timestamp"] = event_date.isoformat()
            dated_events.append(event)
        return dated_events

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info("[TemporalDynamics] Synthesizing timeline...")

        base_date = datetime.fromisoformat(self.config["start_date"])

        event_categories = {
            "encounters": input_data.get("encounters", []),
            "conditions": input_data.get("conditions", []),
            "procedures": input_data.get("procedures", []),
            "medications": input_data.get("medications", []),
            "xray_images": input_data.get("xray_images", []),
        }

        timeline = []
        for key, events in event_categories.items():
            if isinstance(events, list) and events:
                # wrap simple types like strings into dicts
                enriched = [{"type": key, "event": e if isinstance(e, dict) else {"value": e}} for e in events]
                enriched = self._assign_dates(enriched, base_date)
                timeline.extend(enriched)

        # sort timeline chronologically
        timeline.sort(key=lambda x: x["timestamp"])

        if self.config["include_timeline"]:
            input_data["timeline"] = timeline

        # optional: update each category in input_data with timestamps (in-place enrichment)
        # Skipped for now to keep things clean — can be added if you want deep enrichment

        return {
            "output": input_data,
            "log": f"TemporalDynamics completed with {len(timeline)} total events sequenced."
        }
