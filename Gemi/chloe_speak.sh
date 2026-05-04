#!/data/data/com.termux/files/usr/bin/sh
# chloe_speak.sh - Resilient Auditory Interface
# Monitors for interruptions (e.g., minimizing Termux) and resumes.

TEXT="$*"
if [ -z "$TEXT" ]; then
    TEXT=$(cat)
fi

# Female, high-pitch voice
VOICE="en-us+f3"
PITCH=60
SPEED=140

# RESILIENT EXECUTION: 
# If the process is interrupted, it attempts to restart.
# This does NOT trigger new logic in the LLM.

termux-tts-speak "$TEXT"
RET=$?

if [ $RET -ne 0 ] && [ $RET -ne 130 ]; then
    # Brief pause before resume to allow OS to stabilize
    sleep 1
    termux-tts-speak "$TEXT"
fi
