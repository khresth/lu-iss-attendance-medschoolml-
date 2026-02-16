# Authentication & Authorisation Overview

## Overview

The LU Medical School Attendance Tracker uses a simplified authentication model appropriate for a local application.

- No authentication required for local application access
- Local machine access control provides security boundary
- No external identity providers needed
- No user accounts or session management
- Access controlled through local file permissions

## Access Control Model

### Local Application Access

- Application runs on localhost only
- Access controlled by operating system user permissions
- No network-facing authentication required
- Physical access to machine provides application access

### Data Access Control

- CSV file access controlled by file system permissions
- Student data protected through local file security
- No external data transmission
- Data privacy maintained through local deployment

## Security Architecture

### Application Security

- No external attack surface
- Localhost-only access (127.0.0.1)
- No authentication bypass vulnerabilities
- Secure coding practices for data handling

### Data Protection

- Student data never leaves local machine
- No external API calls or data transmission
- CSV files stored locally with appropriate permissions
- No database or external storage services

## User Management

### No User Accounts

- No user registration or login required
- No user profiles or preferences stored
- No session management needed
- No password management

### Access Control

- Access controlled through local machine security
- File permissions control data access
- No role-based access control needed
- Administrative access through OS-level permissions

## Compliance Considerations

### Data Privacy

- Student data remains on local machines
- No external data processing or storage
- Compliance with local data protection regulations
- No third-party data sharing

### Audit Trail

- No user activity logging required
- File system access logging available through OS
- Application usage tracked at local level
- No central audit trail needed

## Security Best Practices

### Local Security

- Ensure proper file permissions on CSV data
- Regular security updates for operating system
- Secure Python environment configuration
- Backup procedures for data protection

### Development Security

- Secure coding practices for data handling
- Input validation for CSV file processing
- Error handling that doesn't expose sensitive information
- Regular code reviews for security issues
