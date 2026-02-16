# Testing Strategy

## Overview

Describe the overall testing philosophy, what we test, and how different test types work together.

## Testing Pyramid

**Content should include:**
- Diagram of the testing pyramid:
  - **Unit tests** (base — most numerous, fastest)
  - **Integration tests** (middle — fewer, test component interactions)
  - **E2E tests** (top — fewest, test full user flows)
- Rationale for this distribution
- Approximate target ratios

## Test Types

### Unit Tests

**Content should include:**
- What they test: individual functions, classes, components in isolation
- Mocking strategy: what to mock (external services, database) and what not to mock
- Speed expectation: < 1 second per test
- Coverage targets (if any)
- **Backend**: [Backend Test Framework], testing business logic and orchestration
- **Frontend**: [Frontend Test Framework], testing component rendering and behaviour

### Integration Tests

**Content should include:**
- What they test: component interactions, database operations, API endpoint behaviour
- Test database strategy (in-memory, containerised, shared fixture)
- Speed expectation: < 10 seconds per test
- **Backend**: [Backend Test Framework] with test server and test database
- **Frontend**: [Data Fetching Library] with mock API responses

### End-to-End Tests

**Content should include:**
- What they test: full user journeys through the running application
- Technology: [E2E Test Framework]
- Page Object pattern usage
- Test environment: local full stack via [Orchestrator]
- Speed expectation: < 30 seconds per test
- When to write E2E tests (critical user paths, regression prevention)

## What to Test

**Content should include:**
- Business logic: always test thoroughly
- API endpoints: test happy path + error cases + auth
- UI components: test rendering, user interactions, accessibility
- AI features: test orchestration logic, mock AI responses
- Data access: test queries return correct results
- Auth flows: test token handling, protected routes

## What NOT to Test

**Content should include:**
- Framework internals (ORM, backend middleware)
- Third-party library behaviour
- Simple data transfer objects
- Auto-generated code (API client, migrations)
- Trivial getters/setters

## Test Data Management

**Content should include:**
- How test data is created (builders, factories, fixtures)
- Test data cleanup strategy
- Shared test data vs per-test data
- Sensitive data handling in tests

## CI/CD Integration

**Content should include:**
- Which tests run on PR (unit + integration)
- Which tests run on merge to `[base-branch]` (all)
- Test result reporting and visibility
- Failure handling (blocking vs non-blocking)
- Test parallelisation
