# System Overview

## Purpose

Describe the overall system at a high level — what it does, who it serves, and why it exists.

**Content should include:**
- Product mission statement and business context
- Target user groups (e.g., internal users, external users, administrators)
- High-level capabilities (e.g., [Feature A], [Feature B], [Feature C])
- Current phase and planned roadmap

## System Context Diagram

Include a C4 Level 1 (System Context) diagram showing [Project Name] and its external dependencies.

**Content should include:**
- Diagram showing the system boundary
- External actors: [User Type A], [User Type B], Administrators
- External systems: [Identity Provider], [AI Service], [Configuration Service], [Secrets Manager]
- Direction of data flow between each actor/system and [Project Name]

## High-Level Architecture Diagram

Include a C4 Level 2 (Container) diagram showing the major components.

**Content should include:**
- [Orchestrator] (orchestration layer)
- [API Gateway] (reverse proxy)
- Backend API
- AI Service layer
- Database
- Frontend application
- Mock Server (development only)
- Background job processor
- Relationships and data flow between each container

## Technology Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | *List framework, UI library, state management, data fetching, etc.* |
| Backend | *List runtime, framework, ORM, background jobs, etc.* |
| AI | *List AI SDK, model provider, prompt management approach* |
| Database | *List RDBMS, migration tool* |
| Infrastructure | *List cloud provider, IaC tool, orchestration, observability* |
| Auth | *List identity provider, token format, auth libraries* |

## Key Architectural Decisions

Link to or summarise the most important architectural decisions (consider using ADR format).

**Decisions to document:**
- Choice of orchestration approach (e.g., .NET Aspire, Docker Compose, Kubernetes)
- Choice of frontend framework and why
- Choice of API gateway / reverse proxy
- Identity provider architecture (single vs multiple pools)
- AI orchestration SDK selection
- Background job processing approach
- UI component library selection

## Non-Functional Requirements

**Content should include:**
- Performance targets (response times, throughput)
- Availability targets (uptime SLA)
- Scalability approach
- Security requirements and compliance considerations
- Data retention policies
- Accessibility standards (WCAG level)
