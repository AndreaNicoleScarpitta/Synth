import React, { useState } from 'react'

// Progress tracking component
const ProgressBar = ({ progress, currentStep, steps }) => {
  return (
    <div style={{ width: '100%', margin: '20px 0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span style={{ fontSize: '14px', fontWeight: '500', color: '#374151' }}>
          {currentStep}
        </span>
        <span style={{ fontSize: '14px', color: '#6b7280' }}>
          {Math.round(progress)}%
        </span>
      </div>
      <div style={{
        width: '100%',
        height: '8px',
        backgroundColor: '#e5e7eb',
        borderRadius: '4px',
        overflow: 'hidden'
      }}>
        <div style={{
          width: `${progress}%`,
          height: '100%',
          backgroundColor: '#3b82f6',
          borderRadius: '4px',
          transition: 'width 0.3s ease'
        }} />
      </div>
      <div style={{ marginTop: '8px', fontSize: '12px', color: '#6b7280' }}>
        {steps.find(step => step.active)?.description || 'Processing...'}
      </div>
    </div>
  );
};

// Custom Multi-Select Component
const MultiSelectDropdown = ({ label, options, placeholder = "Select options...", emoji = "" }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedItems, setSelectedItems] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredOptions = options.filter(option => 
    option.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const toggleOption = (option) => {
    setSelectedItems(prev => 
      prev.includes(option) 
        ? prev.filter(item => item !== option)
        : [...prev, option]
    );
  };

  const removeItem = (item) => {
    setSelectedItems(prev => prev.filter(i => i !== item));
  };

  return (
    <div style={{ position: 'relative', width: '100%' }}>
      <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151' }}>
        {emoji} {label}
      </label>
      
      {/* Selected Items Display */}
      {selectedItems.length > 0 && (
        <div style={{ 
          marginBottom: '8px', 
          display: 'flex', 
          flexWrap: 'wrap', 
          gap: '6px',
          maxHeight: '80px',
          overflowY: 'auto'
        }}>
          {selectedItems.map(item => (
            <span 
              key={item}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                padding: '4px 8px',
                backgroundColor: '#dbeafe',
                color: '#1d4ed8',
                borderRadius: '16px',
                fontSize: '12px',
                gap: '4px'
              }}
            >
              {item}
              <button
                onClick={() => removeItem(item)}
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#1d4ed8',
                  cursor: 'pointer',
                  fontSize: '14px',
                  padding: '0',
                  lineHeight: '1'
                }}
              >
                ×
              </button>
            </span>
          ))}
        </div>
      )}
      
      {/* Dropdown Trigger */}
      <div
        onClick={() => setIsOpen(!isOpen)}
        style={{
          width: '100%',
          padding: '12px',
          border: '1px solid #d1d5db',
          borderRadius: '6px',
          backgroundColor: 'white',
          cursor: 'pointer',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        <span style={{ color: selectedItems.length > 0 ? '#374151' : '#9ca3af' }}>
          {selectedItems.length > 0 ? `${selectedItems.length} selected` : placeholder}
        </span>
        <span style={{ transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }}>
          ▼
        </span>
      </div>

      {/* Dropdown Menu */}
      {isOpen && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: '0',
          right: '0',
          backgroundColor: 'white',
          border: '1px solid #d1d5db',
          borderRadius: '6px',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
          zIndex: 1000,
          maxHeight: '200px',
          overflow: 'hidden'
        }}>
          {/* Search Input */}
          <div style={{ padding: '12px', borderBottom: '1px solid #e5e7eb' }}>
            <input
              type="text"
              placeholder="Search options..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                width: '100%',
                padding: '8px',
                border: '1px solid #d1d5db',
                borderRadius: '4px',
                fontSize: '14px'
              }}
            />
          </div>
          
          {/* Options List */}
          <div style={{ maxHeight: '150px', overflowY: 'auto' }}>
            {filteredOptions.map(option => (
              <div
                key={option}
                onClick={() => toggleOption(option)}
                style={{
                  padding: '10px 12px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  backgroundColor: selectedItems.includes(option) ? '#f3f4f6' : 'white',
                  borderBottom: '1px solid #f3f4f6'
                }}
                onMouseEnter={(e) => e.target.style.backgroundColor = '#f9fafb'}
                onMouseLeave={(e) => e.target.style.backgroundColor = selectedItems.includes(option) ? '#f3f4f6' : 'white'}
              >
                <input
                  type="checkbox"
                  checked={selectedItems.includes(option)}
                  onChange={() => {}}
                  style={{ margin: '0' }}
                />
                <span style={{ fontSize: '14px' }}>{option}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    minHeight: '100vh',
    background: '#ffffff',
    fontFamily: 'Inter, system-ui, sans-serif'
  },
  header: {
    position: 'fixed' as const,
    top: 0,
    left: 0,
    right: 0,
    zIndex: 50,
    background: 'rgba(255, 255, 255, 0.98)',
    backdropFilter: 'blur(10px)',
    borderBottom: '1px solid #f1f5f9',
    boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)'
  },
  nav: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 24px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    height: '64px'
  },
  logo: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px'
  },
  logoIcon: {
    width: '32px',
    height: '32px',
    borderRadius: '6px',
    background: 'linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: 'white',
    fontWeight: 'bold',
    fontSize: '14px'
  },
  logoText: {
    fontWeight: '600',
    fontSize: '20px',
    color: '#0f172a'
  },
  status: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    fontSize: '14px',
    color: '#6b7280'
  },
  statusDot: {
    width: '8px',
    height: '8px',
    backgroundColor: '#06b6d4',
    borderRadius: '50%',
    animation: 'pulse 2s infinite'
  },
  main: {
    paddingTop: '64px'
  },
  hero: {
    position: 'relative' as const,
    overflow: 'hidden',
    padding: '80px 24px 64px'
  },
  heroContent: {
    maxWidth: '1200px',
    margin: '0 auto',
    textAlign: 'center' as const
  },
  heroTitle: {
    fontSize: '56px',
    fontWeight: '700',
    color: '#0f172a',
    marginBottom: '24px',
    lineHeight: '1.1',
    textAlign: 'center' as const,
    letterSpacing: '-0.02em'
  },
  heroSubtitle: {
    fontSize: '24px',
    fontWeight: '500',
    color: '#0ea5e9',
    marginBottom: '32px',
    maxWidth: '800px',
    margin: '0 auto 32px',
    letterSpacing: '0.05em'
  },
  heroDescription: {
    fontSize: '18px',
    color: '#475569',
    marginBottom: '48px',
    maxWidth: '680px',
    margin: '0 auto 48px',
    lineHeight: '1.6'
  },
  heroStats: {
    display: 'flex',
    justifyContent: 'center',
    gap: '48px',
    marginBottom: '40px',
    flexWrap: 'wrap' as const
  },
  statItem: {
    textAlign: 'center' as const
  },
  statNumber: {
    fontSize: '32px',
    fontWeight: '700',
    color: '#0f172a',
    display: 'block'
  },
  statLabel: {
    fontSize: '13px',
    color: '#64748b',
    textTransform: 'uppercase' as const,
    letterSpacing: '0.05em',
    fontWeight: '500'
  },
  buttonContainer: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '16px',
    justifyContent: 'center',
    marginBottom: '64px'
  },
  primaryButton: {
    background: '#0ea5e9',
    color: 'white',
    padding: '14px 28px',
    borderRadius: '6px',
    fontWeight: '500',
    border: 'none',
    cursor: 'pointer',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
    transition: 'all 0.2s',
    fontSize: '16px'
  },
  secondaryButton: {
    border: '1px solid #cbd5e1',
    color: '#475569',
    padding: '14px 28px',
    borderRadius: '6px',
    fontWeight: '500',
    background: 'white',
    cursor: 'pointer',
    transition: 'all 0.2s',
    fontSize: '16px'
  },
  features: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '80px 24px'
  },
  featuresHeader: {
    textAlign: 'center' as const,
    marginBottom: '64px'
  },
  featuresTitle: {
    fontSize: '32px',
    fontWeight: '600',
    color: '#0f172a',
    marginBottom: '16px'
  },
  featuresSubtitle: {
    fontSize: '18px',
    color: '#475569',
    maxWidth: '800px',
    margin: '0 auto'
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '32px'
  },
  card: {
    background: 'white',
    borderRadius: '8px',
    padding: '28px',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
    border: '1px solid #f1f5f9',
    transition: 'all 0.3s'
  },
  cardIcon: {
    width: '48px',
    height: '48px',
    borderRadius: '12px',
    marginBottom: '16px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  },
  cardTitle: {
    fontSize: '20px',
    fontWeight: '600',
    marginBottom: '8px',
    color: '#1f2937'
  },
  cardDescription: {
    color: '#6b7280',
    lineHeight: '1.6'
  },
  cta: {
    background: '#f8fafc',
    color: '#0f172a',
    padding: '80px 24px',
    borderTop: '1px solid #e2e8f0'
  },
  ctaContent: {
    maxWidth: '1200px',
    margin: '0 auto',
    textAlign: 'center' as const
  },
  ctaTitle: {
    fontSize: '36px',
    fontWeight: 'bold',
    marginBottom: '24px'
  },
  ctaSubtitle: {
    fontSize: '20px',
    marginBottom: '32px',
    maxWidth: '600px',
    margin: '0 auto 32px',
    opacity: 0.9
  },
  ctaButton: {
    background: '#0ea5e9',
    color: 'white',
    padding: '14px 28px',
    borderRadius: '6px',
    fontWeight: '500',
    border: 'none',
    cursor: 'pointer',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
    fontSize: '16px'
  }
}

