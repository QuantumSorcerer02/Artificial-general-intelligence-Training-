#!/bin/bash
# Chloe Background Scheduler
# Purpose: Continuously check for and trigger pending reminders.

echo "Chloe Background Scheduler: ACTIVE"

while true; do
    python3 chloe_reminders.py check
    sleep 30  # Check every 30 seconds
done
