from threading import Lock

class MetricCollector:
    def __init__(self):
        self._lock = Lock()
        self.data = {
            "durations": {},   # { "AgentName": [durations...] }
            "retries": {},     # { "AgentName": retry_count }
        }

    def record_duration(self, name: str, seconds: float):
        with self._lock:
            self.data["durations"].setdefault(name, []).append(seconds)

    def record_retry(self, name: str):
        with self._lock:
            self.data["retries"][name] = self.data["retries"].get(name, 0) + 1

    def export(self) -> dict:
        """Return a snapshot of all metrics."""
        with self._lock:
            return dict(self.data)
