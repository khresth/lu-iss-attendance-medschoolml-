#!/usr/bin/env bash

echo -e "\033]0;MBChB Attendance Dashboard\007"
echo "Starting MBChB Attendance Dashboard..."
echo "Please wait..."


if ! python3 -c "import gradio, pandas, plotly, openpyxl" 2>/dev/null; then
    echo ""
    echo "Some required Python packages are missing (gradio, pandas, plotly, openpyxl)."
    echo "Installing them now (user-level install – no password needed)..."
    echo ""

    python3 -m pip install --user -r requirements.txt


    if ! python3 -c "import gradio, pandas, plotly, openpyxl" 2>/dev/null; then
        echo ""
        echo "ERROR: Installation failed or packages still not found."
        echo "Try running this manually in a terminal:"
        echo "    cd \"$(dirname "$0")\""
        echo "    python3 -m pip install --user -r requirements.txt"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    else
        echo "Packages installed successfully!"
    fi
else
    echo "All required packages are already installed."
fi

echo ""
echo "When you see a line like:"
echo "Running on local URL: http://127.0.0.1:7860"
echo "→ your browser should open automatically."
echo "If it doesn't, copy-paste that URL into your browser."
echo ""

python3 app.py

echo ""
echo "Dashboard has stopped."
read -p "Press Enter to close this window..."
