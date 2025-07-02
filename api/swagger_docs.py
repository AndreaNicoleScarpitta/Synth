"""
Swagger UI Documentation Server
Serves comprehensive API documentation for Synthetic Ascension platform
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import yaml
import json
import os

def create_docs_app():
    """Create FastAPI app for serving API documentation"""
    
    app = FastAPI(
        title="Synthetic Ascension API Documentation",
        description="Comprehensive API documentation for the EHR synthesis platform",
        version="3.0.0"
    )
    
    @app.get("/", response_class=HTMLResponse)
    async def docs_home():
        """Serve comprehensive API documentation homepage"""
        
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Synthetic Ascension API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
    <style>
        body { margin: 0; padding: 0; }
        .swagger-ui .topbar { display: none; }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }
        .header h1 { margin: 0; font-size: 2.5rem; }
        .header p { margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9; }
        .nav-section {
            background: #f8f9fa;
            padding: 1rem 2rem;
            border-bottom: 1px solid #dee2e6;
        }
        .nav-links {
            display: flex;
            gap: 2rem;
            align-items: center;
            flex-wrap: wrap;
        }
        .nav-link {
            color: #495057;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            border: 1px solid #ced4da;
            transition: all 0.2s;
        }
        .nav-link:hover {
            background: #e9ecef;
            text-decoration: none;
        }
        .nav-link.primary {
            background: #007bff;
            color: white;
            border-color: #007bff;
        }
        .nav-link.primary:hover {
            background: #0056b3;
        }
        .content { padding: 2rem; }
        .api-section {
            margin-bottom: 3rem;
            padding: 1.5rem;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            background: white;
        }
        .api-section h3 {
            color: #495057;
            margin-top: 0;
            border-bottom: 2px solid #007bff;
            padding-bottom: 0.5rem;
        }
        .endpoint-list {
            list-style: none;
            padding: 0;
        }
        .endpoint-list li {
            padding: 0.5rem 0;
            border-bottom: 1px solid #f8f9fa;
        }
        .endpoint-list li:last-child {
            border-bottom: none;
        }
        .method {
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 3px;
            color: white;
            font-weight: bold;
            font-size: 0.8rem;
            margin-right: 0.5rem;
            min-width: 45px;
            text-align: center;
        }
        .method.get { background: #28a745; }
        .method.post { background: #007bff; }
        .method.put { background: #ffc107; color: #212529; }
        .method.delete { background: #dc3545; }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        .feature {
            padding: 1.5rem;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            background: white;
        }
        .feature h4 {
            color: #007bff;
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏥 Synthetic Ascension API</h1>
        <p>Advanced AI-powered EHR synthesis platform with 50+ specialized agents</p>
    </div>
    
    <div class="nav-section">
        <div class="nav-links">
            <a href="/swagger" class="nav-link primary">📊 Interactive API Docs</a>
            <a href="/openapi.json" class="nav-link">📋 OpenAPI Spec (JSON)</a>
            <a href="/openapi.yaml" class="nav-link">📄 OpenAPI Spec (YAML)</a>
            <a href="http://localhost:8004" class="nav-link">🚀 Enhanced Backend V3</a>
            <a href="http://localhost:5000" class="nav-link">💻 React Frontend</a>
        </div>
    </div>
    
    <div class="content">
        <div class="features">
            <div class="feature">
                <h4>🤖 50+ Specialized Agents</h4>
                <p>Comprehensive agentic architecture with Doer/Coordinator/Adversarial roles across 6 categories</p>
            </div>
            <div class="feature">
                <h4>🔒 Enterprise Privacy</h4>
                <p>Differential privacy, k-anonymity scoring, and clinical realism certification</p>
            </div>
            <div class="feature">
                <h4>🌊 Langflow Integration</h4>
                <p>Visual workflow export and modification with plug-and-play compatibility</p>
            </div>
            <div class="feature">
                <h4>📈 Real-time Monitoring</h4>
                <p>6-phase pipeline execution with comprehensive audit trails and performance metrics</p>
            </div>
        </div>
        
        <div class="api-section">
            <h3>🎯 Core Generation API</h3>
            <ul class="endpoint-list">
                <li><span class="method post">POST</span> <code>/api/v3/generate</code> - Generate synthetic EHR data with 50+ agents</li>
                <li><span class="method get">GET</span> <code>/api/v3/jobs/{job_id}</code> - Check job status with phase tracking</li>
                <li><span class="method get">GET</span> <code>/api/v3/jobs/{job_id}/results</code> - Get detailed results with privacy assessments</li>
                <li><span class="method get">GET</span> <code>/api/v3/analytics</code> - Platform analytics and agent performance</li>
            </ul>
        </div>
        
        <div class="api-section">
            <h3>🌊 Langflow Integration</h3>
            <ul class="endpoint-list">
                <li><span class="method get">GET</span> <code>/api/v3/langflow/export</code> - Export workflows as Langflow JSON</li>
                <li><span class="method get">GET</span> <code>/api/v3/langflow/download</code> - Download workflow ZIP file</li>
                <li><span class="method get">GET</span> <code>/api/v3/langflow/templates</code> - Get workflow templates</li>
                <li><span class="method post">POST</span> <code>/api/v3/langflow/execute</code> - Execute Langflow workflows</li>
            </ul>
        </div>
        
        <div class="api-section">
            <h3>🎨 UX Dashboard API</h3>
            <ul class="endpoint-list">
                <li><span class="method get">GET</span> <code>/api/ux/dashboard/summary</code> - Dashboard overview data</li>
                <li><span class="method get">GET</span> <code>/api/ux/dashboard/recent-jobs</code> - Recent jobs for UI display</li>
                <li><span class="method get">GET</span> <code>/api/ux/agents/status</code> - Agent status monitoring</li>
                <li><span class="method get">GET</span> <code>/api/ux/system/metrics</code> - System performance metrics</li>
                <li><span class="method get">GET</span> <code>/api/ux/system/health</code> - System health status</li>
            </ul>
        </div>
        
        <div class="api-section">
            <h3>🏗️ Agent Architecture</h3>
            <p><strong>Cohort Constructor (11 agents):</strong> Demographics, comorbidities, clinical realism certification</p>
            <p><strong>Clinical Journey (11 agents):</strong> Procedures, medications, care pathways, journey validation</p>
            <p><strong>Data Robustness (10 agents):</strong> Missingness injection, privacy guards, noise modeling</p>
            <p><strong>QA & Validation (13 agents):</strong> Statistical validation, FHIR export, bias detection</p>
            <p><strong>Explanation (13 agents):</strong> Report generation, provenance tracking, literature linking</p>
            <p><strong>Supervision (9 agents):</strong> Performance monitoring, chaos testing, orchestration</p>
        </div>
    </div>
</body>
</html>
        """
    
    @app.get("/swagger", response_class=HTMLResponse)
    async def swagger_ui():
        """Serve Swagger UI for interactive API documentation"""
        
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Synthetic Ascension API - Swagger UI</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
    <style>
        .swagger-ui .topbar { display: none; }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
    <script>
        SwaggerUIBundle({
            url: '/openapi.yaml',
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.presets.standalone
            ],
            layout: "StandaloneLayout",
            deepLinking: true,
            showExtensions: true,
            showCommonExtensions: true
        });
    </script>
</body>
</html>
        """
    
    @app.get("/openapi.yaml")
    async def get_openapi_yaml():
        """Serve OpenAPI specification as YAML"""
        return FileResponse("api/openapi_spec.yaml", media_type="application/x-yaml")
    
    @app.get("/openapi.json")
    async def get_openapi_json():
        """Serve OpenAPI specification as JSON"""
        
        # Convert YAML to JSON
        if os.path.exists("api/openapi_spec.yaml"):
            with open("api/openapi_spec.yaml", 'r') as f:
                yaml_content = yaml.safe_load(f)
            return yaml_content
        else:
            return {"error": "OpenAPI specification not found"}
    
    return app


if __name__ == "__main__":
    import uvicorn
    app = create_docs_app()
    uvicorn.run(app, host="0.0.0.0", port=8001)