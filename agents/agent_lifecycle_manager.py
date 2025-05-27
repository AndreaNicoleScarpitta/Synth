"""
Agent Lifecycle Management System
Comprehensive orchestration of AI agents with flywheel data collection
"""

import asyncio
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import threading
from contextlib import asynccontextmanager

from utils.agentic_database_manager import (
    get_agentic_database_manager, AgentState, InteractionType
)

class AgentCapability(Enum):
    """Core agent capabilities"""
    LITERATURE_SEARCH = "literature_search"
    COHORT_GENERATION = "cohort_generation"
    DATA_VALIDATION = "data_validation"
    BIOMEDICAL_ANALYSIS = "biomedical_analysis"
    USER_INTERACTION = "user_interaction"
    TOOL_ORCHESTRATION = "tool_orchestration"
    LEARNING_ADAPTATION = "learning_adaptation"
    MEMORY_MANAGEMENT = "memory_management"

class TaskPriority(Enum):
    """Task execution priorities"""
    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"
    BACKGROUND = "background"

@dataclass
class AgentTask:
    """Agent task definition"""
    task_id: str
    agent_id: str
    task_type: str
    priority: TaskPriority
    input_data: Dict[str, Any]
    context: Dict[str, Any]
    expected_output: Optional[Dict[str, Any]]
    timeout_seconds: int
    retry_count: int
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    status: str
    result: Optional[Dict[str, Any]]
    error_details: Optional[str]

