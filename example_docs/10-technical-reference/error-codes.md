# Error Handling Reference

## Overview

Error handling in the LU Medical School Attendance Tracker is implemented through user-friendly messages displayed in the Gradio interface. Since this is a local application without an API, errors are shown directly to users in the web interface.

## Error Display Format

Errors are displayed as text messages in the Gradio interface:

- Status text boxes show loading and processing messages
- Error messages appear in the interface where the issue occurred
- No error codes - plain English descriptions

## Common Error Messages

### File Loading Errors

| Message | Cause | Resolution |
|---------|-------|------------|
| "File for [module] not provided." | Missing file upload | Upload the required CSV file |
| "File for [module] not found." | File path issue | Check file exists and is readable |
| "Error loading file: [details]" | File corruption or format issue | Re-export from ITPI dashboard |
| "Missing 'studentId' column." | Invalid CSV format | Ensure CSV has correct column headers |
| "Missing 'startDateTime' column." | Invalid CSV format | Ensure CSV has correct column headers |
| "Missing required columns." | CSV missing required fields | Check CSV has all required columns |
| "No valid data after cleaning." | All data filtered out | Check data quality and filters |

### Data Processing Errors

| Message | Cause | Resolution |
|---------|-------|------------|
| "Module data not loaded." | Data not uploaded | Upload module CSV file first |
| "Rotation data not loaded." | Rotation file missing | Upload rotation mapping file |
| "No events in selected date range." | Date filter too narrow | Expand date range |
| "Invalid date format." | Date parsing failed | Check CSV date format |
| "Please select a module and valid date range." | Missing selection | Select module and dates |
| "No placement data." | No placement events found | Check placement pattern matching |

### Analysis Errors

| Message | Cause | Resolution |
|---------|-------|------------|
| "Select a student first." | No student selected | Select student from dropdown |
| "Invalid student selection." | Student ID parsing failed | Try reselecting student |
| "No data for student [id]." | Student not in dataset | Check student ID and data |
| "Module not loaded." | Data not available | Load module data first |
| "Graph not available for rotation data." | Feature limitation | Use attendance data for graphs |

### Notes File Errors

| Message | Cause | Resolution |
|---------|-------|------------|
| "Book1.xlsx not uploaded - notes will be empty." | Optional file missing | Upload Book1.xlsx for notes |
| "Error loading Book1.xlsx: [details]" | Excel file issue | Check file format and encoding |

## Troubleshooting Guide

### When Errors Occur

1. Check the error message in the interface
2. Verify data files are properly formatted
3. Ensure all required files are uploaded
4. Check file permissions and encoding (UTF-8)
5. Restart the application if issues persist

### Prevention

- Always export fresh data from ITPI dashboard
- Verify CSV files open correctly in spreadsheet software
- Use consistent file naming conventions
- Keep backup copies of working data files
