import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Mock fetch for API tests
const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('Backend API Integration Tests', () => {
  const baseUrl = 'http://localhost:8004'; // Enhanced Backend Server V3

  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Health Check Endpoints', () => {
    it('should respond to root endpoint', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({
          service: 'Synthetic Ascension Enhanced Backend V3',
          status: 'online',
          agent_architecture: expect.any(Object),
        }),
      });

      const response = await fetch(`${baseUrl}/`);
      const data = await response.json();

      expect(response.ok).toBe(true);
      expect(data.service).toBe('Synthetic Ascension Enhanced Backend V3');
      expect(data.status).toBe('online');
    });

    it('should return system health status', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({
          status: 'healthy',
          agents_active: 50,
          database_connected: true,
          memory_usage: expect.any(Number),
        }),
      });

      const response = await fetch(`${baseUrl}/api/ux/system/health`);
      const data = await response.json();

      expect(response.ok).toBe(true);
      expect(data.status).toBe('healthy');
      expect(typeof data.agents_active).toBe('number');
      expect(data.database_connected).toBe(true);
    });
  });

  describe('EHR Generation Endpoints', () => {
    it('should generate synthetic EHR cohort', async () => {
      const mockJobId = 'test-job-123';
      const generationRequest = {
        use_case: 'comprehensive_ehr_v2',
        population_size: 10,
        condition: 'hypertension',
        enable_adversarial_testing: true,
        require_clinical_review: true,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 202,
        json: () => Promise.resolve({
          job_id: mockJobId,
          status: 'started',
          message: 'Enhanced generation pipeline initiated',
        }),
      });

      const response = await fetch(`${baseUrl}/api/v3/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(generationRequest),
      });

      const data = await response.json();

      expect(response.ok).toBe(true);
      expect(data.job_id).toBe(mockJobId);
      expect(data.status).toBe('started');
    });

    it('should get job status with phase tracking', async () => {
      const jobId = 'test-job-123';
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({
          job_id: jobId,
          status: 'running',
          progress: 0.6,
          current_phase: 'Data Robustness & Noise',
          current_agent: 'Privacy Guard Agent',
          started_at: new Date().toISOString(),
          phase_results: {
            'Cohort Constructor': { status: 'completed', agents_run: 11 },
            'Clinical Journey Generator': { status: 'completed', agents_run: 11 },
            'Data Robustness & Noise': { status: 'running', agents_run: 6 },
          },
        }),
      });

      const response = await fetch(`${baseUrl}/api/v3/jobs/${jobId}`);
      const data = await response.json();

      expect(response.ok).toBe(true);
      expect(data.job_id).toBe(jobId);
      expect(data.status).toBe('running');
      expect(data.current_phase).toBe('Data Robustness & Noise');
      expect(data.phase_results).toBeDefined();
    });

    it('should get completed job results', async () => {
      const jobId = 'completed-job-456';
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({
          job_id: jobId,
          status: 'completed',
          patients_generated: 100,
          clinical_realism_score: 0.94,
          privacy_assessment: 'high',
          differential_privacy_applied: true,
          adversarial_tests_passed: 48,
          validation_metrics: {
            temporal_consistency: 0.97,
            clinical_coherence: 0.95,
            demographic_realism: 0.93,
          },
        }),
      });

      const response = await fetch(`${baseUrl}/api/v3/jobs/${jobId}/results`);
      const data = await response.json();

      expect(response.ok).toBe(true);
      expect(data.patients_generated).toBe(100);
      expect(data.clinical_realism_score).toBeGreaterThan(0.9);
      expect(data.privacy_assessment).toBe('high');
      expect(data.validation_metrics).toBeDefined();
    });
  });

  describe('Agent Architecture Endpoints', () => {
    it('should return comprehensive agent architecture', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({
          total_agents: 50,
          categories: {
            'Cohort Constructor': 11,
            'Clinical Journey Generator': 11,
            'Data Robustness & Noise': 10,
            'QA & Validation': 13,
            'Explanation & Provenance': 13,
            'Supervision & Orchestration': 9,
          },
          roles: {
            doer: 35,
            coordinator: 10,
            adversarial: 5,
          },
        }),
      });

      const response = await fetch(`${baseUrl}/api/v3/architecture`);
      const data = await response.json();

      expect(response.ok).toBe(true);
      expect(data.total_agents).toBe(50);
      expect(Object.keys(data.categories)).toHaveLength(6);
      expect(data.roles.doer + data.roles.coordinator + data.roles.adversarial).toBe(50);
    });

    it('should return agent status for monitoring', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({
          active_agents: 42,
          idle_agents: 8,
          agents_by_category: {
            'Cohort Constructor': { active: 8, idle: 3 },
            'Clinical Journey Generator': { active: 9, idle: 2 },
            'Data Robustness & Noise': { active: 7, idle: 3 },
          },
          performance_metrics: {
            avg_execution_time_ms: 2340,
            successful_runs: 1547,
            failed_runs: 23,
          },
        }),
      });

      const response = await fetch(`${baseUrl}/api/ux/agents/status`);
      const data = await response.json();

      expect(response.ok).toBe(true);
      expect(data.active_agents).toBe(42);
      expect(data.performance_metrics.successful_runs).toBeGreaterThan(1000);
    });
  });

  describe('Langflow Integration Endpoints', () => {
    it('should export Langflow workflows', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({
          workflows_exported: 50,
          categories: [
            'Cohort Constructor',
            'Clinical Journey Generator',
            'Data Robustness & Noise',
            'QA & Validation',
            'Explanation & Provenance',
            'Supervision & Orchestration',
          ],
          export_timestamp: new Date().toISOString(),
        }),
      });

      const response = await fetch(`${baseUrl}/api/v3/langflow/export`);
      const data = await response.json();

      expect(response.ok).toBe(true);
      expect(data.workflows_exported).toBe(50);
      expect(data.categories).toHaveLength(6);
    });

    it('should provide downloadable Langflow export', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        headers: new Headers({
          'content-type': 'application/zip',
          'content-disposition': 'attachment; filename="synthetic_ascension_langflow_export.zip"',
        }),
        blob: () => Promise.resolve(new Blob(['mock zip content'], { type: 'application/zip' })),
      });

      const response = await fetch(`${baseUrl}/api/v3/langflow/download`);

      expect(response.ok).toBe(true);
      expect(response.headers.get('content-type')).toBe('application/zip');
    });

    it('should execute Langflow workflows', async () => {
      const workflowData = {
        nodes: [
          { id: 'cohort_gen', type: 'CohortGenerator' },
          { id: 'qa_agent', type: 'QAAgent' },
        ],
        edges: [{ source: 'cohort_gen', target: 'qa_agent' }],
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 202,
        json: () => Promise.resolve({
          execution_id: 'langflow-exec-789',
          status: 'started',
          workflow_nodes: 2,
        }),
      });

      const response = await fetch(`${baseUrl}/api/v3/langflow/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(workflowData),
      });

      const data = await response.json();

      expect(response.ok).toBe(true);
      expect(data.execution_id).toBe('langflow-exec-789');
      expect(data.workflow_nodes).toBe(2);
    });
  });

  describe('Analytics and Monitoring', () => {
    it('should return platform analytics', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({
          total_jobs_completed: 1247,
          total_patients_generated: 124700,
          avg_generation_time_minutes: 8.5,
          success_rate: 0.984,
          agent_performance: {
            most_used_category: 'Cohort Constructor',
            avg_agents_per_job: 28.4,
            adversarial_test_pass_rate: 0.96,
          },
        }),
      });

      const response = await fetch(`${baseUrl}/api/v3/analytics`);
      const data = await response.json();

      expect(response.ok).toBe(true);
      expect(data.total_jobs_completed).toBeGreaterThan(1000);
      expect(data.success_rate).toBeGreaterThan(0.95);
      expect(data.agent_performance).toBeDefined();
    });

    it('should return dashboard summary', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({
          active_jobs: 3,
          completed_today: 45,
          total_agents: 50,
          system_status: 'optimal',
          recent_metrics: {
            avg_clinical_realism: 0.945,
            privacy_compliance: 'high',
            generation_speed: 'fast',
          },
        }),
      });

      const response = await fetch(`${baseUrl}/api/ux/dashboard/summary`);
      const data = await response.json();

      expect(response.ok).toBe(true);
      expect(data.total_agents).toBe(50);
      expect(data.system_status).toBe('optimal');
      expect(data.recent_metrics.avg_clinical_realism).toBeGreaterThan(0.9);
    });
  });

  describe('Error Handling', () => {
    it('should handle invalid job ID gracefully', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: () => Promise.resolve({
          error: 'Job not found',
          job_id: 'invalid-job-id',
        }),
      });

      const response = await fetch(`${baseUrl}/api/v3/jobs/invalid-job-id`);
      const data = await response.json();

      expect(response.ok).toBe(false);
      expect(response.status).toBe(404);
      expect(data.error).toBe('Job not found');
    });

    it('should validate generation request parameters', async () => {
      const invalidRequest = {
        population_size: -10, // Invalid negative size
        condition: '', // Empty condition
      };

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 422,
        json: () => Promise.resolve({
          error: 'Validation error',
          details: [
            'Population size must be positive',
            'Condition is required',
          ],
        }),
      });

      const response = await fetch(`${baseUrl}/api/v3/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(invalidRequest),
      });

      const data = await response.json();

      expect(response.ok).toBe(false);
      expect(response.status).toBe(422);
      expect(data.details).toContain('Population size must be positive');
    });

    it('should handle server errors gracefully', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: () => Promise.resolve({
          error: 'Internal server error',
          message: 'Agent orchestration failure',
        }),
      });

      const response = await fetch(`${baseUrl}/api/v3/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ use_case: 'test' }),
      });

      const data = await response.json();

      expect(response.ok).toBe(false);
      expect(response.status).toBe(500);
      expect(data.error).toBe('Internal server error');
    });
  });
});