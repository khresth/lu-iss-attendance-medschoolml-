# Backend Code Guide

## Overview

A practical guide for developers working on the LU Medical School Attendance Tracker — conventions, patterns, and how to do common tasks.

## Application Structure

- Single file application (`app.py`) contains all functionality
- No separate backend/frontend architecture
- Gradio provides web interface framework
- Pandas handles data processing
- Plotly provides visualization capabilities

## Adding New Features

### Adding New Chart Types

**Steps:**
1. Create new chart function in `app.py` that takes data parameters
2. Use Plotly for visualization (go.Figure(), add_trace(), update_layout())
3. Add Gradio Plot component to interface
4. Connect data processing function to chart via event handlers
5. Test with sample data to ensure correct rendering

**Example code pattern:**
```python
def plot_new_chart(data, parameters):
    fig = go.Figure()
    fig.add_trace(go.Scatter(...))
    fig.update_layout(title="...", xaxis_title="...")
    return fig
```

**Add to Gradio interface:**
```python
new_chart = gr.Plot(label="New Chart")
button.click(plot_new_chart, inputs=[...], outputs=[new_chart])
```

### Adding New Data Filters

**Steps:**
1. Add filter parameter to Gradio interface (Dropdown, Slider, Checkbox)
2. Implement filtering logic in data processing function
3. Apply filter to dataframe using Pandas operations
4. Update all dependent outputs (tables, charts)
5. Test filter combinations for edge cases

**Code pattern:**
```python
# Add to interface
new_filter = gr.Dropdown(choices=["A", "B"], label="Filter By")

# Use in function
def process_data(data, filter_value):
    if filter_value:
        data = data[data['column'] == filter_value]
    return data
```

### Adding New CSV Data Sources

**Steps:**
1. Update `load_and_clean_data()` or create new loader function
2. Define required columns for new data type
3. Add file format validation
4. Test with actual data files
5. Update documentation with new file format

**Example loader function:**
```python
def load_new_data_type(file_path):
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    # Validate required columns
    required = ['col1', 'col2']
    if not all(col in df.columns for col in required):
        return None, "Missing required columns"
    # Clean and process
    return df, "Loaded successfully"
```

## Code Conventions

### Function Naming

- Use descriptive function names that explain what they do
- Follow Python PEP 8 naming conventions (snake_case)
- Prefix related functions consistently:
  - `load_*` for data loading functions
  - `plot_*` for chart generation functions
  - `analyze_*` for analysis functions
  - `update_*` for UI update functions

### Variable Naming

- Use clear, descriptive variable names
- Follow Python naming conventions (snake_case)
- Use meaningful names for dataframes (e.g., `attendance_df`, `student_data`)
- Avoid single-letter variables except for loop indices (i, j)
- Constants should be UPPER_CASE (e.g., `PLACEMENT_PATTERNS`)

### Code Organization

- Group related functions together (loaders, analyzers, plotters)
- Separate data processing from UI code
- Use comments to explain complex logic
- Keep functions focused and single-purpose
- Global variables for shared state should be minimized

## Data Processing Patterns

### CSV File Processing

- Use Pandas `read_csv()` with `encoding='utf-8-sig'` for Excel-generated CSVs
- Use `on_bad_lines='skip'` to handle malformed rows
- Handle missing data with `.fillna()` and `.dropna()`
- Validate required columns exist before processing
- Clean and standardize data types (e.g., dates, student IDs)

### Data Validation

- Check for required columns before processing
- Validate data formats (dates with pd.to_datetime, IDs as strings)
- Handle missing or invalid data gracefully
- Provide clear error messages in return values
- Show validation errors in Gradio status textbox

### Performance Optimization

- Use Pandas vectorized operations instead of loops
- Use `.loc[]` and `.iloc[]` for efficient data access
- Consider memory usage for large datasets (10,000+ rows)
- Use appropriate data types (category for repeated strings)
- Avoid unnecessary data copying

## Gradio Interface Patterns

### Component Creation

- Use descriptive labels for all components
- Group related components in gr.Row() and gr.Column()
- Use appropriate input types (File, Dropdown, Slider, Checkbox)
- Provide clear instructions in component labels
- Handle user input validation in processing functions

### Layout Organization

- Use Gradio layout components (Row, Column, Tabs) effectively
- Organize interface logically: inputs at top, outputs below
- Group related functionality in Tabs (Summary, Details, Placement, Macro)
- Use consistent spacing and alignment
- Responsive design is handled by Gradio automatically

## Error Handling

### Data Loading Errors

- Handle missing files gracefully with try/except blocks
- Provide clear error messages: "File for {module} not provided."
- Return None for failed loads so UI can show appropriate message
- Allow recovery by letting users upload correct files
- Always validate data before processing

### Chart Generation Errors

- Return empty go.Figure() for invalid data instead of crashing
- Provide fallback messages in status textbox
- Handle edge cases (empty dataframes, missing columns)
- Ensure user-friendly error messages in UI
- Test with edge cases: empty files, single row, very large datasets

## Testing Patterns

### Manual Testing

Test the application with various scenarios:
- Different CSV file formats and sizes
- Verify chart accuracy against known data
- Test data validation with intentionally bad files
- Check error handling and user feedback
- Test performance with large datasets (5,000+ rows)

### Data Validation Testing

- Test with missing columns - should show clear error
- Test with invalid data formats - should handle gracefully
- Test with empty files - should not crash
- Test with very large files - should process in reasonable time
- Verify error messages are helpful to users

## Configuration Management

### Environment Variables

- This application uses minimal configuration
- File paths are relative to app.py location
- No external API keys or secrets needed
- All configuration is through file locations and user inputs
- Default values are used throughout

### File Path Management

- Use relative paths for data files (same directory as app.py)
- Use os.path.exists() to validate files before loading
- Provide clear error messages for missing files
- Use consistent file naming: lusi_mbchb[year][sem].csv, y[year]r1.csv
- Handle different operating systems via os.path.join()
