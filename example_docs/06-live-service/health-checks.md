# Health Checks

## Overview

Document the health check endpoints, what they verify, and how they're used.

## Health Check Endpoints

| Endpoint | Purpose | Used By |
|----------|---------|---------|
| `/health` | Readiness check — is the service ready to accept traffic? | Load balancer, orchestrator |
| `/alive` | Liveness check — is the process running and not deadlocked? | Container orchestrator |

## Readiness Check (`/health`)

**Content should include:**
- What it verifies:
  - Database connectivity
  - AI service reachability (if applicable)
  - Required configuration loaded
  - Migration service completed
- Response format (healthy, degraded, unhealthy)
- Expected response time (should be < 1s)
- What happens when it returns unhealthy (removed from load balancer)

## Liveness Check (`/alive`)

**Content should include:**
- What it verifies:
  - Process is responsive
  - No thread deadlocks
- Lighter-weight than readiness check
- What happens when it returns unhealthy (container restart)

## Dependency Health

**Content should include:**
- How to check health of each dependency:
  - Database: connection test
  - AI service: endpoint reachable
  - Identity provider: JWKS endpoint reachable
  - Configuration service: key retrieval
- Dependency health status in `/health` response
- Graceful degradation when non-critical dependencies are unhealthy

## Monitoring Health Checks

**Content should include:**
- How health checks are polled (load balancer, orchestrator probe, etc.)
- Poll interval and failure thresholds
- How health check failures trigger alerts
- Health check history and trends (dashboard location)

## Adding a New Health Check

**Content should include:**
- How to implement a custom health check
- How to register it in the health check pipeline
- Categorisation: readiness vs liveness
- Timeout configuration for health check operations
- Testing health checks locally
