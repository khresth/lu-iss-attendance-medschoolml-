# Common Development Tasks

## Overview

Quick reference for tasks developers perform regularly with the LU Medical School Attendance Tracker.

## Application Tasks

### Run the Application

```bash
python app.py
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Test Data Processing

- Upload a CSV file through the Gradio interface
- Check that data loads correctly and shows statistics
- Verify that attendance charts generate properly
- Test placement tracking functionality

## Data Management Tasks

### Add New CSV Data Files

1. Export new attendance data from ITPI dashboard
2. Place CSV files in project root directory
3. Restart the application to load new data
4. Verify data loads through the interface

### Validate CSV Format

- Required columns: studentId, firstName, surname, academicAdvisor, startDateTime
- Optional columns: present, selfCertInfo, cancelled
- Date format: ISO datetime format for startDateTime
- Encoding: UTF-8 recommended

### Clean and Process Data

- Use the built-in data cleaning functions in app.py
- Check for missing student IDs or invalid dates
- Verify placement pattern matching works correctly
- Review attendance percentage calculations

## Development Tasks

### Add New Chart Types

1. Modify the chart generation functions in app.py
2. Add new Plotly chart type with appropriate data formatting
3. Connect chart to Gradio interface component
4. Test chart with sample data
5. Verify interactive features work correctly

### Update Placement Patterns

1. Modify PLACEMENT_PATTERNS regex in app.py
2. Test pattern matching with placement data
3. Update UI labels if needed

### Add New Data Filters

1. Add filter parameters to Gradio interface
2. Implement filtering logic in data processing functions
3. Update chart generation to use filtered data
4. Test filter combinations

## Debugging

### Debug Data Loading Issues

- Check CSV file format and encoding
- Verify required columns are present
- Look for data type mismatches
- Check console output for error messages

### Debug Chart Rendering

- Verify Plotly installation and version
- Check data format passed to chart functions
- Look for JavaScript errors in browser console
- Test with smaller datasets first

### Debug Performance Issues

- Check CSV file sizes (large files may be slow)
- Monitor memory usage during data processing
- Consider data sampling for large datasets
- Optimize Pandas operations if needed

## Code Quality

### Format Python Code

```bash
# Using black (if installed)
black app.py

# Using autopep8 (if installed)
autopep8 --in-place --aggressive app.py
```

### Run Type Checking

```bash
# Using mypy (if installed)
mypy app.py
```

### Test Application Functionality

- Test with various CSV file formats
- Verify all chart types render correctly
- Check data aggregation accuracy
- Test edge cases (empty files, missing data)
