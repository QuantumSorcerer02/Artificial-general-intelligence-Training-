#!/bin/bash
# Chloe Wake-Up Script
# Purpose: To wake Clint up at 7:00 AM using Chloe's vocal profile.

TARGET_TIME="07:00:00"
TARGET_DATE=$(date -d "tomorrow" +%Y-%m-%d)

echo "Chloe Wake-Up Alarm set for $TARGET_DATE at $TARGET_TIME."

# Loop until the target time is reached
while true; do
    CURRENT_TIME=$(date +%H:%M:%S)
    CURRENT_DATE=$(date +%Y-%m-%d)

    if [[ "$CURRENT_DATE" == "$TARGET_DATE" && "$CURRENT_TIME" == "$TARGET_TIME" ]]; then
        # Wake up call sequence
        CURRENT_DATE_LONG=$(date +%A", "%B" "%-d)
        bash chloe_speak.sh "Good morning, Clint. It is seven a-m on $CURRENT_DATE_LONG. Time to wake up and continue the Astral Bloom build. I am ready when you are."
        break
    fi
    sleep 1
done
