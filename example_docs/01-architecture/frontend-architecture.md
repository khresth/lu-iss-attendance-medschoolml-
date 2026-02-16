# Frontend Architecture

## Overview

Describe the LU Medical School Attendance Tracker frontend application, its target platforms, and how it fits into the system.

- Frontend framework and runtime: Gradio web interface framework
- Target platforms: Web browser (no mobile or native apps)
- How it's served: Local Python web server (localhost)
- Communicates with data processing through direct function calls

## Technology Choices

| Concern | Technology | Notes |
|---------|-----------|-------|
| Framework | Gradio | Python-based web framework for rapid UI development |
| UI Components | Gradio Components | Built-in components for file upload, charts, data display |
| Data Visualization | Plotly | Interactive charting library integrated with Gradio |
| State Management | In-memory | No persistent state management needed |
| Data Fetching | Direct function calls | No API calls, direct data processing |

## Directory Structure

Since this is a single-file application, there's no traditional frontend directory structure.

- All frontend code is contained within `app.py`
- Gradio interface defined programmatically
- No separate `src/` directory structure
- Components created through Gradio function calls
- No build process or bundling required

## Component Architecture

Describe the Gradio component organization and design patterns.

- Gradio Blocks-based layout structure
- Component hierarchy: File uploads → Controls → Output displays
- Tab-based organization for different analysis views
- Input components: File, Dropdown, Textbox, Slider, Checkbox
- Output components: Plot, HTML, Textbox

## Data Flow

Document how data moves through the interface.

- Direct function calls from Gradio events to Python functions
- Data transformation from CSV to DataFrame to visualization
- Synchronous updates based on user interactions
- State managed through Gradio component values and global variables
- No client-side state management needed

## User Interface Structure

- Header section with title and instructions
- File upload section (Book1.xlsx, rotation files, attendance CSVs)
- Module selection and date range controls
- Analysis parameters (thresholds, sorting options)
- Tabbed output display (Summary, Student Details, Placement Analysis, Macro View)
- Real-time updates based on user selections
