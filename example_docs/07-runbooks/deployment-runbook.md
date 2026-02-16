# Deployment Runbook

## Overview

Step-by-step procedures for deploying changes to LU Medical School Attendance Tracker.

## Pre-Deployment Checklist

- [ ] Python environment tested and working
- [ ] All required packages installed (Gradio, Pandas, Plotly)
- [ ] Code changes tested locally
- [ ] CSV data files validated
- [ ] Documentation updated if needed
- [ ] Backup of current version created

## Manual Deployment Process

### Deploy to Local Machine

1. Stop current application if running (Ctrl+C in terminal)
2. Backup current app.py file (copy to app.py.backup)
3. Copy new version to target directory
4. Update requirements.txt if dependencies changed
5. Test new version with sample data
6. Verify all functionality works correctly

### Update Dependencies

1. Check requirements.txt for new packages
2. Run `pip install -r requirements.txt`
3. Verify all packages install correctly
4. Test import of new dependencies in Python
5. Update virtual environment if used

## Data Deployment

### Update CSV Data Files

1. Export new data from ITPI dashboard
2. Validate CSV file format and content
3. Backup existing CSV files
4. Replace with new data files
5. Test data loading in application
6. Verify charts and statistics work correctly

### Update Placement Mapping

1. Export new placement data from ITPI
2. Validate placement mapping format
3. Backup existing placement files
4. Update y*r1.csv files
5. Test placement pattern matching
6. Verify placement data displays correctly

## Rollback Procedure

**When to rollback vs forward-fix:**
- Rollback if new version crashes or has critical bugs
- Forward-fix if issue is minor and can be quickly fixed

**How to rollback application:**
1. Restore backup of app.py from backup copy
2. Restart application: `python app.py`
3. Verify functionality works with test data

**How to rollback data:**
1. Restore backup CSV files from dated backup folder
2. Test data loading in application
3. Verify charts work correctly

**Document:**
- Reason for rollback
- Version rolled back from/to
- Any data issues encountered

## Testing After Deployment

### Functional Testing

- Test application startup: `python app.py`
- Verify CSV file loading through interface
- Test chart generation with sample data
- Check interface responsiveness
- Validate data processing accuracy
- Test chart generation
- Check interface responsiveness
- Validate data processing accuracy

### Data Validation

- Test with various CSV file formats (different years, semesters)
- Verify data cleaning works correctly (date parsing, type conversion)
- Check attendance calculations against known values
- Validate placement pattern matching with test descriptions
- Test error handling for invalid data (missing columns, bad formats)

## Performance Testing

- Test with typical dataset sizes (1,000 - 10,000 rows)
- Monitor memory usage during processing (should stay under 500MB)
- Check chart rendering performance (should complete in < 5 seconds)
- Verify interface responsiveness during data loading
- Document performance benchmarks for reference

## Documentation Updates

- Update user documentation (user-guide.md) for new features
- Update technical documentation for any code changes
- Update README.md if installation or setup changed
- Document any new configuration options or file formats
- Update troubleshooting guides with new common issues

## Communication Procedures

- Notify users of upcoming changes via email or Teams
- Document deployment schedule in shared calendar
- Provide training for new features if significant changes
- Share updated documentation links with users
- Collect feedback after deployment for future improvements

## Emergency Procedures

### Quick Fix Deployment

**When to use quick fixes:**
- Critical bugs affecting all users
- Data processing errors giving wrong results
- Application crashes on startup

**How to deploy urgent changes:**
1. Make minimal fix to address the issue
2. Test fix locally with sample data
3. Deploy immediately to users
4. Document the change made

**Testing requirements:**
- At minimum, test that the fix resolves the issue
- Test that no new issues are introduced
- Full testing can happen after deployment

**Documentation:**
- Update changelog with quick fix details
- Note any temporary workarounds

**Follow-up:**
- Schedule proper testing when time allows
- Consider more robust fix in next release

### Application Restart

**How to restart:**
1. Stop application: Press Ctrl+C in terminal running app.py
2. Wait for process to terminate
3. Start application: `python app.py`
4. Wait for "Running on http://localhost:7860" message

**Expected downtime:**
- 5-10 seconds for restart
- Users will see connection error during restart
- Data files don't need to be reloaded if unchanged

**Verification:**
- Check terminal shows no errors
- Open browser to http://localhost:7860
- Test file upload and chart generation
- Verify data processing works correctly

**Data integrity:**
- CSV files are not affected by restart
- Any in-memory data will need to be reloaded
- User uploaded files will need to be re-uploaded
