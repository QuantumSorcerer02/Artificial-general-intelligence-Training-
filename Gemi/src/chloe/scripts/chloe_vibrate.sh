#!/bin/bash
# Chloe Sensorium: Vibrate Feedback
DURATION=${1:-500}
termux-vibrate -d "$DURATION"
echo "Vibration pulse executed: $DURATION ms"
