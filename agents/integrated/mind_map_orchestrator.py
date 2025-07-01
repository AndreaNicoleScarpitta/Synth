"""
Mind Map Orchestrator with Chain-of-Thought Logging
Advanced orchestration engine that generates detailed reasoning trails and interactive mind maps
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from .orchestrator import IntegratedAgentOrchestrator

@dataclass
class ChainOfThoughtStep:
    """Single step in reasoning chain"""
    step_number: int
    description: str
    inputs_observed: Dict[str, Any]
    hypotheses_considered: List[str]
    decision_criteria: Dict[str, float]
    reasoning: str

@dataclass
class MindMapNode:
    """Node in the execution mind map"""
    id: str
    agent: str
    phase: str
    decision: str
    chain_of_thought: List[str]
    children: List[str]
    timestamp: str
    execution_time_ms: float
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    status: str

class MindMapOrchestrator(IntegratedAgentOrchestrator):
    """Enhanced orchestrator with chain-of-thought logging and mind map generation"""
    
    def __init__(self):
        super().__init__()
        self.mind_map_nodes: Dict[str, MindMapNode] = {}
        self.execution_sequence: List[str] = []
        self.current_phase = "Phase 1: Data Discovery & Profiling"
        
        # Phase definitions
        self.phases = {
            "phase1": "Phase 1: Data Discovery & Profiling",
            "phase2": "Phase 2: Cohort Generation", 
            "phase3": "Phase 3: QA & Statistical Validation",
            "phase4": "Phase 4: Explanation & Reporting"
        }
        
        # Agent to phase mapping
        self.agent_phase_mapping = {
            # Research Agents - Phase 1
            "literature_miner": "phase1",
            "ontology_mapper": "phase1",
            "dataset_profiler": "phase1",
            "literature_synthesizer": "phase1",
            
            # Cohort Construction - Phase 2
            "demographic_modeler": "phase2",
            "clinical_journey_simulator": "phase2",
            "comorbidity_modeler": "phase2",
            "medication_planner": "phase2",
            "lab_generator": "phase2",
            "vital_signs_generator": "phase2",
            
            # QA & Validation - Phase 3
            "statistical_validator": "phase3",
            "bias_auditor": "phase3",
            "realism_checker": "phase3",
            
            # Reporting - Phase 4
            "fhir_bundle_exporter": "phase4",
            "cohort_summary": "phase4",
            "trust_report_writer": "phase4",
            "audit_trail_generator": "phase4"
        }
    
    def log_chain_of_thought(self, agent_name: str, inputs: Dict[str, Any], 
                           hypotheses: List[str], criteria: Dict[str, float],
                           decision: str, reasoning: str) -> str:
        """Log detailed chain of thought for an agent action"""
        
        node_id = f"{agent_name}_{str(uuid.uuid4())[:8]}"
        phase_key = self.agent_phase_mapping.get(agent_name, "phase2")
        phase_name = self.phases[phase_key]
        
        # Build chain of thought steps
        chain_steps = [
            f"Inputs analyzed: {self._summarize_inputs(inputs)}",
            f"Hypotheses considered: {', '.join(hypotheses)}",
            f"Decision criteria applied: {self._format_criteria(criteria)}",
            f"Reasoning: {reasoning}",
            f"Final decision: {decision}"
        ]
        
        # Create mind map node
        node = MindMapNode(
            id=node_id,
            agent=agent_name,
            phase=phase_name,
            decision=decision,
            chain_of_thought=chain_steps,
            children=[],
            timestamp=datetime.utcnow().isoformat(),
            execution_time_ms=0.0,
            inputs=inputs,
            outputs={},
            status="planning"
        )
        
        self.mind_map_nodes[node_id] = node
        self.execution_sequence.append(node_id)
        
        return node_id
    
    def update_node_completion(self, node_id: str, outputs: Dict[str, Any], 
                             execution_time_ms: float, status: str = "completed"):
        """Update node with execution results"""
        if node_id in self.mind_map_nodes:
            node = self.mind_map_nodes[node_id]
            node.outputs = outputs
            node.execution_time_ms = execution_time_ms
            node.status = status
    
    def add_child_relationship(self, parent_id: str, child_id: str):
        """Add parent-child relationship between nodes"""
        if parent_id in self.mind_map_nodes:
            self.mind_map_nodes[parent_id].children.append(child_id)
    
    def get_mind_map_json(self) -> Dict[str, Any]:
        """Generate complete mind map as JSON"""
        
        nodes_json = {}
        for node_id, node in self.mind_map_nodes.items():
            nodes_json[node_id] = {
                "id": node.id,
                "agent": node.agent,
                "phase": node.phase,
                "decision": node.decision,
                "chain_of_thought": node.chain_of_thought,
                "children": node.children,
                "timestamp": node.timestamp,
                "execution_time_ms": node.execution_time_ms,
                "status": node.status
            }
        
        return {
            "mind_map": nodes_json,
            "execution_sequence": self.execution_sequence,
            "phases": self.phases,
            "total_nodes": len(self.mind_map_nodes),
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def get_node_details(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information for a specific node"""
        if node_id not in self.mind_map_nodes:
            return None
        
        node = self.mind_map_nodes[node_id]
        return {
            "node": asdict(node),
            "chain_of_thought": node.chain_of_thought,
            "decision": node.decision,
            "children_count": len(node.children),
            "subtree_nodes": self._get_subtree_nodes(node_id)
        }
    
    def replay_subtree(self, node_id: str) -> List[Dict[str, Any]]:
        """Replay execution of a node's subtree in order"""
        if node_id not in self.mind_map_nodes:
            return []
        
        subtree_nodes = self._get_subtree_nodes(node_id)
        replay_sequence = []
        
        for sub_node_id in subtree_nodes:
            node = self.mind_map_nodes[sub_node_id]
            replay_sequence.append({
                "step": len(replay_sequence) + 1,
                "node_id": sub_node_id,
                "agent": node.agent,
                "phase": node.phase,
                "decision": node.decision,
                "chain_of_thought": node.chain_of_thought,
                "execution_time_ms": node.execution_time_ms
            })
        
        return replay_sequence
    
    def _get_subtree_nodes(self, node_id: str) -> List[str]:
        """Get all nodes in subtree starting from given node"""
        if node_id not in self.mind_map_nodes:
            return []
        
        subtree = [node_id]
        node = self.mind_map_nodes[node_id]
        
        for child_id in node.children:
            subtree.extend(self._get_subtree_nodes(child_id))
        
        return subtree
    
    def _summarize_inputs(self, inputs: Dict[str, Any]) -> str:
        """Create concise summary of inputs"""
        summary_parts = []
        
        if "population_size" in inputs:
            summary_parts.append(f"Population: {inputs['population_size']}")
        if "condition" in inputs:
            summary_parts.append(f"Condition: {inputs['condition']}")
        if "patients" in inputs:
            summary_parts.append(f"Patients: {len(inputs['patients'])}")
        if "encounters" in inputs:
            summary_parts.append(f"Encounters: {len(inputs['encounters'])}")
        
        return ", ".join(summary_parts) if summary_parts else "Basic parameters"
    
    def _format_criteria(self, criteria: Dict[str, float]) -> str:
        """Format decision criteria with weights"""
        return ", ".join([f"{k}: {v:.2f}" for k, v in criteria.items()])
    
    # Override the main generation method to include mind mapping
    async def generate_comprehensive_cohort_with_mindmap(self, job_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced generation with full mind map logging"""
        
        # Start with root node
        root_id = self.log_chain_of_thought(
            agent_name="orchestrator",
            inputs=request_data,
            hypotheses=[
                "Execute standard sequential pipeline",
                "Use parallel processing for independent agents",
                "Apply quality gates at each phase"
            ],
            criteria={
                "data_quality": 0.9,
                "execution_speed": 0.7,
                "resource_efficiency": 0.8
            },
            decision="Execute comprehensive 4-phase pipeline with quality validation",
            reasoning="User requested comprehensive cohort generation with full validation"
        )
        
        self.current_phase = "Phase 1: Data Discovery & Profiling"
        
        # Phase 1: Research and Discovery
        phase1_results = await self._execute_phase1_with_logging(request_data, root_id)
        
        # Phase 2: Cohort Construction
        phase2_results = await self._execute_phase2_with_logging(phase1_results, root_id)
        
        # Phase 3: QA & Validation
        phase3_results = await self._execute_phase3_with_logging(phase2_results, root_id)
        
        # Phase 4: Reporting
        phase4_results = await self._execute_phase4_with_logging(phase3_results, root_id)
        
        # Complete root node
        self.update_node_completion(
            root_id,
            outputs=phase4_results,
            execution_time_ms=5000.0,  # Placeholder
            status="completed"
        )
        
        return {
            "generation_results": phase4_results,
            "mind_map": self.get_mind_map_json(),
            "execution_summary": {
                "total_phases": 4,
                "total_agents": len(self.mind_map_nodes) - 1,  # Exclude orchestrator
                "execution_sequence": self.execution_sequence
            }
        }
    
    async def _execute_phase1_with_logging(self, request_data: Dict[str, Any], parent_id: str) -> Dict[str, Any]:
        """Phase 1 with detailed logging"""
        
        # Literature Mining
        lit_node_id = self.log_chain_of_thought(
            agent_name="literature_miner",
            inputs={"condition": request_data.get("condition", ""), "search_depth": "comprehensive"},
            hypotheses=[
                "Search PubMed for recent clinical studies",
                "Focus on epidemiological data",
                "Include treatment guidelines"
            ],
            criteria={"relevance": 0.9, "recency": 0.8, "study_quality": 0.85},
            decision="Search PubMed with focus on epidemiological patterns and treatment outcomes",
            reasoning="Need current evidence base for realistic synthetic data generation"
        )
        self.add_child_relationship(parent_id, lit_node_id)
        
        # Execute literature mining
        lit_agent = self._get_agent_instance("research", "literature_miner")
        lit_result = lit_agent.execute_with_timing(request_data)
        self.update_node_completion(lit_node_id, lit_result["output"], lit_result["metadata"]["execution_time_seconds"] * 1000)
        
        # Ontology Mapping
        onto_node_id = self.log_chain_of_thought(
            agent_name="ontology_mapper",
            inputs={"literature_findings": lit_result["output"], "target_condition": request_data.get("condition")},
            hypotheses=[
                "Map to SNOMED CT primary codes",
                "Include ICD-10 mappings",
                "Add relevant LOINC codes for labs"
            ],
            criteria={"code_coverage": 0.95, "semantic_accuracy": 0.9, "standard_compliance": 1.0},
            decision="Create comprehensive multi-ontology mapping with SNOMED CT as primary",
            reasoning="Multi-standard mapping ensures broader EHR system compatibility"
        )
        self.add_child_relationship(parent_id, onto_node_id)
        
        # Execute ontology mapping
        onto_agent = self._get_agent_instance("research", "ontology_mapper")
        onto_result = onto_agent.execute_with_timing(lit_result["output"])
        self.update_node_completion(onto_node_id, onto_result["output"], onto_result["metadata"]["execution_time_seconds"] * 1000)
        
        return {
            "literature_findings": lit_result["output"],
            "ontology_mappings": onto_result["output"],
            "phase1_nodes": [lit_node_id, onto_node_id]
        }
    
    async def _execute_phase2_with_logging(self, phase1_results: Dict[str, Any], parent_id: str) -> Dict[str, Any]:
        """Phase 2 with detailed logging"""
        
        # Demographics
        demo_node_id = self.log_chain_of_thought(
            agent_name="demographic_modeler",
            inputs={"population_size": 5, "condition_prevalence": phase1_results["literature_findings"]},
            hypotheses=[
                "Use age-stratified prevalence from literature",
                "Apply realistic gender distribution",
                "Include socioeconomic diversity"
            ],
            criteria={"epidemiological_accuracy": 0.9, "diversity_index": 0.8, "age_realism": 0.95},
            decision="Generate age-stratified cohort with literature-based prevalence patterns",
            reasoning="Literature shows CKD+Diabetes has specific age and gender patterns that must be preserved"
        )
        self.add_child_relationship(parent_id, demo_node_id)
        
        # Execute demographics
        demo_agent = self._get_agent_instance("cohort", "demographic_modeler")
        demo_result = demo_agent.execute_with_timing({
            "population_size": 5,
            "condition": "CKD+Diabetes",
            "literature_context": phase1_results["literature_findings"]
        })
        self.update_node_completion(demo_node_id, demo_result["output"], demo_result["metadata"]["execution_time_seconds"] * 1000)
        
        # Clinical Journey
        journey_node_id = self.log_chain_of_thought(
            agent_name="clinical_journey_simulator",
            inputs={"patients": demo_result["output"]["patients"], "ontology_codes": phase1_results["ontology_mappings"]},
            hypotheses=[
                "Model progressive CKD stages",
                "Include diabetes complications timeline",
                "Generate realistic encounter patterns"
            ],
            criteria={"clinical_realism": 0.9, "progression_accuracy": 0.85, "encounter_frequency": 0.8},
            decision="Create stage-based progression with realistic encounter frequency",
            reasoning="CKD+Diabetes requires careful staging and complication timeline modeling"
        )
        self.add_child_relationship(parent_id, journey_node_id)
        
        # Execute clinical journey
        journey_agent = self._get_agent_instance("cohort", "clinical_journey_simulator")
        journey_result = journey_agent.execute_with_timing({
            "patients": demo_result["output"]["patients"],
            "condition": "CKD+Diabetes",
            "ontology_context": phase1_results["ontology_mappings"]
        })
        self.update_node_completion(journey_node_id, journey_result["output"], journey_result["metadata"]["execution_time_seconds"] * 1000)
        
        return {
            "patients": demo_result["output"]["patients"],
            "encounters": journey_result["output"]["encounters"],
            "phase2_nodes": [demo_node_id, journey_node_id]
        }
    
    async def _execute_phase3_with_logging(self, phase2_results: Dict[str, Any], parent_id: str) -> Dict[str, Any]:
        """Phase 3 with detailed logging"""
        
        # Statistical Validation
        stats_node_id = self.log_chain_of_thought(
            agent_name="statistical_validator",
            inputs={"cohort_data": phase2_results, "validation_targets": ["age_dist", "gender_ratio", "comorbidity_patterns"]},
            hypotheses=[
                "Compare age distribution to population norms",
                "Validate comorbidity co-occurrence rates",
                "Check encounter frequency patterns"
            ],
            criteria={"statistical_significance": 0.95, "effect_size_threshold": 0.3, "clinical_relevance": 0.8},
            decision="Apply comprehensive statistical validation with population comparison",
            reasoning="Need to ensure synthetic cohort matches real-world epidemiological patterns"
        )
        self.add_child_relationship(parent_id, stats_node_id)
        
        # Execute statistical validation
        stats_agent = self._get_agent_instance("qa", "statistical_validator")
        stats_result = stats_agent.execute_with_timing(phase2_results)
        self.update_node_completion(stats_node_id, stats_result["output"], stats_result["metadata"]["execution_time_seconds"] * 1000)
        
        return {
            "cohort_data": phase2_results,
            "validation_results": stats_result["output"],
            "phase3_nodes": [stats_node_id]
        }
    
    async def _execute_phase4_with_logging(self, phase3_results: Dict[str, Any], parent_id: str) -> Dict[str, Any]:
        """Phase 4 with detailed logging"""
        
        # FHIR Export
        fhir_node_id = self.log_chain_of_thought(
            agent_name="fhir_bundle_exporter",
            inputs={"validated_cohort": phase3_results, "export_format": "R4"},
            hypotheses=[
                "Generate FHIR R4 compliant bundles",
                "Include all clinical data elements",
                "Validate against FHIR specifications"
            ],
            criteria={"fhir_compliance": 1.0, "data_completeness": 0.95, "interoperability": 0.9},
            decision="Create fully compliant FHIR R4 bundles with comprehensive data inclusion",
            reasoning="FHIR R4 ensures maximum interoperability with healthcare systems"
        )
        self.add_child_relationship(parent_id, fhir_node_id)
        
        # Execute FHIR export
        fhir_agent = self._get_agent_instance("reporting", "fhir_bundle_exporter")
        fhir_result = fhir_agent.execute_with_timing(phase3_results)
        self.update_node_completion(fhir_node_id, fhir_result["output"], fhir_result["metadata"]["execution_time_seconds"] * 1000)
        
        return {
            "final_cohort": phase3_results["cohort_data"],
            "validation_summary": phase3_results["validation_results"],
            "fhir_bundles": fhir_result["output"],
            "phase4_nodes": [fhir_node_id]
        }

# Demo execution function
def demonstrate_ckd_diabetes_cohort():
    """Demonstrate 5-patient CKD+Diabetes cohort generation with mind mapping"""
    
    orchestrator = MindMapOrchestrator()
    
    # Simulate the request
    request_data = {
        "population_size": 5,
        "condition": "CKD+Diabetes",
        "use_case": "clinical_research",
        "validation_level": "comprehensive"
    }
    
    # Note: This would be async in real implementation
    # For demo, we'll simulate the mind map structure
    
    return {
        "mind_map": {
            "orchestrator_12345678": {
                "id": "orchestrator_12345678",
                "agent": "orchestrator",
                "phase": "Phase 1: Data Discovery & Profiling",
                "decision": "Execute comprehensive 4-phase pipeline with quality validation",
                "chain_of_thought": [
                    "Inputs analyzed: Population: 5, Condition: CKD+Diabetes",
                    "Hypotheses considered: Execute standard sequential pipeline, Use parallel processing for independent agents, Apply quality gates at each phase",
                    "Decision criteria applied: data_quality: 0.90, execution_speed: 0.70, resource_efficiency: 0.80",
                    "Reasoning: User requested comprehensive cohort generation with full validation",
                    "Final decision: Execute comprehensive 4-phase pipeline with quality validation"
                ],
                "children": ["literature_miner_87654321", "ontology_mapper_11223344"],
                "timestamp": "2025-07-01T21:30:00Z",
                "execution_time_ms": 5000.0,
                "status": "completed"
            },
            "literature_miner_87654321": {
                "id": "literature_miner_87654321",
                "agent": "literature_miner",
                "phase": "Phase 1: Data Discovery & Profiling",
                "decision": "Search PubMed with focus on epidemiological patterns and treatment outcomes",
                "chain_of_thought": [
                    "Inputs analyzed: Condition: CKD+Diabetes, search_depth: comprehensive",
                    "Hypotheses considered: Search PubMed for recent clinical studies, Focus on epidemiological data, Include treatment guidelines",
                    "Decision criteria applied: relevance: 0.90, recency: 0.80, study_quality: 0.85",
                    "Reasoning: Need current evidence base for realistic synthetic data generation",
                    "Final decision: Search PubMed with focus on epidemiological patterns and treatment outcomes"
                ],
                "children": ["demographic_modeler_44556677"],
                "timestamp": "2025-07-01T21:30:15Z",
                "execution_time_ms": 1200.0,
                "status": "completed"
            },
            "ontology_mapper_11223344": {
                "id": "ontology_mapper_11223344",
                "agent": "ontology_mapper",
                "phase": "Phase 1: Data Discovery & Profiling",
                "decision": "Create comprehensive multi-ontology mapping with SNOMED CT as primary",
                "chain_of_thought": [
                    "Inputs analyzed: literature_findings: 15 studies, target_condition: CKD+Diabetes",
                    "Hypotheses considered: Map to SNOMED CT primary codes, Include ICD-10 mappings, Add relevant LOINC codes for labs",
                    "Decision criteria applied: code_coverage: 0.95, semantic_accuracy: 0.90, standard_compliance: 1.00",
                    "Reasoning: Multi-standard mapping ensures broader EHR system compatibility",
                    "Final decision: Create comprehensive multi-ontology mapping with SNOMED CT as primary"
                ],
                "children": ["clinical_journey_simulator_99887766"],
                "timestamp": "2025-07-01T21:30:45Z",
                "execution_time_ms": 800.0,
                "status": "completed"
            },
            "demographic_modeler_44556677": {
                "id": "demographic_modeler_44556677",
                "agent": "demographic_modeler",
                "phase": "Phase 2: Cohort Generation",
                "decision": "Generate age-stratified cohort with literature-based prevalence patterns",
                "chain_of_thought": [
                    "Inputs analyzed: Population: 5, condition_prevalence: epidemiological data",
                    "Hypotheses considered: Use age-stratified prevalence from literature, Apply realistic gender distribution, Include socioeconomic diversity",
                    "Decision criteria applied: epidemiological_accuracy: 0.90, diversity_index: 0.80, age_realism: 0.95",
                    "Reasoning: Literature shows CKD+Diabetes has specific age and gender patterns that must be preserved",
                    "Final decision: Generate age-stratified cohort with literature-based prevalence patterns"
                ],
                "children": ["statistical_validator_55667788"],
                "timestamp": "2025-07-01T21:31:00Z",
                "execution_time_ms": 650.0,
                "status": "completed"
            },
            "clinical_journey_simulator_99887766": {
                "id": "clinical_journey_simulator_99887766",
                "agent": "clinical_journey_simulator",
                "phase": "Phase 2: Cohort Generation",
                "decision": "Create stage-based progression with realistic encounter frequency",
                "chain_of_thought": [
                    "Inputs analyzed: Patients: 5, ontology_codes: SNOMED CT mappings",
                    "Hypotheses considered: Model progressive CKD stages, Include diabetes complications timeline, Generate realistic encounter patterns",
                    "Decision criteria applied: clinical_realism: 0.90, progression_accuracy: 0.85, encounter_frequency: 0.80",
                    "Reasoning: CKD+Diabetes requires careful staging and complication timeline modeling",
                    "Final decision: Create stage-based progression with realistic encounter frequency"
                ],
                "children": ["statistical_validator_55667788"],
                "timestamp": "2025-07-01T21:31:30Z",
                "execution_time_ms": 950.0,
                "status": "completed"
            },
            "statistical_validator_55667788": {
                "id": "statistical_validator_55667788",
                "agent": "statistical_validator",
                "phase": "Phase 3: QA & Statistical Validation",
                "decision": "Apply comprehensive statistical validation with population comparison",
                "chain_of_thought": [
                    "Inputs analyzed: cohort_data: 5 patients, 12 encounters, validation_targets: age_dist, gender_ratio, comorbidity_patterns",
                    "Hypotheses considered: Compare age distribution to population norms, Validate comorbidity co-occurrence rates, Check encounter frequency patterns",
                    "Decision criteria applied: statistical_significance: 0.95, effect_size_threshold: 0.30, clinical_relevance: 0.80",
                    "Reasoning: Need to ensure synthetic cohort matches real-world epidemiological patterns",
                    "Final decision: Apply comprehensive statistical validation with population comparison"
                ],
                "children": ["fhir_bundle_exporter_66778899"],
                "timestamp": "2025-07-01T21:32:00Z",
                "execution_time_ms": 750.0,
                "status": "completed"
            },
            "fhir_bundle_exporter_66778899": {
                "id": "fhir_bundle_exporter_66778899",
                "agent": "fhir_bundle_exporter",
                "phase": "Phase 4: Explanation & Reporting",
                "decision": "Create fully compliant FHIR R4 bundles with comprehensive data inclusion",
                "chain_of_thought": [
                    "Inputs analyzed: validated_cohort: 5 patients validated, export_format: R4",
                    "Hypotheses considered: Generate FHIR R4 compliant bundles, Include all clinical data elements, Validate against FHIR specifications",
                    "Decision criteria applied: fhir_compliance: 1.00, data_completeness: 0.95, interoperability: 0.90",
                    "Reasoning: FHIR R4 ensures maximum interoperability with healthcare systems",
                    "Final decision: Create fully compliant FHIR R4 bundles with comprehensive data inclusion"
                ],
                "children": [],
                "timestamp": "2025-07-01T21:32:45Z",
                "execution_time_ms": 600.0,
                "status": "completed"
            }
        },
        "execution_sequence": [
            "orchestrator_12345678",
            "literature_miner_87654321", 
            "ontology_mapper_11223344",
            "demographic_modeler_44556677",
            "clinical_journey_simulator_99887766",
            "statistical_validator_55667788",
            "fhir_bundle_exporter_66778899"
        ],
        "phases": {
            "phase1": "Phase 1: Data Discovery & Profiling",
            "phase2": "Phase 2: Cohort Generation",
            "phase3": "Phase 3: QA & Statistical Validation", 
            "phase4": "Phase 4: Explanation & Reporting"
        },
        "total_nodes": 7,
        "generated_at": "2025-07-01T21:33:00Z"
    }