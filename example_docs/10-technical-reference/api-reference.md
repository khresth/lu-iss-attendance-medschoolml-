# API Reference

## Overview

Comprehensive reference for the [Project Name] REST API.

## Base URL

| Environment | Base URL |
|------------|----------|
| Local | `https://localhost:[port]` (via Gateway) |
| Staging | *staging gateway URL* |
| Production | *production gateway URL* |

## Authentication

**Content should include:**
- All endpoints require a Bearer token (JWT from [Identity Provider])
- Token must be included in the `Authorization` header: `Bearer <token>`
- How to obtain a token (OAuth flow via [Auth SDK])
- Token format and expected claims

## Common Response Format

### Success Response

```json
{
  "data": { ... }
}
```

### Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable error description",
    "details": { ... }
  },
  "requestId": "correlation-id-here"
}
```

**Content should include:**
- List of standard error codes
- HTTP status code mapping
- How `requestId` can be used for debugging

## Endpoints

### [Resource A] (e.g., Core Domain Objects)

**Content should include for each endpoint:**
- HTTP method and path
- Description
- Request headers
- Request body schema (with examples)
- Response body schema (with examples)
- Possible error responses
- Authentication/authorisation requirements

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/[resource-a]` | *List user's items* |
| `POST` | `/api/[resource-a]` | *Create a new item* |
| `GET` | `/api/[resource-a]/{id}` | *Get a specific item* |
| `PUT` | `/api/[resource-a]/{id}` | *Update an item* |
| `DELETE` | `/api/[resource-a]/{id}` | *Delete an item* |

### [Resource B] (e.g., AI Feature A)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/[resource-b]` | *Submit for AI analysis* |
| `GET` | `/api/[resource-b]/{id}` | *Get analysis results* |

### [Resource C] (e.g., AI Feature B)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/[resource-c]` | *Submit for AI analysis* |
| `GET` | `/api/[resource-c]/{id}` | *Get analysis results* |

### Terms

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/terms/accept` | *Record terms acceptance* |
| `GET` | `/api/terms/status` | *Check terms acceptance status* |

### Users (Admin)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/users` | *List allowed users* |
| `POST` | `/api/users` | *Invite a new user* |
| `DELETE` | `/api/users/{id}` | *Remove a user* |

### Resources

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/resources` | *List learning resources* |

### Prompts (Admin)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/prompts` | *List AI prompts* |
| `PUT` | `/api/prompts/{id}` | *Update an AI prompt* |

## OpenAPI / Swagger

**Content should include:**
- Swagger UI URL: `https://localhost:[port]/swagger` (local)
- How to download the OpenAPI spec
- How the spec is used for frontend code generation
- Versioning approach for the API spec
