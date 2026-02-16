# Frontend Code Guide

## Overview

A practical guide for developers working on the LU Medical School Attendance Tracker frontend — Gradio interface conventions, patterns, and how to do common tasks.

## Gradio Interface Structure

- Single interface defined in `app.py`
- Gradio components for user interaction
- No separate frontend codebase
- Interface defined programmatically
- Real-time updates and interactivity

## Adding New Interface Components

### Adding New Input Components

**Steps:**
1. Add Gradio input component to interface definition (gr.Textbox, gr.Dropdown, etc.)
2. Connect component to data processing function via event handler
3. Handle user input validation in the processing function
4. Update output components based on input changes
5. Test component functionality with various inputs

**Common input types:**
- `gr.File()` - File uploads (CSV, Excel)
- `gr.Dropdown()` - Selection from options
- `gr.Slider()` - Numeric range selection
- `gr.Textbox()` - Text input
- `gr.Checkbox()` - Boolean options
- `gr.Date()` - Date selection (if needed)

**Layout positioning:**
- Use `gr.Row()` for horizontal grouping
- Use `gr.Column()` for vertical stacking
- Use `with` context managers for nesting

### Adding New Output Components

**Steps:**
1. Add Gradio output component (gr.Plot, gr.HTML, gr.Textbox)
2. Connect to data processing or chart function via outputs parameter
3. Format output appropriately for the component type
4. Handle update triggers via event handlers (button.click, dropdown.change)
5. Test output display with sample data

**Common output types:**
- `gr.Plot()` - Plotly charts and visualizations
- `gr.HTML()` - Rich text and data tables
- `gr.Textbox()` - Status messages and logs
- `gr.Dataframe()` - Tabular data display
- `gr.Image()` - Static images (if needed)

**Update patterns:**
- Button click triggers processing
- Dropdown change triggers updates
- Use `gr.update()` for conditional component updates

## Interface Layout Patterns

### Component Organization

- Use Gradio layout components (Row, Column, Tabs) for structure
- Group related functionality together in logical sections
- Create logical sections: File Upload, Controls, Results
- Use consistent spacing and alignment within rows/columns
- Responsive design is handled automatically by Gradio
- Create logical sections for different features
- Use consistent spacing and alignment
- Responsive design considerations

### User Experience Patterns

- Provide clear instructions and labels
- Use progress indicators for long operations
- Give feedback for user actions
- Handle errors gracefully
- Design for intuitive workflow

## Data Visualization Patterns

### Chart Integration

- Use Plotly charts rendered in Gradio's Plot component (`gr.Plot()`)
- Format chart data as pandas DataFrame or dictionary before passing to Plotly
- Update charts by returning new figures from event handlers
- Leverage Plotly's interactive features (zoom, pan, hover tooltips)
- Handle rendering errors by returning empty figures with error messages

### Data Display

- Use `gr.HTML()` for rich text and data tables (more flexible than Dataframe)
- Format numbers to 2 decimal places for readability
- Handle large datasets by showing summaries rather than full tables
- Sort and filter data in Pandas before displaying
- Export data by allowing users to copy from HTML tables

## Event Handling Patterns

### Input Processing

- Connect inputs to functions using event handlers (`button.click()`, `dropdown.change()`)
- Validate inputs in processing functions before using them
- Handle combinations of multiple inputs gracefully
- Provide immediate feedback through status messages
- Cache expensive operations using global variables if needed

### Real-time Updates

- Use `gr.update()` to dynamically update component properties
- Trigger updates on input changes with `dropdown.change()`
- Avoid concurrent updates by processing sequentially
- Manage state through return values and global variables
- Optimize by only updating components that need to change

## Styling and Theming

### Component Styling

- Use Gradio's built-in theming (light/dark mode)
- Apply consistent labels and descriptions
- Rely on Gradio's default accessibility features
- Use appropriate component types for data (File for uploads, Dropdown for choices)
- Test interface at different window sizes

### Custom CSS

- Minimal CSS needed - Gradio handles most styling
- Can add custom CSS via `gr.Blocks(css="...")` if required
- Test any custom styling across browsers
- Maintain consistency with default Gradio theme
- Document any custom CSS for future maintainers

## Error Handling in Interface

### Input Validation

- Validate file uploads by checking file extensions and content
- Check data formats match expected CSV structure
- Show clear error messages in status textbox
- Guide users to correct issues with specific instructions
- Handle edge cases (empty files, wrong format) gracefully

### Processing Errors

- Display error messages in the Gradio status textbox
- Provide recovery options (re-upload file, adjust filters)
- Show Python errors in terminal for debugging
- Maintain application stability - don't crash on errors
- Help users troubleshoot with specific guidance

## Performance Optimization

### Interface Responsiveness

- Gradio handles most rendering optimization automatically
- For large datasets, filter data before displaying
- Minimize updates by returning only changed outputs
- Cache computed results in global variables
- Monitor performance through user feedback and timing

### Data Processing

- Optimize Pandas operations using vectorized methods
- Use efficient data structures (avoid unnecessary copies)
- Handle large datasets carefully (10,000+ rows)
- Provide progress feedback through status textbox
- Monitor memory usage with system tools

## Testing Interface Components

### Manual Testing

- Test all input combinations (different files, dates, thresholds)
- Verify output accuracy against known data
- Check error handling with invalid inputs
- Test with various data formats and sizes
- Validate complete user workflows

### User Experience Testing

- Test interface intuitiveness with new users
- Verify Gradio's built-in accessibility features
- Check responsive design at different window sizes
- Test with different browsers (Chrome, Firefox, Edge)
- Gather user feedback for improvements

## Common Patterns and Best Practices

### Code Organization

- Group related interface elements together in rows/columns
- Use descriptive variable names for components
- Add comments for complex event handling logic
- Separate data processing functions from UI layout code
- Maintain consistent patterns across similar components

### User Interface Design

- Keep interface simple and intuitive
- Provide clear labels and instructions
- Use consistent terminology throughout
- Ensure error messages are helpful and actionable
- Group related functionality together
- Use tabs to organize complex output (Summary, Details, Placement, Macro)
- Use consistent terminology
- Ensure accessibility
- Test with actual users
