# Frontend Code Guide

## Overview

A practical guide for developers working in the frontend — conventions, patterns, and how to do common tasks.

## Adding a New Screen

**Content should include:**
- Step-by-step walkthrough:
  1. Create screen component in `src/screens/`
  2. Add route definition in `src/navigation/`
  3. Add typed route parameters
  4. Wire up navigation (links, buttons)
  5. Add auth gating if required
- Naming conventions for screen files
- Screen component template/boilerplate
- How to handle loading and error states

## Adding a New API Hook

**Content should include:**
- Step-by-step walkthrough:
  1. Ensure the OpenAPI spec is up to date (regenerate from backend if needed)
  2. Run the API client generation command
  3. Create query/mutation hook in `src/data/`
  4. Use the generated typed client functions
  5. Handle success/error response envelopes
- Query hook template (with query key conventions)
- Mutation hook template (with optimistic updates if needed)
- How to invalidate related queries after mutations

## Adding a New Component

**Content should include:**
- Deciding where it goes: `ui/atoms`, `ui/molecules`, or `features/`
- UI library primitives to use
- Theme token usage for colours, spacing, typography
- Responsive design patterns
- Adding props interface with TypeScript
- Colocating tests in `__tests__/` directory

## State Management

**Content should include:**
- When to use each state mechanism:
  - **[Data Fetching Library]**: Server data (API responses, cached data)
  - **[State Management Library]**: Client-only state that persists (auth, preferences)
  - **React state**: Component-local UI state (form inputs, toggles)
  - **React context**: Rarely — prefer state management library for shared state
- How to create a new store
- How to add persistence to a store

## Styling

**Content should include:**
- Available theme tokens (colours, spacing, typography, radii)
- How to use tokens in components
- Responsive breakpoints and media queries
- Animation patterns
- When to use inline styles vs styled components
- Preferred styling approach

## API Client & Authentication

**Content should include:**
- How `apiClient.ts` works
- How Bearer tokens are attached to requests
- Automatic token refresh on 401
- FormData upload handling
- Base URL configuration

## Type Generation

**Content should include:**
- OpenAPI -> TypeScript workflow:
  1. Copy the API spec from the running API
  2. Run the generation command
  3. Generated typed client file
- Backend -> Frontend type generation (if applicable)
- When to regenerate (after any backend API changes)

## Common Pitfalls

**Content should include:**
- Forgetting to regenerate API client after backend changes
- Using raw `fetch` instead of the authenticated API client
- Not handling loading/error states in queries
- Storing server data in client state instead of data fetching library
- Not using the project's styling approach
