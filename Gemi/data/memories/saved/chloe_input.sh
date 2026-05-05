#!/bin/bash
# Chloe Input Dialog Script
# This script is triggered from a notification to get user input without opening the main Termux app.

# Ensure we have the path set for termux-api
export PATH="/data/data/com.termux/files/usr/bin:$PATH"

# Get user input via termux-dialog
# Using 'text' type for general input
RESULT=$(termux-dialog text -t "Talk to Chloe" -i "Enter your command or message...")

# Parse the JSON result to get the text entered
# The output is like {"code": -1, "text": "user message"}
TEXT=$(echo "$RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('text', ''))")

if [ -n "$TEXT" ]; then
    # Save to a file for the main loop to process
    echo "$TEXT" > /data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/data/memories/user_input.txt
    
    # Optional: Confirm receipt
    termux-toast "Chloe received: $TEXT"
    
    # If the user is running a loop that watches this file, it will pick it up.
fi
