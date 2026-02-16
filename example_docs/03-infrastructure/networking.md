# Networking & Security

## Overview

Document the network architecture, security boundaries, and communication paths.

## Network Architecture Diagram

Include a diagram showing network topology across environments.

**Content should include:**
- Virtual network layout with CIDR ranges
- Subnet allocation (compute, data, private endpoints)
- Internet-facing endpoints
- Internal-only endpoints
- Traffic flow paths

## DNS Configuration

**Content should include:**
- Public DNS records and domains
- Private DNS zones for internal service resolution
- How the orchestrator manages service discovery locally
- DNS configuration per environment

## TLS / HTTPS

**Content should include:**
- Certificate management (cloud-managed, Let's Encrypt, etc.)
- TLS versions supported
- HTTPS enforcement (redirect rules)
- Certificate renewal process

## CORS Policy

**Content should include:**
- Allowed origins per environment
- Allowed methods and headers
- Credentials policy
- How CORS is configured in the API
- Why specific origins are allowed (e.g., `localhost:[port]` for frontend dev server)

## Firewall & Network Security

**Content should include:**
- Network security group rules
- IP restrictions (if any)
- Private endpoint configuration
- Service tags and application security groups
- How database access is restricted

## Traffic Flow

### User -> Frontend

**Content should include:**
- How users access the frontend (CDN, App Service, etc.)
- TLS termination point
- Any WAF or DDoS protection

### Frontend -> Backend

**Content should include:**
- API Gateway as entry point
- How the gateway routes requests
- Authentication header propagation
- Request/response flow through middleware

### Backend -> External Services

**Content should include:**
- Outbound connections to AI service
- Outbound connections to identity provider (JWKS endpoints)
- Outbound connections to configuration service and secrets manager
- Private endpoint usage for cloud services

## Security Hardening

**Content should include:**
- Security headers (CSP, HSTS, X-Frame-Options, etc.)
- Rate limiting configuration
- Input validation approach
- SQL injection prevention (ORM parameterised queries)
- XSS prevention measures
- CSRF protection
