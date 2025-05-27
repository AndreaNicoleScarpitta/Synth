import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Navigation } from './components/Navigation'
import { LandingPage } from './pages/LandingPage'
import { DemoConfiguration } from './pages/DemoConfiguration'
import { ResultsOverview } from './pages/ResultsOverview'
import { PatientExplorer } from './pages/PatientExplorer'
import { AdvancedAnalytics } from './pages/AdvancedAnalytics'
import { MLAnalytics } from './pages/MLAnalytics'
import { AuditTrails } from './pages/AuditTrails'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <Navigation />
      <main className="pt-16">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/demo" element={<DemoConfiguration />} />
          <Route path="/results" element={<ResultsOverview />} />
          <Route path="/patients" element={<PatientExplorer />} />
          <Route path="/analytics" element={<AdvancedAnalytics />} />
          <Route path="/ml" element={<MLAnalytics />} />
          <Route path="/audit" element={<AuditTrails />} />
        </Routes>
      </main>
    </div>
  )
}

export default App