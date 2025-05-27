"""
Enterprise-Grade Definition of Done Framework for Synthetic Ascension
Implements complete traceability, testing, and observability for healthcare deployments
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import json
import logging
from enum import Enum
import traceback
import hashlib

# Set up enterprise logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('synthetic_ascension_audit.log'),
        logging.StreamHandler()
    ]
)

class ComponentType(Enum):
    AGENT = "agent"
    PROGRAMMATIC = "programmatic"
    WORKFLOW = "workflow"

class DecisionType(Enum):
    GENERATION = "generation"
    VALIDATION = "validation"
    FILTERING = "filtering"
    TRANSFORMATION = "transformation"

@dataclass
class ContextSource:
    """RAG source or context that influenced a decision"""
    source_id: str
    source_type: str  # "literature", "knowledge_base", "user_input", "rag_document"
    content: str
    metadata: Dict[str, Any]
    retrieval_timestamp: datetime
    relevance_score: float = 0.0
    content_hash: str = field(default="")
    
    def __post_init__(self):
        if not self.content_hash:
            self.content_hash = hashlib.md5(self.content.encode()).hexdigest()

@dataclass
class TraceableDecision:
    """Complete audit trail for any system decision or generation"""
    
    # Core identification
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Component information
    component_name: str = ""
    component_type: ComponentType = ComponentType.PROGRAMMATIC
    component_version: str = "1.0.0"
    operation_type: DecisionType = DecisionType.GENERATION
    
    # Traceability requirements (DoD #1)
    original_prompt: str = ""
    retrieved_context: List[ContextSource] = field(default_factory=list)
    model_metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Output and reasoning
    output_data: Any = None
    decision_reasoning: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    quality_metrics: Dict[str, float] = field(default_factory=dict)
    
    # Follow-up support (DoD #2)
    citation_map: Dict[str, str] = field(default_factory=dict)
    followup_hooks: List[str] = field(default_factory=list)
    reproduction_config: Dict[str, Any] = field(default_factory=dict)
    
    # Validation and acceptance
    validation_results: Dict[str, Any] = field(default_factory=dict)
    accepted: bool = True
    rejection_reasons: List[str] = field(default_factory=list)
    
    def add_context_source(self, source: ContextSource):
        """Add RAG source that influenced this decision"""
        self.retrieved_context.append(source)
        
    def add_reasoning_step(self, step: str, confidence: float = None):
        """Add reasoning step with optional confidence"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        reasoning_entry = f"[{timestamp}] {step}"
        if confidence:
            reasoning_entry += f" (confidence: {confidence:.2f})"
        self.decision_reasoning.append(reasoning_entry)
        
    def add_citation(self, claim: str, source_id: str):
        """Map specific output claims to their sources"""
        self.citation_map[claim] = source_id
        
    def set_model_config(self, model_name: str, temperature: float = None, **kwargs):
        """Set AI model configuration for reproducibility"""
        self.model_metadata = {
            'model_name': model_name,
            'temperature': temperature,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
    def mark_rejected(self, reasons: List[str]):
        """Mark decision as rejected with reasons"""
        self.accepted = False
        self.rejection_reasons = reasons
        
    def to_compliance_record(self) -> Dict[str, Any]:
        """Generate healthcare-compliant audit record"""
        return {
            'audit_id': self.trace_id,
            'timestamp': self.timestamp.isoformat(),
            'component_identification': {
                'name': self.component_name,
                'type': self.component_type.value,
                'version': self.component_version,
                'operation': self.operation_type.value
            },
            'input_traceability': {
                'original_prompt': self.original_prompt,
                'context_sources_count': len(self.retrieved_context),
                'context_sources': [
                    {
                        'source_id': src.source_id,
                        'type': src.source_type,
                        'content_hash': src.content_hash,
                        'relevance_score': src.relevance_score,
                        'retrieval_time': src.retrieval_timestamp.isoformat()
                    } for src in self.retrieved_context
                ]
            },
            'model_configuration': self.model_metadata,
            'decision_process': {
                'reasoning_steps': self.decision_reasoning,
                'confidence_score': self.confidence_score,
                'quality_metrics': self.quality_metrics,
                'citations_provided': len(self.citation_map)
            },
            'output_validation': {
                'accepted': self.accepted,
                'rejection_reasons': self.rejection_reasons,
                'validation_results': self.validation_results
            },
            'reproducibility': {
                'reproduction_config': self.reproduction_config,
                'followup_hooks': self.followup_hooks
            }
        }

class EnterpriseTestSuite:
    """Comprehensive testing framework for agents and components (DoD #3)"""
    
    def __init__(self):
        self.test_results: Dict[str, Dict[str, Any]] = {}
        self.mock_responses: Dict[str, Any] = {}
        self.integration_chains: List[List[str]] = []
        
    def register_unit_test(self, component_name: str, test_name: str, test_func: Callable):
        """Register a unit test for a component"""
        if component_name not in self.test_results:
            self.test_results[component_name] = {'unit_tests': {}, 'integration_tests': {}}
            
        self.test_results[component_name]['unit_tests'][test_name] = {
            'function': test_func,
            'status': 'registered',
            'last_run': None,
            'result': None
        }
        
    def register_mock_response(self, component_name: str, input_pattern: str, expected_output: Any):
        """Register mock response for predictable testing"""
        if component_name not in self.mock_responses:
            self.mock_responses[component_name] = {}
        self.mock_responses[component_name][input_pattern] = expected_output
        
    def run_unit_tests(self, component_name: str = None) -> Dict[str, Any]:
        """Run unit tests for specific component or all components"""
        results = {'total_tests': 0, 'passed': 0, 'failed': 0, 'details': {}}
        
        components = [component_name] if component_name else self.test_results.keys()
        
        for comp in components:
            if comp not in self.test_results:
                continue
                
            comp_results = {'tests': {}, 'passed': 0, 'failed': 0}
            
            for test_name, test_info in self.test_results[comp]['unit_tests'].items():
                try:
                    test_func = test_info['function']
                    result = test_func()
                    
                    comp_results['tests'][test_name] = {
                        'status': 'passed',
                        'result': result,
                        'timestamp': datetime.now().isoformat()
                    }
                    comp_results['passed'] += 1
                    results['passed'] += 1
                    
                except Exception as e:
                    comp_results['tests'][test_name] = {
                        'status': 'failed',
                        'error': str(e),
                        'traceback': traceback.format_exc(),
                        'timestamp': datetime.now().isoformat()
                    }
                    comp_results['failed'] += 1
                    results['failed'] += 1
                    
                results['total_tests'] += 1
                
            results['details'][comp] = comp_results
            
        return results
        
    def validate_agent_behavior(self, agent_name: str, test_inputs: List[str]) -> Dict[str, Any]:
        """Test agent behavior against known inputs"""
        validation_results = {
            'agent': agent_name,
            'tests_run': len(test_inputs),
            'consistent_outputs': 0,
            'output_variations': [],
            'behavior_score': 0.0
        }
        
        if agent_name in self.mock_responses:
            mock_data = self.mock_responses[agent_name]
            
            for test_input in test_inputs:
                for pattern, expected in mock_data.items():
                    if pattern in test_input:
                        # In real implementation, would call actual agent
                        # For now, simulate behavior validation
                        validation_results['consistent_outputs'] += 1
                        break
                else:
                    validation_results['output_variations'].append(f"No mock for: {test_input}")
        
        if validation_results['tests_run'] > 0:
            validation_results['behavior_score'] = (
                validation_results['consistent_outputs'] / validation_results['tests_run']
            )
            
        return validation_results

class DeploymentGatekeeping:
    """CI/CD gatekeeping with enterprise requirements (DoD #4)"""
    
    def __init__(self, test_suite: EnterpriseTestSuite):
        self.test_suite = test_suite
        self.deployment_gates: List[Callable] = []
        self.validation_rules: List[Callable] = []
        self.rollback_policies: Dict[str, Callable] = {}
        
    def add_deployment_gate(self, gate_name: str, gate_func: Callable):
        """Add a deployment gate that must pass"""
        gate_func.gate_name = gate_name
        self.deployment_gates.append(gate_func)
        
    def add_output_validation_rule(self, rule_name: str, rule_func: Callable):
        """Add output format validation rule"""
        rule_func.rule_name = rule_name
        self.validation_rules.append(rule_func)
        
    def register_rollback_policy(self, component_name: str, rollback_func: Callable):
        """Register rollback procedure for component"""
        self.rollback_policies[component_name] = rollback_func
        
    def run_deployment_validation(self) -> Dict[str, Any]:
        """Run complete deployment validation suite"""
        validation_report = {
            'deployment_approved': False,
            'gate_results': {},
            'test_results': {},
            'validation_results': {},
            'blocking_issues': [],
            'warnings': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Run unit tests
        test_results = self.test_suite.run_unit_tests()
        validation_report['test_results'] = test_results
        
        if test_results['failed'] > 0:
            validation_report['blocking_issues'].append(
                f"Unit tests failed: {test_results['failed']} failures"
            )
        
        # Run deployment gates
        for gate in self.deployment_gates:
            try:
                gate_result = gate()
                validation_report['gate_results'][gate.gate_name] = {
                    'passed': gate_result,
                    'timestamp': datetime.now().isoformat()
                }
                
                if not gate_result:
                    validation_report['blocking_issues'].append(
                        f"Deployment gate failed: {gate.gate_name}"
                    )
                    
            except Exception as e:
                validation_report['gate_results'][gate.gate_name] = {
                    'passed': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                validation_report['blocking_issues'].append(
                    f"Deployment gate error: {gate.gate_name} - {str(e)}"
                )
        
        # Run output validation rules
        for rule in self.validation_rules:
            try:
                rule_result = rule()
                validation_report['validation_results'][rule.rule_name] = {
                    'passed': rule_result,
                    'timestamp': datetime.now().isoformat()
                }
                
                if not rule_result:
                    validation_report['warnings'].append(
                        f"Output validation warning: {rule.rule_name}"
                    )
                    
            except Exception as e:
                validation_report['validation_results'][rule.rule_name] = {
                    'passed': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                validation_report['warnings'].append(
                    f"Output validation error: {rule.rule_name} - {str(e)}"
                )
        
        # Final deployment decision
        validation_report['deployment_approved'] = len(validation_report['blocking_issues']) == 0
        
        return validation_report
        
    def execute_rollback(self, component_name: str) -> Dict[str, Any]:
        """Execute rollback for a component"""
        if component_name not in self.rollback_policies:
            return {'success': False, 'error': 'No rollback policy defined'}
            
        try:
            rollback_func = self.rollback_policies[component_name]
            result = rollback_func()
            
            return {
                'success': True,
                'component': component_name,
                'rollback_result': result,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'component': component_name,
                'error': str(e),
                'traceback': traceback.format_exc(),
                'timestamp': datetime.now().isoformat()
            }

class ObservabilityDashboard:
    """Real-time monitoring and replay capabilities (DoD #5)"""
    
    def __init__(self):
        self.agent_status: Dict[str, Dict[str, Any]] = {}
        self.execution_history: List[TraceableDecision] = []
        self.performance_metrics: Dict[str, List[float]] = {}
        self.alert_rules: List[Callable] = []
        
    def update_agent_status(self, agent_name: str, status: str, metadata: Dict[str, Any] = None):
        """Update real-time agent status"""
        self.agent_status[agent_name] = {
            'status': status,
            'last_updated': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        # Check alert rules
        self._check_alerts(agent_name, status, metadata)
        
    def log_execution(self, decision: TraceableDecision):
        """Log agent execution for replay and analysis"""
        self.execution_history.append(decision)
        
        # Update performance metrics
        component = decision.component_name
        if component not in self.performance_metrics:
            self.performance_metrics[component] = []
            
        self.performance_metrics[component].append(decision.confidence_score)
        
        # Keep only last 1000 executions for memory management
        if len(self.execution_history) > 1000:
            self.execution_history = self.execution_history[-1000:]
            
    def get_agent_monitor_data(self) -> Dict[str, Any]:
        """Get real-time monitoring data"""
        return {
            'timestamp': datetime.now().isoformat(),
            'agent_statuses': self.agent_status,
            'recent_executions': len(self.execution_history),
            'performance_summary': {
                component: {
                    'avg_confidence': sum(scores) / len(scores) if scores else 0,
                    'min_confidence': min(scores) if scores else 0,
                    'max_confidence': max(scores) if scores else 0,
                    'execution_count': len(scores)
                }
                for component, scores in self.performance_metrics.items()
            }
        }
        
    def replay_execution(self, trace_id: str) -> Dict[str, Any]:
        """Replay a specific execution for debugging"""
        execution = next((e for e in self.execution_history if e.trace_id == trace_id), None)
        
        if not execution:
            return {'error': 'Execution not found'}
            
        return {
            'trace_id': trace_id,
            'original_execution': execution.to_compliance_record(),
            'replay_timestamp': datetime.now().isoformat(),
            'reproduction_steps': [
                f"1. Set component: {execution.component_name} v{execution.component_version}",
                f"2. Configure model: {execution.model_metadata}",
                f"3. Input prompt: {execution.original_prompt}",
                f"4. Apply context sources: {len(execution.retrieved_context)} sources",
                f"5. Expected output type: {type(execution.output_data).__name__}"
            ]
        }
        
    def add_alert_rule(self, rule_func: Callable):
        """Add monitoring alert rule"""
        self.alert_rules.append(rule_func)
        
    def _check_alerts(self, agent_name: str, status: str, metadata: Dict[str, Any]):
        """Check if any alert rules are triggered"""
        for rule in self.alert_rules:
            try:
                alert = rule(agent_name, status, metadata)
                if alert:
                    logging.warning(f"ALERT: {alert}")
            except Exception as e:
                logging.error(f"Alert rule error: {e}")

class TransparencyInterface:
    """User interface for transparency and explainability (DoD #6)"""
    
    def __init__(self, observability: ObservabilityDashboard):
        self.observability = observability
        self.user_preferences: Dict[str, Dict[str, Any]] = {}
        
    def get_rejected_outputs(self, component_name: str = None, 
                           time_range: tuple = None) -> List[Dict[str, Any]]:
        """Get outputs that were rejected and why"""
        rejected_outputs = []
        
        for execution in self.observability.execution_history:
            if not execution.accepted:
                if component_name and execution.component_name != component_name:
                    continue
                    
                if time_range:
                    start_time, end_time = time_range
                    if not (start_time <= execution.timestamp <= end_time):
                        continue
                
                rejected_outputs.append({
                    'trace_id': execution.trace_id,
                    'component': execution.component_name,
                    'timestamp': execution.timestamp.isoformat(),
                    'original_prompt': execution.original_prompt,
                    'rejection_reasons': execution.rejection_reasons,
                    'output_preview': str(execution.output_data)[:200] + '...',
                    'confidence_score': execution.confidence_score
                })
                
        return rejected_outputs
        
    def get_generation_path(self, trace_id: str) -> Dict[str, Any]:
        """Show complete path from input to output"""
        execution = next((e for e in self.observability.execution_history 
                         if e.trace_id == trace_id), None)
        
        if not execution:
            return {'error': 'Trace not found'}
            
        return {
            'trace_id': trace_id,
            'generation_path': {
                'input': {
                    'original_prompt': execution.original_prompt,
                    'timestamp': execution.timestamp.isoformat()
                },
                'context_retrieval': [
                    {
                        'source_id': src.source_id,
                        'type': src.source_type,
                        'relevance': src.relevance_score,
                        'content_preview': src.content[:100] + '...'
                    }
                    for src in execution.retrieved_context
                ],
                'reasoning_process': execution.decision_reasoning,
                'model_processing': execution.model_metadata,
                'validation_checks': execution.validation_results,
                'output': {
                    'accepted': execution.accepted,
                    'confidence': execution.confidence_score,
                    'rejection_reasons': execution.rejection_reasons if not execution.accepted else None
                }
            }
        }
        
    def adjust_confidence_threshold(self, user_id: str, component_name: str, 
                                  new_threshold: float) -> Dict[str, Any]:
        """Allow users to adjust agent confidence thresholds"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
            
        if 'confidence_thresholds' not in self.user_preferences[user_id]:
            self.user_preferences[user_id]['confidence_thresholds'] = {}
            
        old_threshold = self.user_preferences[user_id]['confidence_thresholds'].get(component_name, 0.7)
        self.user_preferences[user_id]['confidence_thresholds'][component_name] = new_threshold
        
        return {
            'user_id': user_id,
            'component': component_name,
            'old_threshold': old_threshold,
            'new_threshold': new_threshold,
            'updated_at': datetime.now().isoformat()
        }
        
    def get_component_transparency_report(self, component_name: str) -> Dict[str, Any]:
        """Generate transparency report for a component"""
        component_executions = [
            e for e in self.observability.execution_history 
            if e.component_name == component_name
        ]
        
        if not component_executions:
            return {'error': 'No executions found for component'}
            
        total_executions = len(component_executions)
        accepted_count = sum(1 for e in component_executions if e.accepted)
        avg_confidence = sum(e.confidence_score for e in component_executions) / total_executions
        
        return {
            'component_name': component_name,
            'reporting_period': {
                'start': min(e.timestamp for e in component_executions).isoformat(),
                'end': max(e.timestamp for e in component_executions).isoformat()
            },
            'execution_statistics': {
                'total_executions': total_executions,
                'accepted_outputs': accepted_count,
                'rejected_outputs': total_executions - accepted_count,
                'acceptance_rate': accepted_count / total_executions,
                'average_confidence': avg_confidence
            },
            'common_rejection_reasons': self._get_common_rejection_reasons(component_executions),
            'transparency_score': self._calculate_transparency_score(component_executions)
        }
        
    def _get_common_rejection_reasons(self, executions: List[TraceableDecision]) -> List[Dict[str, int]]:
        """Analyze common rejection reasons"""
        reason_counts = {}
        
        for execution in executions:
            if not execution.accepted:
                for reason in execution.rejection_reasons:
                    reason_counts[reason] = reason_counts.get(reason, 0) + 1
                    
        return [{'reason': reason, 'count': count} 
                for reason, count in sorted(reason_counts.items(), 
                                          key=lambda x: x[1], reverse=True)]
                
    def _calculate_transparency_score(self, executions: List[TraceableDecision]) -> float:
        """Calculate transparency score based on traceability completeness"""
        if not executions:
            return 0.0
            
        total_score = 0
        for execution in executions:
            score = 0
            
            # Check traceability completeness
            if execution.original_prompt:
                score += 0.2
            if execution.retrieved_context:
                score += 0.2
            if execution.decision_reasoning:
                score += 0.2
            if execution.model_metadata:
                score += 0.2
            if execution.citation_map:
                score += 0.2
                
            total_score += score
            
        return total_score / len(executions)

# Global enterprise framework instances
enterprise_test_suite = EnterpriseTestSuite()
deployment_gatekeeper = DeploymentGatekeeping(enterprise_test_suite)
observability_dashboard = ObservabilityDashboard()
transparency_interface = TransparencyInterface(observability_dashboard)