from abc import ABC, abstractmethod
from datetime import datetime
import logging

class BaseAgent(ABC):
    def __init__(self):
        self.agent_name = self.__class__.__name__

    @abstractmethod
    def run(self, input_data: dict) -> dict:
        """
        Main execution method. Should return:
        {
            "output": ...,
            "log": ...,
            "timestamp": ...,
            "agent": ...
        }
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
        return self.standard_response(output={}, log=f"Fallback: {reason}")
