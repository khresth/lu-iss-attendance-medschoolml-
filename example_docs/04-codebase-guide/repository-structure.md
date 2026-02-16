# Repository Structure

## Overview

Provide a map of the LU Medical School Attendance Tracker repository so developers can quickly find what they're looking for.

## Top-Level Layout

```
lu-iss-attendance-medschoolml-/
├── app.py                  # Main application entry point
├── requirements.txt        # Python dependencies
├── click-here.bat         # Windows startup script
├── click-here.sh          # Linux/Mac startup script
├── example_docs/          # Documentation
├── lusi_mbchb101.csv      # Year 1 attendance data
├── lusi_mbchb201.csv      # Year 2 attendance data
├── lusi_mbchb301.csv      # Year 3 attendance data
├── lusi_mbchb401.csv      # Year 4 attendance data
├── lusi_mbchb501.csv      # Year 5 attendance data
├── y2r1.csv              # Year 2 rotation mapping
├── y3r1.csv              # Year 3 rotation mapping
├── y4r1.csv              # Year 4 rotation mapping
├── y5r1.csv              # Year 5 rotation mapping
├── Book1.xlsx          # Student notes and email data (optional)
└── README.md             # Project overview
```

- `app.py` - Single main application file containing all functionality
- `requirements.txt` - Python package dependencies
- `example_docs/` - Complete documentation suite
- CSV files - Attendance and placement data from ITPI dashboard
- `Book1.xlsx` - Optional Excel file with student notes and email addresses
- Startup scripts - Easy application launching for different platforms

## Application Structure

### Main Application (app.py)

- Data loading and cleaning functions
- Gradio interface definition
- Chart generation with Plotly
- Placement pattern matching
- Student notes management
- Attendance percentage calculations

### Key Functions in app.py

- `load_and_clean_data()` - CSV file processing and validation
- `parse_pattern_to_days()` - Placement pattern parsing
- Chart generation functions - Various Plotly visualizations
- Gradio interface components - UI elements and layout
- Data filtering and aggregation functions

## Data Files

### Attendance Data Files

- `lusi_mbchb101.csv` - Year 1 MBChB attendance data
- `lusi_mbchb201.csv` - Year 2 MBChB attendance data
- `lusi_mbchb301.csv` - Year 3 MBChB attendance data
- `lusi_mbchb401.csv` - Year 4 MBChB attendance data
- `lusi_mbchb501.csv` - Year 5 MBChB attendance data

### Placement Mapping Files

- `y2r1.csv` - Year 2 rotation placement mapping
- `y3r1.csv` - Year 3 rotation placement mapping
- `y4r1.csv` - Year 4 rotation placement mapping
- `y5r1.csv` - Year 5 rotation placement mapping

### Student Notes File

- `Book1.xlsx` - Optional Excel file containing student notes and email addresses
- Sheet1 contains columns: Student ID, Email, Notes 1, Notes 2
- Notes 1 and Notes 2 are concatenated for display in the application
- If not provided, notes functionality will be empty but the app still works

```
example_docs/
├── 01-architecture/        # System design and architecture
├── 02-authentication/      # Authentication (not applicable)
├── 03-infrastructure/     # Infrastructure and deployment
├── 04-codebase-guide/      # This section
├── 05-getting-started/    # Setup and onboarding
├── 06-live-service/       # Production deployment
├── 07-runbooks/          # Operational procedures
├── 08-testing/           # Testing approaches
├── 09-user-docs/         # End-user documentation
├── 10-technical-reference/ # Technical details
└── README.md             # Documentation overview
```

## Configuration Files

### Python Dependencies

- `requirements.txt` - All required Python packages
- Gradio for web interface
- Pandas for data processing
- Plotly for data visualization
- Standard library modules

### Startup Scripts

- `click-here.bat` - Windows batch file for easy startup
- `click-here.sh` - Linux/Mac shell script for startup
- Both scripts run `python app.py`

## Key Files to Know

**Key files table:**

| File | Purpose |
|------|---------|
| `app.py` | Main application with all functionality |
| `requirements.txt` | Python package dependencies |
| `click-here.bat` | Windows startup script |
| `click-here.sh` | Linux/Mac startup script |
| `lusi_mbchb*.csv` | Attendance data files by year |
| `y*r1.csv` | Placement mapping files |
| `Book1.xlsx` | Student notes and emails (optional) |
| `example_docs/README.md` | Documentation overview |

## Development Workflow

- Single file application - all code in `app.py`
- Documentation in `example_docs/` directory
- Data files in root directory
- No complex build process required
- Direct Python execution for testing
