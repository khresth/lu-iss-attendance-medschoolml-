# Common Issues & Resolutions

## Overview

A troubleshooting guide for frequently encountered issues in production and development.

## Production Issues

### Users Cannot Sign In

**Symptoms:** Users see an error on the auth screen, or are redirected in a loop.

**Diagnosis steps:**
1. Check which auth pool is affected (primary, secondary, or both)
2. Check identity provider service health
3. Check API structured logs for authentication errors
4. Check error tracking for related frontend errors
5. Verify callback URLs haven't changed
6. Check CORS configuration

**Common causes and resolutions:**
- *Identity provider hosted UI down* -> Check provider status, wait for recovery
- *Callback URL mismatch* -> Verify URLs in identity provider app client settings
- *Token validation failure* -> Check JWKS endpoint reachability, verify issuer config
- *CORS blocking* -> Verify allowed origins include the frontend URL

### AI Features Not Working

**Symptoms:** AI-powered features return errors or timeout.

**Diagnosis steps:**
1. Check AI service health
2. Check API logs for AI-related errors
3. Check for rate limiting / throttling
4. Verify API key and endpoint configuration
5. Check error tracking for AI service errors

**Common causes and resolutions:**
- *AI service rate limited* -> Wait for quota reset, consider scaling tier
- *Model deployment changed* -> Verify model deployment name in configuration
- *Prompt not found* -> Check Prompt table in database for the relevant feature
- *Timeout* -> AI request taking too long, check model latency metrics

### Background Jobs Failing

**Symptoms:** Async tasks not completing (e.g., content generation, analysis).

**Diagnosis steps:**
1. Check background job dashboard for failed jobs
2. Review job error details and stack traces
3. Check for resource constraints (memory, CPU)
4. Check dependent service health (AI, database)

**Common causes and resolutions:**
- *Transient AI failure* -> Jobs should auto-retry; check retry count
- *Database connection exhaustion* -> Check connection pool metrics
- *Out of memory* -> Check input sizes, consider resource scaling

### High Latency

**Symptoms:** Users report slow loading, monitoring shows elevated response times.

**Diagnosis steps:**
1. Check monitoring dashboard for latency trends
2. Identify which endpoints are slow (distributed traces)
3. Check database query performance
4. Check AI service latency
5. Check for resource contention (CPU, memory, connections)

**Common causes and resolutions:**
- *Slow database queries* -> Check execution plans, add indexes
- *AI service latency* -> Consider caching, async processing
- *High traffic* -> Scale up/out resources

## Development Issues

### Orchestrator Won't Start

**Common causes and resolutions:**
- *Docker not running* -> Start Docker Desktop
- *Port conflicts* -> Check which ports are in use, stop conflicting services
- *Database password not set* -> Enter password when prompted
- *Orchestrator workload not installed* -> Run installation command

### Frontend Can't Reach API

**Common causes and resolutions:**
- *Gateway not running* -> Check orchestrator dashboard, restart gateway
- *CORS error* -> Check browser console, verify CORS config includes frontend dev server URL
- *Wrong base URL* -> Verify API base URL environment variable

### Database Migration Fails

**Common causes and resolutions:**
- *Pending model changes* -> Create a new migration first
- *Migration conflicts* -> Resolve merge conflicts in migration files
- *Connection string wrong* -> Check user secrets configuration

### API Client Out of Date

**Symptoms:** TypeScript errors after backend API changes.

**Resolution:**
1. Ensure API is running
2. Export fresh API spec
3. Run API client generation command
4. Fix any breaking changes in frontend code

### Tests Failing Locally

**Common causes and resolutions:**
- *Backend tests* -> Check database is running, check test configuration
- *Frontend tests* -> Run `npm install`, check Node version
- *E2E tests* -> Ensure full stack is running, check E2E test browsers installed
