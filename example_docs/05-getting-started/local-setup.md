# Local Development Setup

## Prerequisites

List all tools and their required versions.

**Content should include:**

| Tool | Version | Installation |
|------|---------|-------------|
| *[Backend Runtime/SDK]* | *[version]* | *Download link or package manager command* |
| Node.js | *[version] LTS* | *Download link or `nvm` command* |
| Docker Desktop | Latest | *Download link* |
| Git | Latest | *Download link* |
| *[Orchestrator workload]* | Latest | *Installation command* |
| *[Cloud CLI]* | Latest | *Installation command* |
| IDE | *Recommended IDEs* | *Extension recommendations* |

## Step-by-Step Setup

### 1. Clone the Repository

**Content should include:**
```bash
git clone <repo-url>
cd [repository-name]
```

### 2. Install Backend Tools

**Content should include:**
```bash
cd backend
[tool restore command]    # Installs formatter, migration tool, API doc CLI
[orchestrator install command]
```

### 3. Install Frontend Dependencies

**Content should include:**
```bash
cd frontend
npm install
```

### 4. Configure User Secrets

**Content should include:**
- How to set the database password: user secrets or environment variable
- How to configure cloud service connections for local development
- Any API keys needed locally

### 5. Start the Full Stack

**Content should include:**
```bash
# From the repository root
[orchestrator run command]
```
- Database password prompt and default value
- What to expect: dashboard opens, services start
- Dashboard URL for monitoring
- Frontend URL (typically `http://localhost:[port]`)
- API URL (via gateway)
- If frontend doesn't auto-start: manual start command

### 6. Verify Everything Works

**Content should include:**
- Check dashboard — all services green
- Open frontend in browser — auth page loads
- Sign in with test credentials (if available)
- Check API health: `curl https://localhost:[port]/health`

## Enable Git Hooks

**Content should include:**
```bash
git config core.hooksPath .husky
```
- What the hooks do (lint, format on commit)
- How to bypass temporarily if needed (not recommended)

## IDE Configuration

### VS Code

**Content should include:**
- Recommended extensions list
- Workspace settings for formatting, linting
- Debug launch configurations
- How to attach debugger to API and frontend

### JetBrains IDE

**Content should include:**
- Recommended plugins
- Solution/project configuration
- Run/debug configuration for the orchestrator

## Troubleshooting Local Setup

**Content should include:**
- Docker not running -> services won't start
- Port conflicts -> how to check and resolve
- Database container fails -> check Docker resources
- npm install fails -> check Node version, clear cache
- Orchestrator workload not installed -> error message and fix
- Package restore fails -> check feed authentication
- Frontend can't reach API -> check gateway is running, CORS config
