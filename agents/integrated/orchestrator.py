"""
Main orchestrator for the integrated multi-agent system
"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List, Tuple

from .cohort_agents import (
    DemographicModeler, ClinicalJourneySimulator, ComorbidityModeler,
    MedicationPlanner, LabGenerator, VitalSignsGenerator
)
from .qa_agents import StatisticalValidator, BiasAuditor, RealismChecker
from .research_agents import (
    LiteratureMiner, OntologyMapper, RealWorldPatternAnalyzer, RegulatoryConstraintChecker
)
from .reporting_agents import (
    FHIRBundleExporter, AuditTrailExplainer, TrustReportWriter, CohortSummaryReporter
)

class IntegratedAgentOrchestrator:
    """Orchestrates the complete multi-agent pipeline with real agent implementations"""
    
    def __init__(self):
        # Initialize all agent instances
        self.cohort_agents = {
            "demographic_modeler": DemographicModeler(),
            "clinical_journey_simulator": ClinicalJourneySimulator(),
            "comorbidity_modeler": ComorbidityModeler(),
            "medication_planner": MedicationPlanner(),
            "lab_generator": LabGenerator(),
            "vital_signs_generator": VitalSignsGenerator()
        }
        
        self.qa_agents = {
            "statistical_validator": StatisticalValidator(),
            "bias_auditor": BiasAuditor(),
            "realism_checker": RealismChecker()
        }
        
        self.research_agents = {
            "literature_miner": LiteratureMiner(),
            "ontology_mapper": OntologyMapper(),
            "real_world_pattern": RealWorldPatternAnalyzer(),
            "regulatory_constraint": RegulatoryConstraintChecker()
        }
        
        self.reporting_agents = {
            "fhir_bundle_exporter": FHIRBundleExporter(),
            "audit_trail_explainer": AuditTrailExplainer(),
            "trust_report_writer": TrustReportWriter(),
            "cohort_summary": CohortSummaryReporter()
        }
        
        self.available_agents = {
            "cohort": list(self.cohort_agents.keys()),
            "qa": list(self.qa_agents.keys()),
            "research": list(self.research_agents.keys()),
            "reporting": list(self.reporting_agents.keys())
        }
    
    async def execute_pipeline(self, job_id: uuid.UUID, request_data: Dict[str, Any], 
                             session=None) -> Dict[str, Any]:
        """Execute the complete multi-agent pipeline with real agents"""
        
        # Initialize pipeline data
        pipeline_data = {
            "job_id": str(job_id),
            "use_case": request_data.get("use_case", "general"),
            "population_size": request_data.get("population_size", 100),
            "condition": request_data.get("condition", "hypertension"),
            "patients": [],
            "encounters": [],
            "lab_results": [],
            "vital_signs": [],
            "validation_results": {},
            "research_insights": {},
            "export_data": {},
            "agent_runs": []
        }
        
        # Determine optimal agent sequence
        agent_sequence = self._build_optimal_sequence(request_data)
        
        # Execute agents in sequence
        for agent_type, agent_name in agent_sequence:
            try:
                result = await self._execute_agent_with_error_handling(
                    agent_type, agent_name, pipeline_data
                )
                
                # Store agent run information
                pipeline_data["agent_runs"].append({
                    "agent_name": agent_name,
                    "agent_type": agent_type,
                    "status": result["metadata"]["status"],
                    "execution_time_ms": int(result["metadata"]["execution_time_seconds"] * 1000),
                    "ran_at": datetime.utcnow()
                })
                
                # Update pipeline data with agent output
                if result["metadata"]["status"] == "success":
                    self._merge_agent_output(pipeline_data, result["output"])
                
            except Exception as e:
                # Log failed execution and continue
                pipeline_data["agent_runs"].append({
                    "agent_name": agent_name,
                    "agent_type": agent_type,
                    "status": "failed",
                    "execution_time_ms": 0,
                    "error": str(e),
                    "ran_at": datetime.utcnow()
                })
                continue
        
        # Generate final summary
        pipeline_data["generation_summary"] = self._generate_pipeline_summary(pipeline_data)
        
        return pipeline_data
    
    def _build_optimal_sequence(self, request_data: Dict[str, Any]) -> List[Tuple[str, str]]:
        """Build optimal agent execution sequence based on request"""
        
        sequence = []
        
        # Phase 1: Research and Evidence Gathering
        sequence.extend([
            ("research", "literature_miner"),
            ("research", "ontology_mapper")
        ])
        
        # Phase 2: Core Data Generation
        sequence.extend([
            ("cohort", "demographic_modeler"),
            ("cohort", "clinical_journey_simulator"),
            ("cohort", "comorbidity_modeler"),
            ("cohort", "medication_planner"),
            ("cohort", "lab_generator"),
            ("cohort", "vital_signs_generator")
        ])
        
        # Phase 3: Quality Assurance
        sequence.extend([
            ("qa", "statistical_validator"),
            ("qa", "bias_auditor"),
            ("qa", "realism_checker")
        ])
        
        # Phase 4: Research Validation
        sequence.extend([
            ("research", "real_world_pattern"),
            ("research", "regulatory_constraint")
        ])
        
        # Phase 5: Reporting and Export
        sequence.extend([
            ("reporting", "cohort_summary"),
            ("reporting", "fhir_bundle_exporter"),
            ("reporting", "trust_report_writer"),
            ("reporting", "audit_trail_explainer")
        ])
        
        return sequence
    
    async def _execute_agent_with_error_handling(self, agent_type: str, agent_name: str, 
                                               pipeline_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent with comprehensive error handling"""
        
        # Get the appropriate agent instance
        agent = self._get_agent_instance(agent_type, agent_name)
        if not agent:
            raise ValueError(f"Agent not found: {agent_type}.{agent_name}")
        
        # Prepare input data for the agent
        agent_input = self._prepare_agent_input(agent_name, pipeline_data)
        
        # Execute agent with timing
        result = agent.execute_with_timing(agent_input)
        
        return result
    
    def _get_agent_instance(self, agent_type: str, agent_name: str):
        """Get the appropriate agent instance"""
        
        agent_collections = {
            "cohort": self.cohort_agents,
            "qa": self.qa_agents,
            "research": self.research_agents,
            "reporting": self.reporting_agents
        }
        
        collection = agent_collections.get(agent_type)
        if collection:
            return collection.get(agent_name)
        
        return None
    
    def _prepare_agent_input(self, agent_name: str, pipeline_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input data specific to each agent's requirements"""
        
        # Base input that all agents receive
        base_input = {
            "job_id": pipeline_data["job_id"],
            "use_case": pipeline_data["use_case"],
            "condition": pipeline_data["condition"],
            "population_size": pipeline_data["population_size"]
        }
        
        # Agent-specific input preparation
        if agent_name in ["demographic_modeler"]:
            return base_input
        
        elif agent_name in ["clinical_journey_simulator", "comorbidity_modeler", "medication_planner"]:
            base_input["patients"] = pipeline_data.get("patients", [])
            return base_input
        
        elif agent_name in ["lab_generator", "vital_signs_generator"]:
            base_input["patients"] = pipeline_data.get("patients", [])
            base_input["encounters"] = pipeline_data.get("encounters", [])
            return base_input
        
        elif agent_name in ["statistical_validator", "bias_auditor", "realism_checker"]:
            base_input["patients"] = pipeline_data.get("patients", [])
            base_input["encounters"] = pipeline_data.get("encounters", [])
            base_input["lab_results"] = pipeline_data.get("lab_results", [])
            base_input["vital_signs"] = pipeline_data.get("vital_signs", [])
            return base_input
        
        elif agent_name in ["literature_miner", "ontology_mapper", "real_world_pattern", "regulatory_constraint"]:
            base_input["patients"] = pipeline_data.get("patients", [])
            base_input["encounters"] = pipeline_data.get("encounters", [])
            return base_input
        
        elif agent_name in ["fhir_bundle_exporter"]:
            base_input["patients"] = pipeline_data.get("patients", [])
            base_input["encounters"] = pipeline_data.get("encounters", [])
            base_input["lab_results"] = pipeline_data.get("lab_results", [])
            base_input["vital_signs"] = pipeline_data.get("vital_signs", [])
            return base_input
        
        elif agent_name in ["trust_report_writer"]:
            base_input["validation_results"] = pipeline_data.get("validation_results", {})
            base_input["bias_audit"] = pipeline_data.get("bias_audit", {})
            base_input["realism_check"] = pipeline_data.get("realism_check", {})
            return base_input
        
        elif agent_name in ["audit_trail_explainer"]:
            base_input["agent_runs"] = pipeline_data.get("agent_runs", [])
            base_input["patients"] = pipeline_data.get("patients", [])
            return base_input
        
        elif agent_name in ["cohort_summary"]:
            base_input["patients"] = pipeline_data.get("patients", [])
            base_input["encounters"] = pipeline_data.get("encounters", [])
            return base_input
        
        return base_input
    
    def _merge_agent_output(self, pipeline_data: Dict[str, Any], agent_output: Dict[str, Any]):
        """Merge agent output into pipeline data"""
        
        # Update patients data
        if "patients" in agent_output:
            pipeline_data["patients"] = agent_output["patients"]
        
        # Update encounters data
        if "encounters" in agent_output:
            pipeline_data["encounters"] = agent_output["encounters"]
        
        # Update lab results
        if "lab_results" in agent_output:
            pipeline_data["lab_results"] = agent_output["lab_results"]
        
        # Update vital signs
        if "vital_signs" in agent_output:
            pipeline_data["vital_signs"] = agent_output["vital_signs"]
        
        # Update validation results
        if "validation_results" in agent_output:
            pipeline_data["validation_results"] = agent_output["validation_results"]
        
        # Update bias audit results
        if "bias_audit" in agent_output:
            pipeline_data["bias_audit"] = agent_output["bias_audit"]
        
        # Update realism check results
        if "realism_check" in agent_output:
            pipeline_data["realism_check"] = agent_output["realism_check"]
        
        # Update literature insights
        if "literature_insights" in agent_output:
            pipeline_data["literature_insights"] = agent_output["literature_insights"]
        
        # Update ontology mappings
        if "ontology_mappings" in agent_output:
            pipeline_data["ontology_mappings"] = agent_output["ontology_mappings"]
        
        # Update export data
        if "fhir_bundle" in agent_output:
            pipeline_data["fhir_bundle"] = agent_output["fhir_bundle"]
        
        # Update trust report
        if "trust_report" in agent_output:
            pipeline_data["trust_report"] = agent_output["trust_report"]
        
        # Update audit trail
        if "audit_trail" in agent_output:
            pipeline_data["audit_trail"] = agent_output["audit_trail"]
        
        # Update cohort summary
        if "cohort_summary" in agent_output:
            pipeline_data["cohort_summary"] = agent_output["cohort_summary"]
    
    def _generate_pipeline_summary(self, pipeline_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive pipeline execution summary"""
        
        agent_runs = pipeline_data.get("agent_runs", [])
        successful_runs = [run for run in agent_runs if run.get("status") == "success"]
        failed_runs = [run for run in agent_runs if run.get("status") == "failed"]
        
        return {
            "execution_summary": {
                "total_agents_executed": len(agent_runs),
                "successful_executions": len(successful_runs),
                "failed_executions": len(failed_runs),
                "success_rate": len(successful_runs) / len(agent_runs) if agent_runs else 0,
                "total_execution_time_ms": sum(run.get("execution_time_ms", 0) for run in agent_runs)
            },
            "data_summary": {
                "patients_generated": len(pipeline_data.get("patients", [])),
                "encounters_generated": len(pipeline_data.get("encounters", [])),
                "lab_results_generated": len(pipeline_data.get("lab_results", [])),
                "vital_signs_generated": len(pipeline_data.get("vital_signs", []))
            },
            "quality_summary": {
                "validation_score": pipeline_data.get("validation_results", {}).get("overall_score", 0.0),
                "bias_score": pipeline_data.get("bias_audit", {}).get("overall_bias_score", 0.0),
                "realism_score": pipeline_data.get("realism_check", {}).get("overall_realism", 0.0),
                "trust_score": pipeline_data.get("trust_report", {}).get("overall_trust_score", 0.0)
            },
            "export_status": {
                "fhir_bundle_ready": "fhir_bundle" in pipeline_data,
                "audit_trail_ready": "audit_trail" in pipeline_data,
                "trust_report_ready": "trust_report" in pipeline_data,
                "summary_report_ready": "cohort_summary" in pipeline_data
            }
        }