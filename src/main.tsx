import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './index.css'
import App from './App'
import PatientRecord from './pages/PatientRecord'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/demo" element={<App />} />
        <Route path="/patient/:patientId" element={<PatientRecord />} />
        <Route path="*" element={<App />} />
      </Routes>
    </Router>
  </React.StrictMode>,
)