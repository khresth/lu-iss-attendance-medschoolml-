# Backend Architecture

## Overview

Describe the backend as a whole — its role, the hosting model, and how it fits into the wider system.

**Content should include:**
- Runtime and framework (e.g., .NET, Node.js, Go)
- Hosting: How the backend is orchestrated and deployed
- Key responsibilities: API surface, business logic, AI orchestration, data persistence, background processing

## Project Structure

Explain each project/module in the backend solution and its responsibility.

**Projects to document:**

| Project | Purpose |
|---------|---------|
| `[AppHost]` | Orchestration — composes all services, wires configuration and service discovery |
| `[API]` | HTTP endpoints, middleware, request/response handling |
| `[AI]` | AI service integration — plugins, connectors, prompt management |
| `[DataModel]` | ORM DbContext, entity definitions, repositories |
| `[ServiceDefaults]` | Cross-cutting concerns: observability, resilience policies, health checks |
| `[Gateway]` | Reverse proxy — routes traffic to API and mock server |
| `[MigrationService]` | Runs database migrations on startup before API becomes available |
| `[DatabaseMigrations]` | Migration files organised by domain area |
| `[Tests.Unit]` | Unit tests for business logic and orchestration |
| `[Tests.Integration]` | Integration tests for database and API |

## API Design

Describe the API layer's patterns and conventions.

**Content should include:**
- API approach (Minimal APIs, controllers, etc.) — why, and how endpoints are organised
- Route group pattern (each feature has its own endpoint file)
- List of endpoint groups: [Feature A], [Feature B], [Feature C], Users, Terms, etc.
- Request/response conventions
- Error envelope format: `{ "error": { "code", "message", "details" }, "requestId" }`
- Versioning strategy (if any)
- Content negotiation and serialisation settings

## Middleware Pipeline

Document the middleware pipeline in order.

**Content should include:**
- Authentication middleware (JWT Bearer)
- `UserContextMiddleware` — extracts user identity from token claims, resolves user source
- Authorisation policies
- CORS configuration
- Exception handling middleware
- Request logging

## Dependency Injection & Configuration

Explain how services are registered and configured.

**Content should include:**
- Extension method pattern for service registration (e.g., `Add[ProjectName]Options()`)
- Strongly-typed Options classes bound from configuration files
- Secrets manager integration for secrets
- Feature flags via configuration service
- How the orchestrator injects connection strings and service URLs

## Background Processing

Document the background job infrastructure.

**Content should include:**
- Background job framework setup and storage backend
- Job types and their purpose
- Retry and failure policies
- Job dashboard access (dev-only)
- How jobs are enqueued from API endpoints

## AI Integration

Provide an overview of the AI layer (detail in [Technical Reference](../10-technical-reference/ai-integration.md)).

**Content should include:**
- AI SDK architecture
- AI service configuration
- Plugin system for different features
- Prompt management approach (e.g., database-stored prompts, file-based templates)
- Responsible AI principles applied

## Logging & Observability

**Content should include:**
- Logging framework configuration (console, file, database sinks)
- OpenTelemetry integration (traces, metrics, logs)
- Error tracking and APM
- Health check endpoints: `/health` (readiness), `/alive` (liveness)
- Correlation IDs and distributed tracing
