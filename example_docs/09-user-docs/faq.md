# Frequently Asked Questions

## General

### What is the LU Medical School Attendance Tracker?

The LU Medical School Attendance Tracker is a data analysis tool for medical school staff to monitor and analyze student attendance patterns across different academic years and rotation placements. It provides visualizations and reports based on data exported from the ITPI attendance dashboard.

### Who can use this application?

Medical school staff, academic advisors, and administrators who need to track student attendance. The application runs locally on your machine - no external accounts or authentication required.

### Is there a cost to use this tool?

No - this is an internal tool provided by the medical school IT department at no cost to staff.

## Getting Started

### How do I start the application?

1. Ensure Python 3.8+ is installed
2. Run `pip install -r requirements.txt` to install dependencies
3. Place your CSV data files in the application directory
4. Run `python app.py`
5. Open your browser to http://localhost:7860

### What data files do I need?

**Required:**
- Attendance CSV files: `lusi_mbchb101.csv` through `lusi_mbchb501.csv` (exported from ITPI dashboard)

**Optional:**
- Rotation mapping files: `y2r1.csv`, `y3r1.csv`, `y4r1.csv`, `y5r1.csv`
- Student notes: `Book1.xlsx`

### Where do I get the data files?

Export attendance data from the ITPI dashboard in CSV format. Contact your IT department if you need help accessing the dashboard or exporting data.

## Using the Application

### How do I analyze attendance for a specific module?

1. Upload the relevant CSV file(s)
2. Click "Load / Refresh Data"
3. Select the module from the dropdown
4. Choose date range and threshold
5. Click "Analyze Attendance"

### What is the placement pattern matching?

The application automatically identifies medical placements using pattern matching on event descriptions. It recognizes patterns like "MED.PLAC", "MED.OTHR", and "Palliative Care" to categorize placement attendance separately from regular teaching sessions.

### How are attendance percentages calculated?

Attendance percentage = (Number of present sessions / Total sessions) × 100

Cancelled sessions are excluded from calculations. Self-certified absences can be filtered separately.

### Can I export the charts and data?

Plotly charts can be saved as images using the camera icon in the top right of each chart. Data tables can be copied from the HTML output.

## Troubleshooting

### The application won't start

- Check Python is installed and in your PATH
- Run `pip install -r requirements.txt` to ensure all dependencies are installed
- Check if port 7860 is already in use
- Look for error messages in the terminal

### CSV files won't load

- Verify files are in the same directory as app.py
- Check file encoding is UTF-8
- Ensure required columns are present: studentId, firstName, surname, academicAdvisor, startDateTime
- Try re-exporting from ITPI dashboard

### Charts are not displaying

- Verify Plotly is installed: `pip install plotly`
- Check browser console for JavaScript errors
- Try a different web browser
- Ensure data loaded successfully first

### The interface is slow

- Large datasets may take time to process
- Try filtering to a smaller date range
- Close other applications to free up memory
- Consider using a more powerful machine for very large datasets

## Data & Privacy

### Is student data secure?

Yes - all data processing happens locally on your machine. No data is transmitted to external servers or cloud services. Keep your workstation secure and follow medical school data protection policies.

### Can I share the application with colleagues?

Yes - share the app.py file and documentation. Each user needs their own copy of the data files (or shared files if on a network drive). Do not share student data files outside authorized personnel.

### How often should I update the data?

Update frequency depends on your needs:
- Weekly: For regular attendance monitoring
- Monthly: For periodic reviews
- Termly: For end-of-term reporting

Always use the latest data from ITPI dashboard for accurate analysis.

## Support

### Who do I contact for help?

- **Technical issues**: Medical school IT department
- **Data access**: Contact your ITPI dashboard administrator
- **Training**: Request training from medical school administration
- **Bug reports**: Email the development team with details and screenshots
