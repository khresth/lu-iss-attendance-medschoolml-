# Backend Testing Guide

## Overview

How to write and run tests for the backend.

## Test Projects

| Project | Type | What It Tests |
|---------|------|--------------|
| `[Tests.Unit]` | Unit | Business logic, services, orchestration |
| `[Tests.Integration]` | Integration | Database operations, API endpoints, middleware |

## Running Tests

```bash
# All unit tests
cd backend && [test command] [Tests.Unit]

# All integration tests
cd backend && [test command] [Tests.Integration]

# Specific test class
[test command] [Tests.Unit] --filter "FullyQualifiedName~ClassName"

# Specific test method
[test command] [Tests.Unit] --filter "FullyQualifiedName~ClassName.MethodName"
```

## Writing Unit Tests

### Conventions

**Content should include:**
- Test class naming: `<ClassUnderTest>Tests`
- Test method naming: `<Method>_<Scenario>_<ExpectedResult>` or descriptive name
- Arrange-Act-Assert pattern
- One assertion per test (where practical)
- Test file location: mirror the source file path in the test project

### Mocking

**Content should include:**
- Mocking framework used (e.g., Moq, NSubstitute, Mockito)
- What to mock: external services, database, AI SDK
- What not to mock: the class under test, simple value objects
- How to set up common mocks (DbContext, HttpClient, AI SDK)

### Example Unit Test

**Content should include:**
- Complete example test for a typical service method
- Example test for an endpoint handler
- Example test for AI plugin logic

## Writing Integration Tests

### Test Infrastructure

**Content should include:**
- How the test database is set up (test fixture, in-memory provider, or Docker)
- Test application factory configuration for API tests
- How to seed test data
- Test isolation (each test gets clean state)
- Shared fixture vs per-test fixture decisions

### Testing Endpoints

**Content should include:**
- How to create authenticated test requests
- How to test authorisation (different user roles)
- How to test request validation
- How to test error responses
- How to test the error envelope format

### Testing Database Operations

**Content should include:**
- How to test repository methods
- How to test complex queries
- How to test migrations apply cleanly
- Transaction handling in tests

## Testing AI Features

**Content should include:**
- How to mock AI service responses
- Testing AI plugin logic
- Testing prompt template rendering
- Testing error handling for AI failures
- How to test without real AI API calls (cost and reliability)

## Test Helpers & Utilities

**Content should include:**
- Shared test builders / factories
- Custom assertion helpers
- Test data generators
- Common test base classes

## Code Coverage

**Content should include:**
- How to generate coverage reports
- Coverage targets (if any)
- What's excluded from coverage metrics
- How to view coverage in IDE / CI
