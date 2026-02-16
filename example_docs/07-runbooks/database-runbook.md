# Database Runbook

## Overview

Operational procedures for database management, maintenance, and troubleshooting.

## Connection Information

**Content should include:**

| Environment | Server | Database | Authentication |
|------------|--------|----------|---------------|
| Local | `localhost,[port]` | *DB name* | SQL auth (password in user secrets) |
| Staging | *Cloud database server* | *DB name* | Managed identity / connection string in secrets manager |
| Production | *Cloud database server* | *DB name* | Managed identity / connection string in secrets manager |

- How to connect from developer machines
- Required tools (e.g., Azure Data Studio, pgAdmin, DataGrip)
- Network access requirements (VPN, firewall rules)

## Backup & Recovery

### Automated Backups

**Content should include:**
- Automated backup schedule
- Retention period
- Geo-redundancy configuration
- How to verify backups are running

### Point-in-Time Restore

**Content should include:**
- When to use (data corruption, accidental deletion)
- Step-by-step procedure:
  1. Identify the point in time to restore to
  2. Initiate restore in cloud portal
  3. Restore creates a new database
  4. Verify restored data
  5. Swap connection strings (if replacing production)
- Expected time to complete
- Testing restore procedures (schedule regular tests)

### Manual Backup

**Content should include:**
- How to take an on-demand backup
- Where to store manual backups
- When manual backups are needed (before risky migrations, etc.)

## Migration Operations

### Applying Migrations

**Content should include:**
- Standard: Migration service applies on startup
- Manual: `[database update command]`
- Verifying migration status: `[migrations list command]`
- Troubleshooting failed migrations

### Creating a New Migration

**Content should include:**
```bash
[migration add command] <Name> \
  --project [migrations-project] \
  --startup-project [api-project]
```
- Review the generated migration file before applying
- Check for data loss warnings
- Test migration against a copy of production data (if significant)

### Rolling Back a Migration

**Content should include:**
- `[database update command] <PreviousMigrationName>`
- When this is safe vs when it's not (data loss risk)
- Preferred approach: create a new migration that reverses the change

## Performance Management

### Monitoring Queries

**Content should include:**
- How to identify slow queries (cloud query performance tools)
- Key queries to monitor
- Index recommendations
- How to add indexes (via ORM migration)

### Connection Pool Management

**Content should include:**
- Connection pool configuration
- How to monitor pool usage
- Symptoms of pool exhaustion
- Tuning pool size

## Common Procedures

### Add an Index

**Content should include:**
- Identify the query that needs optimisation
- Create migration with index definition
- Test impact on staging
- Deploy via standard pipeline

### Archive Old Data

**Content should include:**
- Data retention policy
- Archive procedure (move to archive table / delete)
- Verification after archive
- Frequency of archive operations

## Troubleshooting

### Connection Failures

**Content should include:**
- Check database firewall rules
- Check private endpoint configuration
- Check connection string in secrets manager
- Check managed identity permissions
- Check for cloud database outages on status page

### Deadlocks

**Content should include:**
- How to identify deadlocks in logs
- Common deadlock causes in the application
- Resolution steps
- Preventive measures

### Database Full / Storage Limit

**Content should include:**
- How to check storage usage
- Immediate actions (clean up, increase tier)
- Long-term solutions (archiving, data cleanup jobs)
