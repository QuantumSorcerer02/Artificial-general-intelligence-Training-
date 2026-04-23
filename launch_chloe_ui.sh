#!/data/data/com.termux/files/usr/bin/bash
# Chloe Launcher Script for Android Notification Action
# This script ensures the correct environment and launches the Chloe/Gemi CLI.

# Setup environment
export PATH="/data/data/com.termux/files/usr/bin:$PATH"
ROOT_DIR="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
cd "$ROOT_DIR"

# Check if a terminal session is already active or if we need to force a new window
# Since this runs in the background from a notification, we use termux-open 
# to bring the Termux app to the foreground and execute the bootloader.

# We'll use a specialized command to launch a new Termux session with the bootloader
am startservice -n com.termux/com.termux.app.TermuxService \
   -a com.termux.service_execute \
   --es com.termux.execute.command "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/bin/Chloe"
