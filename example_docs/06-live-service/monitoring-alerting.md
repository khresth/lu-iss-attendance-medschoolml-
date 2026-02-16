# Monitoring & Alerting

## Overview

The LU Medical School Attendance Tracker is a local application with manual monitoring. Since it runs on individual workstations, there is no centralized monitoring or alerting infrastructure.

## Monitoring Approach

### Local Application Monitoring

| Aspect | How to Monitor | Indicator |
|--------|----------------|-----------|
| Application Status | Terminal window | Python process running |
| Data Loading | Gradio interface status box | "Loaded X rows" messages |
| File Access | Error messages in UI | "File not found" errors |
| Performance | User experience | Response time for operations |
| Memory Usage | System task manager | Python memory consumption |

## Manual Health Checks

### Daily Usage Verification

**Check:**
1. Application starts without errors
2. CSV files load successfully
3. Charts render correctly
4. Interface is responsive

### Weekly Maintenance

**Check:**
1. Review any error messages from the week
2. Verify data files are current
3. Check for any performance issues
4. Update data from ITPI dashboard if needed

## Troubleshooting Indicators

### Warning Signs

| Sign | Meaning | Action |
|------|---------|--------|
| Slow chart rendering | Large dataset or memory pressure | Reduce date range, close other apps |
| File loading errors | CSV format issues | Re-export from ITPI dashboard |
| Application crashes | Insufficient resources | Free up memory, restart application |
| Interface unresponsive | Browser or Gradio issue | Refresh browser, restart app |

### Common Issues and Solutions

**Slow Performance:**
- Check dataset size
- Monitor system memory usage
- Close unnecessary applications
- Use smaller date ranges for analysis

**File Loading Failures:**
- Verify CSV file encoding (UTF-8)
- Check required columns are present
- Ensure files are in correct directory
- Re-export data from ITPI if corrupted

**Chart Display Issues:**
- Verify Plotly is properly installed
- Check browser console for JavaScript errors
- Try different browser if issues persist
- Ensure data loaded correctly

## No Automated Alerting

**Important:** This application does not have:
- Automated alerting systems
- Paging/on-call procedures
- Service level monitoring
- Error rate tracking
- Performance dashboards

All monitoring is manual through the Gradio interface and terminal output.

## User Feedback

### Reporting Issues

Users should report issues to:
- **IT Department**: Technical problems, bugs
- **Medical School Admin**: Data quality issues, feature requests

### Information to Include

When reporting issues:
1. What operation were you performing
2. What error message appeared (if any)
3. Size of data file being processed
4. Browser and operating system
5. Any terminal error messages
