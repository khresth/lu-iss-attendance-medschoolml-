# Environments

## Overview

Document all environments, their purpose, and how they differ.

## Environment Summary

| Environment | Purpose | URL | Deployment | Notes |
|------------|---------|-----|------------|-------|
| Local | *Developer workstation* | *localhost URLs* | *Manual via [Orchestrator]* | *Full stack runs locally* |
| Staging | *Pre-production testing* | *staging URL* | *CI/CD pipeline* | *Mirrors production config* |
| Production | *Live user traffic* | *production URL* | *CI/CD pipeline with approval* | *Restricted access* |

## Local Development Environment

**Content should include:**
- What runs locally: Database (Docker), API, Gateway, Frontend dev server, Mock server
- [Orchestrator] orchestrates all services
- Dashboard URL for monitoring
- Default ports for each service
- How to start the local environment
- Database password: prompted on first run, stored in user secrets

## Staging Environment

**Content should include:**
- Cloud resource group and subscription
- Deployed services and their cloud resources
- Database configuration
- Identity provider pool IDs for staging
- Configuration and secrets manager instances
- How to access logs and monitoring
- Who has access and how to request it

## Production Environment

**Content should include:**
- Cloud resource group and subscription
- Deployed services and their cloud resources
- Database configuration
- Identity provider pool IDs for production
- Configuration and secrets manager instances
- Access restrictions and approval requirements
- Disaster recovery configuration

## Environment-Specific Configuration

**Content should include:**
- How environment-specific values are managed (configuration service + secrets manager)
- Feature flags that differ between environments
- CORS allowed origins per environment
- OAuth redirect URIs per environment
- Logging levels per environment
- Error tracking DSN and environment tagging

## Promotion Strategy

**Content should include:**
- How changes flow from local -> staging -> production
- What gates exist between environments (tests, approvals)
- Database migration promotion strategy
- Configuration change promotion strategy
- Rollback procedures per environment
