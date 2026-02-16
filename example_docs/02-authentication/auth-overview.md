# Authentication & Authorisation Overview

## Overview

Describe the authentication architecture at a high level — what it achieves and why it's designed this way.

**Content should include:**
- Identity provider model (single or multiple providers supporting distinct user populations)
- [User Type A] users (e.g., internal/organizational users) via [Primary Auth Pool]
- [User Type B] users (e.g., external users) via [Secondary Auth Pool] with social login
- JWT-based authentication with Bearer tokens
- Policy-based authorisation on the backend

## Authentication Flow Diagram

Include a sequence diagram showing the complete auth flow for each user type.

### [Primary Auth Flow]

**Content should include:**
- User clicks "Sign in with [Organization]"
- Frontend configures [Auth SDK] for primary [Identity Provider] pool
- Redirect to organization hosted UI
- User authenticates with organizational credentials
- Redirect back with authorization code
- [Auth SDK] exchanges code for tokens
- Frontend stores tokens in auth store
- User completes onboarding (e.g., risk acknowledgement, terms acceptance)
- Terms acceptance recorded via API call
- Subsequent API calls include Bearer token

### [Secondary Auth Flow]

**Content should include:**
- User clicks "Sign in with [Social Provider]"
- Frontend configures [Auth SDK] for secondary [Identity Provider] pool
- Redirect to external hosted UI
- User authenticates with social provider
- Redirect back with authorization code
- [Auth SDK] exchanges code for tokens
- Frontend stores tokens in auth store
- User completes onboarding (same flow as primary)
- Terms acceptance recorded via API call

## User Identity Resolution

**Content should include:**
- How `UserContextMiddleware` determines user source from JWT issuer claim
- Claim mapping: which claims identify users from each provider
- Group extraction from group claims
- How user context is propagated through the request pipeline

## Authorisation Policies

**Content should include:**
- List of authorisation policies (e.g., "anyUser", "adminOnly")
- What each policy requires
- How policies are applied to endpoint groups
- Role-based access considerations (admin, standard user)

## External User Access Control

**Content should include:**
- Whitelist/allowlist mechanism for external users
- How administrators invite external users
- [Identity Provider] user creation for invited users
- Lifecycle: invitation -> account creation -> first sign-in

## Security Considerations

**Content should include:**
- Token expiry and refresh strategy
- CORS configuration and allowed origins
- HTTPS enforcement
- OWASP considerations addressed
- PII handling in tokens and logs
