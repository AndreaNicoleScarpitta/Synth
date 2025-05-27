import { create } from 'zustand'

interface CohortConfig {
  size: number
  ageRange: [number, number]
  complexity: 'low' | 'medium' | 'high'
  conditions: string[]
}

interface AppState {
  cohortConfig: CohortConfig
  currentWorkflow: 'idle' | 'generation' | 'analysis' | 'complete'
  isGenerating: boolean
  generatedData: any[]
  
  // Actions
  setCohortConfig: (updates: Partial<CohortConfig>) => void
  setCurrentWorkflow: (workflow: AppState['currentWorkflow']) => void
  setIsGenerating: (generating: boolean) => void
  setGeneratedData: (data: any[]) => void
}

export const useAppStore = create<AppState>((set) => ({
  cohortConfig: {
    size: 1000,
    ageRange: [18, 65],
    complexity: 'medium',
    conditions: []
  },
  currentWorkflow: 'idle',
  isGenerating: false,
  generatedData: [],
  
  setCohortConfig: (updates) =>
    set((state) => ({
      cohortConfig: { ...state.cohortConfig, ...updates }
    })),
  
  setCurrentWorkflow: (workflow) => set({ currentWorkflow: workflow }),
  setIsGenerating: (generating) => set({ isGenerating: generating }),
  setGeneratedData: (data) => set({ generatedData: data })
}))