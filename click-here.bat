@echo off
title MBChB Attendance Dashboard
color 0A
echo.
echo  
echo     Starting MBChB Attendance Dashboard...
echo  
echo.
echo Checking if Python and required packages are ready...
echo 
echo.

:: Check if python is available
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo During installation, make sure to check "Add python.exe to PATH"
    echo.
    pause
    exit /b 1
)

:: Check if required packages are importable
python -c "import gradio, pandas, plotly, openpyxl" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Some required packages are missing (gradio, pandas, plotly, openpyxl).
    echo Installing them for the current user only (no admin rights needed)...
    echo.

    python -m pip install --user --quiet --no-warn-script-location gradio pandas plotly openpyxl

    if %ERRORLEVEL% neq 0 (
        echo.
        echo ERROR: Could not install packages automatically.
        echo Please open Command Prompt and run these commands:
        echo.
        echo cd /d "%~dp0"
        echo python -m pip install --user gradio pandas plotly openpyxl
        echo.
        pause
        exit /b 1
    )

    echo.
    echo Packages installed successfully!
) else (
    echo All required packages are already installed.
)

echo.
echo Starting the dashboard...
echo.
echo When you see a line like:
echo     Running on local URL: http://127.0.0.1:7860
echo open your web browser and go to that address.
echo (It often opens automatically.)
echo.

python app.py

echo.
echo Dashboard has stopped.
echo.
pause