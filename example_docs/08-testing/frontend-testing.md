# Frontend Testing Guide

## Overview

How to write and run tests for the frontend.

## Running Tests

```bash
# All unit tests
cd frontend && npm run test

# Watch mode (re-runs on file change)
cd frontend && npm run test -- --watch

# Specific file
cd frontend && npm run test -- path/to/file.test.tsx

# With coverage
cd frontend && npm run test -- --coverage
```

## Writing Unit Tests

### Conventions

**Content should include:**
- Test file naming: `ComponentName.test.tsx` or `hookName.test.ts`
- Test file location: `__tests__/` directory colocated with source
- Test structure: `describe` block per component/hook, `it` block per behaviour
- Descriptive test names that read as sentences

### Testing Components

**Content should include:**
- Testing library philosophy: test user behaviour, not implementation
- How to render components with required providers (data fetching, navigation, theme)
- Common queries: `getByText`, `getByRole`, `getByTestId`
- User interaction simulation: `fireEvent`, `userEvent`
- Async testing: `waitFor`, `findBy` queries
- Snapshot testing: when to use (sparingly) and when to avoid

### Example Component Test

**Content should include:**
- Complete example test for a typical screen component
- Example with data fetching provider
- Example testing loading, success, and error states
- Example testing user interaction (button press, form submission)

### Testing Hooks

**Content should include:**
- `renderHook` from testing library
- Testing custom hooks with dependencies (API client, stores)
- Testing data fetching hooks (with provider)
- Testing state management store hooks

### Testing Data Hooks

**Content should include:**
- Mocking API responses with API mocking library or manual mocks
- Testing query hooks (loading, success, error states)
- Testing mutation hooks (optimistic updates, error handling)
- Testing cache invalidation

## Mocking

### API Mocks

**Content should include:**
- API mocking library setup for intercepting API calls (if used)
- Manual mock approach for API client
- How to create typed mock responses
- Resetting mocks between tests

### Navigation Mocks

**Content should include:**
- How to mock the navigation/routing library
- Testing navigation actions (navigate, goBack)
- Providing navigation context in tests

### Store Mocks

**Content should include:**
- How to mock state management stores
- Providing initial state for tests
- Testing state changes

## Accessibility Testing

**Content should include:**
- Testing with accessibility queries (`getByRole`, `getByLabelText`)
- Automated a11y checks (e.g., jest-axe or similar)
- What to check: labels, roles, contrast, keyboard navigation

## Common Pitfalls

**Content should include:**
- Forgetting to wrap components in required providers
- Testing implementation details instead of user behaviour
- Not waiting for async operations
- Over-using snapshots
- Not cleaning up after tests (timers, event listeners)
