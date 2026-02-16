# Developer Onboarding

## Welcome

Introduce the project, the team, and what a new developer needs to know on day one.

**Content should include:**
- What [Project Name] is and who it's for
- Team structure and key contacts
- Communication channels (Teams, Slack, etc.)
- Sprint cadence and ceremonies
- Where to ask questions

## Access Checklist

Provide a checklist of accounts, tools, and permissions a new developer needs.

**Content should include:**

- [ ] Source control access (repository, boards, pipelines)
- [ ] Cloud portal access (staging resource group)
- [ ] Documentation space access
- [ ] Identity provider console access (read-only)
- [ ] Error tracking project access
- [ ] Package feed access (if private packages used)
- [ ] VPN / network access (if required)
- [ ] Development machine setup (see [Local Setup](./local-setup.md))

## Key Documentation

**Content should include:**
- Links to this documentation set
- Links to the project README and CLAUDE.md
- Links to design documents / ADRs
- Links to design files (e.g., Figma)
- Links to work item tracking

## Architecture Quick Start

**Content should include:**
- 5-minute overview of the system architecture
- Link to full [System Overview](../01-architecture/system-overview.md)
- Key things to understand before writing code:
  - Orchestration model
  - Authentication architecture
  - API pattern
  - Frontend data flow pattern

## Development Workflow

**Content should include:**
- Branching strategy (feature branches from `[base-branch]`, naming conventions)
- PR process (reviewers, CI checks, merge requirements)
- Code review expectations
- Pre-commit hooks (linting, formatting)
- How to enable hooks: `git config core.hooksPath .husky`

## First Tasks

**Content should include:**
- Suggested onboarding tasks to build familiarity:
  1. Set up local environment and run the full stack
  2. Make a small frontend change (e.g., update text on a screen)
  3. Add a simple backend endpoint
  4. Write a unit test
  5. Create a PR and go through the review process
- Where to find "good first issue" work items
