import React from 'react'
import { Routes, Route, useNavigate } from 'react-router-dom'
import { ThemeProvider } from './contexts/ThemeContext'
import Navigation from './components/Navigation'
import LandingPage from './pages/LandingPage'
import DemoConfiguration from './pages/DemoConfiguration'
import ResultsOverview from './pages/ResultsOverview'
import PatientExplorer from './pages/PatientExplorer'
import AdvancedAnalytics from './pages/AdvancedAnalytics'
import MLAnalytics from './pages/MLAnalytics'
import AuditTrails from './pages/AuditTrails'

function App() {
  const navigate = useNavigate()
  
  const handleStartDemo = () => {
    navigate('/demo')
  }

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-white dark:bg-neutral-900 transition-colors duration-300">
        <Navigation />
        <Routes>
          <Route path="/" element={<LandingPage onStartDemo={handleStartDemo} />} />
          <Route path="/demo" element={<DemoConfiguration />} />
          <Route path="/results" element={<ResultsOverview />} />
          <Route path="/patients" element={<PatientExplorer />} />
          <Route path="/analytics" element={<AdvancedAnalytics />} />
          <Route path="/ml" element={<MLAnalytics />} />
          <Route path="/audit" element={<AuditTrails />} />
        </Routes>
      </div>
    </ThemeProvider>
  )
}

export default App