# Observability Reference

## Overview

The LU Medical School Attendance Tracker is a local Python application with minimal observability needs. Since it's a single-user local tool, traditional observability infrastructure is not required.

## Debugging Approach

### Console Output

- Python print statements and error tracebacks appear in terminal
- Gradio status messages shown in web interface
- No external logging services or dashboards

### Application Monitoring

| Aspect | Method | Location |
|--------|--------|----------|
| Startup status | Terminal output | Console where `python app.py` runs |
| File loading | Status textbox in Gradio UI | Main interface |
| Data processing | Status messages | Analysis section |
| Errors | Exception tracebacks | Terminal console |

## Troubleshooting

### When Issues Occur

1. Check the terminal window running the application for Python errors
2. Look at status messages in the Gradio interface
3. Verify data files are properly formatted
4. Check browser console for JavaScript errors (rare)

### Common Debug Steps

- Run `python app.py` in terminal to see all output
- Use print() statements in app.py for debugging
- Test data files separately in Python/pandas
- Check file permissions and encoding

## No External Monitoring

**Important:** This application does not use:
- OpenTelemetry or distributed tracing
- External logging services
- Metrics dashboards
- Error tracking services (Sentry, etc.)
- Application Performance Monitoring (APM)

All debugging is done through local console output and the Gradio interface status messages.
