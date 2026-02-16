# End-to-End Testing Guide

## Overview

How to write and run E2E tests that exercise the full LU Medical School Attendance Tracker application stack.

## Prerequisites

- Python application running locally
- Web browser for interface testing (Chrome, Firefox, Edge, Safari)
- Test CSV files prepared with various scenarios
- Test environment matching user setup (same OS, Python version)
- Manual testing procedures documented

## Running E2E Tests

Since this is a local application, E2E testing is primarily manual:

```bash
# Manual E2E testing workflow
# 1. Start application: python app.py
# 2. Open browser: http://localhost:7860
# 3. Execute test scenarios manually
# 4. Document results and issues

# For automated browser testing (if implemented)
# Install Playwright: npx playwright install
# Run tests: npx playwright test
```

## Test Scenarios

### Complete User Workflow Testing

1. Test complete attendance analysis workflow:
   - Load CSV data → Process data → Generate charts → Analyze results
2. Test with different academic years (Y1-Y5) and data sources
3. Verify placement mapping and pattern matching accuracy
4. Test data export by copying from HTML tables
5. Verify error handling displays clear messages

### Data Quality Testing

- Test with various CSV file formats (different years, semesters)
- Test data cleaning and validation processes
- Test error handling for malformed data (missing columns, bad formats)
- Test with edge cases: missing data, duplicate records, invalid dates
- Verify attendance calculation accuracy against manual calculations

### User Interface Testing

- Test file upload functionality with different file types
- Test chart generation and interactive features
- Test data filtering and selection capabilities
- Test user interface responsiveness and usability
- Test error messages and user guidance

### Performance Testing

- Test with large datasets to verify performance
- Test memory usage during data processing
- Test chart rendering speed with complex data
- Test application startup and shutdown times
- Verify system resource utilization

## Test Architecture

### Manual Test Procedures

- Step-by-step test procedures for each scenario
- Test data preparation and setup
- Expected results and verification steps
- Test result documentation and reporting
- Issue identification and troubleshooting

### Browser Testing

- Test interface in different browsers (Chrome, Firefox, Safari, Edge)
- Verify Gradio compatibility across browsers
- Test responsive design on different screen sizes
- Test JavaScript functionality and chart rendering
- Verify accessibility features

## Test Documentation

### Test Case Documentation

- Document complete test scenarios and procedures
- Record test results, issues, and resolutions
- Maintain test data inventory and versions
- Create test checklists and verification procedures
- Document test environment requirements

### Regression Testing

- Test existing functionality after application changes
- Verify performance doesn't degrade with new versions
- Test with historical data and edge cases
- Validate backward compatibility for data formats
- Test complete user workflows after changes

## Test Automation (Optional)

### Simple Test Automation

```python
# e2e_test_scenarios.py
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_attendance_workflow():
    # Automated test for complete workflow
    driver = webdriver.Chrome()
    try:
        driver.get('http://localhost:7860')
        # Add automated interactions here
        time.sleep(2)
    finally:
        driver.quit()

if __name__ == '__main__':
    test_attendance_workflow()
```

### Test Reporting

- Generate test execution reports
- Document test coverage and results
- Track performance metrics during testing
- Create issue reports for bugs found
- Maintain test history and trends

## Debugging E2E Tests

- Check browser console for JavaScript errors
- Verify application is running on correct port
- Check element locators are correct
- Take screenshots on failure for debugging
- Review application logs in terminal
