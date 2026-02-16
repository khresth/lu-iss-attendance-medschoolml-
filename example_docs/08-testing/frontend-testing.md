# Frontend Testing Guide

## Overview

How to write and run tests for the LU Medical School Attendance Tracker frontend (Gradio interface).

## Running Tests

Since this is a Gradio-based application, testing is primarily manual:

```bash
# Start the application for testing
python app.py

# Test with different browsers if needed
# Access http://localhost:7860 in browser

# Manual testing of all features
# Test file upload, data processing, chart generation
```

## Writing Tests

### Test Data Preparation

- Create sample CSV files for testing different scenarios
- Test data with various data quality issues (missing values, bad formats)
- Prepare edge case data (empty files, large datasets 5000+ rows)
- Create test data for different academic years (Y1-Y5)
- Document test data requirements in test_data/README.md

### Interface Testing

- Test Gradio component functionality (file upload, dropdowns, buttons)
- Verify file upload handling (CSV, Excel formats)
- Test chart generation and display (Plotly charts render correctly)
- Test user interface responsiveness (window resizing)
- Test error handling and user feedback (clear error messages)

### Data Processing Tests

- Test data loading functions with various inputs
- Validate data cleaning logic (date parsing, type conversion)
- Test attendance calculations against expected values
- Verify placement pattern matching with test descriptions
- Test error handling with invalid/missing data

### Testing Hooks

Not applicable for Gradio application - no React hooks or custom hooks to test.
All state is managed through Gradio's internal state management and function returns.

### Testing Data Hooks

Not applicable - this application uses direct function calls, not data hooks.
Data is passed directly from Gradio inputs to processing functions via the `inputs` parameter.
- Mocking API responses with API mocking library or manual mocks
- Testing query hooks (loading, success, error states)
- Testing mutation hooks (optimistic updates, error handling)
- Testing cache invalidation

## Mocking

Not applicable for this Gradio application - no API calls to mock, no navigation, no state management stores.
All functionality is local with direct function calls.

## Accessibility Testing

- Test keyboard navigation through Gradio interface (Tab, Enter, Space)
- Verify form labels are descriptive and clear
- Check color contrast of charts and text (Gradio defaults are generally good)
- Test with browser zoom (Ctrl +/-) to ensure readability
- Gradio provides basic accessibility - no automated a11y checks needed

## Common Pitfalls

- Not testing with real CSV data files (always test with actual data)
- Testing only happy path - missing error handling verification
- Not waiting for data processing to complete before checking results
- Testing on only one browser (test on at least Chrome and Firefox)
- Not cleaning up test data files after testing (delete temporary test files)
