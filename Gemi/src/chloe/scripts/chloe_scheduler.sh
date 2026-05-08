#!/bin/bash
# Chloe Background Scheduler
# Purpose: Continuously check for and trigger pending reminders.

echo "Chloe Background Scheduler: ACTIVE"

ROOT_DIR="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"

while true; do
    python3 "$ROOT_DIR/src/chloe/core/chloe_reminders.py" check
    sleep 30  # Check every 30 seconds
done
