"""
Base agent class for the integrated multi-agent system
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
import time
import uuid
from datetime import datetime

class BaseIntegratedAgent(ABC):
    """Base class for all integrated agents"""
    
    def __init__(self, name: Optional[str] = None):
        self.name = name or self.__class__.__name__
        self.agent_id = str(uuid.uuid4())
        self.logger = logging.getLogger(self.name)
        
    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's main functionality
        
        Args:
            input_data: Input parameters and data for the agent
            
        Returns:
            Dictionary containing:
            - output: The agent's output data
            - log: Execution log messages
            - metadata: Agent execution metadata
        """
        pass
    
    def execute_with_timing(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent with timing and error handling"""
        start_time = time.time()
        
        try:
            self.logger.info(f"Starting execution of {self.name}")
            result = self.run(input_data)
            
            execution_time = time.time() - start_time
            
            # Add metadata
            result.setdefault("metadata", {}).update({
                "agent_name": self.name,
                "agent_id": self.agent_id,
                "execution_time_seconds": execution_time,
                "status": "success",
                "timestamp": datetime.utcnow().isoformat()
            })
            
            self.logger.info(f"Completed {self.name} in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_result = {
                "output": {},
                "log": f"Error in {self.name}: {str(e)}",
                "metadata": {
                    "agent_name": self.name,
                    "agent_id": self.agent_id,
                    "execution_time_seconds": execution_time,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
            self.logger.error(f"Error in {self.name}: {str(e)}")
            return error_result
    
    def validate_input(self, input_data: Dict[str, Any], required_keys: list) -> bool:
        """Validate that required input keys are present"""
        missing_keys = [key for key in required_keys if key not in input_data]
        if missing_keys:
            raise ValueError(f"Missing required input keys: {missing_keys}")
        return True