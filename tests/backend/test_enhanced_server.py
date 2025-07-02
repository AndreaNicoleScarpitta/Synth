"""
Comprehensive Backend Tests for Enhanced Synthetic Ascension Server V3
Tests the 50+ agent architecture, API endpoints, and system integration
"""

import pytest
import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, Any


class TestEnhancedBackendServer:
    """Test suite for Enhanced Backend Server V3 with comprehensive agent architecture"""
    
    BASE_URL = "http://localhost:8004"
    
    @pytest.fixture
    def client(self):
        """HTTP client for API testing"""
        return httpx.AsyncClient(base_url=self.BASE_URL, timeout=30.0)
    
    @pytest.mark.asyncio
    async def test_health_check(self, client: httpx.AsyncClient):
        """Test basic health check endpoint"""
        response = await client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["service"] == "Synthetic Ascension Enhanced Backend V3"
        assert data["status"] == "online"
        assert "agent_architecture" in data
        assert data["agent_architecture"]["total_agents"] == 50
    
    @pytest.mark.asyncio
    async def test_agent_architecture_overview(self, client: httpx.AsyncClient):
        """Test comprehensive agent architecture endpoint"""
        response = await client.get("/api/v3/architecture")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_agents"] == 50
        
        # Verify all 6 agent categories
        expected_categories = [
            "Cohort Constructor",
            "Clinical Journey Generator", 
            "Data Robustness & Noise",
            "QA & Validation",
            "Explanation & Provenance",
            "Supervision & Orchestration"
        ]
        
        for category in expected_categories:
            assert category in data["categories"]
            assert isinstance(data["categories"][category], int)
        
        # Verify agent roles distribution
        assert "roles" in data
        assert data["roles"]["doer"] + data["roles"]["coordinator"] + data["roles"]["adversarial"] == 50
    
    @pytest.mark.asyncio
    async def test_ehr_generation_request(self, client: httpx.AsyncClient):
        """Test enhanced EHR generation with comprehensive agent pipeline"""
        generation_request = {
            "use_case": "comprehensive_ehr_v2",
            "population_size": 25,
            "condition": "diabetes_mellitus_type_2",
            "enable_adversarial_testing": True,
            "require_clinical_review": True,
            "privacy_level": "high",
            "pipeline_config": {
                "enable_differential_privacy": True,
                "clinical_realism_threshold": 0.9,
                "temporal_consistency_check": True
            }
        }
        
        response = await client.post("/api/v3/generate", json=generation_request)
        assert response.status_code == 202
        
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "started"
        assert "Enhanced generation pipeline initiated" in data["message"]
        
        return data["job_id"]
    
    @pytest.mark.asyncio
    async def test_job_status_tracking(self, client: httpx.AsyncClient):
        """Test comprehensive job status tracking with phase monitoring"""
        # Start a generation job first
        job_id = await self.test_ehr_generation_request(client)
        
        # Check job status
        response = await client.get(f"/api/v3/jobs/{job_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["job_id"] == job_id
        assert data["status"] in ["pending", "running", "completed", "failed"]
        assert "progress" in data
        assert 0.0 <= data["progress"] <= 1.0
        
        # Verify phase tracking
        if "phase_results" in data:
            expected_phases = [
                "Cohort Constructor",
                "Clinical Journey Generator",
                "Data Robustness & Noise", 
                "QA & Validation",
                "Explanation & Provenance",
                "Supervision & Orchestration"
            ]
            
            for phase_name, phase_data in data["phase_results"].items():
                assert phase_name in expected_phases
                assert "status" in phase_data
                assert phase_data["status"] in ["pending", "running", "completed", "failed"]
    
    @pytest.mark.asyncio
    async def test_job_results_comprehensive(self, client: httpx.AsyncClient):
        """Test detailed job results with clinical metrics and privacy assessment"""
        # For this test, we'll use a mock completed job ID
        # In a real scenario, you'd wait for job completion or use a pre-completed job
        job_id = "test-completed-job-123"
        
        response = await client.get(f"/api/v3/jobs/{job_id}/results")
        
        # If job doesn't exist, that's expected for this test
        if response.status_code == 404:
            pytest.skip("No completed job available for testing results")
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify comprehensive result structure
            expected_fields = [
                "patients_generated",
                "clinical_realism_score",
                "privacy_assessment", 
                "differential_privacy_applied",
                "adversarial_tests_passed",
                "validation_metrics"
            ]
            
            for field in expected_fields:
                assert field in data
            
            # Verify clinical metrics
            if "validation_metrics" in data:
                metrics = data["validation_metrics"]
                assert "temporal_consistency" in metrics
                assert "clinical_coherence" in metrics
                assert "demographic_realism" in metrics
                
                # All metrics should be between 0 and 1
                for metric_value in metrics.values():
                    assert 0.0 <= metric_value <= 1.0
    
    @pytest.mark.asyncio
    async def test_langflow_export_system(self, client: httpx.AsyncClient):
        """Test Langflow workflow export functionality"""
        response = await client.get("/api/v3/langflow/export")
        assert response.status_code == 200
        
        data = response.json()
        assert data["workflows_exported"] == 50
        assert len(data["categories"]) == 6
        assert "export_timestamp" in data
        
        # Verify timestamp is recent (within last hour)
        export_time = datetime.fromisoformat(data["export_timestamp"].replace('Z', '+00:00'))
        time_diff = datetime.now(export_time.tzinfo) - export_time
        assert time_diff.total_seconds() < 3600  # Less than 1 hour
    
    @pytest.mark.asyncio 
    async def test_langflow_download(self, client: httpx.AsyncClient):
        """Test Langflow ZIP download functionality"""
        response = await client.get("/api/v3/langflow/download")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/zip"
        assert "synthetic_ascension_langflow_export.zip" in response.headers.get("content-disposition", "")
    
    @pytest.mark.asyncio
    async def test_langflow_workflow_execution(self, client: httpx.AsyncClient):
        """Test execution of Langflow workflows"""
        workflow_data = {
            "workflow_name": "test_cohort_generation",
            "nodes": [
                {
                    "id": "demographic_agent",
                    "type": "DemographicAgent",
                    "config": {"age_range": [25, 65], "gender_distribution": "balanced"}
                },
                {
                    "id": "clinical_agent", 
                    "type": "ClinicalAgent",
                    "config": {"condition": "hypertension", "severity": "moderate"}
                }
            ],
            "edges": [
                {"source": "demographic_agent", "target": "clinical_agent"}
            ]
        }
        
        response = await client.post("/api/v3/langflow/execute", json=workflow_data)
        assert response.status_code == 202
        
        data = response.json()
        assert "execution_id" in data
        assert data["status"] == "started"
        assert data["workflow_nodes"] == 2
    
    @pytest.mark.asyncio
    async def test_system_analytics(self, client: httpx.AsyncClient):
        """Test comprehensive system analytics"""
        response = await client.get("/api/v3/analytics")
        assert response.status_code == 200
        
        data = response.json()
        
        # Verify analytics structure
        expected_fields = [
            "total_jobs_completed",
            "total_patients_generated", 
            "avg_generation_time_minutes",
            "success_rate",
            "agent_performance"
        ]
        
        for field in expected_fields:
            assert field in data
        
        # Verify agent performance metrics
        agent_perf = data["agent_performance"]
        assert "most_used_category" in agent_perf
        assert "avg_agents_per_job" in agent_perf
        assert "adversarial_test_pass_rate" in agent_perf
        
        # Success rates should be reasonable
        assert 0.5 <= data["success_rate"] <= 1.0
        assert 0.5 <= agent_perf["adversarial_test_pass_rate"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_ux_dashboard_endpoints(self, client: httpx.AsyncClient):
        """Test UX-focused dashboard endpoints"""
        # Test dashboard summary
        response = await client.get("/api/ux/dashboard/summary")
        assert response.status_code == 200
        
        data = response.json()
        assert "active_jobs" in data
        assert "completed_today" in data
        assert "total_agents" in data
        assert data["total_agents"] == 50
        assert "system_status" in data
        assert data["system_status"] in ["optimal", "good", "warning", "error"]
        
        # Test recent jobs
        response = await client.get("/api/ux/dashboard/recent-jobs?limit=5")
        assert response.status_code == 200
        
        jobs_data = response.json()
        assert isinstance(jobs_data, list)
        assert len(jobs_data) <= 5
        
        # Test agent status
        response = await client.get("/api/ux/agents/status")
        assert response.status_code == 200
        
        agent_data = response.json()
        assert "active_agents" in agent_data
        assert "idle_agents" in agent_data
        assert agent_data["active_agents"] + agent_data["idle_agents"] == 50
    
    @pytest.mark.asyncio
    async def test_system_health_monitoring(self, client: httpx.AsyncClient):
        """Test comprehensive system health monitoring"""
        response = await client.get("/api/ux/system/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "warning", "critical"]
        assert "agents_active" in data
        assert "database_connected" in data
        assert data["database_connected"] is True
        assert "memory_usage" in data
        
        # Test system metrics
        response = await client.get("/api/ux/system/metrics")
        assert response.status_code == 200
        
        metrics = response.json()
        assert "cpu_usage" in metrics
        assert "memory_usage" in metrics
        assert "disk_usage" in metrics
        assert "active_connections" in metrics
    
    @pytest.mark.asyncio
    async def test_error_handling(self, client: httpx.AsyncClient):
        """Test comprehensive error handling"""
        # Test invalid job ID
        response = await client.get("/api/v3/jobs/invalid-job-123")
        assert response.status_code == 404
        
        error_data = response.json()
        assert "error" in error_data
        assert "Job not found" in error_data["error"]
        
        # Test invalid generation request
        invalid_request = {
            "population_size": -10,  # Invalid
            "condition": "",         # Empty
            "privacy_level": "invalid"  # Invalid enum
        }
        
        response = await client.post("/api/v3/generate", json=invalid_request)
        assert response.status_code == 422
        
        validation_error = response.json()
        assert "error" in validation_error
        assert "validation" in validation_error["error"].lower()
    
    @pytest.mark.asyncio
    async def test_api_documentation_availability(self, client: httpx.AsyncClient):
        """Test that API documentation is available"""
        response = await client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        
        # Test OpenAPI specification
        response = await client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_spec = response.json()
        assert openapi_spec["openapi"] == "3.0.0"
        assert "info" in openapi_spec
        assert "Synthetic Ascension" in openapi_spec["info"]["title"]
    
    @pytest.mark.asyncio
    async def test_concurrent_job_handling(self, client: httpx.AsyncClient):
        """Test system's ability to handle concurrent generation jobs"""
        tasks = []
        
        for i in range(3):
            request_data = {
                "use_case": f"concurrent_test_{i}",
                "population_size": 10,
                "condition": "hypertension",
                "enable_adversarial_testing": False
            }
            
            task = client.post("/api/v3/generate", json=request_data)
            tasks.append(task)
        
        # Execute all requests concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All should succeed
        for response in responses:
            assert not isinstance(response, Exception)
            assert response.status_code == 202
            
            data = response.json()
            assert "job_id" in data
            assert data["status"] == "started"


class TestSystemIntegration:
    """Integration tests that verify the entire system works together"""
    
    @pytest.mark.asyncio
    async def test_full_workflow_integration(self):
        """Test complete workflow from generation to results retrieval"""
        async with httpx.AsyncClient(base_url="http://localhost:8004", timeout=60.0) as client:
            # Step 1: Generate EHR data
            generation_request = {
                "use_case": "integration_test",
                "population_size": 5,  # Small for faster testing
                "condition": "hypertension",
                "enable_adversarial_testing": True,
                "require_clinical_review": True
            }
            
            response = await client.post("/api/v3/generate", json=generation_request)
            assert response.status_code == 202
            
            job_data = response.json()
            job_id = job_data["job_id"]
            
            # Step 2: Monitor job progress
            max_attempts = 30  # 5 minutes with 10-second intervals
            attempt = 0
            
            while attempt < max_attempts:
                await asyncio.sleep(10)  # Wait 10 seconds
                
                status_response = await client.get(f"/api/v3/jobs/{job_id}")
                assert status_response.status_code == 200
                
                status_data = status_response.json()
                
                if status_data["status"] == "completed":
                    # Step 3: Retrieve results
                    results_response = await client.get(f"/api/v3/jobs/{job_id}/results")
                    assert results_response.status_code == 200
                    
                    results = results_response.json()
                    assert results["patients_generated"] == 5
                    assert "clinical_realism_score" in results
                    assert "privacy_assessment" in results
                    break
                    
                elif status_data["status"] == "failed":
                    pytest.fail(f"Job failed: {status_data.get('error', 'Unknown error')}")
                
                attempt += 1
            
            else:
                pytest.fail("Job did not complete within expected time")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])