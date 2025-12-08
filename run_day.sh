#!/bin/bash
# Helper script to run daily solutions
# Usage: ./run_day.sh 18

if [ -z "$1" ]; then
    echo "Usage: ./run_day.sh <day_number>"
    exit 1
fi

DAY="day$1.py"

if [ ! -f "$DAY" ]; then
    echo "Error: $DAY not found"
    exit 1
fi

python "$DAY"
