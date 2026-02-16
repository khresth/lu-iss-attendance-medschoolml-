# Application Testing Guide

## Overview

How to write and run tests for LU Medical School Attendance Tracker.

## Test Approach

Since this is a single-file Python application, testing focuses on:

| Test Type | What It Tests | Approach |
|------------|--------------|---------|
| Manual Testing | Application functionality, data processing, UI interaction | Direct testing with sample data |
| Data Validation | CSV file handling, data cleaning logic | Test with various file formats |
| Performance Testing | Processing speed, memory usage, chart rendering | Test with different dataset sizes |

## Running Tests

### Manual Testing Process

```bash
# Start the application
python app.py

# Test with sample data
# Upload various CSV files
# Verify charts and statistics
# Test edge cases and error handling
```

### Data Validation Testing

```bash
# Test with different CSV formats
python -c "
import pandas as pd
# Test data loading function
df = pd.read_csv('test_file.csv')
# Validate required columns
required_cols = ['studentId', 'firstName', 'surname', 'academicAdvisor', 'startDateTime']
missing_cols = [col for col in required_cols if col not in df.columns]
print(f'Missing columns: {missing_cols}')
"
```

## Writing Tests

### Test Data Preparation

- Create sample CSV files for testing with known data
- Test data with various scenarios:
  - Valid complete data with all required columns
  - Missing required columns (should fail gracefully)
  - Invalid date formats (should handle errors)
  - Duplicate records (should be handled)
  - Large datasets (performance testing)
  - Empty files (edge case)
- Keep test files in test_data/ directory

### Data Processing Tests

- Test data loading functions with various file formats
- Validate data cleaning logic (date parsing, type conversion)
- Test attendance calculations against known values
- Verify placement pattern matching with test descriptions
- Test error handling and recovery for bad data

### User Interface Tests

- Test Gradio interface loads without errors
- Verify file upload functionality works
- Test chart generation and display
- Test interactive elements (dropdowns, buttons, sliders)
- Verify responsive behavior at different window sizes

### Performance Tests

- Measure application startup time (should be < 5 seconds)
- Test data processing speed with various file sizes
- Monitor memory usage during processing
- Test chart rendering performance
- Test with large datasets (5000+ rows)

## Test Scenarios

### Happy Path Testing

- Load valid CSV files successfully
- Generate attendance charts
- Test data filtering by date range
- Verify attendance calculations
- Test placement mapping accuracy

### Error Handling Tests

- Test with missing files - should show clear error
- Test with invalid CSV formats - should handle gracefully
- Test with corrupted data - should not crash
- Test memory constraints with very large files
- Test network issues (if applicable)

### Edge Case Testing

- Empty datasets - should show "No data" message
- Single record datasets - should display correctly
- Very large datasets - should process without crashing
- Special characters in data (accents, apostrophes)
- Boundary values (100% attendance, 0% attendance)

## Test Documentation

### Test Case Documentation

- Document test scenarios with expected results
- Record actual test outcomes and any issues found
- Maintain inventory of test data files used
- Document test environment setup
- Keep test results for regression comparison

### Regression Testing

- Test existing functionality after any code changes
- Verify performance doesn't degrade with new versions
- Test with historical data to ensure consistency
- Validate backward compatibility for data formats
- Test complete user workflows after changes

## Test Environment Setup

### Test Data Management

- Organize test CSV files by scenario in test_data/ folder
- Name files descriptively: test_valid.csv, test_missing_cols.csv
- Clean up temporary test data after testing
- Document test data requirements
- Keep backup of important test datasets

### Test Configuration

- Use consistent test environment (Python version, packages)
- Document test Python version in README
- Specify required package versions in requirements.txt
- Test on different operating systems if possible
- Configure test logging for debugging

## Quality Assurance

### Test Review Process

- Review test coverage of all major functionality
- Verify test results accuracy against expected outcomes
- Document any test limitations or gaps
- Identify areas needing additional testing
- Plan test improvements for next iteration

### User Acceptance Testing

- Test with actual medical school staff users
- Use real ITPI dashboard data (anonymized if sharing)
- Test in actual usage environment (user's workstation)
- Collect user feedback on interface and functionality
- Document user experience issues for improvement

## Test Automation

### Simple Test Scripts

```python
# test_data_loading.py
import sys
sys.path.append('.')
from app import load_and_clean_data

def test_data_loading():
    # Test with various file scenarios
    test_files = [
        'test_valid.csv',
        'test_missing_columns.csv',
        'test_invalid_format.csv',
        'test_empty.csv'
    ]
    
    for file in test_files:
        print(f"Testing {file}...")
        df, dates, message = load_and_clean_data('test', file)
        print(f"Result: {message}")
        assert df is not None or 'Error' in message

if __name__ == '__main__':
    test_data_loading()
```

### Batch Testing

- Create test scripts for common scenarios
- Automate repetitive testing tasks where possible
- Generate test reports documenting results
- Schedule regular test runs before releases
- Monitor test results over time for trends
