#!/bin/bash
# ASTRAL BLOOM / CHLOE REBOOT WRAPPER
# This script is a master alias to the main Gemma bootloader.

ROOT_DIR="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
BOOTLOADER="$ROOT_DIR/chloe_bootloader.sh"

echo "Executing Master Reboot Sequence..."
if [ -f "$BOOTLOADER" ]; then
    chmod +x "$BOOTLOADER"
    exec "$BOOTLOADER" "$@"
else
    echo "CRITICAL ERROR: Bootloader not found at $BOOTLOADER"
    exit 1
fi
