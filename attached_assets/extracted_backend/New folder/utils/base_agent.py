# utils/base_agent.py

import abc
from typing import Any, Dict
from utils.logger import log_chain_of_thought


class BaseAgent(abc.ABC):
    """
    Abstract base class that all agents inherit from.
    Ensures consistent structure: input, output, logging, and error handling.
    """

    def __init__(self, name: str, config: Dict[str, Any] = None):
        # Name of the agent, e.g. "PhenotypeAssembler"
        self.name = name

        # Optional runtime config passed from orchestrator
        self.config = config or {}

    @abc.abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Must be implemented by child classes.
        Should return a dictionary with `output` and `log` keys at minimum.
        """
        pass

    def format_output(self, output_data: Dict[str, Any], log: str) -> Dict[str, Any]:
        """
        Wrap output in a consistent structure used by orchestrator and reporters.
        """
        return {
            "agent": self.name,
            "output": output_data,
            "log": log,
            "success": True
        }

    def run_with_logging(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Wrapper for running the agent and logging its chain-of-thought.
        Catches errors and returns a structured failure response if needed.
        """
        try:
            result = self.run(input_data)

            # Log chain-of-thought to file
            log_chain_of_thought(self.name, result.get("log", "No CoT log returned."))

            return self.format_output(result.get("output", {}), result.get("log", ""))
        
        except Exception as e:
            return {
                "agent": self.name,
                "output": {},
                "log": f"❌ Error during execution: {str(e)}",
                "success": False
            }
