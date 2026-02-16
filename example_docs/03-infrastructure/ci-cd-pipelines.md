# CI/CD Pipelines

## Overview

Document the continuous integration and deployment pipeline architecture.

## Pipeline Architecture Diagram

Include a diagram showing the pipeline stages and their dependencies.

**Content should include:**
- Source: [CI/CD Platform] repository
- Trigger conditions (branch, PR, manual)
- Pipeline stages and their order
- Environments and approval gates
- Artifact flow between stages

## Backend Pipeline (`pipeline/backend.yml`)

### Trigger Configuration

**Content should include:**
- Which branches trigger the pipeline
- Path filters (only runs when backend files change)
- PR validation rules

### Build Stage

**Content should include:**
- SDK/runtime version used
- Dependency restore with package feed configuration
- Build command and configuration
- Test execution — which test projects run
- Build artifact publishing

### API Documentation Stage

**Content should include:**
- OpenAPI spec generation
- API collection generation (e.g., Postman)
- Where artifacts are published

### Deployment Stage

**Content should include:**
- Target environments and deployment order
- Deployment method (e.g., App Service deploy, container push)
- Pre-deployment steps (database migrations)
- Post-deployment validation (smoke tests, health checks)
- Rollback triggers

## Frontend Pipeline (`pipeline/frontend.yml`)

### Trigger Configuration

**Content should include:**
- Which branches trigger the pipeline
- Path filters (only runs when frontend files change)

### Build & Test Stage

**Content should include:**
- Node.js version used
- `npm install` with registry configuration
- Lint validation
- Unit test execution
- Production build
- Build artifact publishing

### Deployment Stage

**Content should include:**
- Static file deployment target
- CDN configuration and cache invalidation
- Environment-specific build variables

## Security Pipeline (`pipeline/security.yml`)

**Content should include:**
- SAST scanning tools and configuration
- Dependency vulnerability scanning
- When it runs (PR, scheduled, etc.)
- How findings are triaged and resolved
- Blocking vs non-blocking rules

## Pipeline Variables & Secrets

**Content should include:**
- Variable groups used
- Service connections (cloud provider, package feeds, etc.)
- How secrets are managed in pipelines
- Per-environment variable overrides

## Adding a New Pipeline

**Content should include:**
- Step-by-step guide for creating a new pipeline
- Template usage and conventions
- Naming conventions
- Required approvals for pipeline changes
