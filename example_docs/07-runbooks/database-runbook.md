# Data Management Runbook

## Overview

Operational procedures for CSV data management, maintenance, and troubleshooting.

## Data File Management

### Data Sources

| Data Type | Source | Format | Update Frequency |
|------------|--------|---------|------------------|
| Attendance Data | ITPI Dashboard Export | CSV | Monthly/Weekly |
| Placement Mapping | ITPI Dashboard Export | CSV | Termly/As needed |
| Student Notes | Manual Entry | Excel (Book1.xlsx) | As needed |

### File Structure

- Attendance files: lusi_mbchb101.csv, lusi_mbchb201.csv, lusi_mbchb301.csv, lusi_mbchb401.csv, lusi_mbchb501.csv
- Placement files: y2r1.csv, y3r1.csv, y4r1.csv, y5r1.csv
- Notes file: Book1.xlsx (optional)
- Required columns: studentId, firstName, surname, academicAdvisor, startDateTime
- Optional columns: present, selfCertInfo, cancelled

## Backup & Recovery

### Automated Backup Procedures

- Manual backup schedule: Copy CSV files before major updates
- Retention period: Keep 3 most recent versions of data files
- Version control: Git tracks code changes
- Store backups in separate folder or cloud storage
- Verify backup integrity by testing file opens correctly

### Point-in-Time Restore

**When to use:** Data corruption, accidental deletion, need to compare with previous version

**Step-by-step procedure:**
1. Identify backup version to restore (check backup folder)
2. Copy backup CSV files to application directory
3. Verify data integrity by loading in application
4. Test key functionality (charts, calculations)
5. Update placement mappings if needed

**Expected time:** 5-10 minutes
**Testing:** Load restored data and verify expected student count

### Manual Backup

**How to take on-demand backup:**
1. Copy all CSV files and Book1.xlsx to backup folder
2. Include date in backup folder name (e.g., backup_2024_01_15)
3. Store in separate location (external drive, cloud storage)

**When needed:** Before ITPI data refreshes, before major analysis, weekly

**Verification:** Open backed-up CSV files to confirm readable

**Naming:** backup_YYYY_MM_DD_format

## Data Quality Management

### Data Validation Procedures

- Automated validation during file loading in `load_and_clean_data()`
- Required column presence checks (studentId, firstName, surname, academicAdvisor, startDateTime)
- Data format validation (dates parsed with pd.to_datetime)
- Date/time format verification (ISO format expected)
- Duplicate detection and handling (studentId + timestamp combinations)

### Data Cleaning Operations

- Standardization of student IDs (stripped whitespace, string type)
- Name formatting preserved as-is from source
- Date/time parsing with pd.to_datetime and timezone removal
- Removal of cancelled records (df['cancelled'] == False)
- Handling of missing or null values via dropna()

### Data Refresh Process

1. Export from ITPI dashboard in CSV format
2. Save with consistent naming: lusi_mbchb[year][semester].csv
3. Validate file opens correctly in spreadsheet software
4. Place in application directory
5. Click "Load / Refresh Data" in application
6. Verify student count matches expected

**Update frequency:**
- Weekly for active monitoring
- Monthly for periodic reviews
- Termly for reporting

## Performance Management

### File Processing Optimization

- Use Pandas vectorized operations instead of loops
- Filter data early to reduce memory usage
- Use efficient string matching with regex for placements
- Avoid unnecessary data copying
- Progress shown through status messages in Gradio UI

### Dataset Size Management

- Monitor file sizes: typical 1-5 MB per module
- Performance impact: noticeable above 10,000 rows
- Archiving: Keep old CSV versions in dated folders
- No compression needed for current file sizes
- Storage: Minimal (under 50 MB total per year)

## Common Procedures

### Add New Data Source

1. Validate new CSV format matches expected structure
2. Update `load_and_clean_data()` to handle new data type
3. Test with sample data file
4. Update documentation with new file format requirements
5. Train users on new data source usage

### Update Placement Patterns

1. Review `PLACEMENT_PATTERNS` regex in app.py
2. Test pattern matching with sample event descriptions
3. Update regex if new placement types need recognition
4. Verify categorization accuracy with test data
5. Document any new placement categories

### Data Archive Operations

**Data retention:**
- Keep current academic year files readily accessible
- Archive previous years to dated folders
- Maintain backup of raw ITPI exports

**Archive procedure:**
1. Create folder with academic year name
2. Copy CSV files to archive folder
3. Verify files copy correctly
4. Document archive location

## Troubleshooting

### File Access Issues

| Problem | Solution |
|---------|----------|
| Permission denied | Check file is not open in another program, verify read permissions |
| File not found | Verify file is in same directory as app.py, check filename spelling |
| File locked | Close Excel or other programs that may have file open |
| Encoding errors | Ensure CSV is UTF-8 encoded, re-export from ITPI if needed |
| Path issues | Use relative paths, avoid special characters in filenames |

### Data Corruption Issues

**Symptoms:**
- Unexpected error messages during loading
- Missing student records
- Incorrect attendance calculations
- Chart display errors

**Resolution:**
1. Identify which file is corrupted
2. Restore from backup copy
3. Validate data loads correctly
4. Re-export from ITPI dashboard if backup unavailable
5. Document incident for future prevention

### Performance Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Slow loading | Large dataset | Reduce date range, filter data |
| High memory use | Too many rows loaded | Close other applications |
| Slow charts | Complex visualization | Use simpler views, export data |
| UI unresponsive | Browser issue | Refresh page, restart app |

**Hardware considerations:**
- 8GB RAM recommended for large datasets
- SSD storage improves file loading
- Modern browser for best performance

## Data Security

### Access Control

- Data files stored on local machine only
- Access controlled by operating system file permissions
- Only authorized medical school staff should have access
- Do not share student data files via email or cloud
- Lock workstation when unattended

### Data Privacy

- Student data is confidential and protected
- Process locally - no external data transmission
- Follow medical school data protection policies
- Handle only data necessary for attendance tracking
- Secure disposal of old data files (secure delete)
