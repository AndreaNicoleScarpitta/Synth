import { create } from 'zustand'

export interface PatientData {
  id: string
  name: string
  age: number
  gender: 'male' | 'female' | 'other'
  diagnosis: string
  riskScore: number
  lastVisit: string
  status: 'active' | 'inactive' | 'critical'
}

export interface CohortConfig {
  size: number
  ageRange: [number, number]
  genderDistribution: {
    male: number
    female: number
    other: number
  }
  conditions: string[]
  complexity: 'low' | 'medium' | 'high'
  timeframe: string
}

export interface AnalysisResult {
  id: string
  title: string
  summary: string
  confidence: number
  dataPoints: number
  generatedAt: string
  type: 'statistical' | 'ml' | 'clinical'
}

interface AppStore {
  // Demo Configuration
  cohortConfig: CohortConfig
  setCohortConfig: (config: Partial<CohortConfig>) => void
  
  // Generated Data
  patients: PatientData[]
  setPatients: (patients: PatientData[]) => void
  
  // Analysis Results
  analysisResults: AnalysisResult[]
  addAnalysisResult: (result: AnalysisResult) => void
  
  // UI State
  isGenerating: boolean
  setIsGenerating: (generating: boolean) => void
  
  selectedPatient: PatientData | null
  setSelectedPatient: (patient: PatientData | null) => void
  
  // Workflow State
  currentWorkflow: 'config' | 'generation' | 'analysis' | 'complete'
  setCurrentWorkflow: (workflow: 'config' | 'generation' | 'analysis' | 'complete') => void
}

export const useAppStore = create<AppStore>((set) => ({
  // Initial state
  cohortConfig: {
    size: 100,
    ageRange: [18, 85],
    genderDistribution: { male: 45, female: 50, other: 5 },
    conditions: ['diabetes', 'hypertension'],
    complexity: 'medium',
    timeframe: '1-year'
  },
  
  patients: [],
  analysisResults: [],
  isGenerating: false,
  selectedPatient: null,
  currentWorkflow: 'config',
  
  // Actions
  setCohortConfig: (config) =>
    set((state) => ({
      cohortConfig: { ...state.cohortConfig, ...config }
    })),
  
  setPatients: (patients) => set({ patients }),
  
  addAnalysisResult: (result) =>
    set((state) => ({
      analysisResults: [result, ...state.analysisResults]
    })),
  
  setIsGenerating: (generating) => set({ isGenerating: generating }),
  
  setSelectedPatient: (patient) => set({ selectedPatient: patient }),
  
  setCurrentWorkflow: (workflow) => set({ currentWorkflow: workflow })
}))