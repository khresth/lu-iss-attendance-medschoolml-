# User Guide

## Overview

End-user documentation for the LU Medical School Attendance Tracker. Written for medical school staff who need to analyze student attendance patterns and placement tracking.

## Getting Started

### Accessing the Application

- Launch the application by running `python app.py` on your local machine
- Application opens in web browser (typically http://localhost:7860)
- No login required - local application access
- Ensure CSV data files are in place before starting

### Preparing Your Data

- Export attendance data from ITPI dashboard in CSV format
- Place CSV files in the same directory as app.py
- Required files: lusi_mbchb101.csv, lusi_mbchb201.csv, lusi_mbchb301.csv, lusi_mbchb401.csv, lusi_mbchb501.csv
- Optional placement files: y2r1.csv, y3r1.csv, y4r1.csv, y5r1.csv
- Optional notes file: Book1.xlsx

### Navigating the Interface

- Main dashboard with file upload area at the top
- Module selection and date range controls
- Analysis parameters (thresholds, sorting options)
- Tabbed output display with four views:
  - **Attendance Summary**: Students below threshold
  - **Student Details**: Individual student charts
  - **Placement Analysis**: Medical placement attendance
  - **Attendance Macro**: Recent placement activity

## Features

### Attendance Data Upload

1. Click "Load / Refresh Data" button after uploading files
2. Upload attendance CSV files through the file interface
3. Supported format: CSV with UTF-8 encoding
4. Required columns: studentId, firstName, surname, academicAdvisor, startDateTime
5. Optional columns: present, selfCertInfo, cancelled
6. Automatic data validation and cleaning occurs on load

### Attendance Percentage Tracking

- View students with attendance below selected threshold
- Filter by specific date ranges using dropdown selectors
- Sort results by attendance percentage or surname
- See overall attendance statistics for selected module
- Compare attendance across different time periods
- Export data by copying from HTML tables

### Placement Monitoring

- Track student placement attendance patterns
- Automatic identification using pattern matching (MED.PLAC, MED.OTHR, Palliative Care)
- View placement days attended by week
- Filter by group/rotation and placement pattern
- Correlate placement data with attendance data
- Identify students with low placement attendance

### Trend Visualization

- Interactive charts using Plotly
- Individual student attendance trends over time
- Cumulative attendance percentage graphs
- Compare student against class average
- Click and drag to zoom on charts
- Save charts as images using the camera icon

### Student Notes Management

- Upload Book1.xlsx file with student notes (optional)
- Notes 1 and Notes 2 fields are concatenated for display
- Student email addresses shown when available
- Notes appear in attendance and placement reports
- Helps track student-specific observations and context

## Data Analysis

### Understanding Attendance Metrics

- **Attendance %**: (Present sessions / Total sessions) × 100
- **Present**: Student marked as attending the session
- **Self-certification**: Flagged absence with student-provided reason
- **Cancelled**: Sessions excluded from calculations
- Use threshold filter to identify at-risk students
- Trend analysis shows attendance patterns over time

### Placement Pattern Analysis

- **MED.PLAC**: Automatic medical placement check-ins
- **MED.OTHR**: Manual medical placement entries
- **Palliative Care**: Palliative care placement sessions
- Patterns identified using regex matching on event descriptions
- Placement attendance tracked separately from teaching sessions
- Weekly breakdown shows days attended per placement

## Tips for Best Results

- Ensure CSV files are properly formatted before upload (UTF-8 encoding)
- Use consistent file naming: lusi_mbchb[year][semester].csv
- Regularly update data from ITPI dashboard for current insights
- Use date range filters to focus on specific teaching periods
- Combine attendance and placement data for comprehensive analysis
- Check "Show only self-certified absences" to identify unexplained absences
- Use "Also sort by surname" for alphabetical student lists

## Troubleshooting

| Problem | Solution |
|---------|----------|
| File upload failing | Check CSV format is UTF-8, verify required columns |
| Charts not displaying | Verify Plotly installation: `pip install plotly` |
| Data loading errors | Check required columns exist, re-export from ITPI |
| Application won't start | Verify Python and dependencies: `pip install -r requirements.txt` |
| Performance issues | Use smaller date ranges, close other applications |
| Port already in use | Stop other applications using port 7860 |

**Reporting Issues:** Contact medical school IT department with error messages and steps to reproduce.
