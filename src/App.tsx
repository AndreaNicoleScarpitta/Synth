import React, { useState } from 'react'

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

function App() {
  const [currentView, setCurrentView] = useState('landing')

  const handleLaunchDemo = () => {
    setCurrentView('demo')
  }

  const handleEnterprisePartnership = () => {
    setCurrentView('enterprise')
  }

  const handleStartDemo = () => {
    setCurrentView('demo')
  }

  const handleBackToLanding = () => {
    setCurrentView('landing')
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
              
              <div style={{...styles.card, maxWidth: '600px', margin: '48px auto'}}>
                <h3 style={styles.cardTitle}>Demo Configuration</h3>
                <div style={{display: 'flex', flexDirection: 'column', gap: '20px', marginTop: '24px'}}>
                  <div>
                    <label style={{display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151'}}>
                      Patient Cohort Size
                    </label>
                    <select style={{width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}>
                      <option>100 patients</option>
                      <option>500 patients</option>
                      <option>1,000 patients</option>
                      <option>5,000 patients</option>
                    </select>
                  </div>
                  
                  <div>
                    <label style={{display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151'}}>
                      Medical Specialty
                    </label>
                    <select style={{width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}>
                      <option>Pediatric Cardiology</option>
                      <option>General Medicine</option>
                      <option>Oncology</option>
                      <option>Orthopedics</option>
                    </select>
                  </div>
                  
                  <div>
                    <label style={{display: 'block', marginBottom: '8px', fontWeight: '500', color: '#374151'}}>
                      Data Complexity
                    </label>
                    <select style={{width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '6px'}}>
                      <option>Standard Clinical Records</option>
                      <option>Complex Multi-System Cases</option>
                      <option>Longitudinal Patient Journeys</option>
                    </select>
                  </div>
                  
                  <button style={{...styles.primaryButton, width: '100%', marginTop: '16px'}}>
                    Generate Synthetic Dataset
                  </button>
                </div>
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