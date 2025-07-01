# pipeline/runner.py

import logging
import sys
import datetime
import argparse

from .config import load_config
from .metrics import MetricCollector
from .fallback import SnapshotFallback
from .exporter import JSONLinesExporter

from .services.phase1_service import run_phase1
from .services.phase2_service import run_phase2
from .services.phase3_service import run_phase3
from .services.phase4_service import run_phase4

# --- Phase 1 – Research Agents ---
from agents.research.competitor_scan import CompetitorScanAgent
from agents.research.regulatory_constraint import RegulatoryConstraintAgent
from agents.research.literature_miner import LiteratureMiner
from agents.research.meta_reasoner import MetaReasoner

# --- Phase 2 – Cohort Construction Agents ---
from agents.cohort.phenotype_assembler import PhenotypeAssembler
from agents.cohort.clinical_journey_simulator import ClinicalJourneyBuilder
from agents.cohort.demographic_modeler import DemographicStratifier
from agents.cohort.comorbidity_modeler import ComorbidityGraphGenerator
from agents.cohort.medication_planner import MedicationSuggester
from agents.cohort.procedure_planner import ProcedureGenerator
from agents.cohort.temporal_synthesizer import TemporalDynamics
from agents.cohort.variant_generator import VariantGenerator
from agents.cohort.adverse_event_modeler import AdverseEventGenerator
from agents.cohort.noise_injector import NoiseInjector
from agents.cohort.note_generator import NoteGenerator
from agents.cohort.format_mapper import FormatMapper
from agents.cohort.narrative_validator import NarrativeValidator

# --- Phase 3 – QA Agents ---
from agents.qa.bias_auditor import BiasAuditor
from agents.qa.label_verifier import LabelVerifier
from agents.qa.outlier_detector import OutlierDetector
from agents.qa.patient_scorecard import PatientScorecard
from agents.qa.qa_orchestrator import QAOrchestrator
from agents.qa.realism_checker import RealismChecker
from agents.qa.schema_validator import SchemaValidator
from agents.qa.statistical_validator import StatisticalValidator
from agents.qa.fix_recommender import FixRecommender

# --- Phase 4 – Reporting Agents ---
from agents.reporting.audit_trail_explainer import AuditTrailExplainer
from agents.reporting.cohort_summary import CohortSummary
from agents.reporting.csv_flatten_adapter import CSVFlattenAdapter
from agents.reporting.format_output_reconstructor import FormatOutputReconstructor
from agents.reporting.format_validator import FormatValidator
from agents.reporting.process_lineage_graph import ProcessLineageGraph
from agents.reporting.regulatory_evidence_writer import RegulatoryEvidence
from agents.reporting.report_orchestrator import ReportOrchestrator
from agents.reporting.trust_report_writer import TrustNarrative
from agents.reporting.trust_report_writer import TrustReportWriter


class PipelineRunner:
    def __init__(self, config_path: str):
        self.config = load_config(config_path)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s"
        )
        self.logger = logging.getLogger(__name__)

        self.metrics = MetricCollector()
        self.fallback = SnapshotFallback()

        self.retry_params = {
            "max_retries": self.config.get("max_retries", 3),
            "initial_backoff": self.config.get("initial_backoff", 1),
            "backoff_factor": self.config.get("backoff_factor", 2),
        }

        # --- Phase 1 ---
        self.phase1_agents = [
            CompetitorScanAgent(),
            RegulatoryConstraintAgent(),
            LiteratureMiner(),
            MetaReasoner()
        ]

        # --- Phase 2 ---
        self.phase2_map = {
            "PhenotypeAssembler": PhenotypeAssembler("PhenotypeAssembler"),
            "ClinicalJourneyBuilder": ClinicalJourneyBuilder("ClinicalJourneyBuilder"),
            "DemographicStratifier": DemographicStratifier("DemographicStratifier"),
            "ComorbidityGraphGenerator": ComorbidityGraphGenerator("ComorbidityGraphGenerator"),
            "MedicationSuggester": MedicationSuggester("MedicationSuggester"),
            "ProcedureGenerator": ProcedureGenerator("ProcedureGenerator"),
            "TemporalDynamics": TemporalDynamics("TemporalDynamics"),
            "VariantGenerator": VariantGenerator("VariantGenerator"),
            "AdverseEventGenerator": AdverseEventGenerator("AdverseEventGenerator"),
            "NoiseInjector": NoiseInjector("NoiseInjector"),
            "NoteGenerator": NoteGenerator("NoteGenerator"),
            "FormatMapper": FormatMapper("FormatMapper"),
            "NarrativeValidator": NarrativeValidator()  # intentionally no name
        }

        # --- Phase 3 ---
        self.phase3_agents = [
            BiasAuditor("BiasAuditor"),
            LabelVerifier("LabelVerifier"),
            OutlierDetector("OutlierDetector"),
            PatientScorecard(),
            QAOrchestrator(),
            RealismChecker("RealismChecker"),
            SchemaValidator(),
            StatisticalValidator("StatisticalValidator"),
            FixRecommender()
]


# Phase 4 – Reporting & Export
        self.phase4_agents = [
            AuditTrailExplainer("AuditTrailExplainer"),
            CohortSummary("CohortSummary"),
            CSVFlattenAdapter("CSVFlattenAdapter"),
            FormatOutputReconstructor("FormatOutputReconstructor"),
            FormatValidator("FormatValidator"),
            ProcessLineageGraph("ProcessLineageGraph"),
            RegulatoryEvidence("RegulatoryEvidence"),
            ReportOrchestrator("ReportOrchestrator"),
            TrustNarrative("TrustNarrative"),
            TrustReportWriter("TrustReportWriter"),
        ]

    def run(self, dry_run=False):
        self.logger.info("Starting pipeline...")

        p1 = run_phase1(
            self.phase1_agents,
            self.config,
            self.metrics,
            self.logger,
            self.fallback,
            self.retry_params
        )

        if dry_run:
            self.logger.info("Dry run complete after Phase 1.")
            return

        p2 = run_phase2(
            self.phase2_map,
            p1,
            self.metrics,
            self.logger,
            self.retry_params
        )

        raw3, qa_metrics = run_phase3(
            self.phase3_agents,
            p2,
            {
                "realism": self.config.get("realism_threshold"),
                "privacy": self.config.get("privacy_threshold"),
                "bias": self.config.get("bias_threshold")
            },
            self.logger
        )

        exporter = JSONLinesExporter(self.config["output_path"])
        final_out = run_phase4(self.phase4_agents, {**p1, **p2, **raw3}, exporter, self.logger)

        total = (
            datetime.datetime.utcnow() -
            self.metrics.data.get("start_time", datetime.datetime.utcnow())
        ).total_seconds()
        self.logger.info(f"Pipeline complete in {total:.1f} seconds.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Synthetic Ascension pipeline")
    parser.add_argument("--config", required=True, help="Path to JSON config file")
    parser.add_argument("--dry-run", action="store_true", help="Only run Phase 1")
    args = parser.parse_args()

    runner = PipelineRunner(args.config)
    runner.run(dry_run=args.dry_run)
