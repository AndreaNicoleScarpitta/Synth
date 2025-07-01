import React, { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import ResultsOverview from './pages/ResultsOverview.tsx'
import PatientRecord from './pages/PatientRecord.tsx'
import { MatrixBackground } from './components/MatrixBackground'
import { SyntheticLogo } from './components/SyntheticLogo'

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

// Comprehensive color palette
const colors = {
  primary: '#fbbf24',     // Gold primary
  secondary: '#f59e0b',   // Amber secondary
  tertiary: '#06b6d4',    // Cyan tertiary (replaces blue)
  accent: '#10b981',      // Emerald accent
  dark: '#0a0a0a',        // Pure black
  darkCard: 'rgba(10, 10, 10, 0.8)', // Semi-transparent black
  text: '#fbbf24',        // Gold text
  textSecondary: '#f59e0b', // Amber secondary text
  textTertiary: '#06b6d4', // Cyan for highlights
  border: '#fbbf24',      // Gold borders
  shadow: 'rgba(251, 191, 36, 0.2)', // Gold shadow
}

const styles = {
  container: {
    minHeight: '100vh',
    background: colors.dark,
    fontFamily: "'Hi Melody', Inter, system-ui, sans-serif",
    color: colors.text
  },
  header: {
    position: 'fixed' as const,
    top: 0,
    left: 0,
    right: 0,
    zIndex: 50,
    background: 'rgba(10, 10, 10, 0.95)',
    backdropFilter: 'blur(10px)',
    borderBottom: '1px solid #fbbf24',
    boxShadow: '0 1px 2px rgba(251, 191, 36, 0.2)'
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
    background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: '#0a0a0a',
    fontWeight: 'bold',
    fontSize: '14px'
  },
  logoText: {
    fontWeight: '600',
    fontSize: '20px',
    color: '#fbbf24'
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
    color: '#fbbf24',
    marginBottom: '24px',
    lineHeight: '1.1',
    textAlign: 'center' as const,
    letterSpacing: '-0.02em',
    textShadow: '0 0 20px rgba(251, 191, 36, 0.5)'
  },
  heroSubtitle: {
    fontSize: '24px',
    fontWeight: '500',
    color: '#f59e0b',
    marginBottom: '32px',
    maxWidth: '800px',
    margin: '0 auto 32px',
    letterSpacing: '0.05em'
  },
  heroDescription: {
    fontSize: '18px',
    color: '#fbbf24',
    marginBottom: '48px',
    maxWidth: '680px',
    margin: '0 auto 48px',
    lineHeight: '1.6',
    opacity: 0.8
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
    color: '#fbbf24',
    marginBottom: '16px'
  },
  featuresSubtitle: {
    fontSize: '18px',
    color: '#f59e0b',
    maxWidth: '800px',
    margin: '0 auto'
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '32px'
  },
  card: {
    background: 'rgba(10, 10, 10, 0.8)',
    borderRadius: '8px',
    padding: '28px',
    boxShadow: '0 1px 3px rgba(251, 191, 36, 0.2)',
    border: '1px solid #fbbf24',
    transition: 'all 0.3s',
    backdropFilter: 'blur(10px)'
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
    color: '#fbbf24'
  },
  cardDescription: {
    color: '#f59e0b',
    lineHeight: '1.6',
    opacity: 0.9
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
    title: "Genetic Algorithm Synthesis",
    description: "Neural networks evolve synthetic patient cohorts with complex genetic markers and phenotypic expressions.",
    color: colors.tertiary,
    icon: "🧬"
  },
  {
    title: "Quantum-Secured Privacy", 
    description: "Quantum-encrypted synthetic data generation with mathematically proven zero-knowledge privacy.",
    color: colors.accent,
    icon: "🔐"
  },
  {
    title: "Consciousness-Level Validation",
    description: "AI consciousness models validate synthetic patterns for biological authenticity and emergent behaviors.",
    color: colors.primary,
    icon: "🧠"
  },
  {
    title: "Synthetic Biology Integration",
    description: "Biomarker-precise synthetic records that model cellular-level processes and genetic interactions.",
    color: colors.secondary,
    icon: "🔬"
  },
  {
    title: "Quantum-Scale Infrastructure",
    description: "Generate patient universes from thousands to billions with quantum-parallel processing power.",
    color: colors.tertiary,
    icon: "⚡"
  },
  {
    title: "Evolutionary Research Platform",
    description: "Self-evolving templates for pharmaceutical discovery, genetic research, and consciousness studies.",
    color: colors.accent,
    icon: "🔬"
  }
]

function App() {
  return (
    <Routes>
      <Route path="/patient/:patientId" element={<PatientRecord />} />
      <Route path="/*" element={<MainApp />} />
    </Routes>
  )
}

function MainApp() {
  const [currentView, setCurrentView] = useState('landing')
  const [isGenerating, setIsGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  const [currentStep, setCurrentStep] = useState('')
  const [generationSteps, setGenerationSteps] = useState([])
  const [generationResults, setGenerationResults] = useState(null)
  const [showSignupForm, setShowSignupForm] = useState(false)
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
    <div className="min-h-screen bg-white">
      <style>
        {`
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Montserrat:wght@400;500;600;700&display=swap');
          
          .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(8, 145, 178, 0.12);
            transition: all 0.3s ease;
          }
          
          .primary-button:hover {
            background: #0e7490;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(8, 145, 178, 0.3);
            transition: all 0.3s ease;
          }
          
          .secondary-button:hover {
            background: #f0fdf4;
            border-color: #10b981;
            color: #047857;
            transition: all 0.3s ease;
          }
          
          .trust-badge {
            opacity: 0.7;
            transition: opacity 0.3s ease;
          }
          
          .trust-badge:hover {
            opacity: 1;
          }
          
          @media (max-width: 768px) {
            .hero-title {
              font-size: 2.5rem !important;
            }
            .hero-subtitle {
              font-size: 1.2rem !important;
            }
          }
        `}
      </style>

      {/* Navigation */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <SyntheticLogo />
          
          <div className="hidden md:flex items-center space-x-8">
            <a href="#features" className="text-slate-600 hover:text-primary-600 font-medium transition-colors">Features</a>
            <a href="#use-cases" className="text-slate-600 hover:text-primary-600 font-medium transition-colors">Use Cases</a>
            <a href="#contact" className="text-slate-600 hover:text-primary-600 font-medium transition-colors">Contact</a>
            <button 
              className="bg-primary-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-primary-700 transition-colors"
              onClick={() => setShowSignupForm(true)}
            >
              Request Demo
            </button>
          </div>
        </nav>
      </header>

      <main>
        {/* Hero Section */}
        <section className="bg-gradient-to-br from-slate-50 to-primary-50 py-20 lg:py-28">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-4xl mx-auto">
              <h1 className="text-4xl md:text-6xl font-bold text-slate-900 mb-6 hero-title" style={{ fontFamily: 'Montserrat, sans-serif' }}>
                Unlock Healthcare AI with <span className="text-primary-600">Privacy-Safe</span> Patient Data
              </h1>
              <p className="text-xl text-slate-600 mb-8 hero-subtitle">
                Synthetic EHR datasets that evolve with the latest medical knowledge – no PHI, no red tape.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
                <button 
                  className="bg-primary-600 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-primary-700 transition-colors primary-button"
                  onClick={() => setShowSignupForm(true)}
                >
                  Request a Demo
                </button>
                <button 
                  className="border-2 border-secondary-500 text-secondary-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-secondary-50 transition-colors secondary-button"
                  onClick={() => setShowSignupForm(true)}
                >
                  Get Early Access
                </button>
              </div>
              
              {/* Trust indicators */}
              <div className="flex flex-wrap justify-center items-center gap-8 text-sm text-slate-500">
                <div className="flex items-center gap-2 trust-badge">
                  <span className="w-3 h-3 bg-secondary-500 rounded-full"></span>
                  HIPAA Compliant
                </div>
                <div className="flex items-center gap-2 trust-badge">
                  <span className="w-3 h-3 bg-secondary-500 rounded-full"></span>
                  100% Synthetic Data
                </div>
                <div className="flex items-center gap-2 trust-badge">
                  <span className="w-3 h-3 bg-secondary-500 rounded-full"></span>
                  No Patient Privacy Risk
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Problem & Solution Section */}
        <section className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div>
                <h2 className="text-3xl font-bold text-slate-900 mb-6">The Challenge</h2>
                <p className="text-lg text-slate-600 mb-6">
                  AI healthcare models are starving for diverse, representative data – but real patient data is siloed, biased, and hard to obtain.
                </p>
                <ul className="space-y-3 text-slate-600">
                  <li className="flex items-start gap-3">
                    <span className="text-red-500 font-semibold">×</span>
                    Long approval processes and IRB hurdles
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-red-500 font-semibold">×</span>
                    Biased datasets with limited population diversity
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-red-500 font-semibold">×</span>
                    Privacy risks and compliance complexity
                  </li>
                </ul>
              </div>
              
              <div>
                <h2 className="text-3xl font-bold text-slate-900 mb-6">Our Solution</h2>
                <p className="text-lg text-slate-600 mb-6">
                  Synthetic Ascension generates unlimited, privacy-safe EHR data that mirrors real-world populations while eliminating compliance barriers.
                </p>
                <ul className="space-y-3 text-slate-600">
                  <li className="flex items-start gap-3">
                    <span className="text-secondary-500 font-semibold">✓</span>
                    Instant access to diverse synthetic datasets
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-secondary-500 font-semibold">✓</span>
                    Zero patient privacy risk with 100% synthetic data
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-secondary-500 font-semibold">✓</span>
                    Statistically equivalent to real populations
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* Key Features Section */}
        <section id="features" className="py-20 bg-slate-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-slate-900 mb-4">Key Features</h2>
              <p className="text-xl text-slate-600 max-w-3xl mx-auto">
                Enterprise-grade synthetic EHR generation with advanced AI validation and comprehensive analytics
              </p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="bg-white p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow card min-h-[180px]">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-3">Privacy by Design</h3>
                <p className="text-slate-600">100% synthetic records with zero PHI, compliant with HIPAA and GDPR from day one.</p>
              </div>
              
              <div className="bg-white p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow card min-h-[180px]">
                <div className="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-3">Diverse & Realistic Data</h3>
                <p className="text-slate-600">Statistically mirrors real patient populations, including rare conditions and underrepresented groups.</p>
              </div>
              
              <div className="bg-white p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow card min-h-[180px]">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-3">Continuously Updated</h3>
                <p className="text-slate-600">AI agents ingest new medical research continuously, so your data never goes stale.</p>
              </div>
              
              <div className="bg-white p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow card min-h-[180px]">
                <div className="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-3">On-Demand & Scalable</h3>
                <p className="text-slate-600">Access via API or UI; generate millions of records in minutes.</p>
              </div>
              
              <div className="bg-white p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow card min-h-[180px]">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-3">Validated Accuracy</h3>
                <p className="text-slate-600">Benchmarked against real-world stats to ensure clinical credibility.</p>
              </div>
              
              <div className="bg-white p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow card min-h-[180px]">
                <div className="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-3">Lightning Fast</h3>
                <p className="text-slate-600">Generate complex patient cohorts in seconds, not months of data collection.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Use Cases Section */}
        <section id="use-cases" className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-slate-900 mb-4">Use Cases</h2>
              <p className="text-xl text-slate-600 max-w-3xl mx-auto">
                Our synthetic EHR platform powers innovation across healthcare research, AI development, and pharmaceutical studies
              </p>
            </div>
            
            <div className="grid lg:grid-cols-3 gap-8">
              <div className="bg-slate-50 p-6 rounded-xl">
                <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-4">AI Model Training</h3>
                <p className="text-slate-600 mb-4 text-sm">
                  Train diagnostic algorithms, risk prediction models, and clinical decision support systems with diverse, validated synthetic data.
                </p>
                <ul className="text-xs text-slate-500 space-y-2">
                  <li>• Diagnostic accuracy improvement</li>
                  <li>• Risk stratification algorithms</li>
                  <li>• Population health analytics</li>
                </ul>
              </div>
              
              <div className="bg-slate-50 p-6 rounded-xl">
                <div className="w-8 h-8 bg-secondary-100 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-4 h-4 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-4">Clinical Research</h3>
                <p className="text-slate-600 mb-4 text-sm">
                  Accelerate clinical studies with ready-to-use synthetic cohorts that match your research criteria exactly.
                </p>
                <ul className="text-xs text-slate-500 space-y-2">
                  <li>• Clinical trial design</li>
                  <li>• Longitudinal studies</li>
                  <li>• Rare disease research</li>
                </ul>
              </div>
              
              <div className="bg-slate-50 p-6 rounded-xl">
                <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-4">Drug Development</h3>
                <p className="text-slate-600 mb-4 text-sm">
                  Support pharmaceutical research with synthetic patient populations for safety studies and efficacy modeling.
                </p>
                <ul className="text-xs text-slate-500 space-y-2">
                  <li>• Drug safety assessment</li>
                  <li>• Efficacy modeling</li>
                  <li>• Regulatory submissions</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* Contact Section */}
        <section id="contact" className="py-20 bg-slate-50">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">
              Ready to Transform Your Research?
            </h2>
            <p className="text-xl text-slate-600 mb-8">
              Contact us for a personalized demo and see how synthetic EHR data can accelerate your projects
            </p>
            
            <div className="grid md:grid-cols-3 gap-8 mb-12">
              <div className="text-center">
                <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="font-semibold text-slate-900 mb-2">Quick Setup</h3>
                <p className="text-slate-600 text-sm">Get started in minutes with our API or web interface</p>
              </div>
              
              <div className="text-center">
                <div className="w-12 h-12 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-5 h-5 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192L5.636 18.364M12 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="font-semibold text-slate-900 mb-2">Expert Support</h3>
                <p className="text-slate-600 text-sm">Our team helps optimize synthetic data for your specific needs</p>
              </div>
              
              <div className="text-center">
                <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <h3 className="font-semibold text-slate-900 mb-2">Compliance Ready</h3>
                <p className="text-slate-600 text-sm">Built-in HIPAA and GDPR compliance with zero privacy risk</p>
              </div>
            </div>
            
            <button 
              className="bg-primary-600 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-primary-700 transition-colors"
              onClick={() => setShowSignupForm(true)}
            >
              Schedule a Demo
            </button>
          </div>
        </section>
      </main>

      {/* Signup Form Modal */}
      {showSignupForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-md w-full p-8">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-slate-900 mb-2">Request Demo Access</h3>
              <p className="text-slate-600">Get early access to Synthetic Ascension's EHR platform</p>
            </div>
            
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Full Name</label>
                <input 
                  type="text" 
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Dr. Jane Smith"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Email Address</label>
                <input 
                  type="email" 
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="jane@hospital.com"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Organization</label>
                <input 
                  type="text" 
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Healthcare Research Institute"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Use Case</label>
                <select className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
                  <option value="">Select your primary use case</option>
                  <option value="ai-training">AI Model Training</option>
                  <option value="clinical-research">Clinical Research</option>
                  <option value="drug-development">Drug Development</option>
                  <option value="other">Other</option>
                </select>
              </div>
              
              <div className="flex gap-3 mt-6">
                <button 
                  type="button"
                  className="flex-1 bg-slate-200 text-slate-700 py-3 rounded-lg font-medium hover:bg-slate-300 transition-colors"
                  onClick={() => setShowSignupForm(false)}
                >
                  Cancel
                </button>
                <button 
                  type="submit"
                  className="flex-1 bg-primary-600 text-white py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors"
                >
                  Request Demo
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default App