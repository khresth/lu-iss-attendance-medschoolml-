# Configuration Reference

## Overview

Comprehensive reference for all configuration keys, environment variables, and feature flags.

## Backend Configuration

### Connection Strings

| Key | Description | Example | Source |
|-----|-------------|---------|--------|
| `ConnectionStrings:[ProjectName]Db` | *Database connection* | *Server=...;Database=...* | *Secrets Manager* |

### Auth (Primary Pool)

| Key | Description | Example |
|-----|-------------|---------|
| `[Auth]:Authority` | *Identity provider issuer URL for primary pool* | `https://[idp-url]/[pool-id]` |
| `[Auth]:ClientId` | *App client ID* | *GUID* |

### Auth (Secondary Pool)

| Key | Description | Example |
|-----|-------------|---------|
| `[ProjectName].ExternalAuth:Authority` | *Identity provider issuer URL for secondary pool* | `https://[idp-url]/[pool-id]` |
| `[ProjectName].ExternalAuth:ClientId` | *App client ID* | *GUID* |

### Secrets Manager

| Key | Description | Example |
|-----|-------------|---------|
| `[SecretsManager]:Endpoint` | *Secrets manager URI* | `https://[resource-name].[provider-domain]/` |

### Error Tracking

| Key | Description | Example |
|-----|-------------|---------|
| `[ErrorTracking]:Dsn` | *Error tracking DSN* | `https://xxx@[provider]/xxx` |
| `[ErrorTracking]:Environment` | *Environment tag* | `staging` / `production` |

### Logging

| Key | Description | Example |
|-----|-------------|---------|
| `[Logging]:MinimumLevel:Default` | *Default log level* | `Information` |
| `[Logging]:MinimumLevel:Override:*` | *Log level overrides per namespace* | `Warning` |

### Background Tasks

| Key | Description | Example |
|-----|-------------|---------|
| `BackgroundTasks:*` | *Background job framework configuration* | *Various* |

### Configuration Service

| Key | Description | Example |
|-----|-------------|---------|
| `AppConfig:Endpoint` | *Configuration service endpoint* | `https://[resource-name].[provider-domain]` |

## Frontend Environment Variables

| Variable | Description | Set By | Example |
|----------|-------------|--------|---------|
| `[PREFIX]_API_BASE_URL` | *Backend gateway URL* | *[Orchestrator] (local) / build config (deployed)* | `https://localhost:[port]` |
| `[PREFIX]_URL_PATH` | *Base path for routing* | *Build config* | `/` |
| `[PREFIX]_ENV` | *Environment identifier* | *Build config* | `stg` / `prod` |
| `PORT` | *Dev server port* | *[Orchestrator]* | `[port]` |

## Feature Flags

**Content should include:**

| Flag | Description | Default | Notes |
|------|-------------|---------|-------|
| *flag-name* | *What the flag controls* | *on/off* | *When to use* |

- How feature flags are managed (configuration service)
- How to check a flag's value in code (backend and frontend)
- How to add a new feature flag

## Orchestrator Configuration

**Content should include:**
- How the orchestrator configures each service
- Environment variable injection
- Service reference URLs
- Resource naming conventions

## Secrets Inventory

**Content should include:**
- List of all secrets in secrets manager (names only, not values)
- Which service uses each secret
- Rotation schedule for each secret
- How to update a secret
