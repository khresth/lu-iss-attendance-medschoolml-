# Repository Structure

## Overview

Provide a map of the repository so developers can quickly find what they're looking for.

## Top-Level Layout

```
[repository-name]/
├── backend/                # Backend solution — API, AI, data, infrastructure
├── frontend/               # Frontend application
├── pipeline/               # CI/CD pipeline definitions
├── e2etests/               # End-to-end tests
├── .husky/                 # Git hooks (lint, format)
├── CLAUDE.md               # AI assistant instructions
└── README.md               # Project overview
```

**Content should include:**
- Brief description of each top-level directory
- Which files are in the root and why
- `.gitignore` highlights (what's excluded)

## Backend Layout

```
backend/
├── [API]/                     # HTTP API
│   ├── Endpoints/             # Route groups by feature
│   ├── Services/              # Business logic services
│   ├── Middleware/             # Custom middleware (UserContext, etc.)
│   └── Program.cs             # Application entry point
├── [AI]/                      # AI service integration
│   ├── Plugins/               # AI plugins per feature
│   └── Connectors/            # AI service connectors
├── [AppHost]/                 # Orchestration
├── [DataModel]/               # ORM entities, DbContext, repositories
├── [DatabaseMigrations]/      # Migration files
├── [Gateway]/                 # Reverse proxy
├── [MigrationService]/        # Startup migration runner
├── [ServiceDefaults]/         # Cross-cutting concerns
├── [Tests.Unit]/              # Unit tests
└── [Tests.Integration]/       # Integration tests
```

**Content should include:**
- Purpose and contents of each subdirectory
- Key files in each project (e.g., `Program.cs`, `DbContext`, etc.)
- How to find endpoints for a given feature
- How to find the AI prompt logic for a feature

## Frontend Layout

```
frontend/
├── src/
│   ├── components/         # Shared UI components
│   │   ├── ui/             # Design system (atoms, molecules)
│   │   └── features/       # Feature-specific components
│   ├── features/           # Feature modules
│   ├── screens/            # Screen components (one per route)
│   ├── navigation/         # Navigation/routing config
│   ├── hooks/              # Custom hooks
│   ├── state/              # State management stores
│   ├── data/               # Data fetching hooks
│   ├── lib/                # Utilities and helpers
│   └── types/              # TypeScript definitions
├── e2etests/               # E2E tests
├── openapi.yml             # API spec for code generation
└── package.json            # Dependencies and scripts
```

**Content should include:**
- Where to add new components, screens, hooks, etc.
- Naming conventions
- Import path conventions

## Configuration Files

**Content should include:**
- Backend config files (e.g., `appsettings.json`)
- `.env` files — frontend environment variables
- `tsconfig.json` — TypeScript config
- `eslint.config.*` — linting rules
- `prettier.config.*` — formatting rules
- Test configuration files
- E2E test configuration files

## Key Files to Know

**Content should include a table of the most important files:**

| File | Purpose |
|------|---------|
| `backend/[AppHost]/Program.cs` | *Orchestrator service composition — the "entry point" for the whole system* |
| `backend/[API]/Program.cs` | *API startup, middleware pipeline, service registration* |
| `backend/[API]/Endpoints/*.cs` | *All HTTP endpoints grouped by feature* |
| `backend/[DataModel]/[ProjectName]DbContext.cs` | *Database schema definition* |
| `frontend/src/navigation/*.tsx` | *Route definitions* |
| `frontend/src/state/auth.ts` | *Auth state management* |
| `frontend/src/lib/apiClient.ts` | *API client configuration* |
