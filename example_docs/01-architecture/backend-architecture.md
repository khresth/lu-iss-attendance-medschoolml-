# Backend Architecture

## Overview

Describe the LU Medical School Attendance Tracker backend — its role, hosting model, and how it fits into the wider system.

- **Runtime and framework:** Python 3.8+ with single-file architecture
- **Hosting:** Local deployment on user machines, no orchestration needed
- **Key responsibilities:** Data processing, web interface, visualization, file management

## Application Structure

Explain the single-file application structure and its components.

| Component | Purpose |
|-----------|---------|
| `app.py` | Main application file containing all functionality |
| Data Loading Functions | CSV file processing and validation |
| Gradio Interface | Web UI components and layout |
| Chart Generation | Plotly visualization functions |
| Data Processing | Pandas-based data manipulation and analysis |

## Key Components

### Data Processing Layer

- CSV file loading and cleaning functions
- Data validation and standardization
- Attendance calculation logic
- Placement pattern matching with regex
- Data aggregation and filtering

### Web Interface Layer

- Gradio web interface framework
- File upload components
- Chart display components
- User interaction handling
- Layout and organization

### Visualization Layer

- Plotly chart generation
- Interactive chart features (zoom, pan, hover)
- Attendance trend visualization
- Placement analysis charts
- Student-specific attendance graphs
- Data formatting for visualization
- Chart type variety (attendance trends, placement distribution)
- Performance optimization for large datasets

## Data Flow

- CSV files → Data loading functions → Data cleaning → Processing → Visualization
- User interactions → Interface updates → Data processing → Chart updates
- No external API calls or database operations
- All processing happens in-memory using Pandas

## Technology Integration

- Python runtime for core logic
- Pandas for data manipulation
- Gradio for web interface
- Plotly for data visualization
- File system for data persistence
- No external service dependencies

## Error Handling

- Try-except blocks for file loading operations
- Graceful handling of missing or malformed CSV files
- User-friendly error messages displayed in Gradio interface
- Data validation before processing
- Fallback behavior when data is unavailable
