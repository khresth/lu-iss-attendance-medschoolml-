# Observability Reference

## Overview

Technical reference for the observability stack — logging, tracing, metrics, and error tracking.

## Observability Architecture

**Content should include:**
- Diagram showing the observability data flow:
  - Application -> OpenTelemetry SDK -> OTLP Exporter -> Monitoring Backend
  - Application -> [Logging Framework] -> Console / File / Database sinks
  - Application -> [Error Tracking Service] SDK -> Error Tracking Cloud
- How the orchestrator dashboard provides local observability

## Structured Logging

### Configuration

**Content should include:**
- Logging framework sinks configured:
  - Console (for local development and container logs)
  - File (rolling file in deployed environments)
  - Database (audit-grade persistence)
- Minimum log levels per namespace
- Enrichment properties (machine name, environment, correlation ID)

### Log Levels

| Level | When to Use | Examples |
|-------|-------------|---------|
| `Verbose` | *Detailed diagnostic info, rarely enabled* | *SQL query text, full request bodies* |
| `Debug` | *Diagnostic info useful during development* | *Cache hit/miss, config values loaded* |
| `Information` | *Normal application behaviour* | *Request received, job completed, user signed in* |
| `Warning` | *Unexpected but handled situations* | *Retry triggered, rate limit approached, slow query* |
| `Error` | *Failed operations that need attention* | *Database error, AI service failure, unhandled exception* |
| `Fatal` | *Application cannot continue* | *Startup failure, configuration missing* |

### Logging Best Practices

**Content should include:**
- Use structured logging (message templates, not string interpolation)
- Include relevant context (user ID, entity ID, operation name)
- Don't log sensitive data (tokens, passwords, PII)
- Use scopes for grouping related log entries
- Examples of good and bad log messages

## Distributed Tracing (OpenTelemetry)

### Configuration

**Content should include:**
- OpenTelemetry SDK setup in service defaults
- Instrumentation libraries enabled:
  - HTTP requests (inbound)
  - Database queries
  - Outbound HTTP calls
- Custom spans for business operations
- OTLP exporter configuration

### Trace Structure

**Content should include:**
- How traces flow through the system:
  - Frontend request -> Gateway -> API -> Database / AI Service
- Trace context propagation (W3C TraceContext headers)
- Span naming conventions
- Custom attributes added to spans

### Querying Traces

**Content should include:**
- How to find traces in the orchestrator dashboard (local)
- How to find traces in the cloud monitoring service (deployed)
- Useful trace queries:
  - Find slow requests
  - Find failed requests
  - Trace a specific user's requests
  - Find database-heavy operations

## Metrics

### Available Metrics

**Content should include:**
- HTTP request metrics (rate, duration, status code distribution)
- Database query metrics (rate, duration)
- AI service metrics (rate, duration, token usage)
- Background job metrics (queue depth, processing time, failure rate)
- Custom business metrics (if any)

### Dashboards

**Content should include:**
- Where to find metrics dashboards
- Key metrics to monitor
- How to add new metrics

## Error Tracking

### Configuration

**Content should include:**
- Backend error tracking SDK setup
- Frontend error tracking SDK setup
- DSN per environment
- Release and environment tagging
- Source map configuration (frontend)

### Issue Management

**Content should include:**
- How errors appear in the error tracking service
- Grouping and deduplication
- Assignment and triage workflow
- Alert rules configured
- Integration with work item tracking (if configured)

### PII Scrubbing

**Content should include:**
- What data is scrubbed before sending to error tracking
- Scrubbing rules configuration
- How to verify scrubbing is working

## Orchestrator Dashboard (Local Development)

**Content should include:**
- How to access the dashboard
- Features:
  - Resource status and health
  - Structured logs with filtering
  - Distributed traces with timeline view
  - Console output per resource
- Using dashboard tools from CLI for programmatic access

## Correlation IDs

**Content should include:**
- How correlation IDs are generated
- How they propagate through the request pipeline
- How to find related logs/traces using a correlation ID
- Where correlation IDs appear in error responses (`requestId`)
