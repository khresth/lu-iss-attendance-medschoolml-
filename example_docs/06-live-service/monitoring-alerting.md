# Monitoring & Alerting

## Overview

Document what is monitored, how alerts are configured, and where to look when something goes wrong.

## Monitoring Stack

**Content should include:**
- OpenTelemetry for traces, metrics, and logs
- Cloud-native monitoring service (e.g., Application Insights, CloudWatch)
- Error tracking service for error tracking and performance monitoring
- Orchestrator Dashboard for local development monitoring
- Background job dashboard for job monitoring

## Dashboards

### Application Health Dashboard

**Content should include:**
- Where to find it (cloud portal, Grafana, etc.)
- Key widgets:
  - Request rate and latency (p50, p95, p99)
  - Error rate (4xx, 5xx)
  - Active users
  - Database connection pool utilisation
  - Background job queue depth

### Infrastructure Dashboard

**Content should include:**
- CPU and memory utilisation
- Database resource usage
- Storage consumption
- Network throughput
- Application instance count

### AI Service Dashboard

**Content should include:**
- AI service request rate and latency
- Token usage and cost
- Rate limiting / throttling events
- Model error rates

## Alert Configuration

### Critical Alerts (Page Immediately)

**Content should include:**

| Alert | Condition | Action |
|-------|-----------|--------|
| Service Down | *Health check fails for > 2 minutes* | *Page on-call, follow [Incident Response](../07-runbooks/incident-response.md)* |
| Error Rate Spike | *5xx rate > 5% for 5 minutes* | *Page on-call, check logs* |
| Database Unreachable | *Connection failures > 0 for 3 minutes* | *Page on-call, check database service* |

### Warning Alerts (Investigate During Business Hours)

**Content should include:**

| Alert | Condition | Action |
|-------|-----------|--------|
| High Latency | *p95 > 2s for 10 minutes* | *Investigate slow queries, AI latency* |
| High CPU | *CPU > 80% for 15 minutes* | *Check for resource contention, consider scaling* |
| Background Job Failures | *Failed jobs > 5 in 1 hour* | *Check job dashboard, review logs* |
| Certificate Expiry | *TLS cert expires within 30 days* | *Renew certificate* |

### Informational Alerts

**Content should include:**
- Deployment completed notifications
- Scheduled maintenance reminders
- Capacity planning thresholds

## Log Access

**Content should include:**
- How to query structured logs
- Common useful queries:
  - Find all errors in the last hour
  - Trace a specific request by correlation ID
  - Find slow database queries
  - Find AI service errors
- Log retention periods
- How to export logs for investigation

## Error Tracking Configuration

**Content should include:**
- Project setup (backend and frontend projects)
- Environment tagging (staging, production)
- Release tracking
- Alert rules configured
- PII scrubbing rules
- How to triage and resolve issues
