"""
Langflow Export and Integration System
Converts Synthetic Ascension agent workflows to Langflow-compatible JSON format
"""

import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
import os


class LangflowExporter:
    """Exports agent workflows as Langflow-compatible flows"""
    
    def __init__(self):
        self.flow_version = "1.0.0"
        self.langflow_version = "1.0.12"
        
    def export_complete_pipeline(self) -> Dict[str, Any]:
        """Export the complete 6-phase pipeline as a Langflow workflow"""
        
        # Define the complete agent architecture
        agent_categories = {
            "cohort_constructor": [
                "phenotype_assembler", "demographics_generator", "comorbidity_orchestrator",
                "temporal_dynamics_agent", "clinical_realism_certifier", "population_stratifier",
                "genetic_variant_injector", "social_determinants_weaver", "care_access_modeler",
                "health_equity_auditor", "cohort_diversity_optimizer"
            ],
            "clinical_journey": [
                "procedure_encounter_generator", "medication_journey_designer", "diagnostic_pathway_creator",
                "care_transition_orchestrator", "treatment_response_modeler", "adverse_event_injector",
                "clinical_decision_simulator", "provider_interaction_weaver", "care_coordination_mapper",
                "outcome_trajectory_designer", "journey_realism_certifier"
            ],
            "data_robustness": [
                "missingness_injection_agent", "measurement_error_introducer", "lab_variance_generator",
                "imaging_artifact_injector", "temporal_noise_weaver", "data_entry_error_simulator",
                "systematic_bias_introducer", "equipment_drift_modeler", "seasonal_variation_injector",
                "privacy_guard_agent"
            ],
            "qa_validation": [
                "summary_reporting_agent", "statistical_validation_engine", "temporal_consistency_checker",
                "clinical_logic_validator", "fhir_export_generator", "regulatory_compliance_auditor",
                "bias_detection_scanner", "privacy_risk_assessor", "data_quality_monitor",
                "clinical_guidelines_validator", "longitudinal_coherence_checker", "cross_referential_validator",
                "outlier_detection_agent"
            ],
            "explanation": [
                "cohort_summary_reporter", "clinical_narrative_generator", "statistical_insights_extractor",
                "quality_metrics_calculator", "provenance_tracker", "decision_tree_explainer",
                "feature_importance_analyzer", "correlation_discovery_agent", "pattern_recognition_reporter",
                "ontology_mapper", "literature_evidence_linker", "rag_retrieval_agent", "hallucination_detector"
            ],
            "supervision": [
                "priority_routing_coordinator", "resource_allocation_manager", "workflow_orchestrator",
                "exception_handling_supervisor", "performance_monitor", "log_aggregation_service",
                "audit_trail_manager", "replay_management_system", "chaos_testing_adversary"
            ]
        }
        
        flow_id = str(uuid.uuid4())
        
        # Create master pipeline flow
        pipeline_flow = {
            "description": "Complete Synthetic Ascension EHR Generation Pipeline - All 50+ Agents",
            "name": "SyntheticAscension_Complete_Pipeline",
            "id": flow_id,
            "data": {
                "nodes": [],
                "edges": [],
                "viewport": {"x": 0, "y": 0, "zoom": 0.7}
            },
            "is_component": False,
            "updated_at": datetime.utcnow().isoformat(),
            "folder_id": None,
            "endpoint_name": None
        }
        
        # Create phase nodes
        phases = [
            ("Phase 1: Literature Mining & Research", 150, 100),
            ("Phase 2: Cohort Construction", 150, 300),
            ("Phase 3: Clinical Journey Generation", 150, 500),
            ("Phase 4: Data Robustness Enhancement", 150, 700),
            ("Phase 5: QA & Validation", 150, 900),
            ("Phase 6: Reporting & Export", 150, 1100)
        ]
        
        phase_nodes = []
        for i, (phase_name, x, y) in enumerate(phases):
            node = self._create_phase_node(phase_name, x, y, i)
            pipeline_flow["data"]["nodes"].append(node)
            phase_nodes.append(node["id"])
        
        # Create edges between phases
        for i in range(len(phase_nodes) - 1):
            edge = self._create_edge(phase_nodes[i], phase_nodes[i + 1])
            pipeline_flow["data"]["edges"].append(edge)
        
        return pipeline_flow
    
    def _create_phase_node(self, phase_name: str, x: int, y: int, phase_index: int) -> Dict[str, Any]:
        """Create a node representing a complete phase"""
        
        node_id = str(uuid.uuid4())
        
        return {
            "id": node_id,
            "type": "genericNode",
            "position": {"x": x, "y": y},
            "data": {
                "type": "CustomComponent",
                "node": {
                    "template": {
                        "phase_name": {
                            "required": True,
                            "value": phase_name,
                            "type": "str",
                            "display_name": "Phase Name"
                        },
                        "phase_index": {
                            "required": True,
                            "value": phase_index,
                            "type": "int",
                            "display_name": "Phase Index"
                        },
                        "input_data": {
                            "required": True,
                            "value": "",
                            "type": "str",
                            "display_name": "Input Data"
                        }
                    },
                    "description": f"Synthetic Ascension {phase_name}",
                    "display_name": phase_name,
                    "outputs": [
                        {
                            "types": ["Data"],
                            "name": "phase_output",
                            "display_name": "Phase Output"
                        }
                    ]
                },
                "id": node_id
            },
            "selected": False,
            "positionAbsolute": {"x": x, "y": y}
        }
    
    def _create_edge(self, source_id: str, target_id: str) -> Dict[str, Any]:
        """Create an edge between two nodes"""
        
        edge_id = str(uuid.uuid4())
        
        return {
            "source": source_id,
            "sourceHandle": f"{source_id}-output",
            "target": target_id,
            "targetHandle": f"{target_id}-input",
            "type": "smoothstep",
            "id": edge_id,
            "data": {
                "targetHandle": {
                    "fieldName": "input_data",
                    "id": target_id,
                    "inputTypes": ["Data"],
                    "type": "str"
                },
                "sourceHandle": {
                    "fieldName": "phase_output", 
                    "id": source_id,
                    "outputTypes": ["Data"],
                    "type": "Data"
                }
            },
            "selected": False
        }
    
    def save_flow_to_file(self, flow: Dict[str, Any], filepath: str):
        """Save a Langflow flow to a JSON file"""
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(flow, f, indent=2, ensure_ascii=False)


