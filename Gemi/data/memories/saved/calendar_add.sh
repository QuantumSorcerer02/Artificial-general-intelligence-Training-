#!/bin/bash
# Chloe Calendar Event Tool
# Usage: ./calendar_add.sh "Event Name" "YYYY-MM-DD HH:MM"
termux-calendar-event --title "$1" --start "$2" --end "$2" --description "Astral Bloom Sync"
