# Cloud Resources

## Overview

Document all cloud resources used by the LU Medical School Attendance Tracker.

## Resource Architecture

Since this is a local application, cloud resources are minimal:

- No cloud infrastructure required
- Local file system storage
- Local Python runtime environment
- Optional Git repository hosting (GitHub/GitLab)
- No external service dependencies

## Local Resources

### Compute Resources

- Local machine Python runtime
- Gradio web server (localhost)
- In-memory data processing with Pandas
- No external compute services required

### Data Storage

- Local CSV file storage
- File system-based data persistence
- No database services required
- Local backup procedures

## Optional External Resources

### Git Repository Hosting

- Optional GitHub/GitLab repository
- Source code version control
- Collaboration platform
- Issue tracking and documentation

### Python Package Repository

- PyPI for package dependencies
- Requirements.txt for dependency management
- Virtual environment for isolation
- Package version pinning

## Resource Requirements

### System Requirements

- Python 3.8+ runtime environment
- Minimum 4GB RAM recommended for processing large datasets
- Disk space for CSV data files (approximately 50 MB per year)
- Modern web browser for Gradio interface (Chrome, Firefox, Edge, Safari)

### Network Requirements

- Internet access required for initial package installation via pip
- Localhost access (127.0.0.1) for running Gradio application
- No external network dependencies required for day-to-day operation
- Optional internet access for Git repository operations

## Security Considerations

### Data Security

- Local file system permissions control access to CSV data files
- CSV files should be stored in secure location with appropriate access controls
- No external data transmission - all processing happens locally
- Student data privacy maintained through local-only deployment
- Follow medical school data protection policies for handling student records

### Application Security

- No external attack surface - application runs locally only
- Local application access restricted to workstation users
- No authentication layer required (access controlled by operating system)
- Secure coding practices for data handling (input validation, error handling)

## Backup and Recovery

### Code Backup

- Use Git for version control and code backup
- Regular local file backups of the application directory
- Git version control history tracks all code changes
- Remote repository synchronization to GitHub/GitLab for redundancy

### Data Backup

- Regular backup of CSV data files before updates
- Re-export data from ITPI dashboard as needed (source of truth)
- Local backup storage in dated folders (e.g., backup_2024_01_15)
- Recovery procedure: Copy backup files back to application directory

## Infrastructure Management

### Environment Setup

- Python environment configuration via requirements.txt
- Dependency installation: `pip install -r requirements.txt`
- Application deployment: Copy files to target directory
- No complex configuration management needed

### Maintenance

- Keep Python updated to supported version (3.8+)
- Update package dependencies periodically: `pip install --upgrade -r requirements.txt`
- Code maintenance and refactoring as needed for new features
- Performance optimization based on user feedback and dataset sizes