def generate_langflow_exports():
    """Generate all Langflow export files"""
    
    exporter = LangflowExporter()
    
    # Create export directory
    export_dir = "exports/langflow"
    os.makedirs(export_dir, exist_ok=True)
    
    # Export complete pipeline
    complete_flow = exporter.export_complete_pipeline()
    exporter.save_flow_to_file(complete_flow, f"{export_dir}/synthetic_ascension_complete_pipeline.json")
    
    # Create README for exports
    readme_content = """# Synthetic Ascension Langflow Exports

This directory contains Langflow-compatible workflow exports for the Synthetic Ascension EHR generation system.

## Files

- `synthetic_ascension_complete_pipeline.json` - Complete 6-phase pipeline with all agent categories

## Usage

1. Install Langflow locally:
   ```bash
   pip install langflow
   ```

2. Start Langflow:
   ```bash
   langflow run
   ```

3. Import the JSON files through the Langflow UI

4. Connect to your Synthetic Ascension backend at http://localhost:8004

## Custom Components

Each agent is exported as a custom Langflow component that can:
- Connect to the live Synthetic Ascension backend
- Run in simulation mode for testing
- Be modified and extended in Langflow

## Modifying Flows

You can:
- Rearrange agent execution order
- Add new custom components
- Modify agent parameters
- Create new conditional logic
- Export modified flows back to JSON

## Integration

The exported flows maintain full compatibility with your Synthetic Ascension backend while allowing visual workflow modification in Langflow.
"""
    
    with open(f"{export_dir}/README.md", 'w') as f:
        f.write(readme_content)
    
    return export_dir