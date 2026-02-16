# System Overview

## Purpose

The LU Medical School Attendance Tracker is a data analysis and visualization tool designed to help medical school staff monitor and analyze student attendance patterns across different academic years and rotation placements.

- **Product mission:** Provide medical school staff with comprehensive attendance analytics and placement tracking capabilities
- **Target user groups:** Medical school staff, academic advisors, administrators
- **High-level capabilities:** Attendance percentage tracking, placement monitoring, trend visualization over time
- **Current phase:** Operational attendance tracking system with data import from ITPI dashboard

## System Context Diagram

Include a C4 Level 1 (System Context) diagram showing LU Medical School Attendance Tracker and its external dependencies.

- **System boundary:** The application runs locally on user workstations
- **External actors:** Medical School Staff, Academic Advisors, System Administrators
- **External systems:** ITPI Attendance Dashboard (data source), Local File System (CSV storage)
- **Data flow:** Staff export data from ITPI → Load into application → Analyze locally → View results

## High-Level Architecture Diagram

Include a C4 Level 2 (Container) diagram showing the major components.

- **Gradio Web Interface** (user interaction layer)
- **Data Processing Engine** (Pandas-based data manipulation)
- **Visualization Engine** (Plotly-based charting)
- **CSV Data Sources** (attendance and placement data)
- **Local File System** (data storage)
- **Single-process data flow:** File upload → Data cleaning → Analysis → Display

## Technology Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | Gradio web interface, Plotly for data visualization |
| Backend | Python 3.x, Pandas for data processing, Plotly for charts |
| Database | CSV files (imported from ITPI dashboard) |
| Infrastructure | Localhost deployment, Python environment required |
| Auth | None (local application access) |

## Key Architectural Decisions

**Decisions documented:**
- Choice of Gradio for rapid web interface development
- Use of CSV files as primary data source from ITPI dashboard
- Pandas for data manipulation and analysis
- Plotly for interactive data visualization
- Local deployment model for medical school internal use
- No authentication layer (local application access)

## Non-Functional Requirements

- **Performance targets:** Responsive UI for datasets up to 10,000 records (charts render in <5 seconds)
- **Availability targets:** Local application availability during working hours (9am-5pm, weekdays)
- **Scalability approach:** Memory-based processing suitable for medical school scale (50-500 students per year)
- **Security requirements:** Local file system access only, no external data transmission
- **Data retention policies:** As per ITPI dashboard data retention (managed by source system)
- **Accessibility standards:** Basic web accessibility through Gradio interface (keyboard navigation, screen reader compatible)
