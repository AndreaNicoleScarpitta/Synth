import React from 'react'
import { useParams } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'

const PatientRecord: React.FC = () => {
  const { patientId } = useParams<{ patientId: string }>()

  const handleBackClick = () => {
    window.close()
  }

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
    backButton: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      backgroundColor: '#f3f4f6',
      color: '#374151',
      padding: '8px 16px',
      borderRadius: '8px',
      border: 'none',
      fontWeight: '500',
      cursor: 'pointer',
      fontSize: '14px',
      marginBottom: '32px'
    },
    patientTitle: {
      fontSize: '36px',
      fontWeight: '700',
      color: '#1f2937',
      marginBottom: '32px',
      textAlign: 'center' as const
    },
    blankMessage: {
      textAlign: 'center' as const,
      fontSize: '18px',
      color: '#6b7280',
      marginTop: '64px'
    }
  }

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <nav style={styles.nav}>
          <div style={styles.logo}>
            <div style={styles.logoIcon}>SA</div>
            <span style={styles.logoText}>Synthetic Ascension</span>
          </div>
          <div>
            <span style={{ fontSize: '14px', color: '#6b7280' }}>
              Patient Record View
            </span>
          </div>
        </nav>
      </header>

      <main style={styles.main}>
        <button style={styles.backButton} onClick={handleBackClick}>
          <ArrowLeft size={16} />
          Close Window
        </button>

        <h1 style={styles.patientTitle}>
          {patientId || 'Unknown Patient'}
        </h1>

        <div style={styles.blankMessage}>
          Intentionally Blank
        </div>
      </main>
    </div>
  )
}

export default PatientRecord