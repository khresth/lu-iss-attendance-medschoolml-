# Incident Response Runbook

## Overview

Step-by-step guide for responding to incidents with LU Medical School Attendance Tracker.

## Severity Levels

| Severity | Definition | Response Time | Examples |
|----------|-----------|---------------|----------|
| **SEV-1** | *Complete application failure or data corruption* | *Immediate (30 min)* | *Application won't start, CSV data corrupted, all users affected* |
| **SEV-2** | *Major feature unavailable or significant performance degradation* | *Within 2 hours* | *Charts not generating, data loading failures, interface unusable* |
| **SEV-3** | *Minor feature issue or performance problem* | *Within business day* | *Slow chart rendering, minor UI issues, partial data loading* |
| **SEV-4** | *Low impact, workaround available* | *Next available maintenance window* | *Cosmetic issues, minor performance slowdown* |

## Incident Response Procedure

### 1. Acknowledge

- Log incident report with timestamp in incident log
- Acknowledge user reports via email or chat
- Initial assessment: single user vs. all users affected
- Set severity level based on user impact and scope
- Communicate acknowledgment to affected users with ETA

### 2. Assess

- Determine number of users affected (single user or all users)
- Check if issue is application-wide or localized to one workstation
- Verify if data files are accessible and not corrupted
- Check if Python environment is working correctly
- Review recent changes or updates that might have caused issue
- Check system resources (memory, disk space available)

### 3. Diagnose

- Check application startup logs in terminal window
- Verify CSV file integrity and format (open in spreadsheet software)
- Test Gradio interface functionality by loading sample data
- Check chart generation with sample data
- Verify Python package installations are correct
- Check system resource utilization (task manager)
- Review error logs for patterns or recurring issues

### 4. Mitigate

**Immediate actions to restore service:**
- Restart application (see [Deployment Runbook](./deployment-runbook.md))
- Restore backup CSV files if data is corrupted
- Rollback to previous application version if code issue
- Clear temporary files to free up disk space
- Free up system resources by closing other applications

**Communication:**
- Inform users of current status and expected resolution time
- Provide workaround instructions if available
- Document all mitigation actions taken for post-incident review

### 5. Resolve

- Implement permanent fix for root cause (code change, data fix)
- Test fix thoroughly before deployment (with sample data)
- Deploy fix following standard procedures (see deployment runbook)
- Verify all functionality works correctly (run through test scenarios)
- Monitor system after fix deployment (check logs, user feedback)
- Update documentation if needed (runbooks, user guides)

### 6. Post-Incident Review

- Schedule post-incident review within 1 week of resolution
- Document complete incident timeline (when detected, diagnosed, resolved)
- Identify root cause and contributing factors (what went wrong and why)
- Define preventive measures (how to avoid recurrence)
- Update runbooks and procedures based on lessons learned
- Share learnings with team and users (if applicable)

## Common Incident Scenarios

### Application Won't Start

1. Check Python installation: `python --version` (should be 3.8+)
2. Verify required packages: `pip list | findstr gradio pandas plotly`
3. Check app.py for syntax errors: `python -m py_compile app.py`
4. Verify system resources: Check available RAM (Task Manager / Activity Monitor)
5. Check port conflicts: Ensure port 7860 is not in use by another application
6. Review recent code changes: Check if recent edits introduced errors

### Data Loading Failures

1. Verify CSV file format and encoding (should be UTF-8)
2. Check file permissions and accessibility (not open in Excel)
3. Validate required columns are present (studentId, firstName, surname, academicAdvisor, startDateTime)
4. Check for file corruption (try opening in spreadsheet software)
5. Test with smaller sample files to isolate issue
6. Review data cleaning logic in load_and_clean_data() function

### Chart Generation Issues

1. Verify Plotly installation: `pip show plotly`
2. Check data format passed to charts (should be DataFrame or dict)
3. Test with simple datasets to isolate complex data issues
4. Check memory usage during generation (may fail on very large datasets)
5. Verify browser JavaScript console for errors (F12 → Console)
6. Review chart generation code in plot_student_attendance() and related functions

### Performance Degradation

1. Monitor system resource usage (CPU, RAM, Disk)
2. Check dataset size impact (larger files = slower processing)
3. Optimize data processing if needed (filter early, use vectorized operations)
4. Clear temporary files and browser cache
5. Consider system upgrades if resources limited (add RAM, use SSD)
6. Profile application performance using Python cProfile if needed

## Communication Procedures

### Internal Notification

- Email or Teams message to IT department for technical issues
- Inform supervisor for SEV-1 or SEV-2 incidents affecting multiple users
- Document in incident log with timestamp and severity

### User Communication

- Email template for widespread issues: "We are aware of [issue] and working on resolution. ETA: [time]."
- Individual support for single-user issues
- Clear and honest updates about progress

### Status Updates

- SEV-1: Updates every 30 minutes until resolved
- SEV-2: Updates every 2 hours
- SEV-3/4: Updates at start and end of business day

### Escalation

- IT Department → IT Manager (if unresolved in 2 hours)
- IT Manager → Medical School Admin (if affecting critical operations)

### Documentation

- Maintain incident log with timeline, actions taken, resolution
- Document lessons learned in post-incident review
- Update runbooks based on new issues encountered

## Prevention Measures

### Regular Backups

- Backup CSV files before ITPI data refreshes
- Backup app.py before code changes
- Keep dated backup folders (backup_YYYY_MM_DD)

### System Monitoring

- Monitor disk space (ensure > 1GB free)
- Monitor memory usage during processing
- Check for Python/process errors in terminal

### Testing

- Test with sample data after code changes
- Test on different browsers if UI issues reported
- Test with various dataset sizes

### Training & Documentation

- Ensure users have access to user guide
- Train new users on proper data export from ITPI
- Document common issues and solutions

### Maintenance

- Update Python packages quarterly: `pip install --upgrade -r requirements.txt`
- Review and update documentation annually
- Archive old data files to free up space

### Performance Monitoring

- Track processing times for different dataset sizes
- Gather user feedback on interface responsiveness
- Optimize slow operations based on profiling
