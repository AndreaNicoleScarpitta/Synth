"""
Langflow-based orchestration for the integrated multi-agent system
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from .orchestrator import IntegratedAgentOrchestrator

class LangflowOrchestrator(IntegratedAgentOrchestrator):
    """Extended orchestrator with Langflow-based visual workflow support"""
    
    def __init__(self):
        super().__init__()
        self.flow_definitions = {}
        self.active_flows = {}
        
    def register_flow(self, flow_name: str, flow_definition: Dict[str, Any]):
        """Register a new Langflow-based workflow"""
        self.flow_definitions[flow_name] = {
            "definition": flow_definition,
            "created_at": datetime.utcnow(),
            "version": "1.0"
        }
    
    async def execute_langflow_pipeline(self, flow_name: str, job_id: uuid.UUID, 
                                      request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a pipeline using Langflow-defined workflow"""
        
        if flow_name not in self.flow_definitions:
            raise ValueError(f"Flow '{flow_name}' not found")
        
        flow_def = self.flow_definitions[flow_name]["definition"]
        
        # Initialize flow execution context
        flow_context = {
            "job_id": str(job_id),
            "flow_name": flow_name,
            "request_data": request_data,
            "nodes": flow_def.get("nodes", []),
            "edges": flow_def.get("edges", []),
            "execution_state": {},
            "completed_nodes": set(),
            "failed_nodes": set(),
            "agent_runs": []
        }
        
        # Execute flow using topological sort of nodes
        execution_order = self._calculate_execution_order(flow_def)
        
        for node_id in execution_order:
            try:
                result = await self._execute_flow_node(node_id, flow_context)
                flow_context["execution_state"][node_id] = result
                flow_context["completed_nodes"].add(node_id)
                
                # Check if we should continue based on conditions
                if not self._should_continue_execution(node_id, result, flow_context):
                    break
                    
            except Exception as e:
                flow_context["failed_nodes"].add(node_id)
                flow_context["execution_state"][node_id] = {"error": str(e)}
                
                # Check if this is a critical failure
                if self._is_critical_node(node_id, flow_def):
                    break
        
        return self._generate_flow_results(flow_context)
    
    def _calculate_execution_order(self, flow_def: Dict[str, Any]) -> List[str]:
        """Calculate topological execution order from flow definition"""
        
        nodes = {node["id"]: node for node in flow_def.get("nodes", [])}
        edges = flow_def.get("edges", [])
        
        # Build dependency graph
        dependencies = {node_id: set() for node_id in nodes.keys()}
        for edge in edges:
            target = edge["target"]
            source = edge["source"]
            dependencies[target].add(source)
        
        # Topological sort
        execution_order = []
        ready_nodes = [node_id for node_id, deps in dependencies.items() if not deps]
        
        while ready_nodes:
            current = ready_nodes.pop(0)
            execution_order.append(current)
            
            # Remove current node from dependencies
            for node_id, deps in dependencies.items():
                if current in deps:
                    deps.remove(current)
                    if not deps and node_id not in execution_order:
                        ready_nodes.append(node_id)
        
        return execution_order
    
    async def _execute_flow_node(self, node_id: str, flow_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single node in the flow"""
        
        nodes = {node["id"]: node for node in flow_context["nodes"]}
        node = nodes[node_id]
        
        node_type = node.get("type", "unknown")
        node_data = node.get("data", {})
        
        if node_type == "agent":
            return await self._execute_agent_node(node_data, flow_context)
        elif node_type == "condition":
            return await self._execute_condition_node(node_data, flow_context)
        elif node_type == "data_transform":
            return await self._execute_transform_node(node_data, flow_context)
        elif node_type == "parallel_group":
            return await self._execute_parallel_group(node_data, flow_context)
        else:
            return {"status": "skipped", "reason": f"Unknown node type: {node_type}"}
    
    async def _execute_agent_node(self, node_data: Dict[str, Any], flow_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an agent node"""
        
        agent_type = node_data.get("agent_type")
        agent_name = node_data.get("agent_name")
        agent_config = node_data.get("config", {})
        
        # Get input data from previous nodes
        input_data = self._prepare_agent_input_from_flow(agent_name, flow_context)
        
        # Apply node-specific configuration
        input_data.update(agent_config)
        
        # Execute the agent
        agent = self._get_agent_instance(agent_type, agent_name)
        if not agent:
            raise ValueError(f"Agent not found: {agent_type}.{agent_name}")
        
        result = agent.execute_with_timing(input_data)
        
        # Store agent execution in flow context
        flow_context["agent_runs"].append({
            "agent_name": agent_name,
            "agent_type": agent_type,
            "status": result["metadata"]["status"],
            "execution_time_ms": int(result["metadata"]["execution_time_seconds"] * 1000),
            "ran_at": datetime.utcnow()
        })
        
        return result
    
    async def _execute_condition_node(self, node_data: Dict[str, Any], flow_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a conditional branching node"""
        
        condition_type = node_data.get("condition_type", "quality_threshold")
        threshold = node_data.get("threshold", 0.8)
        metric_path = node_data.get("metric_path", "validation_results.overall_score")
        
        # Extract the metric value from execution state
        metric_value = self._extract_metric_from_context(metric_path, flow_context)
        
        if condition_type == "quality_threshold":
            condition_met = metric_value >= threshold
        elif condition_type == "patient_count":
            condition_met = metric_value >= threshold
        elif condition_type == "bias_check":
            condition_met = metric_value <= threshold  # Lower bias is better
        else:
            condition_met = True  # Default pass-through
        
        return {
            "status": "completed",
            "condition_met": condition_met,
            "metric_value": metric_value,
            "threshold": threshold
        }
    
    async def _execute_transform_node(self, node_data: Dict[str, Any], flow_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a data transformation node"""
        
        transform_type = node_data.get("transform_type", "pass_through")
        
        if transform_type == "filter_patients":
            criteria = node_data.get("criteria", {})
            return self._filter_patients(criteria, flow_context)
        elif transform_type == "enhance_data":
            enhancement = node_data.get("enhancement", {})
            return self._enhance_patient_data(enhancement, flow_context)
        elif transform_type == "aggregate_metrics":
            return self._aggregate_quality_metrics(flow_context)
        else:
            return {"status": "completed", "transform": "pass_through"}
    
    async def _execute_parallel_group(self, node_data: Dict[str, Any], flow_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute multiple agents in parallel"""
        
        parallel_agents = node_data.get("agents", [])
        
        # Create tasks for parallel execution
        tasks = []
        for agent_config in parallel_agents:
            task = self._execute_agent_node(agent_config, flow_context)
            tasks.append(task)
        
        # Execute in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        successful_results = []
        failed_results = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed_results.append({
                    "agent": parallel_agents[i].get("agent_name", f"agent_{i}"),
                    "error": str(result)
                })
            else:
                successful_results.append(result)
        
        return {
            "status": "completed",
            "parallel_execution": True,
            "successful_count": len(successful_results),
            "failed_count": len(failed_results),
            "results": successful_results,
            "failures": failed_results
        }
    
    def _should_continue_execution(self, node_id: str, result: Dict[str, Any], flow_context: Dict[str, Any]) -> bool:
        """Determine if execution should continue based on node result"""
        
        # Check for critical failures
        if result.get("status") == "error":
            return False
        
        # Check conditional nodes
        if result.get("condition_met") is False:
            return False
        
        # Check quality thresholds
        quality_score = result.get("quality_score", 1.0)
        if quality_score < 0.3:  # Very low quality
            return False
        
        return True
    
    def _is_critical_node(self, node_id: str, flow_def: Dict[str, Any]) -> bool:
        """Check if a node is marked as critical for execution"""
        
        nodes = {node["id"]: node for node in flow_def.get("nodes", [])}
        node = nodes.get(node_id, {})
        
        return node.get("data", {}).get("critical", False)
    
    def _extract_metric_from_context(self, metric_path: str, flow_context: Dict[str, Any]) -> float:
        """Extract a metric value from the execution context using dot notation"""
        
        # Navigate through nested dictionary using dot notation
        parts = metric_path.split(".")
        current = flow_context["execution_state"]
        
        try:
            for part in parts:
                if isinstance(current, dict):
                    current = current.get(part, {})
                elif isinstance(current, list) and part.isdigit():
                    current = current[int(part)]
                else:
                    return 0.0
            
            return float(current) if isinstance(current, (int, float)) else 0.0
        except (KeyError, ValueError, IndexError):
            return 0.0
    
    def _filter_patients(self, criteria: Dict[str, Any], flow_context: Dict[str, Any]) -> Dict[str, Any]:
        """Filter patients based on criteria"""
        
        # This would filter patients from the execution state
        # Implementation depends on your specific patient data structure
        return {
            "status": "completed",
            "filter_applied": criteria,
            "patients_filtered": 0  # Placeholder
        }
    
    def _enhance_patient_data(self, enhancement: Dict[str, Any], flow_context: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance patient data with additional attributes"""
        
        return {
            "status": "completed",
            "enhancement_applied": enhancement,
            "patients_enhanced": 0  # Placeholder
        }
    
    def _aggregate_quality_metrics(self, flow_context: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate quality metrics from multiple nodes"""
        
        metrics = {}
        for node_id, result in flow_context["execution_state"].items():
            if "validation_results" in result:
                metrics[node_id] = result["validation_results"]
        
        return {
            "status": "completed",
            "aggregated_metrics": metrics,
            "overall_quality": sum(m.get("overall_score", 0) for m in metrics.values()) / len(metrics) if metrics else 0
        }
    
    def _prepare_agent_input_from_flow(self, agent_name: str, flow_context: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare agent input based on flow execution state"""
        
        # Start with base input
        base_input = {
            "job_id": flow_context["job_id"],
            "use_case": flow_context["request_data"].get("use_case", "langflow_execution"),
            "condition": flow_context["request_data"].get("condition", "general"),
            "population_size": flow_context["request_data"].get("population_size", 100)
        }
        
        # Add data from previous successful nodes
        execution_state = flow_context["execution_state"]
        
        # Extract patients, encounters, etc. from completed nodes
        for node_result in execution_state.values():
            if isinstance(node_result, dict) and "output" in node_result:
                output = node_result["output"]
                if "patients" in output:
                    base_input["patients"] = output["patients"]
                if "encounters" in output:
                    base_input["encounters"] = output["encounters"]
                if "lab_results" in output:
                    base_input["lab_results"] = output["lab_results"]
                if "vital_signs" in output:
                    base_input["vital_signs"] = output["vital_signs"]
        
        return base_input
    
    def _generate_flow_results(self, flow_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final results from flow execution"""
        
        return {
            "flow_name": flow_context["flow_name"],
            "job_id": flow_context["job_id"],
            "completed_nodes": list(flow_context["completed_nodes"]),
            "failed_nodes": list(flow_context["failed_nodes"]),
            "agent_runs": flow_context["agent_runs"],
            "execution_state": flow_context["execution_state"],
            "generation_summary": {
                "total_nodes_executed": len(flow_context["completed_nodes"]),
                "successful_nodes": len(flow_context["completed_nodes"]),
                "failed_nodes": len(flow_context["failed_nodes"]),
                "success_rate": len(flow_context["completed_nodes"]) / 
                              (len(flow_context["completed_nodes"]) + len(flow_context["failed_nodes"])) 
                              if (flow_context["completed_nodes"] or flow_context["failed_nodes"]) else 0
            }
        }

# Predefined Langflow templates
LANGFLOW_TEMPLATES = {
    "comprehensive_ehr": {
        "name": "Comprehensive EHR Generation",
        "description": "Full pipeline with all agent categories",
        "nodes": [
            {"id": "research_start", "type": "agent", "data": {"agent_type": "research", "agent_name": "literature_miner"}},
            {"id": "ontology", "type": "agent", "data": {"agent_type": "research", "agent_name": "ontology_mapper"}},
            {"id": "demographics", "type": "agent", "data": {"agent_type": "cohort", "agent_name": "demographic_modeler"}},
            {"id": "clinical_journey", "type": "agent", "data": {"agent_type": "cohort", "agent_name": "clinical_journey_simulator"}},
            {"id": "quality_check", "type": "condition", "data": {"condition_type": "quality_threshold", "threshold": 0.7}},
            {"id": "validation_parallel", "type": "parallel_group", "data": {
                "agents": [
                    {"agent_type": "qa", "agent_name": "statistical_validator"},
                    {"agent_type": "qa", "agent_name": "bias_auditor"},
                    {"agent_type": "qa", "agent_name": "realism_checker"}
                ]
            }},
            {"id": "export", "type": "agent", "data": {"agent_type": "reporting", "agent_name": "fhir_bundle_exporter"}}
        ],
        "edges": [
            {"source": "research_start", "target": "ontology"},
            {"source": "ontology", "target": "demographics"},
            {"source": "demographics", "target": "clinical_journey"},
            {"source": "clinical_journey", "target": "quality_check"},
            {"source": "quality_check", "target": "validation_parallel"},
            {"source": "validation_parallel", "target": "export"}
        ]
    },
    
    "rapid_prototyping": {
        "name": "Rapid Prototyping Flow",
        "description": "Minimal pipeline for quick iterations",
        "nodes": [
            {"id": "demographics", "type": "agent", "data": {"agent_type": "cohort", "agent_name": "demographic_modeler"}},
            {"id": "encounters", "type": "agent", "data": {"agent_type": "cohort", "agent_name": "clinical_journey_simulator"}},
            {"id": "basic_validation", "type": "agent", "data": {"agent_type": "qa", "agent_name": "statistical_validator"}},
            {"id": "export", "type": "agent", "data": {"agent_type": "reporting", "agent_name": "cohort_summary"}}
        ],
        "edges": [
            {"source": "demographics", "target": "encounters"},
            {"source": "encounters", "target": "basic_validation"},
            {"source": "basic_validation", "target": "export"}
        ]
    },
    
    "quality_focused": {
        "name": "Quality-Focused Pipeline",
        "description": "Emphasis on validation and quality assurance",
        "nodes": [
            {"id": "demographics", "type": "agent", "data": {"agent_type": "cohort", "agent_name": "demographic_modeler"}},
            {"id": "clinical_data", "type": "parallel_group", "data": {
                "agents": [
                    {"agent_type": "cohort", "agent_name": "clinical_journey_simulator"},
                    {"agent_type": "cohort", "agent_name": "comorbidity_modeler"},
                    {"agent_type": "cohort", "agent_name": "medication_planner"}
                ]
            }},
            {"id": "comprehensive_qa", "type": "parallel_group", "data": {
                "agents": [
                    {"agent_type": "qa", "agent_name": "statistical_validator"},
                    {"agent_type": "qa", "agent_name": "bias_auditor"},
                    {"agent_type": "qa", "agent_name": "realism_checker"}
                ]
            }},
            {"id": "quality_gate", "type": "condition", "data": {"condition_type": "quality_threshold", "threshold": 0.85}},
            {"id": "trust_report", "type": "agent", "data": {"agent_type": "reporting", "agent_name": "trust_report_writer"}}
        ],
        "edges": [
            {"source": "demographics", "target": "clinical_data"},
            {"source": "clinical_data", "target": "comprehensive_qa"},
            {"source": "comprehensive_qa", "target": "quality_gate"},
            {"source": "quality_gate", "target": "trust_report"}
        ]
    }
}