"""
Integrated multi-agent system for comprehensive synthetic EHR generation
"""

from .base_agent import BaseIntegratedAgent
from .orchestrator import IntegratedAgentOrchestrator

from .cohort_agents import (
    DemographicModeler,
    ClinicalJourneySimulator, 
    ComorbidityModeler,
    MedicationPlanner,
    LabGenerator,
    VitalSignsGenerator
)

from .qa_agents import (
    StatisticalValidator,
    BiasAuditor,
    RealismChecker
)

from .research_agents import (
    LiteratureMiner,
    OntologyMapper,
    RealWorldPatternAnalyzer,
    RegulatoryConstraintChecker
)

from .reporting_agents import (
    FHIRBundleExporter,
    AuditTrailExplainer,
    TrustReportWriter,
    CohortSummaryReporter
)

__all__ = [
    "BaseIntegratedAgent",
    "IntegratedAgentOrchestrator",
    "DemographicModeler",
    "ClinicalJourneySimulator", 
    "ComorbidityModeler",
    "MedicationPlanner",
    "LabGenerator",
    "VitalSignsGenerator",
    "StatisticalValidator",
    "BiasAuditor",
    "RealismChecker",
    "LiteratureMiner",
    "OntologyMapper",
    "RealWorldPatternAnalyzer",
    "RegulatoryConstraintChecker",
    "FHIRBundleExporter",
    "AuditTrailExplainer",
    "TrustReportWriter",
    "CohortSummaryReporter"
]