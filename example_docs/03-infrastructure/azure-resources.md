# Cloud Resources

## Overview

Document all cloud resources used by the platform, their purpose, and how they're provisioned.

## Resource Topology Diagram

Include a diagram showing all cloud resources and their relationships.

**Content should include:**
- Resource groups and their contents
- Network topology (VNets, subnets, private endpoints)
- Data flow between resources
- External dependencies (identity provider, etc.)

## Compute Resources

### Application Hosting

**Content should include:**
- Hosting model for the API (e.g., App Service, Container Apps, ECS)
- SKU and scaling configuration
- Custom domain and TLS certificate
- Environment variables and app settings
- Deployment slots (if used)

### Gateway

**Content should include:**
- API Gateway / reverse proxy hosting
- Routing configuration for API and mock server
- SSL termination

## Data Resources

### Database

**Content should include:**
- Server name, database name per environment
- SKU and performance tier
- Backup configuration and retention
- Connection string management (via secrets manager)
- Firewall rules and private endpoint configuration

## Configuration & Secrets

### Configuration Service

**Content should include:**
- Instance name per environment
- Key naming conventions
- Feature flag definitions
- How configuration is loaded at application startup
- Refresh intervals and sentinel keys

### Secrets Manager

**Content should include:**
- Instance name per environment
- Secrets inventory (connection strings, API keys, auth secrets)
- Access policies (which identities can read)
- Secret rotation schedule and procedures
- Integration with configuration service (secret references)

## Networking

**Content should include:**
- Virtual network configuration
- Subnet layout
- Private endpoints for database, secrets manager, configuration service
- DNS configuration (private DNS zones)
- Network security groups and rules

## Monitoring Resources

**Content should include:**
- Application monitoring instance
- Log analytics workspace
- Alert rules and action groups
- Error tracking project configuration

## Infrastructure as Code

**Content should include:**
- IaC tool and project location (e.g., Terraform, Bicep, Pulumi)
- How to plan and apply changes
- State file management (remote backend)
- Module organisation
- Naming conventions for resources
- Tagging strategy
