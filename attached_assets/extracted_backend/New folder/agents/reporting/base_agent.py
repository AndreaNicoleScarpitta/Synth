# Defines BaseReportingAgent for shared logic
class BaseReportingAgent:
    def __init__(self, config: dict = None):
        self.config = config or {}

    def run(self, data: dict) -> dict:
        raise NotImplementedError("Each reporting agent must implement its own `run` method.")

    def validate_input(self, data: dict) -> bool:
        # Optional input validation logic
        return True

    def load_cached(self):
        # Optional fallback logic
        return {
            "status": "cached_fallback",
            "content": None
        }
