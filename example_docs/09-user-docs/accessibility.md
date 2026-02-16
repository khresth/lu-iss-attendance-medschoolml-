# Accessibility Statement

## Overview

The LU Medical School Attendance Tracker is built using Gradio, which provides basic web accessibility features. This document outlines the current accessibility status and limitations.

## Our Commitment

We aim to make the attendance tracker accessible to all medical school staff. The application uses Gradio's built-in accessibility features, including semantic HTML and ARIA labels where supported.

## Current Accessibility Features

### Supported Features

- Keyboard navigation for interactive elements
- Form labels on input fields
- Semantic HTML structure
- Focus indicators on interactive elements
- Text-based status messages

### Browser and Assistive Technology Support

- Modern browsers (Chrome, Firefox, Edge, Safari)
- Basic screen reader compatibility through Gradio
- Keyboard-only operation possible
- No mobile app - web browser only

## Known Limitations

| Issue | Impact | Workaround |
|-------|--------|------------|
| Complex data tables | Screen readers may have difficulty with large HTML tables | Use browser zoom, copy data to spreadsheet |
| Charts and graphs | Visual information may not be fully accessible to screen readers | Data available in tabular form alongside charts |
| Color-coded data | Some information conveyed through color alone | Check table data for actual values |
| Interactive plots | Plotly charts have limited keyboard navigation | Use alternative data views in tables |

## Getting Help

### Chart Accessibility

- Chart descriptions and titles
- Color contrast in visualizations
- Alternative text for data representations
- Request data in alternative formats if needed
- Report accessibility issues for future improvements

## Feedback

### Compliance Status

- Meets basic web accessibility standards
- Gradio framework provides accessible components
- Ongoing improvements based on feedback
- Accessibility feedback welcome via IT department
- Used to prioritize improvements in future releases
