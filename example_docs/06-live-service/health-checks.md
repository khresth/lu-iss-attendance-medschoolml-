# Health Checks

## Overview

Document health check procedures for LU Medical School Attendance Tracker, what they verify, and how they're used.

## Manual Health Check Procedures

| Check | Purpose | Performed By |
|--------|---------|-------------|
| Application Startup | Verify application launches successfully | User/IT staff |
| Data Loading | Verify CSV files load correctly | User/IT staff |
| Interface Functionality | Verify Gradio interface works | User/IT staff |
| Chart Generation | Verify charts render correctly | User/IT staff |

## Application Startup Check

**What it verifies:**
- Python environment is correctly configured (version 3.8+)
- All required packages are installed (gradio, pandas, plotly, openpyxl)
- Gradio interface starts successfully without errors
- Application binds to correct port (7860 by default)

**How to perform:**
1. Open terminal in application directory
2. Run: `python app.py`
3. Check terminal output for errors

**Expected result:**
- Terminal shows "Running on http://localhost:7860"
- No error messages in terminal
- Browser opens automatically or can access http://localhost:7860

**If it fails:**
- Check Python installation: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check if port 7860 is already in use
- Review error message for specific issue

## Data Loading Check

**What it verifies:**
- CSV files are accessible and readable from application directory
- Required columns are present (studentId, firstName, surname, academicAdvisor, startDateTime)
- Data formats are correct (dates parseable, IDs as strings)
- No corruption in data files (no malformed rows)

**How to perform:**
1. Start application: `python app.py`
2. Upload a CSV file through the file interface
3. Click "Load / Refresh Data" button
4. Check status message for success/failure

**Expected result:**
- Status shows "Loaded X rows from filename.csv"
- Module appears in dropdown selector
- No error messages about missing columns

**If it fails:**
- Verify CSV file is UTF-8 encoded (re-export from ITPI if needed)
- Check file has all required columns (studentId, firstName, surname, academicAdvisor, startDateTime)
- Ensure file is not open in Excel or another program
- Check file permissions (readable by current user)

## Interface Functionality Check

**What it verifies:**
- Gradio interface loads correctly in web browser
- All interactive elements work (buttons, dropdowns, file uploads)
- File upload functionality accepts CSV and Excel files
- Charts display correctly in the interface

**How to perform:**
1. Start application: `python app.py`
2. Open browser to http://localhost:7860
3. Test file upload by selecting a CSV file
4. Test dropdown selectors (module, dates, thresholds)
5. Click "Analyze Attendance" button
6. Check all tabs display correctly (Summary, Student Details, Placement Analysis, Macro View)

**Expected result:**
- Interface loads completely without errors
- All buttons are clickable
- Dropdowns show options and respond to selection
- File uploads successfully

**If it fails:**
- Try different browser (Chrome, Firefox, Edge)
- Check if port 7860 is blocked by firewall
- Clear browser cache and reload page
- Check console (F12) for JavaScript errors
- Restart application

## Chart Generation Check

**What it verifies:**
- Plotly charts render correctly in the browser
- Data visualization is accurate and matches input data
- Interactive features work (zoom, pan, hover tooltips)
- Performance is acceptable (charts load within 5 seconds)

**How to perform:**
1. Load data in application
2. Select a module and date range
3. Click "Analyze Attendance"
4. Navigate to "Student Details" tab
5. Select a student from the radio list
6. Verify chart displays correctly

**Expected result:**
- Chart renders without errors
- Chart shows attendance trend line
- Hovering shows data points with values
- Chart can be zoomed and panned
- Chart saves correctly when using camera icon

**If it fails:**
- Verify Plotly is installed: `pip show plotly`
- Check browser console for JavaScript errors
- Test with smaller dataset to isolate size issue
- Try different browser
- Check data loaded correctly before chart generation
- Expected result: Charts display correctly, data is accurate
- What happens if it fails: Check Plotly installation, data format

## Dependency Health

### Python

**Check:**
- Verify Python version: `python --version` (should be 3.8+)
- Test Python installation: `python -c "import sys; print(sys.version)"`

**If issues:**
- Reinstall Python from python.org
- Check PATH environment variable includes Python

### Gradio

