#!/bin/bash
cd "$(dirname "$0")"

# 1. Detect the appropriate Python interpreter
PYTHON_CMD=""
for cmd in /Library/Frameworks/Python.framework/Versions/3.*/bin/python3 python3.12 python3.11 python3.10 python3; do
    if command -v $cmd &> /dev/null; then
        if $cmd -c "import tkinter" &> /dev/null; then
            PYTHON_CMD=$cmd
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "============================================================"
    echo "Python with GUI support (Tkinter) is required."
    echo "Please download and install official Python from:"
    echo "https://www.python.org/downloads/macos/"
    echo "============================================================"
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Using: $($PYTHON_CMD --version)"

# 2. Create virtual environment if it does not exist
if [ ! -d "venv" ]; then
    echo "Setting up environment for the first time..."
    $PYTHON_CMD -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 3. Launch the application
python3 bioprinter_app.py