class AgentLifecycleManager:
    """
    Manages the complete lifecycle of AI agents with comprehensive flywheel logging
    """
    
    def __init__(self):
        self.db_manager = get_agentic_database_manager()
        self.active_agents = {}
        self.task_queue = asyncio.Queue()
        self.agent_pools = {}
        self.performance_monitors = {}
        self.learning_controllers = {}
        self.session_contexts = {}
        
        # Initialize core agents
        self._initialize_core_agents()
    
    def _initialize_core_agents(self):
        """Initialize core system agents"""
        core_agents = [
            {
                "agent_id": "literature_agent",
                "agent_type": "biomedical_search",
                "capabilities": [
                    AgentCapability.LITERATURE_SEARCH.value,
                    AgentCapability.BIOMEDICAL_ANALYSIS.value
                ],
                "configuration": {
                    "max_concurrent_searches": 5,
                    "cache_results": True,
                    "quality_threshold": 0.7
                }
            },
            {
                "agent_id": "cohort_agent",
                "agent_type": "data_generation",
                "capabilities": [
                    AgentCapability.COHORT_GENERATION.value,
                    AgentCapability.DATA_VALIDATION.value
                ],
                "configuration": {
                    "max_patients_per_batch": 50,
                    "validation_enabled": True,
                    "demographic_balancing": True
                }
            },
            {
                "agent_id": "validation_agent",
                "agent_type": "quality_control",
                "capabilities": [
                    AgentCapability.DATA_VALIDATION.value,
                    AgentCapability.LEARNING_ADAPTATION.value
                ],
                "configuration": {
                    "statistical_tests": True,
                    "medical_terminology_check": True,
                    "bias_detection": True
                }
            },
            {
                "agent_id": "orchestrator_agent",
                "agent_type": "workflow_coordination",
                "capabilities": [
                    AgentCapability.TOOL_ORCHESTRATION.value,
                    AgentCapability.USER_INTERACTION.value,
                    AgentCapability.MEMORY_MANAGEMENT.value
                ],
                "configuration": {
                    "max_workflow_depth": 10,
                    "timeout_management": True,
                    "error_recovery": True
                }
            }
        ]
        
        for agent_config in core_agents:
            self.register_agent(**agent_config)
    
    def register_agent(self, agent_id: str, agent_type: str, capabilities: List[str],
                      configuration: Dict[str, Any] = None) -> bool:
        """Register an agent with the lifecycle manager"""
        try:
            # Register in database
            success = self.db_manager.register_agent(
                agent_id=agent_id,
                agent_type=agent_type,
                capabilities=capabilities,
                configuration=configuration
            )
            
            if success:
                self.active_agents[agent_id] = {
                    "agent_type": agent_type,
                    "capabilities": capabilities,
                    "configuration": configuration or {},
                    "status": AgentState.INITIALIZED,
                    "current_sessions": [],
                    "performance_metrics": {
                        "total_tasks": 0,
                        "successful_tasks": 0,
                        "avg_response_time": 0,
                        "last_activity": datetime.utcnow()
                    }
                }
                
                # Log agent registration
                self.db_manager.record_learning_event(
                    agent_id=agent_id,
                    event_type="agent_registration",
                    learning_data={
                        "agent_type": agent_type,
                        "capabilities": capabilities,
                        "registration_time": datetime.utcnow().isoformat()
                    }
                )
                
                return True
            return False
            
        except Exception as e:
            print(f"Failed to register agent {agent_id}: {e}")
            return False
    
    async def start_agent_session(self, agent_id: str, user_id: str = None,
                                 session_type: str = "conversation",
                                 context: Dict[str, Any] = None) -> Optional[str]:
        """Start a new agent session with comprehensive logging"""
        try:
            if agent_id not in self.active_agents:
                raise ValueError(f"Agent {agent_id} not registered")
            
            session_id = self.db_manager.start_session(
                agent_id=agent_id,
                session_type=session_type,
                user_id=user_id,
                context=context
            )
            
            if session_id:
                # Update agent status
                self.active_agents[agent_id]["current_sessions"].append(session_id)
                self.db_manager.update_agent_status(agent_id, AgentState.RUNNING)
                
                # Initialize session context
                self.session_contexts[session_id] = {
                    "agent_id": agent_id,
                    "user_id": user_id,
                    "session_type": session_type,
                    "context": context or {},
                    "started_at": datetime.utcnow(),
                    "interaction_count": 0,
                    "memory_items": [],
                    "performance_data": []
                }
                
                # Log session start
                await self.log_interaction(
                    session_id=session_id,
                    agent_id=agent_id,
                    interaction_type=InteractionType.USER_QUERY,
                    input_data={"action": "session_start", "context": context or {}},
                    output_data={"session_id": session_id, "status": "started"},
                    context={"user_id": user_id, "session_type": session_type}
                )
                
                return session_id
            
            return None
            
        except Exception as e:
            print(f"Failed to start agent session: {e}")
            return None
    
    async def log_interaction(self, session_id: str, agent_id: str,
                             interaction_type: InteractionType,
                             input_data: Dict[str, Any],
                             output_data: Dict[str, Any],
                             context: Dict[str, Any] = None,
                             duration_ms: int = 0,
                             success: bool = True,
                             error_details: str = None) -> Optional[str]:
        """Log agent interaction with performance tracking"""
        try:
            start_time = time.time()
            
            # Enhanced context with session data
            enhanced_context = context or {}
            if session_id in self.session_contexts:
                session_ctx = self.session_contexts[session_id]
                enhanced_context.update({
                    "session_age_seconds": (datetime.utcnow() - session_ctx["started_at"]).total_seconds(),
                    "session_interaction_count": session_ctx["interaction_count"],
                    "agent_capabilities": self.active_agents.get(agent_id, {}).get("capabilities", [])
                })
            
            # Log interaction
            interaction_id = self.db_manager.log_interaction(
                session_id=session_id,
                agent_id=agent_id,
                interaction_type=interaction_type,
                input_data=input_data,
                output_data=output_data,
                context=enhanced_context,
                duration_ms=duration_ms,
                success=success,
                error_details=error_details
            )
            
            # Update session context
            if session_id in self.session_contexts:
                self.session_contexts[session_id]["interaction_count"] += 1
                self.session_contexts[session_id]["performance_data"].append({
                    "interaction_id": interaction_id,
                    "duration_ms": duration_ms,
                    "success": success,
                    "timestamp": datetime.utcnow()
                })
            
            # Update agent performance metrics
            if agent_id in self.active_agents:
                metrics = self.active_agents[agent_id]["performance_metrics"]
                metrics["total_tasks"] += 1
                if success:
                    metrics["successful_tasks"] += 1
                
                # Calculate rolling average response time
                current_avg = metrics["avg_response_time"]
                total_tasks = metrics["total_tasks"]
                metrics["avg_response_time"] = (
                    (current_avg * (total_tasks - 1) + duration_ms) / total_tasks
                )
                metrics["last_activity"] = datetime.utcnow()
            
            # Store important interactions in agent memory
            if interaction_type in [InteractionType.DECISION_POINT, InteractionType.ERROR_HANDLING]:
                await self.store_agent_memory(
                    agent_id=agent_id,
                    session_id=session_id,
                    memory_type="episodic",
                    content={
                        "interaction_id": interaction_id,
                        "interaction_type": interaction_type.value,
                        "input_summary": str(input_data)[:500],
                        "output_summary": str(output_data)[:500],
                        "success": success,
                        "error_details": error_details
                    },
                    importance_score=0.8 if not success else 0.6
                )
            
            return interaction_id
            
        except Exception as e:
            print(f"Failed to log interaction: {e}")
            return None
    
    async def store_agent_memory(self, agent_id: str, session_id: str,
                                memory_type: str, content: Dict[str, Any],
                                importance_score: float = 0.5,
                                tags: List[str] = None) -> Optional[str]:
        """Store agent memory with contextual importance"""
        try:
            # Calculate importance based on content and context
            adjusted_importance = self._calculate_memory_importance(
                content, memory_type, importance_score
            )
            
            memory_id = self.db_manager.store_memory(
                agent_id=agent_id,
                session_id=session_id,
                memory_type=memory_type,
                content=content,
                importance_score=adjusted_importance,
                tags=tags
            )
            
            # Update session memory tracking
            if session_id in self.session_contexts:
                self.session_contexts[session_id]["memory_items"].append({
                    "memory_id": memory_id,
                    "memory_type": memory_type,
                    "importance_score": adjusted_importance,
                    "created_at": datetime.utcnow()
                })
            
            return memory_id
            
        except Exception as e:
            print(f"Failed to store agent memory: {e}")
            return None
    
    def _calculate_memory_importance(self, content: Dict[str, Any],
                                   memory_type: str, base_importance: float) -> float:
        """Calculate memory importance based on content and type"""
        importance = base_importance
        
        # Boost importance for error patterns
        if "error" in str(content).lower() or "fail" in str(content).lower():
            importance += 0.2
        
        # Boost importance for successful complex tasks
        if memory_type == "procedural" and "success" in content:
            importance += 0.15
        
        # Boost importance for user feedback
        if "feedback" in content or "rating" in content:
            importance += 0.25
        
        return min(1.0, importance)
    
    async def execute_agent_task(self, agent_id: str, task_type: str,
                                input_data: Dict[str, Any],
                                context: Dict[str, Any] = None,
                                timeout_seconds: int = 300) -> Dict[str, Any]:
        """Execute a task through an agent with comprehensive logging"""
        start_time = time.time()
        task_id = str(uuid.uuid4())
        
        try:
            if agent_id not in self.active_agents:
                raise ValueError(f"Agent {agent_id} not registered")
            
            # Create task record
            task = AgentTask(
                task_id=task_id,
                agent_id=agent_id,
                task_type=task_type,
                priority=TaskPriority.NORMAL,
                input_data=input_data,
                context=context or {},
                expected_output=None,
                timeout_seconds=timeout_seconds,
                retry_count=0,
                created_at=datetime.utcnow(),
                started_at=datetime.utcnow(),
                completed_at=None,
                status="running",
                result=None,
                error_details=None
            )
            
            # Execute task based on agent capabilities
            result = await self._execute_task_by_type(task)
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Update task completion
            task.completed_at = datetime.utcnow()
            task.status = "completed" if result.get("success") else "failed"
            task.result = result
            
            # Log task execution as interaction
            session_id = context.get("session_id") if context else None
            if session_id:
                await self.log_interaction(
                    session_id=session_id,
                    agent_id=agent_id,
                    interaction_type=InteractionType.TOOL_CALL,
                    input_data={"task_type": task_type, "input_data": input_data},
                    output_data=result,
                    context=context,
                    duration_ms=duration_ms,
                    success=result.get("success", False),
                    error_details=result.get("error")
                )
            
            return result
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_result = {
                "success": False,
                "error": str(e),
                "task_id": task_id,
                "duration_ms": duration_ms
            }
            
            # Log error
            session_id = context.get("session_id") if context else None
            if session_id:
                await self.log_interaction(
                    session_id=session_id,
                    agent_id=agent_id,
                    interaction_type=InteractionType.ERROR_HANDLING,
                    input_data={"task_type": task_type, "input_data": input_data},
                    output_data=error_result,
                    context=context,
                    duration_ms=duration_ms,
                    success=False,
                    error_details=str(e)
                )
            
            return error_result
    
    async def _execute_task_by_type(self, task: AgentTask) -> Dict[str, Any]:
        """Execute task based on type and agent capabilities"""
        agent_info = self.active_agents.get(task.agent_id)
        if not agent_info:
            return {"success": False, "error": "Agent not found"}
        
        capabilities = agent_info.get("capabilities", [])
        
        # Route task to appropriate execution method
        if task.task_type == "literature_search" and AgentCapability.LITERATURE_SEARCH.value in capabilities:
            return await self._execute_literature_search(task)
        elif task.task_type == "cohort_generation" and AgentCapability.COHORT_GENERATION.value in capabilities:
            return await self._execute_cohort_generation(task)
        elif task.task_type == "data_validation" and AgentCapability.DATA_VALIDATION.value in capabilities:
            return await self._execute_data_validation(task)
        else:
            return {
                "success": False,
                "error": f"Task type {task.task_type} not supported by agent {task.agent_id}"
            }
    
    async def _execute_literature_search(self, task: AgentTask) -> Dict[str, Any]:
        """Execute literature search task"""
        try:
            # Simulate literature search execution
            # In real implementation, this would call the actual literature agent
            await asyncio.sleep(0.1)  # Simulate processing time
            
            query = task.input_data.get("query", "")
            max_results = task.input_data.get("max_results", 20)
            
            return {
                "success": True,
                "task_id": task.task_id,
                "results": {
                    "query": query,
                    "max_results": max_results,
                    "found_articles": max_results,
                    "execution_time": "simulated"
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _execute_cohort_generation(self, task: AgentTask) -> Dict[str, Any]:
        """Execute cohort generation task"""
        try:
            # Simulate cohort generation
            await asyncio.sleep(0.2)  # Simulate processing time
            
            problem_statement = task.input_data.get("problem_statement", "")
            cohort_size = task.input_data.get("cohort_size", 10)
            
            return {
                "success": True,
                "task_id": task.task_id,
                "results": {
                    "problem_statement": problem_statement,
                    "cohort_size": cohort_size,
                    "generated_patients": cohort_size,
                    "execution_time": "simulated"
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _execute_data_validation(self, task: AgentTask) -> Dict[str, Any]:
        """Execute data validation task"""
        try:
            # Simulate data validation
            await asyncio.sleep(0.1)  # Simulate processing time
            
            data = task.input_data.get("data", {})
            validation_type = task.input_data.get("validation_type", "basic")
            
            return {
                "success": True,
                "task_id": task.task_id,
                "results": {
                    "validation_type": validation_type,
                    "data_quality_score": 0.95,
                    "issues_found": 0,
                    "execution_time": "simulated"
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def add_user_feedback(self, interaction_id: str, agent_id: str,
                               user_id: str, feedback_data: Dict[str, Any]) -> bool:
        """Add user feedback for continuous improvement"""
        try:
            feedback_id = self.db_manager.add_user_feedback(
                interaction_id=interaction_id,
                agent_id=agent_id,
                user_id=user_id,
                feedback_type="user_rating",
                feedback_data=feedback_data
            )
            
            if feedback_id:
                # Trigger learning event based on feedback
                await self._process_feedback_for_learning(
                    agent_id, interaction_id, feedback_data
                )
                return True
            return False
            
        except Exception as e:
            print(f"Failed to add user feedback: {e}")
            return False
    
    async def _process_feedback_for_learning(self, agent_id: str,
                                           interaction_id: str,
                                           feedback_data: Dict[str, Any]):
        """Process user feedback to generate learning events"""
        try:
            rating = feedback_data.get("rating", 3)
            
            # Generate learning event for low ratings
            if rating <= 2:
                self.db_manager.record_learning_event(
                    agent_id=agent_id,
                    event_type="negative_feedback",
                    trigger_interaction_id=interaction_id,
                    learning_data={
                        "feedback_rating": rating,
                        "feedback_text": feedback_data.get("text", ""),
                        "improvement_area": "response_quality"
                    },
                    performance_impact=-0.1,
                    confidence=0.8
                )
            
            # Generate learning event for high ratings
            elif rating >= 4:
                self.db_manager.record_learning_event(
                    agent_id=agent_id,
                    event_type="positive_reinforcement",
                    trigger_interaction_id=interaction_id,
                    learning_data={
                        "feedback_rating": rating,
                        "feedback_text": feedback_data.get("text", ""),
                        "success_pattern": "high_quality_response"
                    },
                    performance_impact=0.05,
                    confidence=0.7
                )
                
        except Exception as e:
            print(f"Failed to process feedback for learning: {e}")
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get comprehensive agent status"""
        if agent_id not in self.active_agents:
            return {"error": "Agent not found"}
        
        agent_info = self.active_agents[agent_id]
        performance_metrics = self.db_manager.get_agent_performance_metrics(agent_id)
        
        return {
            "agent_id": agent_id,
            "agent_type": agent_info["agent_type"],
            "status": agent_info["status"].value if hasattr(agent_info["status"], 'value') else agent_info["status"],
            "capabilities": agent_info["capabilities"],
            "active_sessions": len(agent_info["current_sessions"]),
            "performance_metrics": performance_metrics,
            "last_activity": agent_info["performance_metrics"]["last_activity"].isoformat()
        }
    
    def get_flywheel_analytics(self) -> Dict[str, Any]:
        """Get comprehensive flywheel analytics"""
        return self.db_manager.get_flywheel_analytics()
    
    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check for agent lifecycle system"""
        try:
            db_health = self.db_manager.health_check()
            
            # Check active agents
            active_count = len([
                agent for agent in self.active_agents.values()
                if agent["status"] in [AgentState.RUNNING, AgentState.WAITING]
            ])
            
            # Check session activity
            active_sessions = len(self.session_contexts)
            
            return {
                "status": "healthy",
                "components": {
                    "agent_lifecycle_manager": {
                        "status": "healthy",
                        "active_agents": active_count,
                        "total_registered_agents": len(self.active_agents),
                        "active_sessions": active_sessions
                    },
                    "agentic_database": db_health
                },
                "last_checked": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "last_checked": datetime.utcnow().isoformat()
            }

# Global instance
_agent_lifecycle_manager = None

def get_agent_lifecycle_manager() -> AgentLifecycleManager:
    """Get or create the global agent lifecycle manager instance"""
    global _agent_lifecycle_manager
    if _agent_lifecycle_manager is None:
        _agent_lifecycle_manager = AgentLifecycleManager()
    return _agent_lifecycle_manager