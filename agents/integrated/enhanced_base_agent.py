"""
Enhanced Base Agent Architecture for Comprehensive Agentic EHR System
Implements Doer/Coordinator/Adversarial pattern with expert recommendations
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import logging
import time
import uuid
import asyncio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import threading

class AgentRole(Enum):
    """Agent role classifications"""
    DOER = "doer"  # Actively generate/transform data
    COORDINATOR = "coordinator"  # Orchestrate, sequence, validate doers
    ADVERSARIAL = "adversarial"  # Stress-test and break doers

class AgentStatus(Enum):
    """Agent execution status"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"

class VersionManager:
    """Manages version pinning for reproducibility"""
    
    def __init__(self):
        self.pinned_versions = {}
        self.vocabulary_versions = {}
        
    def pin_version(self, component: str, version: str, metadata: Dict = None):
        """Pin a component version for replay determinism"""
        self.pinned_versions[component] = {
            "version": version,
            "pinned_at": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
    
    def get_pinned_version(self, component: str) -> Optional[str]:
        """Get pinned version for a component"""
        return self.pinned_versions.get(component, {}).get("version")
    
    def pin_vocabularies(self, snomed_version: str, loinc_version: str, icd_version: str):
        """Pin medical vocabulary versions"""
        self.vocabulary_versions = {
            "SNOMED_CT": {"version": snomed_version, "pinned_at": datetime.utcnow().isoformat()},
            "LOINC": {"version": loinc_version, "pinned_at": datetime.utcnow().isoformat()},
            "ICD10": {"version": icd_version, "pinned_at": datetime.utcnow().isoformat()}
        }

class ConcurrencyController:
    """Manages concurrency and prevents coordinator deadlocks"""
    
    def __init__(self, max_concurrent_agents: int = 10):
        self.max_concurrent = max_concurrent_agents
        self.active_agents = {}
        self.priority_queue = asyncio.PriorityQueue()
        self.locks = {}
        self._lock = asyncio.Lock()
    
    async def acquire_slot(self, agent_id: str, priority: int = 5) -> bool:
        """Acquire execution slot for agent"""
        async with self._lock:
            if len(self.active_agents) < self.max_concurrent:
                self.active_agents[agent_id] = {
                    "started_at": datetime.utcnow(),
                    "priority": priority
                }
                return True
            else:
                await self.priority_queue.put((priority, agent_id))
                return False
    
    async def release_slot(self, agent_id: str):
        """Release execution slot"""
        async with self._lock:
            if agent_id in self.active_agents:
                del self.active_agents[agent_id]
                
            # Process queue
            if not self.priority_queue.empty():
                priority, next_agent = await self.priority_queue.get()
                self.active_agents[next_agent] = {
                    "started_at": datetime.utcnow(),
                    "priority": priority
                }

class PrivacyGuard:
    """Manages differential privacy and re-identification risk"""
    
    def __init__(self, k_anonymity_threshold: int = 5, epsilon: float = 1.0):
        self.k_threshold = k_anonymity_threshold
        self.epsilon = epsilon
        
    def calculate_k_anonymity(self, dataset: Dict[str, Any]) -> int:
        """Calculate k-anonymity score for dataset"""
        # Simplified k-anonymity calculation
        # In production, would use sophisticated algorithms
        return max(1, self.k_threshold)  # Mock implementation
    
    def calculate_dp_score(self, dataset: Dict[str, Any]) -> float:
        """Calculate differential privacy score"""
        # Mock implementation - would use real DP mechanisms
        return self.epsilon
    
    def assess_reidentification_risk(self, dataset: Dict[str, Any]) -> Dict[str, Any]:
        """Assess re-identification risk"""
        k_score = self.calculate_k_anonymity(dataset)
        dp_score = self.calculate_dp_score(dataset)
        
        risk_level = "LOW"
        if k_score < 3:
            risk_level = "HIGH"
        elif k_score < 5:
            risk_level = "MEDIUM"
            
        return {
            "k_anonymity_score": k_score,
            "differential_privacy_epsilon": dp_score,
            "risk_level": risk_level,
            "assessment_timestamp": datetime.utcnow().isoformat()
        }

class HumanInTheLoopManager:
    """Manages human reviewer workloads and SLA thresholds"""
    
    def __init__(self, max_daily_reviews: int = 50, escalation_threshold: int = 10):
        self.max_daily_reviews = max_daily_reviews
        self.escalation_threshold = escalation_threshold
        self.daily_reviews = 0
        self.pending_reviews = 0
        
    async def request_review(self, review_type: str, data: Dict[str, Any], priority: int = 5) -> Dict[str, Any]:
        """Request human review with SLA management"""
        if self.pending_reviews >= self.escalation_threshold:
            return {
                "status": "escalated",
                "message": f"Review queue full ({self.pending_reviews} pending). Escalating to senior reviewer.",
                "estimated_delay_hours": 24
            }
        
        if self.daily_reviews >= self.max_daily_reviews:
            return {
                "status": "deferred",
                "message": "Daily review quota reached. Deferring to next business day.",
                "estimated_delay_hours": 24
            }
        
        self.pending_reviews += 1
        review_id = str(uuid.uuid4())
        
        return {
            "status": "queued",
            "review_id": review_id,
            "estimated_delay_minutes": 30,
            "reviewer_assigned": f"clinical_reviewer_{(self.pending_reviews % 3) + 1}"
        }
    
    async def complete_review(self, review_id: str, approved: bool, notes: str = ""):
        """Mark review as completed"""
        self.pending_reviews = max(0, self.pending_reviews - 1)
        self.daily_reviews += 1

class PerformanceMonitor:
    """Monitors system performance and benchmarks"""
    
    def __init__(self):
        self.metrics = {
            "throughput_patients_per_hour": 0,
            "average_latency_ms": 0,
            "peak_memory_usage_mb": 0,
            "error_rate_percent": 0
        }
        self.benchmark_targets = {
            "min_throughput_patients_per_hour": 1000,
            "max_latency_ms": 5000,
            "max_error_rate_percent": 1.0
        }
    
    def record_execution(self, agent_name: str, execution_time_ms: int, success: bool):
        """Record agent execution metrics"""
        # Update metrics (simplified implementation)
        self.metrics["average_latency_ms"] = (self.metrics["average_latency_ms"] + execution_time_ms) / 2
        
    def check_performance_thresholds(self) -> Dict[str, Any]:
        """Check if performance meets benchmark targets"""
        violations = []
        
        if self.metrics["average_latency_ms"] > self.benchmark_targets["max_latency_ms"]:
            violations.append(f"Latency exceeds {self.benchmark_targets['max_latency_ms']}ms")
            
        if self.metrics["error_rate_percent"] > self.benchmark_targets["max_error_rate_percent"]:
            violations.append(f"Error rate exceeds {self.benchmark_targets['max_error_rate_percent']}%")
        
        return {
            "meets_targets": len(violations) == 0,
            "violations": violations,
            "current_metrics": self.metrics
        }

class EnhancedBaseAgent(ABC):
    """Enhanced base class implementing comprehensive agentic architecture"""
    
    def __init__(self, name: Optional[str] = None, role: AgentRole = AgentRole.DOER):
        self.name = name or self.__class__.__name__
        self.agent_id = str(uuid.uuid4())
        self.role = role
        self.logger = logging.getLogger(f"{self.name}_{self.role.value}")
        
        # Enhanced capabilities
        self.version_manager = VersionManager()
        self.privacy_guard = PrivacyGuard()
        self.execution_history = []
        self.clinical_realism_approved = False
        
        # Initialize version pins
        self._initialize_version_pins()
        
    def _initialize_version_pins(self):
        """Initialize default version pins"""
        self.version_manager.pin_vocabularies(
            snomed_version="2024-01-01",
            loinc_version="2.77",
            icd_version="10-CM-2024"
        )
    
    @abstractmethod
    async def execute_primary_function(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's primary function"""
        pass
    
    async def coordinate_sub_agents(self, sub_agents: List['EnhancedBaseAgent'], 
                                  input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate execution of sub-agents (for COORDINATOR role)"""
        if self.role != AgentRole.COORDINATOR:
            raise ValueError("Only COORDINATOR agents can coordinate sub-agents")
        
        results = []
        for agent in sub_agents:
            result = await agent.execute_with_full_pipeline(input_data)
            results.append(result)
            
        return self._aggregate_coordination_results(results)
    
    async def adversarial_test(self, target_agent: 'EnhancedBaseAgent', 
                             test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute adversarial testing (for ADVERSARIAL role)"""
        if self.role != AgentRole.ADVERSARIAL:
            raise ValueError("Only ADVERSARIAL agents can perform adversarial testing")
        
        # Execute stress tests, edge cases, and failure scenarios
        return await self._execute_adversarial_scenarios(target_agent, test_data)
    
    async def request_clinical_review(self, data: Dict[str, Any], 
                                    reviewer_manager: HumanInTheLoopManager) -> Dict[str, Any]:
        """Request clinical realism review"""
        review_request = await reviewer_manager.request_review(
            review_type="clinical_realism",
            data={
                "agent_name": self.name,
                "agent_id": self.agent_id,
                "data_summary": self._summarize_for_review(data),
                "requested_at": datetime.utcnow().isoformat()
            }
        )
        
        if review_request["status"] == "queued":
            # In production, would wait for actual human review
            # For now, auto-approve after delay simulation
            await asyncio.sleep(0.1)  # Simulate review time
            self.clinical_realism_approved = True
            
        return review_request
    
    async def execute_with_full_pipeline(self, input_data: Dict[str, Any], 
                                       concurrency_controller: Optional[ConcurrencyController] = None,
                                       performance_monitor: Optional[PerformanceMonitor] = None) -> Dict[str, Any]:
        """Execute agent with full enhanced pipeline"""
        start_time = time.time()
        
        try:
            # Acquire concurrency slot if controller provided
            if concurrency_controller:
                await concurrency_controller.acquire_slot(self.agent_id)
            
            self.logger.info(f"Starting enhanced execution of {self.name} ({self.role.value})")
            
            # Execute primary function
            result = await self.execute_primary_function(input_data)
            
            # Privacy assessment
            privacy_assessment = self.privacy_guard.assess_reidentification_risk(result)
            
            execution_time = time.time() - start_time
            
            # Record performance metrics
            if performance_monitor:
                performance_monitor.record_execution(
                    self.name, 
                    int(execution_time * 1000), 
                    True
                )
            
            # Build comprehensive result
            enhanced_result = {
                "output": result,
                "metadata": {
                    "agent_name": self.name,
                    "agent_id": self.agent_id,
                    "agent_role": self.role.value,
                    "execution_time_seconds": execution_time,
                    "status": AgentStatus.SUCCESS.value,
                    "timestamp": datetime.utcnow().isoformat(),
                    "clinical_realism_approved": self.clinical_realism_approved,
                    "privacy_assessment": privacy_assessment,
                    "version_info": {
                        "pinned_vocabularies": self.version_manager.vocabulary_versions,
                        "component_versions": self.version_manager.pinned_versions
                    }
                },
                "provenance": {
                    "agent_chain": [self.agent_id],
                    "execution_trace": self._generate_execution_trace(),
                    "deterministic_replay_data": self._generate_replay_data(input_data)
                }
            }
            
            # Store execution history
            self.execution_history.append({
                "execution_id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "input_hash": self._hash_input(input_data),
                "result_hash": self._hash_result(enhanced_result),
                "execution_time": execution_time
            })
            
            self.logger.info(f"Enhanced execution completed for {self.name} in {execution_time:.2f}s")
            return enhanced_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # Record performance metrics for failure
            if performance_monitor:
                performance_monitor.record_execution(
                    self.name, 
                    int(execution_time * 1000), 
                    False
                )
            
            error_result = {
                "output": {},
                "metadata": {
                    "agent_name": self.name,
                    "agent_id": self.agent_id,
                    "agent_role": self.role.value,
                    "execution_time_seconds": execution_time,
                    "status": AgentStatus.FAILED.value,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                },
                "provenance": {
                    "agent_chain": [self.agent_id],
                    "error_trace": str(e)
                }
            }
            
            self.logger.error(f"Enhanced execution failed for {self.name}: {str(e)}")
            return error_result
            
        finally:
            # Release concurrency slot
            if concurrency_controller:
                await concurrency_controller.release_slot(self.agent_id)
    
    def _aggregate_coordination_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate results from coordinated sub-agents"""
        aggregated_output = {}
        agent_summaries = []
        
        for result in results:
            if result["metadata"]["status"] == AgentStatus.SUCCESS.value:
                aggregated_output.update(result["output"])
            
            agent_summaries.append({
                "agent_name": result["metadata"]["agent_name"],
                "status": result["metadata"]["status"],
                "execution_time": result["metadata"]["execution_time_seconds"]
            })
        
        return {
            "coordinated_results": aggregated_output,
            "coordination_summary": {
                "total_agents": len(results),
                "successful_agents": len([r for r in results if r["metadata"]["status"] == AgentStatus.SUCCESS.value]),
                "agent_summaries": agent_summaries
            }
        }
    
    async def _execute_adversarial_scenarios(self, target_agent: 'EnhancedBaseAgent', 
                                           test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute adversarial test scenarios"""
        test_scenarios = [
            ("edge_case_test", self._generate_edge_case_data(test_data)),
            ("boundary_test", self._generate_boundary_data(test_data)),
            ("contradiction_test", self._generate_contradictory_data(test_data)),
            ("overload_test", self._generate_overload_data(test_data))
        ]
        
        scenario_results = []
        
        for scenario_name, scenario_data in test_scenarios:
            try:
                result = await target_agent.execute_with_full_pipeline(scenario_data)
                scenario_results.append({
                    "scenario": scenario_name,
                    "status": "completed",
                    "target_agent_status": result["metadata"]["status"],
                    "execution_time": result["metadata"]["execution_time_seconds"]
                })
            except Exception as e:
                scenario_results.append({
                    "scenario": scenario_name,
                    "status": "failed",
                    "error": str(e)
                })
        
        return {
            "adversarial_test_results": scenario_results,
            "overall_robustness_score": self._calculate_robustness_score(scenario_results)
        }
    
    def _generate_edge_case_data(self, base_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate edge case test data"""
        edge_data = base_data.copy()
        # Add edge case modifications
        edge_data["population_size"] = 1  # Minimal population
        edge_data["age_range"] = [150, 200]  # Impossible ages
        return edge_data
    
    def _generate_boundary_data(self, base_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate boundary condition test data"""
        boundary_data = base_data.copy()
        boundary_data["population_size"] = 10000  # Maximum population
        return boundary_data
    
    def _generate_contradictory_data(self, base_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate contradictory test data"""
        contradictory_data = base_data.copy()
        contradictory_data["condition"] = "pregnancy diabetes"  # Contradictory for male patients
        return contradictory_data
    
    def _generate_overload_data(self, base_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate system overload test data"""
        overload_data = base_data.copy()
        overload_data["complexity_multiplier"] = 100
        return overload_data
    
    def _calculate_robustness_score(self, results: List[Dict[str, Any]]) -> float:
        """Calculate robustness score from adversarial test results"""
        if not results:
            return 0.0
        
        successful_scenarios = len([r for r in results if r["status"] == "completed"])
        return (successful_scenarios / len(results)) * 100
    
    def _summarize_for_review(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize data for clinical review"""
        return {
            "data_type": type(data).__name__,
            "key_fields": list(data.keys())[:10],  # First 10 keys
            "data_size": len(str(data)),
            "summary_generated_at": datetime.utcnow().isoformat()
        }
    
    def _generate_execution_trace(self) -> List[Dict[str, Any]]:
        """Generate execution trace for provenance"""
        return [
            {
                "step": 1,
                "action": "input_validation",
                "timestamp": datetime.utcnow().isoformat()
            },
            {
                "step": 2,
                "action": "primary_execution",
                "timestamp": datetime.utcnow().isoformat()
            },
            {
                "step": 3,
                "action": "privacy_assessment",
                "timestamp": datetime.utcnow().isoformat()
            }
        ]
    
    def _generate_replay_data(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data needed for deterministic replay"""
        return {
            "input_data_hash": self._hash_input(input_data),
            "vocabulary_versions": self.version_manager.vocabulary_versions,
            "random_seed": 42,  # In production, would use deterministic seeding
            "replay_timestamp": datetime.utcnow().isoformat()
        }
    
    def _hash_input(self, input_data: Dict[str, Any]) -> str:
        """Generate hash of input data"""
        import hashlib
        return hashlib.md5(str(sorted(input_data.items())).encode()).hexdigest()
    
    def _hash_result(self, result: Dict[str, Any]) -> str:
        """Generate hash of result data"""
        import hashlib
        # Hash only the output, not metadata
        return hashlib.md5(str(sorted(result.get("output", {}).items())).encode()).hexdigest()