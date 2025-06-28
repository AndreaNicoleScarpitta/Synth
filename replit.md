# Synthetic Ascension EHR Platform

## Project Overview
An advanced AI-powered Electronic Health Record (EHR) synthesis platform that generates comprehensive synthetic medical data with cutting-edge visualization and privacy-preserving technologies.

**Current Status:** React frontend with multiple FastAPI backends, now enhanced with Model Context Protocol (MCP) integration

## Architecture Overview

### Frontend Layer
- **React Frontend** (Port 5000) - Professional web interface with TypeScript
- Clean, modern UI with Tailwind CSS
- Real-time data visualization and analytics

### Backend Services
1. **FastAPI MCP Server** (Port 8002) - **PRIMARY** - Latest integration
   - Combines REST API endpoints with Model Context Protocol
   - AI agent integration capabilities
   - Enhanced patient generation with specialty focus
   - MCP tools for AI model interaction

2. **Simple API Server** (Port 8000) - Operational backup
   - Clean REST endpoints for basic functionality
   - Patient cohort generation and analytics

3. **Comprehensive EHR API** (Port 8080) - Running
   - Full EHR database models and relationships
   - Complex medical data structures

### AI Agent Layer
- **MCP Integration** - Model Context Protocol for AI agent interaction
- **FastMCP Tools** - AI-accessible functions for patient generation
- **Multi-agent orchestration** capabilities

## Recent Changes

### 2025-06-28 - Major Architecture Update
✅ **Security Fix** - Replaced vulnerable XML parser with defusedxml library
✅ **Streamlit Removal** - Completely removed all Streamlit components for cleaner architecture  
✅ **MCP Integration** - Added Model Context Protocol support for AI agents
✅ **FastAPI Enhancement** - Created unified FastAPI + MCP server (Port 8002)

## Technical Stack

### Core Technologies
- **Frontend:** React, TypeScript, Tailwind CSS, Vite
- **Backend:** FastAPI, Python 3.11
- **AI Integration:** Model Context Protocol (MCP), FastMCP
- **Database:** PostgreSQL, SQLAlchemy
- **Security:** DefusedXML, CORS middleware

### Key Dependencies
- React ecosystem (React Router, Zustand, Recharts)
- FastAPI with MCP integration (fastmcp, mcp packages)
- Medical data libraries (pandas, numpy, plotly)
- Security and validation tools

## API Architecture

### REST Endpoints (FastAPI MCP Server - Port 8002)
```
GET  /                          - Health check and service info
GET  /health                    - Comprehensive health check  
POST /api/v1/generate/cohort    - Generate patient cohorts
GET  /api/v1/cohorts           - List all generated cohorts
GET  /api/v1/cohort/{id}       - Get specific cohort details
GET  /api/v1/analytics/dashboard - Platform analytics
GET  /mcp                      - MCP endpoint information
```

### MCP Tools (AI Agent Integration)
```
mcp_generate_patients  - Generate synthetic patient cohorts
mcp_analyze_cohort    - Analyze demographics and clinical data
```

### MCP Resources
```
platform_capabilities - Platform documentation and capabilities
```

## User Preferences
- **Architecture:** FastAPI + MCP for AI agent integration
- **Frontend:** React-only (Streamlit removed)
- **Security:** Enterprise-grade with proper vulnerability management
- **API Design:** RESTful with MCP extension for AI capabilities

## Development Guidelines
- Use FastAPI for all new backend development
- Integrate MCP for AI agent capabilities
- Maintain React frontend as primary interface
- Follow security best practices (no vulnerable libraries)
- Document all API changes and architectural decisions

## Deployment Configuration
- **Frontend:** Port 5000 (React + Vite)
- **Primary API:** Port 8002 (FastAPI + MCP)
- **Backup API:** Port 8000 (Simple FastAPI)
- **Legacy API:** Port 8080 (Comprehensive EHR)

## Integration Points
1. **React ↔ FastAPI:** Standard HTTP/JSON communication
2. **AI Agents ↔ MCP:** Model Context Protocol for tool access
3. **Database ↔ APIs:** SQLAlchemy ORM with PostgreSQL
4. **Security Layer:** CORS, input validation, secure XML parsing

## Next Steps
- Test MCP integration with AI agents
- Optimize React frontend for API communication
- Consider consolidating multiple API servers
- Enhance authentication and authorization