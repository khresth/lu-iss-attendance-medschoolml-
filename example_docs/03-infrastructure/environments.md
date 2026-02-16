# Environments

## Overview

Document all environments, their purpose, and how they differ.

## Environment Summary

| Environment | Purpose | URL | Deployment | Notes |
|------------|---------|-----|------------|-------|
| Local | Developer workstation | http://localhost:7860 | Manual via python app.py | Single application instance |
| Development | Testing with sample data | localhost:port | Manual deployment | For feature testing |
| Production | Live medical school use | localhost:7860 | Manual deployment | Local machine deployment |

## Local Development Environment

- Single Python application (app.py)
- Gradio web interface on port 7860
- Local file system access for CSV data
- No external services required
- In-memory data processing with Pandas
- No database or external dependencies

## Development Environment

- Local machine with Python 3.8+
- Test CSV files for development
- Debug logging enabled
- Hot reload not applicable (restart application) of app.py
- Debug logging enabled
- Performance monitoring for optimization

## Production Environment

- Real ITPI dashboard CSV data
- Medical school staff workstations
- Optimized for performance with large datasets
- Error handling and logging configured
- Data validation and cleaning
- Local machine deployment for medical school staff

## Environment Differences

### Configuration Differences

- CSV file paths (test vs production data)
- Logging levels (debug vs info)
- Data validation strictness
- Performance optimization settings for production datasets
- Error handling verbosity

### Data Differences

- Test data sets for development
- Production data from ITPI dashboard
- Data refresh frequency
- Backup and retention policies
- Data privacy and security considerations

## Environment Setup

- Same application code works across all environments
- Only data files differ between environments
- Configuration via environment variables or local files
- No external service dependencies to configure

## Deployment Strategy

- Manual deployment via file copy
- Python environment setup
- Dependency management via requirements.txt
- Configuration via environment variables
- Rollback via file restoration
