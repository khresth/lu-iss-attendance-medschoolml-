# Integration Patterns

## Overview

Document how the system integrates with external services and internal components communicate.

## Service Communication

### Internal Communication

**Content should include:**
- How frontend communicates with backend (via API Gateway)
- API Gateway routing rules — which paths go where
- How the orchestrator manages service discovery and URL injection
- Request/response format (JSON, content types)

### Orchestration

**Content should include:**
- How the orchestrator composes services
- Environment variable injection
- Service reference wiring
- Health check dependencies (migration service completes before API starts)

## External Service Integrations

### AI Service

**Content should include:**
- Connection configuration (endpoint, API key, model deployment names)
- How the AI SDK wraps the AI service provider
- Rate limiting and retry policies
- Model versions used and upgrade strategy

### Configuration Service

**Content should include:**
- How configuration is loaded at startup
- Feature flag management
- Configuration refresh strategy
- Key naming conventions

### Secrets Manager

**Content should include:**
- What secrets are stored (connection strings, API keys, etc.)
- How secrets are referenced from configuration
- Access policies and managed identity setup
- Secret rotation procedures

### Identity Provider

**Content should include:**
- Integration architecture (single or multiple pools)
- JWT validation configuration
- Token exchange flow
- Cross-reference to [Authentication docs](../02-authentication/)

### Error Tracking Service

**Content should include:**
- DSN configuration for backend and frontend
- What events are captured (errors, transactions, breadcrumbs)
- Environment and release tagging
- PII scrubbing rules

## API Client Generation

**Content should include:**
- OpenAPI spec generation from backend
- How to export the API spec from a running API
- Code generation for frontend typed client
- Process: Backend changes -> regenerate spec -> regenerate client -> update frontend hooks
- Type generation from backend to frontend (if applicable)

## Resilience Patterns

**Content should include:**
- Retry policies
- Circuit breaker configuration
- Timeout policies
- Fallback strategies for AI service unavailability
- Token refresh retry on 401
