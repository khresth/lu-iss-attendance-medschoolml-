# Backend Code Guide

## Overview

A practical guide for developers working in the backend — conventions, patterns, and how to do common tasks.

## Adding a New Endpoint

**Content should include:**
- Step-by-step walkthrough:
  1. Create a new endpoint file in the endpoints directory
  2. Define a static class with a `MapEndpoints` extension method
  3. Register the endpoint group in the application entry point
  4. Add authentication/authorisation requirements
  5. Define request/response DTOs
  6. Implement the handler logic
- Example code for a typical CRUD endpoint
- How to add OpenAPI documentation attributes
- How to return the standard error envelope

## Adding a New Entity

**Content should include:**
- Step-by-step walkthrough:
  1. Create entity class in the data model project
  2. Add `DbSet<T>` property to the DbContext
  3. Configure entity (indexes, relationships, owned types)
  4. Create migration with the appropriate command
  5. Verify migration SQL
- Entity conventions (naming, primary keys, audit fields)
- When to use owned types vs separate entities
- Adding type export attributes for frontend type generation

## Adding a New AI Feature

**Content should include:**
- How to create a new AI plugin
- Prompt template format and storage
- How to register the plugin in DI
- How to call AI from an endpoint
- Error handling for AI service failures
- Testing AI integrations

## Configuration & Options Pattern

**Content should include:**
- How to create a new strongly-typed options class
- How to bind it from configuration files
- How to register it with the DI container
- Extension method pattern: `Add[FeatureName]Options()`
- How to use the configuration service and secrets manager references

## Error Handling

**Content should include:**
- Standard error envelope format
- How to return errors from endpoints
- Exception handling middleware behaviour
- Logging errors with correlation IDs
- When to throw vs return error results

## Dependency Injection Conventions

**Content should include:**
- Service lifetime guidelines (scoped, transient, singleton)
- Extension method pattern for feature registration
- How the orchestrator injects external service connections
- How to resolve services in API handlers

## Background Job Conventions

**Content should include:**
- How to create a new background job
- How to enqueue a job from an endpoint
- Retry and failure configuration
- How to monitor jobs via dashboard
- Job idempotency requirements
