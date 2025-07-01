// Medical field help content for complex healthcare data fields
export const medicalFieldHelp = {
  // Organization & Use Case Fields
  currentEhrSystem: {
    title: "Current EHR System",
    content: "Electronic Health Record (EHR) system your organization currently uses for patient data management. This helps us understand integration requirements and data migration needs.",
    examples: [
      "Epic Systems",
      "Cerner (Oracle Health)",
      "allscripts",
      "athenahealth",
      "eClinicalWorks",
      "Custom/In-house system"
    ]
  },
  
  useCases: {
    title: "Primary Use Cases",
    content: "Specific applications where you plan to use synthetic EHR data. This helps us customize the data generation to match your research or development needs.",
    examples: [
      "AI/ML model training for diagnostic algorithms",
      "Clinical decision support system development", 
      "Population health analytics and research",
      "Drug discovery and pharmaceutical research",
      "Healthcare software testing and validation",
      "Medical device development and testing"
    ]
  },

  // Medical Specialties & Data Types
  medicalSpecialties: {
    title: "Medical Specialties",
    content: "Clinical specialties or medical domains where you need synthetic patient data. Each specialty has unique data patterns and clinical workflows.",
    examples: [
      "Cardiology (heart conditions, ECGs, cardiac procedures)",
      "Oncology (cancer treatments, chemotherapy protocols)",
      "Pediatrics (childhood diseases, growth charts)",
      "Psychiatry (mental health conditions, therapy notes)",
      "Emergency Medicine (trauma cases, acute care)",
      "Endocrinology (diabetes, hormone disorders)"
    ]
  },

  dataComplexity: {
    title: "Data Complexity Level",
    content: "The sophistication and clinical accuracy required for your synthetic patient data. Higher complexity includes more realistic co-morbidities, medication interactions, and longitudinal care patterns.",
    examples: [
      "Basic: Simple demographics and common diagnoses",
      "Intermediate: Multiple conditions with realistic progression",
      "Advanced: Complex multi-system diseases with specialist care",
      "Research-grade: Publication-ready data with statistical validation"
    ]
  },

  // Clinical Data Requirements
  patientVolume: {
    title: "Patient Volume Requirements",
    content: "Number of synthetic patient records needed for your project. Volume affects statistical power, model training effectiveness, and research validity.",
    examples: [
      "Small pilot: 1,000 - 10,000 patients",
      "Standard research: 10,000 - 100,000 patients", 
      "Large-scale study: 100,000 - 1,000,000 patients",
      "Enterprise deployment: 1,000,000+ patients"
    ]
  },

  timeRange: {
    title: "Clinical Time Range",
    content: "Historical period covered by synthetic patient data. Affects seasonal patterns, medication availability, and clinical practice evolution.",
    examples: [
      "Recent: Last 2-3 years (current practices)",
      "Medium-term: Last 5-10 years (practice evolution)",
      "Long-term: 10+ years (longitudinal studies)",
      "Multi-generational: 20+ years (population trends)"
    ]
  },

  // Technical & Compliance Requirements
  dataFormats: {
    title: "Required Data Formats",
    content: "Technical formats needed for data delivery and system integration. Different formats support different use cases and compliance requirements.",
    examples: [
      "FHIR R4 (modern interoperability standard)",
      "HL7 v2.x (legacy system integration)",
      "CSV/Excel (analysis and research)",
      "JSON/XML (web applications and APIs)",
      "DICOM (medical imaging data)",
      "Custom database schemas"
    ]
  },

  complianceRequirements: {
    title: "Compliance & Regulatory Requirements",
    content: "Healthcare regulations and standards that your synthetic data must meet. Critical for clinical research, FDA submissions, and international deployments.",
    examples: [
      "HIPAA (US healthcare privacy)",
      "GDPR (EU data protection)",
      "FDA 21 CFR Part 11 (electronic records)",
      "ISO 13485 (medical device quality)",
      "ICH GCP (clinical trial standards)",
      "Local healthcare regulations"
    ]
  },

  // Research & Analytics
  studyPopulation: {
    title: "Target Study Population",
    content: "Demographic and clinical characteristics of the patient population you need to study. Ensures representative and statistically valid synthetic cohorts.",
    examples: [
      "Pediatric cancer patients (0-18 years)",
      "Elderly with multiple chronic conditions (65+ years)",
      "Pregnant women with gestational diabetes",
      "Adults with rare genetic disorders",
      "Multi-ethnic urban population",
      "Rural underserved communities"
    ]
  },

  clinicalOutcomes: {
    title: "Clinical Outcomes of Interest",
    content: "Specific medical events, treatments, or health metrics you want to analyze. Drives the clinical realism and statistical properties of synthetic data.",
    examples: [
      "Treatment response rates and efficacy",
      "Adverse drug reactions and safety profiles",
      "Hospital readmission risk factors",
      "Disease progression and survival curves",
      "Quality of life measurements",
      "Healthcare utilization patterns"
    ]
  },

  // Integration & Technical
  integrationRequirements: {
    title: "System Integration Requirements", 
    content: "Technical specifications for how synthetic data will connect with your existing healthcare IT infrastructure and workflows.",
    examples: [
      "Real-time API integration with EHR",
      "Batch data loading into data warehouse",
      "Cloud-based analytics platform connection",
      "On-premises secure data environment",
      "Multi-site research network integration",
      "Vendor-neutral data exchange formats"
    ]
  },

  qualityMetrics: {
    title: "Data Quality & Validation Metrics",
    content: "Statistical and clinical measures used to ensure synthetic data meets research and regulatory standards for authenticity and utility.",
    examples: [
      "Statistical distribution matching (p-values, effect sizes)",
      "Clinical correlation validation (comorbidity patterns)",
      "Temporal consistency checks (care progressions)",
      "Demographic representativeness (census alignment)",
      "Rare event frequency validation",
      "Expert clinical review and approval"
    ]
  }
};

// Helper function to get field help
export const getFieldHelp = (fieldKey) => {
  return medicalFieldHelp[fieldKey] || null;
};

// Grouped field help for different contexts
export const fieldHelpGroups = {
  basic: ['currentEhrSystem', 'useCases', 'patientVolume'],
  clinical: ['medicalSpecialties', 'dataComplexity', 'timeRange', 'studyPopulation'],
  technical: ['dataFormats', 'integrationRequirements', 'complianceRequirements'],
  research: ['clinicalOutcomes', 'qualityMetrics']
};