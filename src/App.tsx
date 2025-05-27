import React from 'react'

const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
    fontFamily: 'Inter, system-ui, sans-serif'
  },
  header: {
    position: 'fixed' as const,
    top: 0,
    left: 0,
    right: 0,
    zIndex: 50,
    background: 'rgba(255, 255, 255, 0.95)',
    backdropFilter: 'blur(10px)',
    borderBottom: '1px solid #e2e8f0',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
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
    borderRadius: '8px',
    background: 'linear-gradient(135deg, #6B4EFF 0%, #1e40af 100%)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: 'white',
    fontWeight: 'bold',
    fontSize: '14px'
  },
  logoText: {
    fontWeight: 'bold',
    fontSize: '20px',
    color: '#1e40af'
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
    backgroundColor: '#10b981',
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
    fontSize: '48px',
    fontWeight: '800',
    color: '#1e40af',
    marginBottom: '24px',
    lineHeight: '1.1'
  },
  heroSubtitle: {
    fontSize: '24px',
    fontWeight: '600',
    color: '#374151',
    marginBottom: '16px',
    maxWidth: '800px',
    margin: '0 auto 16px'
  },
  heroDescription: {
    fontSize: '18px',
    color: '#6b7280',
    marginBottom: '32px',
    maxWidth: '600px',
    margin: '0 auto 32px'
  },
  buttonContainer: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '16px',
    justifyContent: 'center',
    marginBottom: '64px'
  },
  primaryButton: {
    background: 'linear-gradient(135deg, #6B4EFF 0%, #1e40af 100%)',
    color: 'white',
    padding: '12px 32px',
    borderRadius: '8px',
    fontWeight: '500',
    border: 'none',
    cursor: 'pointer',
    boxShadow: '0 4px 12px rgba(107, 78, 255, 0.3)',
    transition: 'all 0.2s',
    fontSize: '16px'
  },
  secondaryButton: {
    border: '2px solid #6B4EFF',
    color: '#6B4EFF',
    padding: '12px 32px',
    borderRadius: '8px',
    fontWeight: '500',
    background: 'transparent',
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
    fontSize: '36px',
    fontWeight: 'bold',
    color: '#1e40af',
    marginBottom: '16px'
  },
  featuresSubtitle: {
    fontSize: '18px',
    color: '#6b7280',
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
    borderRadius: '12px',
    padding: '24px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
    border: '1px solid #e5e7eb',
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
    background: 'linear-gradient(135deg, #6B4EFF 0%, #1e40af 100%)',
    color: 'white',
    padding: '80px 24px'
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
    background: 'white',
    color: '#1e40af',
    padding: '12px 32px',
    borderRadius: '8px',
    fontWeight: '500',
    border: 'none',
    cursor: 'pointer',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
    fontSize: '16px'
  }
}

const features = [
  {
    title: "Synthetic Patient Generation",
    description: "Create realistic patient cohorts with complex medical histories, demographics, and clinical pathways.",
    gradient: "linear-gradient(135deg, #6B4EFF 0%, #8b5cf6 100%)"
  },
  {
    title: "Privacy-First Architecture",
    description: "HIPAA-compliant synthetic data generation with zero risk of patient privacy exposure.",
    gradient: "linear-gradient(135deg, #10b981 0%, #34d399 100%)"
  },
  {
    title: "AI-Powered Validation",
    description: "Advanced statistical validation and bias detection to ensure data quality and representativeness.",
    gradient: "linear-gradient(135deg, #1e40af 0%, #3b82f6 100%)"
  },
  {
    title: "Real-time Analytics",
    description: "Interactive dashboards and comprehensive audit trails for complete transparency and control.",
    gradient: "linear-gradient(135deg, #f59e0b 0%, #f97316 100%)"
  },
  {
    title: "Scalable Infrastructure",
    description: "Generate cohorts from hundreds to millions of patients with enterprise-grade performance.",
    gradient: "linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)"
  },
  {
    title: "Research Ready",
    description: "Pre-configured templates for clinical trials, drug discovery, and healthcare AI development.",
    gradient: "linear-gradient(135deg, #ec4899 0%, #f472b6 100%)"
  }
]

function App() {
  return (
    <div style={styles.container}>
      <style>
        {`
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
          @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
          }
          .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
          }
          .primary-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(107, 78, 255, 0.4);
          }
          .secondary-button:hover {
            background: #6B4EFF;
            color: white;
          }
          .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
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
            <h1 style={styles.heroTitle}>Synthetic Ascension</h1>
            <p style={styles.heroSubtitle}>Simulate. Validate. Ascend.</p>
            <p style={styles.heroDescription}>
              Your launchpad to validated, privacy-safe EHR simulation—fueling the next generation of AI, research, and healthtech.
            </p>
            
            <div style={{...styles.buttonContainer, flexDirection: 'row'}} className="button-container">
              <button style={styles.primaryButton} className="primary-button">
                Launch Demo →
              </button>
              <button style={styles.secondaryButton} className="secondary-button">
                Design Partnership Interest
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
                <div style={{...styles.cardIcon, background: feature.gradient}}>
                  <div style={{width: '24px', height: '24px', background: 'white', borderRadius: '4px'}}></div>
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
            <button style={styles.ctaButton} className="cta-button">
              Start Your Demo →
            </button>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App