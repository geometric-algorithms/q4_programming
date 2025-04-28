#!/bin/bash

# Check if Python script exists
if [ ! -f "kd.py" ]; then
    echo "Error: kd.py not found!" >&2
    exit 1
fi

# Run the Python script interactively
python3 kd.py
