import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Play, Settings, Info } from 'lucide-react'

const DemoConfiguration = () => {
  const navigate = useNavigate()
  const [config, setConfig] = useState({
    cohortSize: 10,
    ageRange: 'newborn',
    condition: 'tetralogy_fallot',
    severity: 'moderate',
    includeGenetic: false,
    includePharmacological: false
  })

  const [isGenerating, setIsGenerating] = useState(false)

  const handleGenerate = async () => {
    setIsGenerating(true)
    // Simulate cohort generation
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Store generated data and navigate to results
    const mockCohortData = Array.from({ length: config.cohortSize }, (_, i) => ({
      id: i + 1,
      age_months: config.ageRange === 'newborn' ? Math.floor(Math.random() * 12) : Math.floor(Math.random() * 36) + 12,
      sex: Math.random() > 0.5 ? 'Male' : 'Female',
      primary_diagnosis: config.condition.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
      weight_kg: 3 + Math.random() * 15,
      height_cm: 45 + Math.random() * 30,
      hemodynamics: {
        heart_rate_bpm: 120 + Math.floor(Math.random() * 40),
        systolic_bp: 70 + Math.floor(Math.random() * 30),
        diastolic_bp: 40 + Math.floor(Math.random() * 20),
        oxygen_saturation: 85 + Math.floor(Math.random() * 15)
      }
    }))

    // Store in localStorage for now (would be proper state management in production)
    localStorage.setItem('cohortData', JSON.stringify(mockCohortData))
    setIsGenerating(false)
    navigate('/results')
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="px-6 py-4 border-b">
          <h1 className="heading-syne text-2xl font-bold text-gray-900">
            Pediatric Cardiology Demo Configuration
          </h1>
          <p className="text-gray-600 mt-2">
            Configure synthetic patient cohort parameters for generation
          </p>
        </div>

        <div className="p-6 space-y-6">
          {/* Cohort Size */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Cohort Size
              <span className="ml-1 text-blue-500">
                <Info className="w-4 h-4 inline" title="Number of synthetic patients to generate" />
              </span>
            </label>
            <select
              value={config.cohortSize}
              onChange={(e) => setConfig({...config, cohortSize: parseInt(e.target.value)})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value={5}>5 patients</option>
              <option value={10}>10 patients</option>
              <option value={25}>25 patients</option>
              <option value={50}>50 patients</option>
              <option value={100}>100 patients</option>
            </select>
          </div>

          {/* Age Range */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Age Range
              <span className="ml-1 text-blue-500">
                <Info className="w-4 h-4 inline" title="Target age demographics for synthetic patients" />
              </span>
            </label>
            <select
              value={config.ageRange}
              onChange={(e) => setConfig({...config, ageRange: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="newborn">Newborn (0-12 months)</option>
              <option value="infant">Infant (1-3 years)</option>
              <option value="mixed">Mixed pediatric ages</option>
            </select>
          </div>

          {/* Primary Condition */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Primary Cardiac Condition
              <span className="ml-1 text-blue-500">
                <Info className="w-4 h-4 inline" title="Primary congenital heart defect for synthetic cohort" />
              </span>
            </label>
            <select
              value={config.condition}
              onChange={(e) => setConfig({...config, condition: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="tetralogy_fallot">Tetralogy of Fallot</option>
              <option value="ventricular_septal_defect">Ventricular Septal Defect (VSD)</option>
              <option value="atrial_septal_defect">Atrial Septal Defect (ASD)</option>
              <option value="hypoplastic_left_heart">Hypoplastic Left Heart Syndrome</option>
              <option value="mixed_conditions">Mixed cardiac conditions</option>
            </select>
          </div>

          {/* Severity */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Condition Severity
              <span className="ml-1 text-blue-500">
                <Info className="w-4 h-4 inline" title="Clinical severity level for hemodynamic modeling" />
              </span>
            </label>
            <select
              value={config.severity}
              onChange={(e) => setConfig({...config, severity: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="mild">Mild</option>
              <option value="moderate">Moderate</option>
              <option value="severe">Severe</option>
              <option value="critical">Critical</option>
            </select>
          </div>

          {/* Advanced Options */}
          <div className="border-t pt-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Advanced Options</h3>
            <div className="space-y-3">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={config.includeGenetic}
                  onChange={(e) => setConfig({...config, includeGenetic: e.target.checked})}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <span className="ml-2 text-sm text-gray-700">
                  Include genetic markers (Coming Soon)
                </span>
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={config.includePharmacological}
                  onChange={(e) => setConfig({...config, includePharmacological: e.target.checked})}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <span className="ml-2 text-sm text-gray-700">
                  Include pharmacological management (Coming Soon)
                </span>
              </label>
            </div>
          </div>

          {/* Generate Button */}
          <div className="border-t pt-6">
            <button
              onClick={handleGenerate}
              disabled={isGenerating}
              className={`w-full flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white ${
                isGenerating 
                  ? 'bg-gray-400 cursor-not-allowed' 
                  : 'bg-primary-600 hover:bg-primary-700'
              } transition-colors`}
            >
              {isGenerating ? (
                <>
                  <Settings className="animate-spin -ml-1 mr-3 h-5 w-5" />
                  Generating Synthetic Cohort...
                </>
              ) : (
                <>
                  <Play className="-ml-1 mr-3 h-5 w-5" />
                  Generate Synthetic Cohort
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DemoConfiguration