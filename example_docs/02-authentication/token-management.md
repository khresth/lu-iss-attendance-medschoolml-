# Token Management

## Overview

Document how authentication tokens are obtained, stored, refreshed, and used throughout the system.

## Token Lifecycle

### Token Acquisition

**Content should include:**
- OAuth 2.0 Authorization Code flow via [Identity Provider] Hosted UI
- [Auth SDK] handles code exchange for tokens
- Three tokens received: ID token, access token, refresh token
- Which token is used for API calls (e.g., ID token as Bearer)

### Token Storage

**Content should include:**
- Auth store with persistence middleware
- What's stored: username, email, ID token, access token, provider type
- Storage backend (e.g., AsyncStorage on native, localStorage on web)
- Security implications of client-side token storage
- What is NOT stored (refresh token management delegated to [Auth SDK])

### Token Refresh

**Content should include:**
- Automatic refresh triggered on 401 response from API
- [Auth SDK] `fetchAuthSession` with `forceRefresh` option
- Retry logic: refresh token -> retry original request
- Failure handling: if refresh fails, redirect to sign-in
- Race condition prevention (multiple concurrent 401s)

### Token Expiry

**Content should include:**
- ID token expiry duration (configured in [Identity Provider])
- Access token expiry duration
- Refresh token expiry duration
- How the frontend detects expiry (reactive on 401, not proactive)

## Backend Token Processing

### UserContextMiddleware

**Content should include:**
- Middleware position in the pipeline
- How it reads the Authorization header
- JWT decoding (without re-validation — already done by auth middleware)
- Issuer-based source detection (which pool the user came from)
- Claim extraction: user ID, email, groups
- How extracted context is made available to endpoints

### Token Validation

**Content should include:**
- Backend framework JWT Bearer authentication handler
- Multiple authority support (all identity provider pools)
- Audience validation
- Signature verification via JWKS
- Clock skew configuration

## Sign-Out

**Content should include:**
- Frontend sign-out flow
- Auth store clearing
- [Auth SDK] session clearing
- [Identity Provider] hosted UI logout endpoint (if used)
- Backend considerations (stateless — no server-side session to invalidate)

## Troubleshooting

**Content should include:**
- Common token-related errors and their causes
- How to decode and inspect a JWT for debugging
- Token mismatch between pools
- Expired token handling edge cases
- How to test auth flows locally
