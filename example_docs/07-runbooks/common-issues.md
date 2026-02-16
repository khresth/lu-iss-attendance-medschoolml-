# Common Issues & Resolutions

## Overview

A troubleshooting guide for frequently encountered issues with LU Medical School Attendance Tracker.

## Application Startup Failures

### Python Environment Issues

**Symptoms:** Application won't start, "python not recognized" errors, import errors.

**Diagnosis steps:**
1. Check Python installation: `python --version` or `python3 --version`
2. Verify pip is installed: `pip --version`
3. Check if required packages are installed: `pip list | grep gradio`
4. Review error messages in terminal
5. Check file permissions on app.py

**Common causes and resolutions:**
- *Python not in PATH* -> Add Python to system PATH or use full path to python.exe
- *Missing packages* -> Run `pip install -r requirements.txt`
- *Package version conflicts* -> Create virtual environment: `python -m venv venv`
- *Permission denied* -> Run as administrator or check file permissions
- *Syntax errors in app.py* -> Check for typos or missing brackets
- *Insufficient resources* -> Free up memory/disk space

### Data Loading Failures

**Symptoms:** CSV files won't load, error messages about data format.

**Diagnosis steps:**
1. Verify CSV file exists and is readable
2. Check file encoding (should be UTF-8)
3. Validate required columns are present
4. Check for file corruption or invalid formats
5. Test with smaller sample files

**Common causes and resolutions:**
- *Wrong file format* -> Export correctly from ITPI dashboard
- *Missing columns* -> Verify required columns: studentId, firstName, surname, academicAdvisor, startDateTime
- *Encoding issues* -> Save CSV as UTF-8 encoding
- *File permissions* -> Check file access permissions
- *Corrupted data* -> Re-export from ITPI dashboard

### Chart Generation Problems

**Symptoms:** Charts won't display, errors in visualization.

**Diagnosis steps:**
1. Verify Plotly is installed correctly
2. Check data format passed to chart functions
3. Test with simple, known-good datasets
4. Check browser JavaScript console for errors
5. Monitor memory usage during chart generation

**Common causes and resolutions:**
- *Plotly not installed* -> Run `pip install plotly`
- *Invalid data format* -> Check data types and structure
- *Memory issues* -> Use smaller datasets or optimize processing
- *Browser compatibility* -> Try different browser or update browser
- *JavaScript errors* -> Check browser console, clear cache

### Performance Issues

**Symptoms:** Slow data processing, unresponsive interface.

**Diagnosis steps:**
1. Monitor system resource usage
2. Check dataset size impact on performance
3. Profile data processing operations
4. Test with different dataset sizes
5. Check for memory leaks

**Common causes and resolutions:**
- *Large datasets* -> Use data sampling, optimize Pandas operations
- *Memory constraints* -> Close other applications, add more RAM
- *Inefficient code* -> Optimize data processing, use vectorized operations
- *System resources* -> Upgrade hardware or use more powerful machine

## Interface Issues

### Gradio Startup Problems

**Symptoms:** Application starts but web interface doesn't open, port conflicts, Gradio errors.

**Diagnosis steps:**
1. Check if port 7860 is already in use: `netstat -an | grep 7860`
2. Verify Gradio installed correctly: `pip show gradio`
3. Check firewall settings for localhost access
4. Look for error messages in terminal output
5. Test with different port: modify `launch()` in app.py

**Common causes and resolutions:**
- *Port already in use* -> Kill process on port 7860 or change port in app.py
- *Gradio not installed* -> Run `pip install gradio`
- *Firewall blocking localhost* -> Add exception for localhost:7860
- *Browser cache issues* -> Clear cache or try different browser
- *JavaScript errors* -> Check browser console, clear cache
- *Firewall blocking* -> Check firewall settings
- *Network issues* -> Check network connectivity

### File Upload Problems

**Symptoms:** Can't upload CSV files, upload errors.

**Diagnosis steps:**
1. Check file size limits
2. Verify file format is CSV
3. Check file permissions
4. Test with different files
5. Check browser console for errors

**Common causes and resolutions:**
- *File too large* -> Split into smaller files or optimize processing
- *Wrong format* -> Ensure file is proper CSV format
- *Browser restrictions* -> Try different browser or check settings
- *Path issues* -> Use simple file paths, avoid special characters

## Data Issues

### Incorrect Attendance Calculations

**Symptoms:** Attendance percentages seem wrong, inconsistent results.

**Diagnosis steps:**
1. Verify data cleaning logic
2. Check date/time processing
3. Validate present/absent counting
4. Test with known-good data
5. Review calculation formulas

**Common causes and resolutions:**
- *Data cleaning errors* -> Review data processing logic
- *Date format issues* -> Verify datetime parsing
- *Counting logic errors* -> Check attendance calculation code
- *Filtering problems* -> Review data filtering logic
- *Edge cases* -> Handle special cases in data

### Placement Pattern Matching Issues

**Symptoms:** Placement patterns not recognized, wrong categorization.

**Diagnosis steps:**
1. Check regex pattern definitions
2. Verify placement data format
3. Test pattern matching with sample data
4. Review pattern matching logic
5. Check case sensitivity and special characters

**Common causes and resolutions:**
- *Incorrect regex* -> Update PLACEMENT_PATTERNS regex
- *Data format changes* -> Update pattern matching logic
- *Case sensitivity* -> Normalize case before matching
- *Special characters* -> Handle special characters in patterns
- *Missing patterns* -> Add new pattern definitions

## Development Issues

### Package Installation Failures

**Symptoms:** pip install fails, dependency conflicts.

**Diagnosis steps:**
1. Check Python version compatibility
2. Verify package names and versions
3. Check for conflicting packages
4. Try clean virtual environment
5. Review error messages carefully

**Common causes and resolutions:**
- *Version conflicts* -> Use compatible package versions
- *Missing build tools* -> Install required build tools
- *Network issues* -> Check internet connection, try different index
- *Permissions* -> Use administrator privileges or virtual environment
- *Corrupted cache* -> Clear pip cache, try again

### Code Testing Issues

**Symptoms:** Tests fail, unexpected behavior during testing.

**Diagnosis steps:**
1. Review test data and setup
2. Check test environment configuration
3. Verify test logic matches requirements
4. Test with different data scenarios
5. Review error messages and logs

**Common causes and resolutions:**
- *Test data issues* -> Update test data to match expected format
- *Environment differences* -> Match test environment to production
- *Logic errors* -> Review and fix test logic
- *Missing dependencies* -> Install test-specific dependencies
- *Timing issues* -> Add proper waits and synchronization
