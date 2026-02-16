# Live Service Overview

## Overview

Describe the production service — what's running, where, and how it serves users.

## Service Architecture (Production)

**Content should include:**
- Deployment topology diagram
- List of deployed services and their cloud resources
- Traffic flow from user request to response
- Geographic region(s) and why

## Service Endpoints

| Service | URL | Purpose | Health Check |
|---------|-----|---------|-------------|
| Frontend | *production URL* | *User-facing web application* | *HTTP 200 on root* |
| API | *internal URL* | *Backend API (via gateway)* | `/health` |
| Gateway | *production URL* | *Reverse proxy routing* | *HTTP 200* |
| Background Job Dashboard | *internal URL* | *Background job monitoring (restricted)* | *N/A* |

## Service Level Objectives (SLOs)

**Content should include:**
- Availability target (e.g., 99.5% uptime during business hours)
- Response time targets (e.g., p95 < 500ms for API, p95 < 2s for AI endpoints)
- Error rate targets (e.g., < 1% 5xx error rate)
- How SLOs are measured and reported
- What happens when SLOs are breached

## Dependencies & External Services

**Content should include:**

| Dependency | SLA | Impact if Down | Fallback |
|-----------|-----|---------------|----------|
| Database | *[SLA]* | *No data access — full outage* | *None* |
| [AI Service] | *[SLA]* | *AI features unavailable — partial degradation* | *Queued retry / user notification* |
| [Identity Provider] | *[SLA]* | *No sign-in — full outage for new sessions* | *Existing tokens still valid until expiry* |
| Configuration Service | *[SLA]* | *Cached config used — no immediate impact* | *Last-known config* |
| Secrets Manager | *[SLA]* | *Secrets cached at startup — no immediate impact* | *Cached secrets* |
| [Error Tracking Service] | *Best effort* | *No error tracking — no user impact* | *Logs still captured* |

## On-Call & Support

**Content should include:**
- On-call rotation schedule
- Escalation path
- Contact information for key personnel
- Out-of-hours support expectations
- Incident communication channels

## Maintenance Windows

**Content should include:**
- Scheduled maintenance windows (day/time)
- How users are notified of planned downtime
- Deployment schedule (e.g., releases to staging on merge, production on approval)
- Database maintenance schedule
