"""
Enhanced Multi-Agent Orchestrator implementing the comprehensive agentic architecture
with Doer/Coordinator/Adversarial pattern and expert recommendations
"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional

from .enhanced_base_agent import (
    EnhancedBaseAgent, AgentRole, ConcurrencyController, 
    HumanInTheLoopManager, PerformanceMonitor, VersionManager
)

# Import all agent categories
from .cohort_agents_enhanced import *
from .clinical_journey_agents import *
from .data_robustness_agents import *
from .qa_agents_enhanced import *
from .research_agents_enhanced import *
from .reporting_agents_enhanced import *
from .supervision_agents import *

class EnhancedAgentOrchestrator:
    """
    Comprehensive multi-agent orchestrator implementing the updated architecture
    with 18+ specialized agents across 6 major categories
    """
    
    def __init__(self):
        # Core system components
        self.concurrency_controller = ConcurrencyController(max_concurrent_agents=15)
        self.human_reviewer = HumanInTheLoopManager(max_daily_reviews=100)
        self.performance_monitor = PerformanceMonitor()
        self.version_manager = VersionManager()
        
        # Initialize all agent categories with Doer/Coordinator/Adversarial pattern
        self._initialize_all_agents()
        
        # Agent execution sequences
        self.execution_phases = [
            "research_phase",
            "cohort_generation_phase", 
            "data_robustness_phase",
            "qa_validation_phase",
            "explanation_provenance_phase",
            "supervision_phase"
        ]
    
    def _initialize_all_agents(self):
        """Initialize all agents with proper role assignments"""
        
        # 1️⃣ Cohort Constructor Agents
        self.cohort_agents = {
            # Phenotype agents
            "phenotype_assembler": PhenotypeAssembler(),
            "phenotype_coordinator": PhenotypeCoordinator(), 
            "phenotype_edge_case_challenger": PhenotypeEdgeCaseChallenger(),
            
            # Demographic agents
            "demographic_stratifier": DemographicStratifier(),
            "demographic_coordinator": DemographicCoordinator(),
            "demographic_boundary_attacker": DemographicBoundaryAttacker(),
            
            # Comorbidity agents
            "comorbidity_graph_generator": ComorbidityGraphGenerator(),
            "comorbidity_graph_coordinator": ComorbidityGraphCoordinator(),
            "comorbidity_disruptor": ComorbidityDisruptor(),
            
            # Clinical realism certification
            "clinical_realism_certifier": ClinicalRealismCertifier()
        }
        
        # 2️⃣ Clinical Journey Generator Agents
        self.clinical_journey_agents = {
            # Procedure & Encounter agents
            "procedure_encounter_agent": ProcedureEncounterAgent(),
            "encounter_coordinator": EncounterCoordinator(),
            "procedure_contradictor": ProcedureContradictor(),
            
            # Temporal dynamics agents
            "temporal_dynamics_agent": TemporalDynamicsAgent(),
            "temporal_flow_coordinator": TemporalFlowCoordinator(),
            "temporal_chaos_agent": TemporalChaosAgent(),
            
            # Medication pattern agents
            "medication_pattern_agent": MedicationPatternAgent(),
            "medication_regimen_coordinator": MedicationRegimenCoordinator(),
            "adherence_adversary": AdherenceAdversary(),
            
            # Journey realism certification
            "journey_realism_certifier": JourneyRealismCertifier()
        }
        
        # 3️⃣ Data Robustness & Noise Agents
        self.data_robustness_agents = {
            # Missingness & Noise agents
            "missingness_noise_injector": MissingnessNoiseInjector(),
            "missingness_pattern_coordinator": MissingnessPatternCoordinator(),
            "extreme_noise_attacker": ExtremeNoiseAttacker(),
            
            # Variant generation agents
            "variant_generator": VariantGenerator(),
            "variant_coordinator": VariantCoordinator(),
            "variant_outlier_challenger": VariantOutlierChallenger(),
            
            # Adverse event agents
            "adverse_event_agent": AdverseEventAgent(),
            "adverse_event_coordinator": AdverseEventCoordinator(),
            "complication_cascade_attacker": ComplicationCascadeAttacker(),
            
            # Privacy protection
            "differential_privacy_guard": DifferentialPrivacyGuard()
        }
        
        # 4️⃣ QA & Validation Agents
        self.qa_validation_agents = {
            # QA Summary agents
            "qa_summary_reporter": QASummaryReporter(),
            "qa_summary_coordinator": QASummaryCoordinator(),
            "qa_confuser": QAConfuser(),
            
            # Temporal validation agents
            "temporal_validator": TemporalValidator(),
            "temporal_qa_coordinator": TemporalQACoordinator(),
            "timeline_saboteur": TimelineSaboteur(),
            
            # QA Feedback agents
            "qa_feedback_router": QAFeedbackRouter(),
            "feedback_routing_coordinator": FeedbackRoutingCoordinator(),
            "feedback_loop_attacker": FeedbackLoopAttacker(),
            
            # FHIR Export agents
            "qa_fhir_exporter": QAFHIRExporter(),
            "export_coordinator": ExportCoordinator(),
            "fhir_conformance_attacker": FHIRConformanceAttacker(),
            
            # Bias & Fairness agents
            "bias_fairness_monitor": BiasFairnessMonitor(),
            "fairness_audit_coordinator": FairnessAuditCoordinator(),
            "bias_amplifier": BiasAmplifier(),
            
            # Re-identification risk
            "reidentification_risk_monitor": ReidentificationRiskMonitor()
        }
        
        # 5️⃣ Explanation & Provenance Agents
        self.explanation_provenance_agents = {
            # Report generation agents
            "report_generator": ReportGenerator(),
            "report_coordination_agent": ReportCoordinationAgent(),
            "report_saboteur": ReportSaboteur(),
            
            # Ontology mapping agents
            "ontology_mapper": OntologyMapper(),
            "ontology_mapping_coordinator": OntologyMappingCoordinator(),
            "ontology_drift_attacker": OntologyDriftAttacker(),
            "ontology_auto_updater": OntologyAutoUpdater(),
            
            # Dataset profiling agents
            "dataset_profile_agent": DatasetProfileAgent(),
            "profile_summary_coordinator": ProfileSummaryCoordinator(),
            "profile_outlier_challenger": ProfileOutlierChallenger(),
            
            # RAG retrieval agents
            "rag_retriever": RAGRetriever(),
            "rag_query_coordinator": RAGQueryCoordinator(),
            "hallucination_provoker": HallucinationProvoker(),
            "rag_reinforcement_trainer": RAGReinforcementTrainer(),
            
            # Provenance tracking agents
            "provenance_tracker": ProvenanceTracker(),
            "provenance_trail_coordinator": ProvenanceTrailCoordinator(),
            "provenance_breaker": ProvenanceBreaker()
        }
        
        # 6️⃣ Supervisor & Orchestrator Agents
        self.supervision_agents = {
            # Priority routing agents
            "priority_router": PriorityRouter(),
            "priority_flow_coordinator": PriorityFlowCoordinator(),
            "priority_disruptor": PriorityDisruptor(),
            
            # Log aggregation agents
            "log_aggregator": LogAggregator(),
            "log_collection_coordinator": LogCollectionCoordinator(),
            "log_flooder": LogFlooder(),
            
            # Replay management agents
            "replay_manager": ReplayManager(),
            "replay_coordination_agent": ReplayCoordinationAgent(),
            "replay_diverter": ReplayDiverter(),
            
            # Adversarial probe agents
            "adversarial_probe_agent": AdversarialProbeAgent(),
            "adversarial_campaign_coordinator": AdversarialCampaignCoordinator(),
            "chaos_monkey": ChaosMonkey(),
            
            # System management agents
            "concurrency_controller_agent": ConcurrencyControllerAgent(),
            "human_sla_manager": HumanSLAManager(),
            "performance_monitor_agent": PerformanceMonitorAgent()
        }
        
        # Aggregate all agents
        self.all_agents = {
            **self.cohort_agents,
            **self.clinical_journey_agents,
            **self.data_robustness_agents,
            **self.qa_validation_agents,
            **self.explanation_provenance_agents,
            **self.supervision_agents
        }
    
    async def execute_comprehensive_pipeline(self, job_id: uuid.UUID, 
                                           request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete comprehensive pipeline with all phases"""
        
        pipeline_data = {
            "job_id": str(job_id),
            "request_data": request_data,
            "phase_results": {},
            "agent_runs": [],
            "overall_status": "running",
            "started_at": datetime.utcnow().isoformat()
        }
        
        try:
            # Execute all phases in sequence
            for phase_name in self.execution_phases:
                phase_result = await self._execute_phase(phase_name, pipeline_data)
                pipeline_data["phase_results"][phase_name] = phase_result
                
                # Check if phase failed critically
                if phase_result.get("critical_failure", False):
                    pipeline_data["overall_status"] = "failed"
                    pipeline_data["failure_reason"] = f"Critical failure in {phase_name}"
                    break
            
            if pipeline_data["overall_status"] == "running":
                pipeline_data["overall_status"] = "completed"
            
            pipeline_data["completed_at"] = datetime.utcnow().isoformat()
            
            # Generate comprehensive summary
            pipeline_data["execution_summary"] = self._generate_execution_summary(pipeline_data)
            
            return pipeline_data
            
        except Exception as e:
            pipeline_data["overall_status"] = "error"
            pipeline_data["error"] = str(e)
            pipeline_data["completed_at"] = datetime.utcnow().isoformat()
            return pipeline_data
    
    async def _execute_phase(self, phase_name: str, pipeline_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific phase of the pipeline"""
        
        phase_agents = self._get_phase_agents(phase_name)
        phase_result = {
            "phase_name": phase_name,
            "started_at": datetime.utcnow().isoformat(),
            "agent_results": [],
            "phase_status": "running"
        }
        
        # Execute agents in phase
        for agent_name, agent in phase_agents.items():
            try:
                agent_result = await agent.execute_with_full_pipeline(
                    pipeline_data,
                    concurrency_controller=self.concurrency_controller,
                    performance_monitor=self.performance_monitor
                )
                
                phase_result["agent_results"].append({
                    "agent_name": agent_name,
                    "status": agent_result["metadata"]["status"],
                    "execution_time": agent_result["metadata"]["execution_time_seconds"],
                    "role": agent.role.value
                })
                
                # Update pipeline data with agent output
                self._merge_agent_output_to_pipeline(pipeline_data, agent_result)
                
            except Exception as e:
                phase_result["agent_results"].append({
                    "agent_name": agent_name,
                    "status": "failed",
                    "error": str(e),
                    "role": getattr(agent, 'role', AgentRole.DOER).value
                })
        
        phase_result["completed_at"] = datetime.utcnow().isoformat()
        phase_result["phase_status"] = "completed"
        
        return phase_result
    
    def _get_phase_agents(self, phase_name: str) -> Dict[str, EnhancedBaseAgent]:
        """Get agents for a specific phase"""
        
        phase_mapping = {
            "research_phase": {
                **{k: v for k, v in self.explanation_provenance_agents.items() 
                   if "ontology" in k or "rag" in k}
            },
            "cohort_generation_phase": self.cohort_agents,
            "data_robustness_phase": self.data_robustness_agents,
            "qa_validation_phase": self.qa_validation_agents,
            "explanation_provenance_phase": {
                **{k: v for k, v in self.explanation_provenance_agents.items() 
                   if "report" in k or "provenance" in k or "dataset" in k}
            },
            "supervision_phase": self.supervision_agents
        }
        
        return phase_mapping.get(phase_name, {})
    
    def _merge_agent_output_to_pipeline(self, pipeline_data: Dict[str, Any], 
                                      agent_result: Dict[str, Any]):
        """Merge agent output into pipeline data"""
        
        if agent_result["metadata"]["status"] == "success":
            # Merge output data
            if "synthetic_patients" not in pipeline_data:
                pipeline_data["synthetic_patients"] = []
            if "encounters" not in pipeline_data:
                pipeline_data["encounters"] = []
            if "validation_results" not in pipeline_data:
                pipeline_data["validation_results"] = {}
            
            output = agent_result["output"]
            
            # Merge different types of output
            if "patients" in output:
                pipeline_data["synthetic_patients"].extend(output["patients"])
            if "encounters" in output:
                pipeline_data["encounters"].extend(output["encounters"])
            if "validation" in output:
                pipeline_data["validation_results"].update(output["validation"])
        
        # Always record agent run
        pipeline_data["agent_runs"].append({
            "agent_name": agent_result["metadata"]["agent_name"],
            "agent_role": agent_result["metadata"]["agent_role"],
            "status": agent_result["metadata"]["status"],
            "execution_time_ms": int(agent_result["metadata"]["execution_time_seconds"] * 1000),
            "ran_at": agent_result["metadata"]["timestamp"]
        })
    
    def _generate_execution_summary(self, pipeline_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive execution summary"""
        
        total_agents = len(pipeline_data["agent_runs"])
        successful_agents = len([r for r in pipeline_data["agent_runs"] if r["status"] == "success"])
        
        # Calculate execution statistics
        execution_times = [r["execution_time_ms"] for r in pipeline_data["agent_runs"]]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        # Count agents by role
        role_counts = {}
        for agent_run in pipeline_data["agent_runs"]:
            role = agent_run.get("agent_role", "unknown")
            role_counts[role] = role_counts.get(role, 0) + 1
        
        return {
            "total_phases": len(self.execution_phases),
            "completed_phases": len(pipeline_data["phase_results"]),
            "total_agents_executed": total_agents,
            "successful_agents": successful_agents,
            "success_rate_percent": (successful_agents / total_agents * 100) if total_agents > 0 else 0,
            "average_execution_time_ms": avg_execution_time,
            "agent_role_distribution": role_counts,
            "synthetic_patients_generated": len(pipeline_data.get("synthetic_patients", [])),
            "encounters_generated": len(pipeline_data.get("encounters", [])),
            "validation_checks_performed": len(pipeline_data.get("validation_results", {})),
            "pipeline_duration_seconds": self._calculate_pipeline_duration(pipeline_data)
        }
    
    def _calculate_pipeline_duration(self, pipeline_data: Dict[str, Any]) -> float:
        """Calculate total pipeline duration"""
        
        try:
            started_at = datetime.fromisoformat(pipeline_data["started_at"].replace('Z', '+00:00'))
            completed_at = datetime.fromisoformat(pipeline_data.get("completed_at", datetime.utcnow().isoformat()).replace('Z', '+00:00'))
            return (completed_at - started_at).total_seconds()
        except:
            return 0.0
    
    def get_agent_architecture_overview(self) -> Dict[str, Any]:
        """Get comprehensive overview of the agent architecture"""
        
        return {
            "architecture_version": "comprehensive_agentic_v2.0",
            "total_agents": len(self.all_agents),
            "agent_categories": {
                "cohort_constructor": {
                    "count": len(self.cohort_agents),
                    "agents": list(self.cohort_agents.keys()),
                    "description": "Define who the patients are - phenotypes, demographics, comorbidities"
                },
                "clinical_journey_generator": {
                    "count": len(self.clinical_journey_agents),
                    "agents": list(self.clinical_journey_agents.keys()),
                    "description": "Define patient history over time - procedures, temporal dynamics, medications"
                },
                "data_robustness_noise": {
                    "count": len(self.data_robustness_agents),
                    "agents": list(self.data_robustness_agents.keys()),
                    "description": "Add realistic messiness - missingness, variants, adverse events"
                },
                "qa_validation": {
                    "count": len(self.qa_validation_agents),
                    "agents": list(self.qa_validation_agents.keys()),
                    "description": "Validate, correct, certify - QA summaries, temporal validation, bias monitoring"
                },
                "explanation_provenance": {
                    "count": len(self.explanation_provenance_agents),
                    "agents": list(self.explanation_provenance_agents.keys()),
                    "description": "Make data explainable, auditable - reports, ontology mapping, RAG, provenance"
                },
                "supervision_orchestration": {
                    "count": len(self.supervision_agents),
                    "agents": list(self.supervision_agents.keys()),
                    "description": "Manage entire lifecycle - priority routing, logging, replay, adversarial testing"
                }
            },
            "execution_phases": self.execution_phases,
            "key_features": [
                "Version pinning for reproducibility",
                "Concurrency management with deadlock prevention", 
                "Differential privacy and re-identification protection",
                "Human-in-the-loop SLA management",
                "Clinical realism certification",
                "Automated ontology updates",
                "RAG hallucination reduction",
                "Performance monitoring and benchmarking",
                "Comprehensive adversarial testing",
                "Full provenance and audit trails"
            ]
        }