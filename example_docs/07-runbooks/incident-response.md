# Incident Response Runbook

## Overview

Step-by-step guide for responding to production incidents.

## Severity Levels

| Severity | Definition | Response Time | Examples |
|----------|-----------|---------------|----------|
| **SEV-1** | *Complete service outage or data loss* | *Immediate (15 min)* | *All users unable to access service, database corruption* |
| **SEV-2** | *Major feature unavailable or significant degradation* | *Within 1 hour* | *AI features down, auth not working for one provider* |
| **SEV-3** | *Minor feature issue or cosmetic problem* | *Within business day* | *Specific endpoint slow, UI rendering bug* |
| **SEV-4** | *Low impact, workaround available* | *Next sprint* | *Non-critical feature edge case, minor UX issue* |

## Incident Response Procedure

### 1. Acknowledge

**Content should include:**
- Acknowledge the incident

### 2. Assess

**Content should include:**
- Determine severity level
- Identify affected users and scope of impact
- Check monitoring dashboards for anomalies
- Review recent deployments or changes
- Check dependency status (cloud provider status pages)

### 3. Diagnose

**Content should include:**
- Check health endpoints: `/health`, `/alive`
- Review structured logs for errors (link to log queries)
- Review distributed traces for failing requests
- Check error tracking for new/spiking errors
- Check database connectivity and performance
- Check background job status in job dashboard
- Check cloud resource health in portal

### 4. Mitigate

**Content should include:**
- Immediate actions to reduce impact:
  - Restart service (see [Deployment Runbook](./deployment-runbook.md))
  - Scale up resources
  - Disable problematic feature via feature flag
  - Rollback to previous deployment
  - Failover to backup (if available)
- Communicate status to stakeholders

### 5. Resolve

**Content should include:**
- Implement permanent fix
- Verify fix in staging before production
- Deploy fix through standard pipeline
- Confirm monitoring returns to normal
- Close the incident

### 6. Post-Incident Review

**Content should include:**
- Schedule post-incident review within 48 hours
- Document timeline of events
- Identify root cause
- Identify contributing factors
- Define action items to prevent recurrence
- Update runbooks if needed
- Share learnings with team

## Communication Template

**Content should include:**
- Internal status update template
- User-facing status update template (if applicable)
- Stakeholder notification template
- Post-incident summary template

## Escalation Contacts

| Role | Name | Contact | When to Escalate |
|------|------|---------|-----------------|