**Check:**
- Verify installation: `pip show gradio`
- Test import: `python -c "import gradio; print(gradio.__version__)"`

**If issues:**
- Reinstall: `pip install --upgrade gradio`
- Check for compatibility issues with other packages

### Pandas

**Check:**
- Verify installation: `pip show pandas`
- Test import and basic functionality: `python -c "import pandas as pd; df = pd.DataFrame({'a': [1,2]}); print(df)"`

**If issues:**
- Reinstall: `pip install --upgrade pandas`
- Check for dependency conflicts

### Plotly

**Check:**
- Verify installation: `pip show plotly`
- Test import: `python -c "import plotly; print(plotly.__version__)"`

**If issues:**
- Reinstall: `pip install --upgrade plotly`
- Check browser compatibility for chart rendering

## Performance Health Checks

### Application Startup Time

**Benchmark:** Application should start within 5 seconds
**How to check:**
1. Run: `python app.py`
2. Measure time until "Running on http://localhost:7860" appears

**If slow:**
- Check for large data files in directory
- Verify no other Python processes consuming resources
- Consider upgrading hardware (SSD helps)

### Memory Usage

**Benchmark:** Should stay under 500MB for typical datasets
**How to check:**
- Windows: Task Manager → Processes → Python
- Mac/Linux: `ps aux | grep python` or Activity Monitor

**If high:**
- Process smaller date ranges
- Close other applications
- Consider adding more RAM

### Chart Rendering Performance

**Benchmark:** Charts should render within 5 seconds
**How to check:**
1. Load data and select student
2. Time how long until chart appears

**If slow:**
- Reduce dataset size with date filters
- Close browser tabs
- Try different browser

### Response Time

**Benchmark:** Interface should respond within 1 second
**How to check:**
- Click buttons and measure response time
- Dropdown selections should be immediate

**If slow:**
- Check system resources
- Reduce dataset complexity
- Restart application

## Troubleshooting Health Issues

### Common Startup Failures

| Issue | Solution |
|-------|----------|
| "Python not recognized" | Add Python to PATH or use full path |
| "Module not found" | Run `pip install -r requirements.txt` |
| "Port already in use" | Kill other processes on port 7860 or change port |
| "Permission denied" | Run as administrator/sudo or check file permissions |

### Data Loading Error Resolution

| Issue | Solution |
|-------|----------|
| "File not found" | Check file is in correct directory |
| "Missing columns" | Re-export CSV from ITPI with all required fields |
| "Encoding error" | Save CSV as UTF-8 encoding |
| "Empty data" | Check CSV has data rows, not just headers |

### Interface Problem Troubleshooting

| Issue | Solution |
|-------|----------|
| Blank page | Check browser console for JavaScript errors |
| Buttons not working | Refresh page or restart application |
| File upload fails | Check file size and format |
| Slow response | Close other applications, reduce data size |

### Chart Generation Issue Fixes

| Issue | Solution |
|-------|----------|
| Chart not displaying | Verify Plotly installed, check browser console |
| Wrong data shown | Verify correct module and student selected |
| Chart won't save | Check browser permissions for downloads |
| Interactive features broken | Try different browser |

### Performance Optimization Guidance

- Use date range filters to limit data volume
- Close unnecessary browser tabs and applications
- Use modern browser (Chrome, Firefox, Edge)
- Keep data files under 10MB when possible

## Automated Health Monitoring

**Not Applicable:** This is a local application without automated monitoring infrastructure.

**Manual Monitoring:**
- Check terminal output for errors during operation
- Monitor system resources during heavy processing
- User feedback on performance issues
- Regular testing of core functionality

## Adding New Health Checks

To add a new health check:

1. **Identify what to verify** (e.g., new data source, new feature)
2. **Define success criteria** (what indicates healthy state)
3. **Document verification steps** (how to perform the check)
4. **Document expected results** (what users should see)
5. **Document troubleshooting** (what to do if check fails)

**Example template:**

```markdown
## New Feature Check

**What it verifies:**
- Feature X loads correctly
- Data processes without errors

**How to perform:**
1. Step 1
2. Step 2

**Expected result:**
- Result description

**If it fails:**
- Troubleshooting step 1
- Troubleshooting step 2
```