const features = [
  {
    title: "Synthetic Patient Generation",
    description: "Create realistic patient cohorts with complex medical histories, demographics, and clinical pathways.",
    color: "#0ea5e9"
  },
  {
    title: "Privacy-First Architecture", 
    description: "HIPAA-compliant synthetic data generation with zero risk of patient privacy exposure.",
    color: "#06b6d4"
  },
  {
    title: "AI-Powered Validation",
    description: "Advanced statistical validation and bias detection to ensure data quality and representativeness.",
    color: "#0284c7"
  },
  {
    title: "Clinical Accuracy",
    description: "Medically precise synthetic records that maintain clinical integrity and diagnostic consistency.",
    color: "#0891b2"
  },
  {
    title: "Scalable Infrastructure",
    description: "Generate cohorts from hundreds to millions of patients with enterprise-grade performance.",
    color: "#0e7490"
  },
  {
    title: "Research Ready",
    description: "Pre-configured templates for clinical trials, drug discovery, and healthcare AI development.",
    color: "#155e75"
  }
]

function AppContent() {
  const [currentView, setCurrentView] = useState('landing')
  const [isGenerating, setIsGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  const [currentStep, setCurrentStep] = useState('')
  const [generationSteps, setGenerationSteps] = useState([])
  const [generationResults, setGenerationResults] = useState(null)
  const [selectedConfigurations, setSelectedConfigurations] = useState({
    populationSize: '',
    cardiacConditions: [],
    hematologicConditions: [],
    demographics: [],
    geneticMarkers: [],
    labParameters: [],
    dataTypes: [],
    procedureTypes: [],
    medications: [],
    specialtyFocus: []
  })

  const handleLaunchDemo = () => {
    setCurrentView('demo')
    // Update URL for unique demo access
    window.history.pushState({}, '', '/demo')
  }

  const handleEnterprisePartnership = () => {
    setCurrentView('enterprise')
    window.history.pushState({}, '', '/enterprise')
  }

  const handleStartDemo = () => {
    setCurrentView('demo')
    window.history.pushState({}, '', '/demo')
  }

  const handleBackToLanding = () => {
    setCurrentView('landing')
    window.history.pushState({}, '', '/')
  }

  const handleGenerateDataset = async () => {
    setIsGenerating(true)
    setProgress(0)
    setGenerationResults(null)
    
    const steps = [
      { id: 'config', name: 'Validating Configuration', description: 'Analyzing selected parameters and validating medical logic', active: true },
      { id: 'literature', name: 'Literature Retrieval', description: 'Searching medical databases for relevant research and clinical guidelines', active: false },
      { id: 'schema', name: 'EHR Schema Generation', description: 'Creating comprehensive medical record structures with proper coding', active: false },
      { id: 'patients', name: 'Patient Data Synthesis', description: 'Generating realistic patient cohorts with authentic clinical data', active: false },
      { id: 'validation', name: 'Medical Validation', description: 'Running clinical validation and bias detection algorithms', active: false },
      { id: 'export', name: 'Data Preparation', description: 'Preparing datasets for export with audit trails', active: false },
      { id: 'complete', name: 'Generation Complete', description: 'Synthetic dataset ready with full documentation', active: false }
    ]
    
    setGenerationSteps(steps)
    
    try {
      // Step 1: Configuration Validation
      setCurrentStep('Validating Configuration...')
      setProgress(5)
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Step 2: Literature Retrieval
      steps[0].active = false
      steps[1].active = true
      setGenerationSteps([...steps])
      setCurrentStep('Searching Medical Literature...')
      setProgress(15)
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Step 3: EHR Schema Generation
      steps[1].active = false
      steps[2].active = true
      setGenerationSteps([...steps])
      setCurrentStep('Building EHR Schema...')
      setProgress(30)
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Step 4: Patient Data Synthesis
      steps[2].active = false
      steps[3].active = true
      setGenerationSteps([...steps])
      setCurrentStep('Generating Patient Cohorts...')
      setProgress(45)
      
      // Simulate the enhanced agentic API for demo
      const response = {
        ok: true,
        json: async () => ({
          workflow_id: 'demo-workflow-' + Date.now(),
          status: 'completed',
          summary: {
            total_patients: parseInt(selectedConfigurations.populationSize?.match(/\d+/)?.[0] || '500'),
            cardiac_conditions_included: selectedConfigurations.cardiacConditions || ['Tetralogy of Fallot'],
            hematologic_conditions_included: selectedConfigurations.hematologicConditions || ['Iron Deficiency Anemia'],
            demographics_breakdown: {
              gender_distribution: { 'Female': 245, 'Male': 255 },
              ethnicity_distribution: { 'Hispanic or Latino': 125, 'Not Hispanic or Latino': 375 }
            },
            clinical_data_generated: {
              lab_parameters: selectedConfigurations.labParameters || ['Complete Blood Count (CBC)', 'Ferritin & Iron Studies'],
              procedure_types: selectedConfigurations.procedureTypes || ['Cardiac Catheterization'],
              data_modalities: selectedConfigurations.dataTypes || ['Lab Results', 'Clinical Notes']
            },
            literature_foundation: {
              papers_reviewed: 15,
              clinical_guidelines: 3,
              evidence_strength: 'High'
            },
            data_quality_metrics: {
              completeness: 0.94,
              consistency: 0.96,
              validity: 0.95,
              uniqueness: 1.0
            }
          },
          agentic_pipeline_results: {
            literature_retrieval: {
              sources_found: 15,
              relevant_papers: [
                {
                  title: "Pediatric Iron Deficiency Anemia: Clinical Guidelines and Treatment Protocols",
                  authors: "Smith, J.A., et al.",
                  journal: "Pediatric Hematology Review",
                  year: 2023,
                  relevance_score: 0.94
                },
                {
                  title: "Hemodynamic Assessment in Tetralogy of Fallot: Modern Approaches", 
                  authors: "Johnson, M.D., et al.",
                  journal: "Pediatric Cardiology",
                  year: 2023,
                  relevance_score: 0.91
                }
              ]
            },
            medical_validation: {
              clinical_consistency_score: 0.96,
              bias_detection_results: {
                gender_balance: "Within acceptable range (49% F, 51% M)",
                ethnic_diversity: "Representative distribution achieved"
              }
            }
          }
        })
      }

      // Alternative: Use the real API when it's working
      // const response = await fetch('http://localhost:8000/api/generate-cohort', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify({
      //     population_size: selectedConfigurations.populationSize || 'Medium Cohort (100-500 patients)',
      //     cardiac_conditions: selectedConfigurations.cardiacConditions || [],
      //     hematologic_conditions: selectedConfigurations.hematologicConditions || [],
      //     demographics: selectedConfigurations.demographics || [],
      //     genetic_markers: selectedConfigurations.geneticMarkers || [],
      //     lab_parameters: selectedConfigurations.labParameters || [],
      //     data_types: selectedConfigurations.dataTypes || [],
      //     procedure_types: selectedConfigurations.procedureTypes || [],
      //     medications: selectedConfigurations.medications || [],
      //     specialty_focus: selectedConfigurations.specialtyFocus || [],
      //     use_case: 'Cardiac Hematology Simulation (Pediatric & Adolescent)',
      //     data_complexity: 'high',
      //     validation_rigor: 'research_grade',
      //     timeline_coverage: 'longitudinal_pediatric'
      //   })
      // })
      
      setProgress(70)
      
      // Step 5: Medical Validation
      steps[3].active = false
      steps[4].active = true
      setGenerationSteps([...steps])
      setCurrentStep('Running Medical Validation...')
      setProgress(80)
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Step 6: Data Preparation
      steps[4].active = false
      steps[5].active = true
      setGenerationSteps([...steps])
      setCurrentStep('Preparing Export Package...')
      setProgress(90)
      
      const results = await response.json()
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Step 7: Complete
      steps[5].active = false
      steps[6].active = true
      setGenerationSteps([...steps])
      setCurrentStep('Generation Complete!')
      setProgress(100)
      
      setGenerationResults(results)
      
      // Navigate to results after a brief pause
      setTimeout(() => {
        setCurrentView('results')
        setIsGenerating(false)
        window.history.pushState({}, '', '/results')
      }, 1500)
      
    } catch (error) {
      console.error('Generation failed:', error)
      setCurrentStep('Generation Failed')
      setIsGenerating(false)
    }
  }

  // Handle browser back/forward buttons
  React.useEffect(() => {
    const handlePopState = () => {
      const path = window.location.pathname
      if (path === '/demo') {
        setCurrentView('demo')
      } else if (path === '/enterprise') {
        setCurrentView('enterprise')
      } else if (path === '/results') {
        setCurrentView('results')
      } else {
        setCurrentView('landing')
      }
    }

    window.addEventListener('popstate', handlePopState)
    return () => window.removeEventListener('popstate', handlePopState)
  }, [])

  if (currentView === 'results') {
    return <ResultsOverview results={generationResults} onBackToDemo={() => {
      setCurrentView('demo')
      window.history.pushState({}, '', '/demo')
    }} />
  }

  if (currentView === 'demo') {
    return (
      <div style={styles.container}>
        <header style={styles.header}>
          <nav style={styles.nav}>
            <div style={styles.logo}>
              <div style={styles.logoIcon}>SA</div>
              <span style={styles.logoText}>Synthetic Ascension</span>
            </div>
            <button 
              style={{...styles.secondaryButton, padding: '8px 16px', fontSize: '14px'}} 
              onClick={handleBackToLanding}
            >
              ← Back to Home
            </button>
          </nav>
        </header>
        
        <main style={styles.main}>
          <section style={styles.hero}>
            <div style={styles.heroContent}>
              <h1 style={{...styles.heroTitle, fontSize: '48px'}}>Interactive Demo</h1>
              <p style={styles.heroSubtitle}>Configure Your Synthetic EHR Generation</p>
              <p style={styles.heroDescription}>
                Explore the power of Synthetic Ascension by customizing patient cohorts, 
                medical specialties, and research parameters in real-time.
              </p>
              
              <div style={{maxWidth: '800px', margin: '48px auto'}}>
                
                {/* Research Use Case Selection */}
                <div style={{...styles.card, marginBottom: '24px'}}>
                  <h3 style={styles.cardTitle}>Select Research Use Case</h3>
                  <div style={{marginTop: '24px'}}>
                    <label style={{display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151'}}>
                      Choose Your Research Scenario:
                    </label>
                    <select style={{width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px', fontSize: '14px'}}>
                      <option value="">Select a research use case...</option>
                      
                      <optgroup label="⭐ Featured Demo">
                        <option>🔬 Cardiac Hematology Simulation (Pediatric & Adolescent)</option>
                      </optgroup>
                      
                      <optgroup label="🩺 Clinical Research">
                        <option>Longitudinal Growth Modeling for Surgical Timing</option>
                        <option>Treatment Response Prediction in Oncology</option>
                        <option>Adverse Event Detection in Polypharmacy</option>
                        <option>Surgical Outcome Prediction Models</option>
                        <option>Post-Operative Hemorrhage Risk Prediction</option>
                        <option>Thrombotic Risk Assessment in CHD Patients</option>
                      </optgroup>
                      
                      <optgroup label="🧬 Pharmaceutical Research">
                        <option>Drug Safety Signal Detection</option>
                        <option>Clinical Trial Patient Stratification</option>
                        <option>Real-World Evidence Generation</option>
                        <option>Biomarker Discovery and Validation</option>
                        <option>Synthetic Control Arms for Rare Disease Trials</option>
                        <option>Iron Deficiency Treatment Efficacy Studies</option>
                      </optgroup>
                      
                      <optgroup label="🤖 AI Model Development">
                        <option>Diagnostic Algorithm Training</option>
                        <option>Risk Stratification Model Development</option>
                        <option>Clinical Decision Support Systems</option>
                        <option>Population Health Analytics</option>
                        <option>Early Detection Models for Cardiac Complications</option>
                        <option>Triage Decision-Making (ICU vs Step-Down)</option>
                      </optgroup>
                      
                      <optgroup label="👶 Pediatric Cardiology">
                        <option>Congenital Heart Defect Progression</option>
                        <option>Surgical Intervention Timing</option>
                        <option>Growth Pattern Analysis</option>
                        <option>Long-term Outcome Prediction</option>
                        <option>Tetralogy of Fallot + Anemia Comorbidity</option>
                        <option>Hypoplastic Left Heart Syndrome Trajectories</option>
                      </optgroup>
                      
                      <optgroup label="🩸 Hematology Research">
                        <option>Sickle Cell Disease in CHD Populations</option>
                        <option>Iron Deficiency Anemia Treatment Outcomes</option>
                        <option>Hemophilia Management in Cardiac Surgery</option>
                        <option>Thrombocytopenia Risk Stratification</option>
                      </optgroup>
                      
                      <optgroup label="🔬 Medical Device Testing">
                        <option>Device Performance Validation</option>
                        <option>Safety Profile Assessment</option>
                        <option>Regulatory Submission Support</option>
                        <option>Post-Market Surveillance</option>
                        <option>EHR Migration & Pipeline Validation</option>
                      </optgroup>
                    </select>
                  </div>
                </div>

                {/* Configuration Parameters */}
                <div style={{...styles.card, marginBottom: '24px'}}>
                  <h3 style={styles.cardTitle}>Configuration Parameters</h3>
                  <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginTop: '24px'}}>
                    
                    <div>
                      <label style={{display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151'}}>
                        Patient Population Size
                      </label>
                      <select style={{width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}>
                        <option>Small Cohort (10-50 patients)</option>
                        <option>Medium Cohort (100-500 patients)</option>
                        <option>Large Cohort (1,000-5,000 patients)</option>
                        <option>Enterprise Scale (10,000+ patients)</option>
                        <option>Featured Demo Scale (N=10,000 Pediatric)</option>
                      </select>
                    </div>

                    <MultiSelectDropdown
                      label="Cardiac Conditions"
                      emoji="🫀"
                      placeholder="Select cardiac conditions..."
                      options={[
                        'Tetralogy of Fallot',
                        'Hypoplastic Left Heart Syndrome',
                        'Coarctation of the Aorta',
                        'Atrial Septal Defect (ASD)',
                        'Ventricular Septal Defect (VSD)',
                        'Patent Ductus Arteriosus',
                        'Transposition of Great Arteries',
                        'Pulmonary Stenosis'
                      ]}
                    />

                    <MultiSelectDropdown
                      label="Hematologic Conditions"
                      emoji="🩸"
                      placeholder="Select hematologic comorbidities..."
                      options={[
                        'Iron Deficiency Anemia',
                        'Sickle Cell Disease',
                        'Thrombocytopenia',
                        'Hemophilia A',
                        'Hemophilia B',
                        'Von Willebrand Disease',
                        'Thalassemia',
                        'Aplastic Anemia'
                      ]}
                    />
                    
                    <div>
                      <label style={{display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151'}}>
                        Data Complexity Level
                      </label>
                      <select style={{width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}>
                        <option>Basic Demographics & Diagnoses</option>
                        <option>Standard Clinical Records</option>
                        <option>Complex Multi-System Cases</option>
                        <option>Longitudinal Patient Journeys</option>
                      </select>
                    </div>
                    
                    <div>
                      <label style={{display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151'}}>
                        Medical Specialty Focus
                      </label>
                      <select style={{width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}>
                        <option>General Medicine</option>
                        <option>Pediatric Cardiology</option>
                        <option>Oncology</option>
                        <option>Emergency Medicine</option>
                        <option>Psychiatry</option>
                        <option>Nephrology</option>
                        <option>Pulmonology</option>
                        <option>Orthopedics</option>
                      </select>
                    </div>
                    
                    <MultiSelectDropdown
                      label="Data Types to Include"
                      emoji="📊"
                      placeholder="Select data modalities to generate..."
                      options={[
                        'Structured Clinical Data (Demographics, Vitals)',
                        'Laboratory Results (CBC, Chemistry, Coagulation)',
                        'EKG/ECG Time Series Data',
                        'Clinical Notes (Progress, Surgical, Discharge)',
                        'Medication Administration Records',
                        'Procedure Codes (CPT)',
                        'Diagnostic Codes (ICD-10)',
                        'Growth & Development Metrics',
                        'Family History Transcripts',
                        'Oxygen Saturation Trends'
                      ]}
                    />
                    
                    <div>
                      <label style={{display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151'}}>
                        Validation Rigor
                      </label>
                      <select style={{width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}>
                        <option>Lenient (Fast Generation)</option>
                        <option>Standard (Balanced)</option>
                        <option>Strict (High Quality)</option>
                        <option>Research Grade (Maximum Rigor)</option>
                      </select>
                    </div>
                    
                    <div>
                      <label style={{display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151'}}>
                        Timeline Coverage
                      </label>
                      <select style={{width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}>
                        <option>Single Point in Time</option>
                        <option>Short Term (Days to Weeks)</option>
                        <option>Medium Term (Months)</option>
                        <option>Long Term (Years)</option>
                        <option>Longitudinal Pediatric (Birth to 18 years)</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* Advanced Settings */}
                <div style={{...styles.card, marginBottom: '24px'}}>
                  <h3 style={styles.cardTitle}>Advanced Settings</h3>
                  <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginTop: '24px'}}>
                    
                    <div>
                      <label style={{display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151'}}>
                        Demographic Distribution
                      </label>
                      <select style={{width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}>
                        <option>Real-World Representative</option>
                        <option>Age-Stratified Cohort</option>
                        <option>Gender-Balanced</option>
                        <option>Ethnically Diverse</option>
                        <option>Custom Distribution</option>
                      </select>
                    </div>
                    
                    <div>
                      <label style={{display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151'}}>
                        Comorbidity Complexity
                      </label>
                      <select style={{width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}>
                        <option>Single Primary Condition</option>
                        <option>Common Comorbidities</option>
                        <option>Complex Multi-System</option>
                        <option>Rare Disease Patterns</option>
                      </select>
                    </div>
                    
                    <div>
                      <label style={{display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151'}}>
                        Treatment Variability
                      </label>
                      <select style={{width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}>
                        <option>Standard Protocol</option>
                        <option>Provider Variation</option>
                        <option>Geographic Differences</option>
                        <option>Experimental Treatments</option>
                      </select>
                    </div>
                    
                    <div>
                      <label style={{display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151'}}>
                        Outcome Distribution
                      </label>
                      <select style={{width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}>
                        <option>Typical Clinical Outcomes</option>
                        <option>Enriched Success Cases</option>
                        <option>Enriched Adverse Events</option>
                        <option>Balanced Mixed Outcomes</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* Generation Button */}
                <div style={{textAlign: 'center'}}>
                  <button 
                    style={{
                      ...styles.primaryButton, 
                      padding: '16px 32px', 
                      fontSize: '16px',
                      opacity: isGenerating ? 0.7 : 1,
                      cursor: isGenerating ? 'not-allowed' : 'pointer'
                    }}
                    onClick={handleGenerateDataset}
                    disabled={isGenerating}
                  >
                    {isGenerating ? '🔄 Generating...' : '🎯 Generate Synthetic Dataset'}
                  </button>
                  <p style={{marginTop: '12px', color: '#6b7280', fontSize: '14px'}}>
                    {isGenerating 
                      ? 'Your synthetic EHR dataset is being generated with full medical validation'
                      : 'Your synthetic EHR dataset will be generated with full audit trails and validation reports'
                    }
                  </p>
                </div>

                {/* Progress Bar */}
                {isGenerating && (
                  <div style={{marginTop: '32px', padding: '24px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e5e7eb'}}>
                    <h3 style={{margin: '0 0 16px 0', color: '#374151', fontSize: '18px', fontWeight: '600'}}>
                      🔬 Generating Synthetic EHR Dataset
                    </h3>
                    <ProgressBar 
                      progress={progress} 
                      currentStep={currentStep}
                      steps={generationSteps}
                    />
                    
                    {/* Active Steps Display */}
                    <div style={{marginTop: '16px'}}>
                      <h4 style={{margin: '0 0 12px 0', color: '#374151', fontSize: '14px', fontWeight: '600'}}>
                        Pipeline Status:
                      </h4>
                      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '8px'}}>
                        {generationSteps.map(step => (
                          <div 
                            key={step.id}
                            style={{
                              padding: '8px 12px',
                              borderRadius: '6px',
                              fontSize: '12px',
                              backgroundColor: step.active ? '#dbeafe' : '#f3f4f6',
                              color: step.active ? '#1d4ed8' : '#6b7280',
                              border: step.active ? '1px solid #3b82f6' : '1px solid #e5e7eb'
                            }}
                          >
                            {step.active ? '🔄' : '✓'} {step.name}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </section>
        </main>
      </div>
    )
  }

  if (currentView === 'enterprise') {
    return (
      <div style={styles.container}>
        <header style={styles.header}>
          <nav style={styles.nav}>
            <div style={styles.logo}>
              <div style={styles.logoIcon}>SA</div>
              <span style={styles.logoText}>Synthetic Ascension</span>
            </div>
            <button 
              style={{...styles.secondaryButton, padding: '8px 16px', fontSize: '14px'}} 
              onClick={handleBackToLanding}
            >
              ← Back to Home
            </button>
          </nav>
        </header>
        
        <main style={styles.main}>
          <section style={styles.hero}>
            <div style={styles.heroContent}>
              <h1 style={{...styles.heroTitle, fontSize: '48px'}}>Enterprise Partnership</h1>
              <p style={styles.heroSubtitle}>Scale Your Healthcare AI with Confidence</p>
              <p style={styles.heroDescription}>
                Partner with Synthetic Ascension to transform your organization's approach 
                to healthcare data and AI development.
              </p>
              
              <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '32px', marginTop: '48px'}}>
                <div style={styles.card}>
                  <div style={{...styles.cardIcon, background: '#0ea5e9'}}>
                    <div style={{width: '24px', height: '24px', background: 'white', borderRadius: '3px'}}></div>
                  </div>
                  <h3 style={styles.cardTitle}>Custom Integration</h3>
                  <p style={styles.cardDescription}>
                    Seamless integration with your existing healthcare systems and workflows.
                  </p>
                </div>
                
                <div style={styles.card}>
                  <div style={{...styles.cardIcon, background: '#06b6d4'}}>
                    <div style={{width: '24px', height: '24px', background: 'white', borderRadius: '3px'}}></div>
                  </div>
                  <h3 style={styles.cardTitle}>Dedicated Support</h3>
                  <p style={styles.cardDescription}>
                    24/7 technical support and dedicated account management for enterprise clients.
                  </p>
                </div>
                
                <div style={styles.card}>
                  <div style={{...styles.cardIcon, background: '#0284c7'}}>
                    <div style={{width: '24px', height: '24px', background: 'white', borderRadius: '3px'}}></div>
                  </div>
                  <h3 style={styles.cardTitle}>Compliance Assurance</h3>
                  <p style={styles.cardDescription}>
                    HIPAA, GDPR, and SOC 2 compliance with comprehensive audit trails.
                  </p>
                </div>
              </div>
              
              <div style={{...styles.card, maxWidth: '500px', margin: '48px auto'}}>
                <h3 style={styles.cardTitle}>Contact Enterprise Sales</h3>
                <div style={{display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '24px'}}>
                  <input 
                    type="text" 
                    placeholder="Your Name" 
                    style={{padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}
                  />
                  <input 
                    type="email" 
                    placeholder="Business Email" 
                    style={{padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}
                  />
                  <input 
                    type="text" 
                    placeholder="Organization" 
                    style={{padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}
                  />
                  <textarea 
                    placeholder="Tell us about your use case and requirements..." 
                    rows={4}
                    style={{padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px', resize: 'vertical'}}
                  />
                  <button style={{...styles.primaryButton, width: '100%'}}>
                    Request Enterprise Demo
                  </button>
                </div>
              </div>
            </div>
          </section>
        </main>
      </div>
    )
  }

  return (
    <div style={styles.container}>
      <style>
        {`
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
          @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
          }
          @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
          }
          .hero-title {
            animation: shimmer 3s ease-in-out infinite;
            background-size: 200% 100%;
          }
          .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
          }
          .primary-button:hover {
            background: #0284c7;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(14, 165, 233, 0.25);
          }
          .secondary-button:hover {
            background: #f8fafc;
            border-color: #94a3b8;
          }
          .cta-button:hover {
            background: #0284c7;
            transform: translateY(-1px);
          }
          @media (min-width: 640px) {
            .button-container {
              flex-direction: row;
            }
          }
        `}
      </style>

      <header style={styles.header}>
        <nav style={styles.nav}>
          <div style={styles.logo}>
            <div style={styles.logoIcon}>SA</div>
            <div style={styles.logoText}>Synthetic Ascension</div>
          </div>
          <div style={styles.status}>
            <div style={styles.statusDot}></div>
            <span>System Online</span>
          </div>
        </nav>
      </header>

      <main style={styles.main}>
        <section style={styles.hero}>
          <div style={styles.heroContent}>
            <h1 style={styles.heroTitle} className="hero-title">Synthetic Ascension</h1>
            <p style={styles.heroSubtitle}>Simulate. Validate. Ascend.</p>
            <p style={styles.heroDescription}>
              The world's most advanced synthetic EHR platform. Generate privacy-safe, clinically accurate patient data that powers breakthrough AI research and accelerates medical innovation—without compromising patient privacy.
            </p>
            
            <div style={styles.heroStats}>
              <div style={styles.statItem}>
                <span style={styles.statNumber}>10M+</span>
                <span style={styles.statLabel}>Synthetic Patients</span>
              </div>
              <div style={styles.statItem}>
                <span style={styles.statNumber}>99.9%</span>
                <span style={styles.statLabel}>Privacy Compliance</span>
              </div>
              <div style={styles.statItem}>
                <span style={styles.statNumber}>500+</span>
                <span style={styles.statLabel}>Research Studies</span>
              </div>
              <div style={styles.statItem}>
                <span style={styles.statNumber}>24/7</span>
                <span style={styles.statLabel}>AI Validation</span>
              </div>
            </div>
            
            <div style={{...styles.buttonContainer, flexDirection: 'row'}} className="button-container">
              <button 
                style={styles.primaryButton} 
                className="primary-button"
                onClick={handleLaunchDemo}
              >
                Launch Demo
              </button>
              <button 
                style={styles.secondaryButton} 
                className="secondary-button"
                onClick={handleEnterprisePartnership}
              >
                Enterprise Partnership
              </button>
            </div>
          </div>
        </section>

        <section style={styles.features}>
          <div style={styles.featuresHeader}>
            <h2 style={styles.featuresTitle}>Enterprise-Grade Synthetic EHR Platform</h2>
            <p style={styles.featuresSubtitle}>
              Generate realistic, privacy-compliant patient data with advanced AI validation and comprehensive analytics.
            </p>
          </div>

          <div style={styles.grid}>
            {features.map((feature, index) => (
              <div key={index} style={styles.card} className="card">
                <div style={{...styles.cardIcon, background: feature.color}}>
                  <div style={{width: '24px', height: '24px', background: 'white', borderRadius: '3px'}}></div>
                </div>
                <h3 style={styles.cardTitle}>{feature.title}</h3>
                <p style={styles.cardDescription}>{feature.description}</p>
              </div>
            ))}
          </div>
        </section>

        <section style={styles.cta}>
          <div style={styles.ctaContent}>
            <h2 style={styles.ctaTitle}>Ready to Transform Your Healthcare Data?</h2>
            <p style={styles.ctaSubtitle}>
              Join leading healthcare organizations and research institutions already using Synthetic Ascension.
            </p>
            <button 
              style={styles.ctaButton} 
              className="cta-button"
              onClick={handleStartDemo}
            >
              Start Your Demo
            </button>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App