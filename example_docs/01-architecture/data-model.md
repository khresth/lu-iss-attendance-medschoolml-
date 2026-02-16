# Data Model

## Overview

Describe the data layer — database technology, ORM, and general approach to data modelling.

**Content should include:**
- Database engine (local and deployed)
- ORM used
- Code-first migrations managed via migrations project
- Migrations run automatically on startup via migration service

## Entity Relationship Diagram

Include a comprehensive ER diagram of the database schema.

**Content should include:**
- All entities and their relationships
- Primary keys, foreign keys, and indexes
- Cardinality notation (one-to-many, many-to-many)
- Colour-coding or grouping by domain area

## Core Entities

Document each entity, its purpose, and key fields.

### User Identity

**Content should include:**
- How user identity is managed (local users table vs delegated to identity provider)
- User ID sourced from JWT claims
- How user identity links to application data
- Access control tables (e.g., whitelist for external users)

### [Domain Entity A]

**Content should include:**
- Entity description — fields, lifecycle states, metadata
- Owned types and nested objects
- Relationship to user
- Tags and categorisation

### [Domain Entity B]

**Content should include:**
- Entity description — fields, states
- Related sub-entities
- Relationship chain (e.g., User -> Parent Entity -> Child Entity -> Details)

### AI & Content

**Content should include:**
- `Prompt` entity — AI prompt templates by feature and lifecycle stage
- `ResourceLink` — learning materials and resources
- Any other AI-related content entities

### Terms & Compliance

**Content should include:**
- `TermsAcceptance` — tracks user consent with timestamps
- Audit and compliance considerations

## Migration Strategy

**Content should include:**
- How to create a new migration (command with project flags)
- How migrations are applied (migration service runs before API)
- Rollback procedures
- Naming conventions for migrations
- How to handle data migrations vs schema migrations

## Data Access Patterns

**Content should include:**
- Repository pattern usage
- Query patterns (filtering by user, pagination)
- How owned types are queried
- Performance considerations (eager vs lazy loading, indexes)
