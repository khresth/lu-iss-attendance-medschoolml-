# Configuration Reference

## Overview

The LU Medical School Attendance Tracker is a simple local Python application with minimal configuration requirements. Most settings are handled through file locations and Gradio's default behavior.

## Application Configuration

### File Paths

| Setting | Description | Default | Notes |
|---------|-------------|---------|-------|
| CSV Data Files | Location of attendance data | Same directory as app.py | Files: lusi_mbchb*.csv |
| Rotation Files | Location of placement mapping | Same directory as app.py | Files: y*r1.csv |
| Notes File | Student notes Excel file | Same directory as app.py | Book1.xlsx (optional) |

### Gradio Configuration

| Setting | Description | Default | Notes |
|---------|-------------|---------|-------|
| Port | Web interface port | 7860 | Auto-selected if in use |
| Host | Interface binding | 127.0.0.1 | Localhost only |
| Share | Public URL sharing | False | Keep disabled for data privacy |

## Python Dependencies

### Required Packages

| Package | Purpose | Version |
|---------|---------|---------|
| gradio | Web interface framework | Latest |
| pandas | Data processing | Latest |
| plotly | Data visualization | Latest |
| openpyxl | Excel file reading | Latest |

## Environment Variables

The application does not require environment variables for basic operation. All configuration is through:
- File locations in the application directory
- User inputs through the Gradio interface
- Default Gradio and Pandas behaviors

## Data File Format Requirements

### Attendance CSV Files (lusi_mbchb*.csv)

| Column | Required | Description |
|--------|----------|-------------|
| studentId | Yes | Unique student identifier |
| firstName | Yes | Student first name |
| surname | Yes | Student surname |
| academicAdvisor | Yes | Assigned advisor name |
| startDateTime | Yes | Session timestamp (ISO format) |
| present | No | Attendance status (true/false) |
| selfCertInfo | No | Self-certification flag |
| cancelled | No | Cancellation status |

### Rotation Mapping Files (y*r1.csv)

| Column | Required | Description |
|--------|----------|-------------|
| Student ID | Yes | Student identifier |
| Group | No | Rotation group number |
| Pattern | No | Placement pattern code |
| Rotation 1 | No | Rotation name (Y5) |

### Student Notes File (Book1.xlsx)

| Column | Required | Description |
|--------|----------|-------------|
| Student ID | Yes | Student identifier |
| Email | No | Student email address |
| Notes 1 | No | First notes field |
| Notes 2 | No | Second notes field |
