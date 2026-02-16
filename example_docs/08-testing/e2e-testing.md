# End-to-End Testing Guide

## Overview

How to write and run E2E tests that exercise the full application stack.

## Prerequisites

**Content should include:**
- Full stack running via the orchestrator
- E2E test browsers installed: `npx playwright install` (or equivalent)
- Test user accounts available
- Configuration for test environment URLs

## Running E2E Tests

```bash
# All E2E tests
cd frontend && npm run test:e2e

# Specific test file
npx playwright test tests/auth.spec.ts

# With UI mode (visual debugging)
npx playwright test --ui

# With headed browser (see the browser)
npx playwright test --headed

# Generate test report
npx playwright show-report
```

## Test Architecture

### Page Object Pattern

**Content should include:**
- Why we use Page Objects (encapsulate page interactions, reduce duplication)
- Page Object structure:
  ```
  e2etests/
  ├── pages/
  │   ├── AuthPage.ts
  │   ├── DashboardPage.ts
  │   ├── [FeatureA]Page.ts
  │   └── [FeatureB]Page.ts
  ├── fixtures/
  │   └── test-fixtures.ts
  └── tests/
      ├── auth.spec.ts
      ├── [feature-a].spec.ts
      └── [feature-b].spec.ts
  ```
- How to create a new Page Object
- Guidelines: Page Objects contain locators and actions, tests contain assertions

### Test Fixtures

**Content should include:**
- How to set up common fixtures (authenticated user, test data)
- E2E test framework fixtures and how to extend them
- Test isolation — each test starts from a known state
- Database seeding for E2E tests (if applicable)

## Writing E2E Tests

### Authentication

**Content should include:**
- How to handle auth in E2E tests
- Saving and reusing auth state (e.g., `storageState`)
- Testing with different user types
- Handling OAuth redirects in tests

### Example Test

**Content should include:**
- Complete example E2E test for a key user journey
- Example of navigating between pages
- Example of form filling and submission
- Example of asserting success/error states
- Example of waiting for API responses

### Best Practices

**Content should include:**
- Test user journeys, not individual components
- Keep tests independent (no ordering dependencies)
- Use resilient locators (roles, labels, test IDs — not CSS selectors)
- Handle async operations with auto-waiting
- Take screenshots on failure for debugging
- Keep tests fast: avoid unnecessary waits, use API calls for setup where possible

## Debugging E2E Tests

**Content should include:**
- Using UI mode
- Using trace viewer
- Taking screenshots and videos on failure
- Using `page.pause()` for interactive debugging
- Viewing browser console output
- Network request inspection

## CI Integration

**Content should include:**
- How E2E tests run in the CI pipeline
- Browser installation in CI environment
- Test parallelisation
- Artifact collection (reports, screenshots, traces)
- Failure handling and retry strategy
