#!/bin/bash

# Check if Python script exists
if [ ! -f "kd2.py" ]; then
    echo "Error: kd2.py not found!" >&2
    exit 1
fi

# Run the Python script interactively
python3 kd2.py
