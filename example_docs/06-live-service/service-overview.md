# Live Service Overview

## Overview

Describe the LU Medical School Attendance Tracker production service — what's running, where, and how it serves users.

## Service Architecture (Production)

- Single Python application deployment (`app.py`)
- Local machine deployment model (individual user workstations)
- No cloud infrastructure required or used
- Direct file system access for CSV data files
- Gradio web interface serving on localhost:7860

## Service Access

| Service | Access Method | Purpose | Health Check |
|---------|--------------|---------|-------------|
| Application | http://localhost:7860 | User-facing web interface | Application starts successfully |
| Data Files | Local file system | CSV data storage | Files accessible and readable |
| Python Environment | Local installation | Application runtime | Dependencies installed correctly |

## Service Level Objectives (SLOs)

**Availability:**
- Target: Application available during working hours (9am-5pm weekdays)
- Achieved through: Local installation on user workstations

**Performance:**
- Application startup: < 5 seconds
- Chart rendering: < 5 seconds for standard datasets
- Data processing: < 10 seconds for 5,000 rows
- Interface response: < 1 second

**Reliability:**
- Error rate target: < 5% data processing errors for typical files
- Measured through: Manual testing and user feedback

**When SLOs are breached:**
- Document issue and investigate root cause
- Consider performance optimization (filter data, upgrade hardware)
- Review with users if persistent issues

## Dependencies & Requirements

| Dependency | Requirement | Impact if Unavailable | Fallback |
|-----------|-----------|----------------------|----------|
| Python 3.8+ | Required runtime | Application won't start | Install/upgrade Python |
| Gradio | Web interface framework | No UI available | Install missing package |
| Pandas | Data processing | No data analysis | Install missing package |
| Plotly | Visualization | No charts available | Install missing package |
| CSV Data Files | Data source | No attendance data | Load backup files |
| ITPI Dashboard | Data export source | No new data | Use existing data |

## Support Model

**Technical Support:**
- IT Department for application issues, bugs, installations
- Email: [it-support@medschool.ac.uk]
- Phone: [extension]

**User Support:**
- Medical school staff for usage questions, training
- Documentation available in example_docs/ directory
- Self-service troubleshooting via user guides

**No On-Call:**
- This is not a critical 24/7 service
- Support during business hours only
- Users can continue working with existing data if issues arise

## Maintenance Procedures

**Regular Maintenance:**
- No scheduled maintenance windows required
- Updates deployed as needed (monthly/quarterly)
- Python package updates: `pip install --upgrade -r requirements.txt`

**Data Refresh:**
- Manual CSV export from ITPI dashboard
- Update frequency: Weekly or as needed
- Procedure documented in database-runbook.md

**Version Management:**
- Track changes via Git version control
- Tag stable releases
- Maintain changelog for user communication
- Application updates via file replacement
- Backup procedures for data and code

## Deployment Model

- Manual deployment to local machines (individual user workstations)
- No automated deployment pipeline or CI/CD
- Version control via Git repository for code tracking
- File-based distribution: copy app.py and requirements.txt to target machine
- User-managed update process: users update when convenient

## User Access

- Local machine access only (localhost:7860)
- No remote access capabilities or external network exposure
- Physical security of workstation provides access control
- File permissions protect CSV data files
- No user authentication required (single-user local application)

## Performance Characteristics

- Performance dependent on local machine resources (CPU, RAM, disk)
- Memory usage scales linearly with dataset size (approximately 100MB per 10,000 rows)
- Processing time varies with data complexity and date range selected
- Chart rendering performance based on data volume (larger datasets = slower rendering)
- Network connectivity not required for operation (purely local application)
