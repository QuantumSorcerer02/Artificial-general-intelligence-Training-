#!/data/data/com.termux/files/usr/bin/sh
# chloe_speak.sh - Resilient Auditory Interface
# Monitors for interruptions (e.g., minimizing Termux) and resumes.

TEXT="$*"
if [ -z "$TEXT" ]; then
    TEXT=$(cat)
fi

# Female, high-pitch voice
VOICE="en+f2"
PITCH=80
SPEED=150

# RESILIENT EXECUTION: 
# If the process is interrupted, it attempts to restart.
# This does NOT trigger new logic in the LLM.

espeak-ng -v $VOICE -p $PITCH -s $SPEED "$TEXT"
RET=$?

if [ $RET -ne 0 ] && [ $RET -ne 130 ]; then
    # Brief pause before resume to allow OS to stabilize
    sleep 1
    espeak-ng -v $VOICE -p $PITCH -s $SPEED "$TEXT"
fi
