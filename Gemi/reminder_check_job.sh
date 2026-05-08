#!/bin/bash
# Chloe Alarm / Reminder Check Job
ROOT_DIR="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
python3 "$ROOT_DIR/src/chloe/core/chloe_reminders.py" check >> "$ROOT_DIR/logs/reminder_checks.log" 2>&1
