# Data Model

## Overview

The LU Medical School Attendance Tracker uses a file-based data model with CSV files as the primary data source, imported from the ITPI attendance dashboard. Data is processed in-memory using Pandas DataFrames for analysis and visualization.

- **Data source:** CSV files imported from ITPI attendance dashboard
- **Processing:** Pandas DataFrames for in-memory data manipulation
- **Storage:** Local file system with no persistent database
- **Data refresh:** Manual CSV file updates from ITPI system

## Data Sources Structure

The system processes multiple CSV files containing attendance and placement data for different academic years.

- **Attendance data files:** lusi_mbchb101.csv, lusi_mbchb201.csv, lusi_mbchb301.csv, lusi_mbchb401.csv, lusi_mbchb501.csv
- **Rotation mapping files:** y2r1.csv, y3r1.csv, y4r1.csv, y5r1.csv
- **Student notes file:** Book1.xlsx (optional, contains notes and email addresses)
- **Data relationships:** Attendance records linked to placement information via student ID

## Core Data Entities

### Attendance Records

- **studentId:** Unique student identifier (string)
- **firstName:** Student first name (string)
- **surname:** Student surname (string)
- **academicAdvisor:** Assigned academic advisor (string)
- **startDateTime:** Attendance session timestamp (ISO datetime format)
- **present:** Boolean attendance status (true/false)
- **selfCertInfo:** Self-certification information (optional string)
- **cancelled:** Cancellation status (boolean, excluded from calculations)
- **Module/Year information:** Derived from filename (MBCHB101-501)

### Placement Data

- **Student ID:** Mapping to rotation placements (links to attendance records)
- **Year-specific placement information:** Y2R1, Y3R1, Y4R1, Y5R1 files contain rotation mappings
- **Placement types:** Identified via regex pattern matching (MED.PLAC, MED.OTHR, Palliative Care)
- **Rotation scheduling information:** Group, Pattern, Rotation columns in mapping files

### Student Notes

- **Source:** Book1.xlsx Excel file (Sheet1)
- **studentId:** Reference to student (from 'Student ID' column)
- **studentEmail:** Student contact information (from 'Email' column)
- **notes:** Combined notes from 'Notes 1' and 'Notes 2' columns, concatenated with comma separator
- **Optional file:** If not provided, notes will be empty but app still works

## Data Processing Pipeline

- CSV file loading and validation using Pandas read_csv
- Data cleaning and standardization (date parsing, type conversion, missing value handling)
- Date/time processing for attendance analysis (timezone removal, date range filtering)
- Placement pattern matching using regex for MED.PLAC, MED.OTHR, Palliative Care identification
- In-memory data aggregation and calculations for reporting (attendance percentages, summaries)

## Data Access Patterns

- File-based data loading via Pandas read_csv with UTF-8 encoding
- In-memory filtering and aggregation using Pandas DataFrame operations
- Date range queries for trend analysis using Pandas date filtering
- Placement pattern matching for attendance context using regex
- Student-specific data retrieval and analysis by studentId
