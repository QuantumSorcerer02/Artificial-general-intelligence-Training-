#!/bin/bash
# Chloe Sensorium: Location Monitor
LOCATION=$(termux-location -p network -r last)
echo "$LOCATION"
