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
1. **Integrated Backend Server** (Port 8003) - **PRIMARY** - Your comprehensive multi-agent system
   - Complete integration of user's sophisticated backend
   - 18+ specialized agents across 4 categories
   - Literature mining, demographics, clinical data, validation, and export
   - SQLite job tracking with comprehensive audit trails

2. **FastAPI MCP Server** (Port 8002) - MCP integration
   - Combines REST API endpoints with Model Context Protocol
   - AI agent integration capabilities
   - Enhanced patient generation with specialty focus

3. **Comprehensive EHR API** (Port 8080) - Legacy system
   - Full EHR database models and relationships
   - Complex medical data structures

4. **Enhanced API Server** (Port 8000) - Basic functionality
   - Clean REST endpoints for simple operations
   - Patient cohort generation and analytics

### AI Agent Layer
- **MCP Integration** - Model Context Protocol for AI agent interaction
- **FastMCP Tools** - AI-accessible functions for patient generation
- **Multi-agent orchestration** capabilities

## Recent Changes

### 2025-07-01 - Complete Matrix Theme Transformation & Logo Integration
✅ **Comprehensive Color Palette** - Implemented gold primary (#fbbf24), amber secondary (#f59e0b), cyan tertiary (#06b6d4), emerald accent (#10b981)
✅ **Custom Synthetic Ascension Logo** - DNA helix with upward arrow and matrix code particles using user-provided design
✅ **Hi Melody Font Integration** - Added Google Font "Hi Melody" throughout interface as requested by user
✅ **Matrix-Themed Feature Cards** - Replaced generic icons with genetic/quantum symbols (🧬, 🔐, 🧠, 🔬, ⚡)
✅ **Futuristic Content Overhaul** - Genetic algorithms, quantum consciousness, synthetic biology terminology
✅ **Enhanced CTA Section** - Redesigned bottom call-to-action with DNA imagery and "Begin Neural Ascension" button
✅ **Removed All Demo Buttons** - Eliminated demo functionality to drive all traffic to signup conversion
✅ **Tertiary Color Implementation** - Replaced all blue elements with complementary cyan tertiary color
✅ **Tailwind Config Update** - Added tertiary color palette and Hi Melody font to configuration

### 2025-07-01 - Comprehensive Design System & Dark Mode Implementation
✅ **Professional Design System** - Implemented healthcare-grade design system with calming color palette
✅ **Dark Mode Support** - Complete dark mode functionality with theme toggle in navigation
✅ **Advanced Landing Page** - Comprehensive 7-section landing page following design system specifications
✅ **Typography & Spacing** - Professional font hierarchy with Inter/Montserrat, consistent spacing grid
✅ **Trust Elements** - HIPAA compliance badges, testimonials section, enterprise security indicators
✅ **Smooth Animations** - Scroll-reveal animations, hover states, and microinteractions

### 2025-07-01 - Beautiful Landing Page & Database Integration
✅ **New Landing Page** - Replaced old design with beautiful persona-based landing page
✅ **Persona Targeting** - AI Builder, Medical Researcher, Healthcare Executive personas
✅ **Interactive Features** - Dynamic content switching, lead capture modal
✅ **Supabase Integration** - Lead capture connected to DATABASE_URL with auto table creation
✅ **Complete Database Access** - Maintained all existing Supabase functionality

### 2025-07-01 - Complete Backend Integration
✅ **User Backend Integration** - Successfully integrated comprehensive multi-agent backend from ZIP file
✅ **18+ Specialized Agents** - Deployed cohort, QA, research, and reporting agents
✅ **New Integrated Server** - Running on Port 8003 with full agent orchestration
✅ **Real Agent Implementation** - Replaced mock agents with actual sophisticated implementations
✅ **Comprehensive Pipeline** - Literature mining → Demographics → Clinical data → Validation → Export

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

### REST Endpoints (Integrated Backend Server - Port 8003) - PRIMARY
```
GET  /                          - Comprehensive system overview and agent architecture
POST /api/v2/generate           - Generate comprehensive synthetic EHR data using 18+ agents
GET  /api/v2/jobs/{job_id}      - Check multi-agent generation job status with real-time progress
GET  /api/v2/jobs/{job_id}/results - Get detailed generation results and quality metrics
GET  /api/v2/analytics          - Platform analytics and agent performance metrics
GET  /docs                      - Interactive API documentation
```

### Integrated Agent Categories
```
Cohort Agents (6):        Demographics, Clinical Journeys, Comorbidities, Medications, Labs, Vitals
QA Agents (3):            Statistical Validation, Bias Detection, Realism Checking
Research Agents (4):      Literature Mining, Ontology Mapping, Pattern Analysis, Regulatory Compliance
Reporting Agents (4):     FHIR Export, Audit Trails, Trust Reports, Cohort Summaries
```

### Legacy REST Endpoints (FastAPI MCP Server - Port 8002)
```
GET  /                          - Health check and service info
POST /api/v1/generate/cohort    - Generate patient cohorts
GET  /api/v1/cohorts           - List all generated cohorts
GET  /mcp                      - MCP endpoint information
```

### MCP Tools (AI Agent Integration)
```
mcp_generate_patients  - Generate synthetic patient cohorts
mcp_analyze_cohort    - Analyze demographics and clinical data
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