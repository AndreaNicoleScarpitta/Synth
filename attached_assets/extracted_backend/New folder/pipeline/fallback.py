from abc import ABC, abstractmethod
from typing import Any

class FallbackStrategy(ABC):
    @abstractmethod
    def handle(self, agent_name: str, exception: Exception) -> Any:
        """Return a fallback output for the named agent."""
        pass

class SnapshotFallback(FallbackStrategy):
    def handle(self, agent_name: str, exception: Exception) -> Any:
        # TODO: load a cached snapshot based on agent_name
        raise NotImplementedError("Snapshot fallback not yet implemented")
