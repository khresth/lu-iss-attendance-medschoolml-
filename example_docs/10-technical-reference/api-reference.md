# API Reference

## Overview

The LU Medical School Attendance Tracker is a local Gradio application and does not expose a REST API. All functionality is accessed through the Gradio web interface at http://localhost:7860.

## Application Interface

### Access URL

| Environment | URL |
|------------|----------|
| Local | `http://localhost:7860` |

### Interface Components

- File upload components for CSV and Excel files
- Dropdown selectors for modules, dates, and thresholds
- Interactive charts using Plotly
- Data tables displayed as HTML
- Text inputs for student search

## Data Processing Functions

### Core Functions

| Function | Purpose | Location |
|----------|---------|----------|
| `load_and_clean_data()` | Load and validate attendance CSV files | `app.py` |
| `load_y5_rotation_data()` | Load Year 5 rotation mapping | `app.py` |
| `load_y3_rotation_data()` | Load Year 3 rotation mapping | `app.py` |
| `load_y4_rotation_data()` | Load Year 4 rotation mapping | `app.py` |
| `load_y2_rotation_data()` | Load Year 2 rotation mapping | `app.py` |
| `load_notes()` | Load student notes from Excel | `app.py` |
| `analyze_attendance()` | Main attendance analysis logic | `app.py` |
| `plot_student_attendance()` | Generate student attendance charts | `app.py` |
| `macro_attendance()` | Macro view of placement attendance | `app.py` |

## Error Handling

### Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| "File not provided" | Missing CSV file | Upload required data file |
| "Missing required columns" | Invalid CSV format | Check CSV has required columns |
| "Error loading file" | File corruption or encoding | Re-export from ITPI dashboard |
| "No data" | Empty date range or filters | Adjust date range or filters |

## No External API

**Important:** This application does not expose any external API endpoints. It is designed as a standalone local tool with no network-facing interfaces beyond the Gradio web UI.
