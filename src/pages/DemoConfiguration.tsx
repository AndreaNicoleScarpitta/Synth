import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Settings, Users, Activity, Play, ChevronDown } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useAppStore } from '@/store/useAppStore'

export function DemoConfiguration() {
  const navigate = useNavigate()
  const { cohortConfig, setCohortConfig, setCurrentWorkflow, setIsGenerating } = useAppStore()
  const [selectedUseCase, setSelectedUseCase] = useState('')

  const useCaseConfigurations = {
    'pediatric-cardiology': {
      size: 500,
      ageRange: [2, 17],
      complexity: 'high' as const,
      conditions: ['cardiovascular disease', 'pediatric care'],
      specialty: 'Pediatric Cardiology & Hematology',
      dataModalities: ['Echocardiography', 'Laboratory Results', 'Clinical Notes', 'Surgical Reports'],
      followUpDuration: 60
    },
    'rare-disease': {
      size: 250,
      ageRange: [0, 65],
      complexity: 'high' as const,
      conditions: ['oncology', 'pediatric care'],
      specialty: 'Medical Genetics',
      dataModalities: ['Genetic Testing', 'Laboratory Results', 'Clinical Notes', 'Imaging Studies'],
      followUpDuration: 120
    },
    'clinical-trials': {
      size: 1000,
      ageRange: [18, 75],
      complexity: 'medium' as const,
      conditions: ['cardiovascular disease', 'diabetes', 'hypertension'],
      specialty: 'Clinical Research',
      dataModalities: ['Laboratory Results', 'Vital Signs', 'Clinical Notes', 'Adverse Events'],
      followUpDuration: 24
    },
    'pharmacovigilance': {
      size: 750,
      ageRange: [12, 85],
      complexity: 'high' as const,
      conditions: ['oncology', 'cardiovascular disease'],
      specialty: 'Pharmacovigilance',
      dataModalities: ['Adverse Event Reports', 'Laboratory Results', 'Clinical Notes', 'Medication History'],
      followUpDuration: 36
    }
  }

  const useCases = [
    {
      id: 'pediatric-cardiology',
      name: 'Pediatric Cardiology Research',
      description: 'Generate synthetic pediatric cardiac patients with comprehensive hematological data for research studies'
    },
    {
      id: 'rare-disease',
      name: 'Rare Disease Studies',
      description: 'Create synthetic cohorts for rare genetic conditions with longitudinal follow-up data'
    },
    {
      id: 'clinical-trials',
      name: 'Clinical Trial Simulation',
      description: 'Simulate patient populations for drug trial design and endpoint validation'
    },
    {
      id: 'pharmacovigilance',
      name: 'Pharmacovigilance Analysis',
      description: 'Generate adverse event reports and medication safety surveillance data'
    }
  ]

  const handleUseCaseChange = (useCaseId: string) => {
    setSelectedUseCase(useCaseId)
    if (useCaseId && useCaseConfigurations[useCaseId]) {
      const config = useCaseConfigurations[useCaseId]
      setCohortConfig({
        size: config.size,
        ageRange: config.ageRange,
        complexity: config.complexity,
        conditions: config.conditions
      })
    }
  }

  const handleStartGeneration = () => {
    setIsGenerating(true)
    setCurrentWorkflow('generation')
    // Simulate generation process
    setTimeout(() => {
      setIsGenerating(false)
      setCurrentWorkflow('complete')
      navigate('/results')
    }, 3000)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <h1 className="font-syne text-4xl font-bold text-ascension-blue mb-4">
          Configure Your Synthetic Cohort
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Define the parameters for your synthetic patient population. Our AI will generate realistic, 
          privacy-compliant data based on your specifications.
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Configuration Panel */}
        <div className="lg:col-span-2 space-y-6">
          {/* Use Case Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Activity className="w-5 h-5 text-signal-violet" />
                <span>Select Use Case Scenario</span>
              </CardTitle>
              <CardDescription>
                Choose a predefined scenario to automatically configure parameters and settings.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="relative">
                <select
                  value={selectedUseCase}
                  onChange={(e) => handleUseCaseChange(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg appearance-none bg-white focus:ring-2 focus:ring-signal-violet focus:border-transparent"
                >
                  <option value="">Select a use case scenario...</option>
                  {useCases.map((useCase) => (
                    <option key={useCase.id} value={useCase.id}>
                      {useCase.name}
                    </option>
                  ))}
                </select>
                <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
              </div>
              
              {selectedUseCase && (
                <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <h4 className="font-semibold text-blue-900 mb-2">
                    {useCases.find(uc => uc.id === selectedUseCase)?.name}
                  </h4>
                  <p className="text-sm text-blue-700 mb-3">
                    {useCases.find(uc => uc.id === selectedUseCase)?.description}
                  </p>
                  <div className="text-sm text-blue-600">
                    <div className="grid grid-cols-2 gap-2">
                      <div><strong>Specialty:</strong> {useCaseConfigurations[selectedUseCase]?.specialty}</div>
                      <div><strong>Patient Count:</strong> {useCaseConfigurations[selectedUseCase]?.size}</div>
                      <div><strong>Age Range:</strong> {useCaseConfigurations[selectedUseCase]?.ageRange[0]}-{useCaseConfigurations[selectedUseCase]?.ageRange[1]} years</div>
                      <div><strong>Complexity:</strong> {useCaseConfigurations[selectedUseCase]?.complexity}</div>
                    </div>
                    <div className="mt-2">
                      <strong>Data Modalities:</strong> {useCaseConfigurations[selectedUseCase]?.dataModalities.join(', ')}
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Users className="w-5 h-5 text-signal-violet" />
                <span>Population Parameters</span>
              </CardTitle>
              <CardDescription>
                Define the size and demographic characteristics of your synthetic cohort.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Cohort Size
                </label>
                <div className="flex items-center space-x-4">
                  <input
                    type="range"
                    min="10"
                    max="10000"
                    value={cohortConfig.size}
                    onChange={(e) => setCohortConfig({ size: parseInt(e.target.value) })}
                    className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                  <span className="text-lg font-semibold text-signal-violet min-w-[80px]">
                    {cohortConfig.size.toLocaleString()}
                  </span>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Age Range
                  </label>
                  <div className="flex items-center space-x-2">
                    <input
                      type="number"
                      value={cohortConfig.ageRange[0]}
                      onChange={(e) => setCohortConfig({ 
                        ageRange: [parseInt(e.target.value), cohortConfig.ageRange[1]] 
                      })}
                      className="w-20 px-3 py-2 border border-gray-300 rounded-md"
                    />
                    <span className="text-gray-500">to</span>
                    <input
                      type="number"
                      value={cohortConfig.ageRange[1]}
                      onChange={(e) => setCohortConfig({ 
                        ageRange: [cohortConfig.ageRange[0], parseInt(e.target.value)] 
                      })}
                      className="w-20 px-3 py-2 border border-gray-300 rounded-md"
                    />
                    <span className="text-gray-500">years</span>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Complexity Level
                  </label>
                  <select
                    value={cohortConfig.complexity}
                    onChange={(e) => setCohortConfig({ 
                      complexity: e.target.value as 'low' | 'medium' | 'high' 
                    })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  >
                    <option value="low">Low - Basic demographics</option>
                    <option value="medium">Medium - Clinical conditions</option>
                    <option value="high">High - Complex comorbidities</option>
                  </select>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Activity className="w-5 h-5 text-biotech-green" />
                <span>Clinical Focus</span>
              </CardTitle>
              <CardDescription>
                Select medical conditions and specialties to focus on.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4">
                {[
                  'Cardiovascular Disease',
                  'Diabetes',
                  'Hypertension',
                  'Respiratory Conditions',
                  'Mental Health',
                  'Oncology',
                  'Pediatric Care',
                  'Geriatric Care'
                ].map((condition) => (
                  <label key={condition} className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      checked={cohortConfig.conditions.includes(condition.toLowerCase())}
                      onChange={(e) => {
                        const conditions = e.target.checked
                          ? [...cohortConfig.conditions, condition.toLowerCase()]
                          : cohortConfig.conditions.filter(c => c !== condition.toLowerCase())
                        setCohortConfig({ conditions })
                      }}
                      className="w-4 h-4 text-signal-violet border-gray-300 rounded"
                    />
                    <span className="text-sm text-gray-700">{condition}</span>
                  </label>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Summary Panel */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Settings className="w-5 h-5 text-ascension-blue" />
                <span>Configuration Summary</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Cohort Size:</span>
                <span className="font-semibold">{cohortConfig.size.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Age Range:</span>
                <span className="font-semibold">
                  {cohortConfig.ageRange[0]}-{cohortConfig.ageRange[1]} years
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Complexity:</span>
                <span className="font-semibold capitalize">{cohortConfig.complexity}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Conditions:</span>
                <span className="font-semibold">{cohortConfig.conditions.length}</span>
              </div>
              
              <div className="pt-4 border-t">
                <div className="text-sm text-gray-500 mb-4">
                  Estimated generation time: ~2-3 minutes
                </div>
                <Button
                  onClick={handleStartGeneration}
                  variant="brand"
                  size="lg"
                  className="w-full"
                >
                  <Play className="w-4 h-4 mr-2" />
                  Generate Synthetic Cohort
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Privacy & Compliance</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-gray-600 space-y-2">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-biotech-green rounded-full"></div>
                <span>HIPAA Compliant</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-biotech-green rounded-full"></div>
                <span>Zero Patient Data Exposure</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-biotech-green rounded-full"></div>
                <span>Synthetic Data Only</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-biotech-green rounded-full"></div>
                <span>Full Audit Trail</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}