# Common Development Tasks

## Overview

Quick reference for tasks developers perform regularly.

## Backend Tasks

### Run the Full Stack

```bash
[orchestrator run command]                # From repo root
```

### Build the Backend

```bash
cd backend
[build command]
```

### Run Backend Unit Tests

```bash
cd backend
[test command] [unit-test-project]
```

### Run Backend Integration Tests

```bash
cd backend
[test command] [integration-test-project]
```

### Format Code

```bash
cd backend
[formatter command]
```

### Create a Database Migration

**Content should include:**
```bash
cd backend
[migration add command] <MigrationName> \
  --project [migrations-project] \
  --startup-project [api-project]
```
- Naming conventions for migrations
- How to verify the generated migration
- How to apply: migrations run automatically on startup

### Update the Database Manually

```bash
cd backend
[database update command] --startup-project [api-project]
```

### Generate OpenAPI Spec

**Content should include:**
- How to access Swagger UI from running API
- How to export the API spec
- URL: `https://localhost:[port]/swagger`

## Frontend Tasks

### Install Dependencies

```bash
cd frontend
npm install
```

### Start Frontend (Standalone)

```bash
cd frontend
npm run dev
```

### Run Linting

```bash
cd frontend
npm run lint                        # Check only
npm run lint:fix                    # Auto-fix
```

### Run Formatting

```bash
cd frontend
npm run format
```

### Run Unit Tests

```bash
cd frontend
npm run test
```

### Run E2E Tests

```bash
cd frontend
npm run test:e2e
```

### Regenerate API Client

**Content should include:**
1. Ensure the backend API is running
2. Copy the OpenAPI spec:
   ```bash
   curl https://localhost:[port]/swagger/v1/swagger.json -o frontend/openapi.yml
   ```
3. Generate the typed client:
   ```bash
   cd frontend
   npm run generate-api
   ```
4. Check for breaking changes in the generated client file

## Git Workflows

### Create a Feature Branch

**Content should include:**
- Branch naming convention
- Base branch (`[base-branch]`)
- Example:
  ```bash
  git checkout [base-branch]
  git pull
  git checkout -b feature/<ticket-number>-<short-description>
  ```

### Create a Pull Request

**Content should include:**
- PR title and description conventions
- Required reviewers
- CI checks that must pass
- Link to work item

### Resolve Merge Conflicts

**Content should include:**
- How to rebase on `[base-branch]`
- Common conflict areas (migrations, package-lock, generated files)
- When to regenerate vs manually resolve

## Debugging

### Attach Debugger to API

**Content should include:**
- How to launch API with debugger attached
- How to set breakpoints
- How to inspect request context

### View Application Logs

**Content should include:**
- Orchestrator dashboard: structured logs, traces, console output
- Log file output location
- How to change log levels

### Inspect Database

**Content should include:**
- How to connect to local database (recommended tools)
- Connection string for local database
- Useful queries for debugging
