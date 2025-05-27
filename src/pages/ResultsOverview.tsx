import React from 'react'

interface ResultsOverviewProps {
  results: any
  onBackToDemo: () => void
}

const ResultsOverview: React.FC<ResultsOverviewProps> = ({ results, onBackToDemo }) => {
  const styles = {
    container: {
      minHeight: '100vh',
      backgroundColor: '#f8fafc',
      fontFamily: 'Inter, system-ui, sans-serif'
    },
    header: {
      backgroundColor: '#ffffff',
      borderBottom: '1px solid #e5e7eb',
      padding: '16px 0'
    },
    nav: {
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '0 24px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    },
    logo: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px'
    },
    logoIcon: {
      width: '32px',
      height: '32px',
      backgroundColor: '#3b82f6',
      color: 'white',
      borderRadius: '8px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontWeight: 'bold',
      fontSize: '14px'
    },
    logoText: {
      fontSize: '20px',
      fontWeight: '600',
      color: '#1f2937'
    },
    main: {
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '32px 24px'
    },
    title: {
      fontSize: '32px',
      fontWeight: '700',
      color: '#1f2937',
      marginBottom: '8px',
      textAlign: 'center' as const
    },
    subtitle: {
      fontSize: '18px',
      color: '#6b7280',
      marginBottom: '32px',
      textAlign: 'center' as const
    },
    card: {
      backgroundColor: '#ffffff',
      borderRadius: '12px',
      padding: '24px',
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
      border: '1px solid #e5e7eb',
      marginBottom: '24px'
    },
    cardTitle: {
      fontSize: '20px',
      fontWeight: '600',
      color: '#1f2937',
      marginBottom: '16px'
    },
    grid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
      gap: '24px',
      marginBottom: '32px'
    },
    statCard: {
      backgroundColor: '#ffffff',
      borderRadius: '12px',
      padding: '20px',
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
      border: '1px solid #e5e7eb',
      textAlign: 'center' as const
    },
    statNumber: {
      fontSize: '32px',
      fontWeight: '700',
      color: '#3b82f6',
      marginBottom: '8px'
    },
    statLabel: {
      fontSize: '14px',
      color: '#6b7280',
      fontWeight: '500'
    },
    button: {
      backgroundColor: '#3b82f6',
      color: 'white',
      border: 'none',
      borderRadius: '8px',
      padding: '12px 24px',
      fontSize: '14px',
      fontWeight: '500',
      cursor: 'pointer',
      transition: 'all 0.2s',
      marginRight: '12px'
    },
    secondaryButton: {
      backgroundColor: 'transparent',
      color: '#3b82f6',
      border: '1px solid #3b82f6',
      borderRadius: '8px',
      padding: '12px 24px',
      fontSize: '14px',
      fontWeight: '500',
      cursor: 'pointer',
      transition: 'all 0.2s'
    },
    successBadge: {
      backgroundColor: '#dcfce7',
      color: '#166534',
      padding: '4px 12px',
      borderRadius: '6px',
      fontSize: '12px',
      fontWeight: '500',
      display: 'inline-block',
      marginBottom: '16px'
    }
  }

  // Mock results if none provided
  const mockResults = {
    summary: {
      total_patients: 500,
      cardiac_conditions_included: ['Tetralogy of Fallot', 'Hypoplastic Left Heart Syndrome'],
      hematologic_conditions_included: ['Iron Deficiency Anemia'],
      demographics_breakdown: {
        gender_distribution: { 'Female': 245, 'Male': 255 },
        ethnicity_distribution: { 'Hispanic or Latino': 125, 'Not Hispanic or Latino': 375 }
      },
      clinical_data_generated: {
        lab_parameters: ['Complete Blood Count (CBC)', 'Ferritin & Iron Studies'],
        procedure_types: ['Cardiac Catheterization', 'Echocardiogram'],
        data_modalities: ['Lab Results', 'Clinical Notes', 'Hemodynamic Data']
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
          }
        ]
      },
      medical_validation: {
        clinical_consistency_score: 0.96,
        bias_detection_results: {
          gender_balance: "Within acceptable range (48% F, 52% M)",
          ethnic_diversity: "Representative distribution achieved"
        }
      }
    }
  }

  const displayResults = results || mockResults

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <nav style={styles.nav}>
          <div style={styles.logo}>
            <div style={styles.logoIcon}>SA</div>
            <span style={styles.logoText}>Synthetic Ascension</span>
          </div>
          <div>
            <button style={styles.secondaryButton} onClick={onBackToDemo}>
              ← Back to Demo
            </button>
            <button style={styles.button}>
              📊 Advanced Analytics
            </button>
          </div>
        </nav>
      </header>

      <main style={styles.main}>
        <div style={styles.successBadge}>
          ✓ Generation Complete
        </div>
        
        <h1 style={styles.title}>Synthetic EHR Dataset Generated</h1>
        <p style={styles.subtitle}>
          Your comprehensive synthetic dataset is ready with full audit trails and medical validation
        </p>

        {/* Key Statistics */}
        <div style={styles.grid}>
          <div style={styles.statCard}>
            <div style={styles.statNumber}>{displayResults.summary?.total_patients || 500}</div>
            <div style={styles.statLabel}>Synthetic Patients</div>
          </div>
          <div style={styles.statCard}>
            <div style={styles.statNumber}>{displayResults.summary?.literature_foundation?.papers_reviewed || 15}</div>
            <div style={styles.statLabel}>Research Papers Reviewed</div>
          </div>
          <div style={styles.statCard}>
            <div style={styles.statNumber}>{Math.round((displayResults.summary?.data_quality_metrics?.consistency || 0.96) * 100)}%</div>
            <div style={styles.statLabel}>Data Quality Score</div>
          </div>
          <div style={styles.statCard}>
            <div style={styles.statNumber}>{displayResults.summary?.clinical_data_generated?.lab_parameters?.length || 2}</div>
            <div style={styles.statLabel}>Lab Parameter Types</div>
          </div>
        </div>

        {/* Medical Conditions */}
        <div style={styles.card}>
          <h3 style={styles.cardTitle}>🫀 Medical Conditions Included</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '16px' }}>
            <div>
              <h4 style={{ fontSize: '14px', fontWeight: '600', color: '#374151', marginBottom: '8px' }}>
                Cardiac Conditions:
              </h4>
              <ul style={{ margin: 0, paddingLeft: '16px', color: '#6b7280' }}>
                {(displayResults.summary?.cardiac_conditions_included || []).map((condition: string, index: number) => (
                  <li key={index} style={{ marginBottom: '4px' }}>{condition}</li>
                ))}
              </ul>
            </div>
            <div>
              <h4 style={{ fontSize: '14px', fontWeight: '600', color: '#374151', marginBottom: '8px' }}>
                Hematologic Conditions:
              </h4>
              <ul style={{ margin: 0, paddingLeft: '16px', color: '#6b7280' }}>
                {(displayResults.summary?.hematologic_conditions_included || []).map((condition: string, index: number) => (
                  <li key={index} style={{ marginBottom: '4px' }}>{condition}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Demographics */}
        <div style={styles.card}>
          <h3 style={styles.cardTitle}>👥 Demographics Breakdown</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '24px' }}>
            <div>
              <h4 style={{ fontSize: '14px', fontWeight: '600', color: '#374151', marginBottom: '12px' }}>
                Gender Distribution:
              </h4>
              {Object.entries(displayResults.summary?.demographics_breakdown?.gender_distribution || {}).map(([gender, count]) => (
                <div key={gender} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                  <span style={{ color: '#6b7280' }}>{gender}:</span>
                  <span style={{ fontWeight: '500', color: '#374151' }}>{count as number}</span>
                </div>
              ))}
            </div>
            <div>
              <h4 style={{ fontSize: '14px', fontWeight: '600', color: '#374151', marginBottom: '12px' }}>
                Ethnicity Distribution:
              </h4>
              {Object.entries(displayResults.summary?.demographics_breakdown?.ethnicity_distribution || {}).map(([ethnicity, count]) => (
                <div key={ethnicity} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                  <span style={{ color: '#6b7280' }}>{ethnicity}:</span>
                  <span style={{ fontWeight: '500', color: '#374151' }}>{count as number}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Data Quality Metrics */}
        <div style={styles.card}>
          <h3 style={styles.cardTitle}>📈 Data Quality Validation</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '16px' }}>
            {Object.entries(displayResults.summary?.data_quality_metrics || {}).map(([metric, score]) => (
              <div key={metric} style={{ textAlign: 'center' }}>
                <div style={{ 
                  fontSize: '24px', 
                  fontWeight: '700', 
                  color: '#3b82f6',
                  marginBottom: '4px' 
                }}>
                  {Math.round((score as number) * 100)}%
                </div>
                <div style={{ 
                  fontSize: '12px', 
                  color: '#6b7280',
                  textTransform: 'capitalize'
                }}>
                  {metric.replace('_', ' ')}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Literature Foundation */}
        <div style={styles.card}>
          <h3 style={styles.cardTitle}>📚 Literature Foundation</h3>
          <div style={{ marginBottom: '16px' }}>
            <div style={{ fontSize: '14px', color: '#6b7280', marginBottom: '8px' }}>
              Evidence Strength: <span style={{ color: '#059669', fontWeight: '600' }}>
                {displayResults.summary?.literature_foundation?.evidence_strength || 'High'}
              </span>
            </div>
            <div style={{ fontSize: '14px', color: '#6b7280' }}>
              Clinical Guidelines: {displayResults.summary?.literature_foundation?.clinical_guidelines || 3} sources
            </div>
          </div>
          
          {displayResults.agentic_pipeline_results?.literature_retrieval?.relevant_papers?.slice(0, 2).map((paper: any, index: number) => (
            <div key={index} style={{ 
              marginBottom: '12px', 
              padding: '12px', 
              backgroundColor: '#f8fafc', 
              borderRadius: '6px',
              border: '1px solid #e5e7eb'
            }}>
              <div style={{ fontSize: '14px', fontWeight: '600', color: '#374151', marginBottom: '4px' }}>
                {paper.title}
              </div>
              <div style={{ fontSize: '12px', color: '#6b7280' }}>
                {paper.authors} • {paper.journal} ({paper.year})
              </div>
              {paper.relevance_score && (
                <div style={{ fontSize: '12px', color: '#059669', marginTop: '4px' }}>
                  Relevance: {Math.round(paper.relevance_score * 100)}%
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Action Buttons */}
        <div style={{ textAlign: 'center', marginTop: '32px' }}>
          <button style={styles.button}>
            📥 Download Dataset (CSV)
          </button>
          <button style={styles.button}>
            📋 Export Audit Report
          </button>
          <button style={styles.secondaryButton}>
            🔍 View Sample Records
          </button>
        </div>
      </main>
    </div>
  )
}

export default ResultsOverview