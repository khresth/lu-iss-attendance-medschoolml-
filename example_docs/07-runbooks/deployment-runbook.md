# Deployment Runbook

## Overview

Step-by-step procedures for deploying changes to each environment.

## Pre-Deployment Checklist

**Content should include:**
- [ ] All CI checks passing on the branch/PR
- [ ] Code review approved
- [ ] Database migrations reviewed (if any)
- [ ] Feature flags configured for the target environment
- [ ] No conflicting deployments in progress
- [ ] Stakeholders notified (if major change)

## Standard Deployment (CI/CD)

### Deploy to Staging

**Content should include:**
- Trigger: merge PR to `[base-branch]`
- Pipeline automatically runs:
  1. Build and test
  2. Publish artifacts
  3. Deploy to staging environment
  4. Run smoke tests
- How to verify deployment succeeded
- How to monitor for issues after deployment

### Deploy to Production

**Content should include:**
- Trigger: manual approval after staging validation
- Pre-production checklist:
  - [ ] Staging has been tested by QA / product
  - [ ] No new errors in error tracking on staging
  - [ ] Performance metrics stable on staging
  - [ ] Approval granted by *(role)*
- Deployment steps
- Post-deployment verification
- Monitoring period (how long to watch before considering complete)

## Database Migration Deployment

**Content should include:**
- Migrations run automatically via migration service on startup
- For destructive migrations (column removal, table drops):
  - Deploy schema change in release N (add new columns, stop writing old)
  - Deploy code change in release N+1 (start using new schema)
  - Deploy cleanup in release N+2 (remove old columns)
- How to verify migrations applied successfully
- Rollback considerations (migrations are generally forward-only)

## Rollback Procedure

**Content should include:**
- When to rollback vs forward-fix
- How to rollback a deployment:
  1. Navigate to CI/CD pipeline
  2. Find the last known good release
  3. Re-deploy that artifact
  4. Verify health checks pass
- Database rollback considerations (usually not possible — prefer forward-fix)
- How to rollback a feature flag change

## Hotfix Deployment

**Content should include:**
- When to use a hotfix (SEV-1 or SEV-2 in production)
- Branching strategy for hotfixes
- Expedited review process
- Direct-to-production deployment (if justified)
- Post-hotfix: backport to `[base-branch]`

## Emergency Procedures

### Restart a Service

**Content should include:**
- How to restart via cloud portal
- How to restart via CLI
- Expected downtime during restart
- How to verify service recovery

### Scale Up/Out

**Content should include:**
- How to scale resources via cloud portal
- Auto-scaling configuration (if enabled)
- Cost implications of scaling
- When to scale back down
