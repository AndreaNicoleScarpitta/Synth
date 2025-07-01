from abc import ABC, abstractmethod
from datetime import datetime
import logging

class BaseQAAgent(ABC):
    def __init__(self):
        self.agent_name = self.__class__.__name__

    @abstractmethod
    def run(self, input_data: dict) -> dict:
        """
        Main execution method. Must return a dictionary containing:
        - 'output': modified or annotated input_data
        - 'log': status or summary message
        - Optional: 'issues', 'score', etc.
        """
        pass

    def standard_response(self, output: dict, log: str = "") -> dict:
        return {
            "output": output,
            "log": f"[{self.agent_name}] {log}",
            "timestamp": datetime.utcnow().isoformat(),
            "agent": self.agent_name
        }

    def fallback(self, reason: str) -> dict:
        logging.warning(f"[{self.agent_name}] Fallback triggered: {reason}")
        return self.standard_response(
            output={},
            log=f"Fallback due to: {reason}"
        )
