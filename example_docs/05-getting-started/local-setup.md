# Local Development Setup

## Prerequisites

| Tool | Version | Installation |
|------|---------|-------------|
| Python | 3.8+ | Download from python.org or package manager |
| pip | Latest | Included with Python |
| Git | Latest | Download from git-scm.com |
| IDE | VS Code, PyCharm | Recommended with Python extensions |

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd lu-iss-attendance-medschoolml-
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare Data Files

- Place CSV files from ITPI dashboard in the project root directory
- Required files: lusi_mbchb101.csv, lusi_mbchb201.csv, lusi_mbchb301.csv, lusi_mbchb401.csv, lusi_mbchb501.csv
- Optional placement files: y2r1.csv, y3r1.csv, y4r1.csv, y5r1.csv
- Optional notes file: Book1.xlsx (student notes and email addresses)

### 4. Start the Application

```bash
python app.py
```

- Application will start on localhost (default port 7860 for Gradio)
- Web interface will open automatically in browser
- If browser doesn't open, navigate to the URL shown in terminal

### 5. Verify Everything Works

- Check that the Gradio interface loads in browser
- Upload a CSV file to test data processing
- Verify that attendance charts and statistics display correctly
- Check that placement tracking features work as expected

## IDE Configuration

### VS Code

- Python extension (Microsoft)
- Jupyter extension for notebook support
- Pylance for IntelliSense
- Recommended workspace settings for Python formatting

### PyCharm

- Python plugin enabled
- Configure Python interpreter for the project
- Set up run configuration for app.py

## Troubleshooting Local Setup

| Issue | Solution |
|-------|----------|
| Python not found | Ensure Python 3.8+ is installed and in PATH |
| Module import errors | Run `pip install -r requirements.txt` again |
| CSV file errors | Check file format and encoding (UTF-8) |
| Gradio doesn't start | Check port conflicts, try different port |
| Charts not displaying | Ensure Plotly is properly installed |
| Data processing slow | Check CSV file sizes, consider sampling large datasets |
