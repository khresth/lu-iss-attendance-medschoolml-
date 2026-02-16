# Error Codes Reference

## Overview

Comprehensive reference for all error codes returned by the API, their meanings, and resolution guidance.

## Error Response Format

All errors follow this envelope:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description of what went wrong",
    "details": {
      // Optional additional context
    }
  },
  "requestId": "unique-correlation-id"
}
```

## HTTP Status Code Mapping

| Status | Category | When Used |
|--------|----------|-----------|
| `400` | Bad Request | *Validation errors, malformed input* |
| `401` | Unauthorised | *Missing or invalid authentication token* |
| `403` | Forbidden | *Authenticated but lacks required permissions* |
| `404` | Not Found | *Requested resource does not exist* |
| `409` | Conflict | *Operation conflicts with current state* |
| `413` | Payload Too Large | *File upload exceeds size limit* |
| `422` | Unprocessable Entity | *Semantically invalid request* |
| `429` | Too Many Requests | *Rate limit exceeded* |
| `500` | Internal Server Error | *Unexpected server error* |
| `502` | Bad Gateway | *Downstream service unavailable* |
| `503` | Service Unavailable | *Service temporarily unavailable* |

## Application Error Codes

### Authentication & Authorisation

| Code | HTTP Status | Description | Resolution |
|------|------------|-------------|------------|
| `AUTH_TOKEN_MISSING` | 401 | *No Bearer token provided* | *Include Authorization header* |
| `AUTH_TOKEN_EXPIRED` | 401 | *JWT has expired* | *Refresh token and retry* |
| `AUTH_TOKEN_INVALID` | 401 | *JWT signature or format is invalid* | *Re-authenticate* |
| `AUTH_INSUFFICIENT_PERMISSIONS` | 403 | *User lacks required role or policy* | *Contact admin for access* |
| `AUTH_USER_NOT_ALLOWED` | 403 | *User not in access control list* | *Contact admin for invitation* |

### Validation

| Code | HTTP Status | Description | Resolution |
|------|------------|-------------|------------|
| `VALIDATION_REQUIRED_FIELD` | 400 | *A required field is missing* | *Check `details` for field name* |
| `VALIDATION_INVALID_FORMAT` | 400 | *Field value has incorrect format* | *Check `details` for expected format* |
| `VALIDATION_FILE_TOO_LARGE` | 413 | *Uploaded file exceeds size limit* | *Reduce file size* |
| `VALIDATION_UNSUPPORTED_FORMAT` | 400 | *File type not supported* | *Use supported format* |

### Resource Errors

| Code | HTTP Status | Description | Resolution |
|------|------------|-------------|------------|
| `RESOURCE_NOT_FOUND` | 404 | *Requested entity does not exist* | *Check ID is correct* |
| `RESOURCE_ALREADY_EXISTS` | 409 | *Duplicate resource* | *Use existing resource or change identifier* |
| `RESOURCE_STATE_CONFLICT` | 409 | *Operation not valid in current state* | *Check entity lifecycle state* |

### AI Service Errors

| Code | HTTP Status | Description | Resolution |
|------|------------|-------------|------------|
| `AI_SERVICE_UNAVAILABLE` | 503 | *AI service not reachable* | *Retry later* |
| `AI_RATE_LIMITED` | 429 | *AI service rate limit exceeded* | *Wait and retry* |
| `AI_PROCESSING_ERROR` | 500 | *AI returned an unexpected error* | *Retry; if persistent, contact support* |
| `AI_RESPONSE_INVALID` | 500 | *AI response could not be parsed* | *Retry; if persistent, check prompt configuration* |

### System Errors

| Code | HTTP Status | Description | Resolution |
|------|------------|-------------|------------|
| `INTERNAL_ERROR` | 500 | *Unexpected server error* | *Report with `requestId` for investigation* |
| `DATABASE_ERROR` | 500 | *Database operation failed* | *Report with `requestId`* |
| `EXTERNAL_SERVICE_ERROR` | 502 | *Downstream service returned an error* | *Retry; check dependency health* |

## Using `requestId` for Debugging

**Content should include:**
- Every error response includes a `requestId` (correlation ID)
- How to use it to find related logs and traces
- Where to search (error tracking, log analytics, orchestrator dashboard)
- Include `requestId` when reporting issues to support

## Client-Side Error Handling

**Content should include:**
- How the frontend handles each error category
- Retry strategy for transient errors (429, 503)
- User-facing error messages for each category
- How to add handling for new error codes
