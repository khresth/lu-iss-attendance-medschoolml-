# Testing Strategy

## Overview

Describe overall testing philosophy for LU Medical School Attendance Tracker, what we test, and how different test types work together.

## Testing Philosophy

- Manual testing approach for single-file application
- Focus on data processing accuracy and user interface functionality
- Emphasis on real-world usage scenarios
- Testing with actual ITPI dashboard data
- Performance testing with various dataset sizes

## Testing Approach

### Manual Testing Focus

- Functional testing of all features
- Data validation with various CSV formats
- User interface testing across different browsers
- Performance testing with realistic dataset sizes
- Error handling and recovery testing

### Testing Environment

- Local testing environment matching user setup
- Test data management and organization
- Consistent Python and package versions
- Browser compatibility testing
- Performance baseline establishment

## Test Types

### Manual Functional Testing

- Application startup and initialization
- CSV file loading and processing
- Data cleaning and validation
- Chart generation and display
- User interface interactions
- Error handling and user feedback
- All testing is manual - no automated test frameworks

### Integration Tests

- What they test: How data flows through the application
- Components: File loading → Data cleaning → Analysis → Display
- Manual verification that components work together correctly
- Testing with real CSV files in the application
- Focus on data accuracy through the full workflow

### End-to-End Tests

- What they test: full user journeys through the running application
- Approach: Manual testing through the Gradio interface
- Test environment: Local Python application on localhost:7860
- Speed expectation: Varies by dataset size (5-30 seconds per workflow)
- Focus on: Critical user paths, regression prevention, data accuracy

## What to Test

- Business logic: Data processing accuracy, attendance calculations
- Data loading: CSV file handling, validation, cleaning
- UI functionality: File uploads, chart generation, filtering
- Error handling: Graceful failure, clear error messages
- Performance: Response time with various dataset sizes

## What NOT to Test

- Framework internals (Pandas operations, Gradio components)
- Third-party library behaviour (Plotly rendering)
- Simple data transformations
- Python standard library functions
- Trivial getters/setters

## Test Data Management

- Create sample CSV files with known data
- Maintain test data inventory with different scenarios
- Use small datasets for quick testing
- Include edge cases: empty files, single records, special characters
- No sensitive student data in test files - use anonymized data

## CI/CD Integration

- This is a local application with no CI/CD pipeline
- Testing is done manually before distributing updates
- Version control via Git tracks changes
- Manual deployment after testing verification
- No automated test execution required
