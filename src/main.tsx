import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './index.css'
import App from './App'
import PatientRecord from './pages/PatientRecord'
import ResultsOverview from './pages/ResultsOverview'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/results" element={<ResultsOverview results={null} onBackToDemo={() => window.location.href = '/'} />} />
        <Route path="/patient/:patientId" element={<PatientRecord />} />
      </Routes>
    </Router>
  </React.StrictMode>,
)