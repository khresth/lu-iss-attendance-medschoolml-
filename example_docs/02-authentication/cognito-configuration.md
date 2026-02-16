# Identity Provider Configuration

## Overview

Document the identity provider setup for all user pools.

## Primary Auth Pool ([Organization])

### Pool Configuration

**Content should include:**
- Pool IDs per environment:
  - Staging: `[pool-id-staging]`
  - Production: `[pool-id-production]`
- Region: `[region]`
- Hosted UI domains per environment
- App client IDs per environment
- Supported OAuth scopes: `openid`, `email`, `profile`
- Callback URLs per environment
- Sign-out URLs per environment

### Custom Claims

**Content should include:**
- `[primary-id-claim]` — primary user identifier (custom claim)
- `[groups-claim]` — group memberships
- `email` — user email address
- Any other custom attributes

### Federation

**Content should include:**
- How organizational SSO federates into this pool
- SAML or OIDC configuration details
- Attribute mapping from organizational IdP to identity provider

## Secondary Auth Pool (External)

### Pool Configuration

**Content should include:**
- Pool IDs per environment:
  - Staging: `[pool-id-staging]`
  - Production: `[pool-id-production]`
- Region: `[region]`
- Hosted UI domains per environment
- App client IDs per environment
- Supported OAuth scopes
- Callback URLs per environment

### Social Identity Providers

**Content should include:**
- Google OAuth configuration
- Apple Sign-In configuration
- How social provider attributes map to identity provider attributes
- `sub` claim used as user identifier

### User Management

**Content should include:**
- How administrators create external user accounts
- Access control table — fields and lifecycle
- Invitation flow: admin adds email -> account created -> email sent -> user signs in
- Account deletion and deprovisioning

## Backend JWT Validation

**Content should include:**
- How the backend framework validates tokens from all pools
- JWKS endpoint configuration
- Issuer validation for multi-pool support
- Clock skew tolerance
- Configuration keys:
  - `[Auth]:Authority`, `[Auth]:ClientId` (primary pool)
  - `[ProjectName].ExternalAuth:Authority`, `[ProjectName].ExternalAuth:ClientId` (secondary pool)

## Frontend Auth SDK Configuration

**Content should include:**
- Dynamic auth configuration switching between pools
- `configureForPrimary()` and `configureForSecondary()` functions
- How the selected provider is persisted across OAuth redirects (sessionStorage)
- OAuth redirect URI resolution at runtime
- Configuration values per environment
