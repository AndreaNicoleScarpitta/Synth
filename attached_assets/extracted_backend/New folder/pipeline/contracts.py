from pydantic import BaseModel
from typing import Any, Dict

# Example: Phase-1 input contract
class Phase1Input(BaseModel):
    config: Dict[str, Any]

# Example: CompetitorResearchAgent output
class CompetitorResearchOutput(BaseModel):
    competitors: Any
    timestamp: str

# TODO: define one BaseModel for each agent’s input and output
