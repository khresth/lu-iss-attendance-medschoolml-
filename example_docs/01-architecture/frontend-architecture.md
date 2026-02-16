# Frontend Architecture

## Overview

Describe the frontend application, its target platforms, and how it fits into the system.

**Content should include:**
- Frontend framework and runtime (e.g., React, Vue, Expo, Next.js)
- Target platforms (web, native mobile, both)
- How it's served in development vs production
- Communicates with backend exclusively through the API Gateway

## Technology Choices

| Concern | Technology | Notes |
|---------|-----------|-------|
| Framework | *[Frontend Framework]* | *Why chosen* |
| UI Library | *[UI Library]* | *Design token system, component primitives* |
| Routing | *[Navigation Library]* | *Typed routes, deep linking support* |
| Server State | *[Data Fetching Library]* | *Typed API client, caching, background refetching* |
| Client State | *[State Management Library]* | *Lightweight, persistence middleware* |
| Auth | *[Auth SDK]* | *OAuth redirect handling, token management* |
| Testing | *[Frontend Test Framework], [E2E Test Framework]* | *Unit and E2E* |
| Error Tracking | *[Error Tracking Service]* | *Crash reporting, performance monitoring* |

## Directory Structure

Explain the `src/` directory layout and the purpose of each folder.

**Content should include:**

```
src/
├── components/       # Reusable UI components
│   ├── ui/           # Design system primitives (atoms, molecules)
│   └── features/     # Feature-specific compound components
├── features/         # Feature modules
├── screens/          # Screen-level components (one per route)
├── navigation/       # Navigation/routing configuration and typed routes
├── hooks/            # Custom React hooks (shared logic)
├── state/            # State management stores (auth, onboarding)
├── data/             # Data fetching hooks for API calls
├── lib/              # Utilities (apiClient, analytics, auth helpers)
└── types/            # TypeScript type definitions
```

- Explanation of when to add code to each folder
- Naming conventions for files and components

## Component Architecture

Describe the component hierarchy and design patterns.

**Content should include:**
- Atomic design approach: atoms -> molecules -> organisms -> screens
- UI library primitive usage
- Theme system and design tokens
- Responsive design approach
- How feature components compose shared UI components

## Data Flow

Document how data moves through the frontend.

**Content should include:**
- API client generation from OpenAPI spec
- Data fetching hooks for server state (queries and mutations)
- State management stores for client-only state
- Data flow diagram: API -> Cache -> Component -> User interaction -> Mutation -> API
- Success/Error response envelope pattern used in data hooks
- Optimistic updates (if used)

## Routing & Navigation

**Content should include:**
- Navigation/routing configuration
- Typed route definitions and how to add new routes
- Auth-gated routing — how unauthenticated users are redirected
- Deep linking configuration
- Navigation patterns (push, replace, reset)

## Authentication Flow (Frontend)

Provide the frontend perspective on auth (backend perspective in [02-authentication](../02-authentication/)).

**Content should include:**
- Auth gate component — onboarding flow (e.g., Welcome -> Terms -> Consent)
- [Auth SDK] OAuth configuration
- Provider selection stored in session/local storage
- Token storage in auth store
- Automatic token refresh on 401 responses
- Sign-out flow and state cleanup

## State Management

**Content should include:**
- Auth store: what it persists, how tokens are managed
- Onboarding store: tracking first-time user experience
- When to use which state mechanism (server state library vs client state library vs local component state)
- Persistence strategy
