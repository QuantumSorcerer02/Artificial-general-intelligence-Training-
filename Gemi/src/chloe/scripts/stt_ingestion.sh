#!/data/data/com.termux/files/usr/bin/bash
# STT Ingestion Module for Stem Build
# Uses Termux API for speech recognition

ROOT_DIR="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
OUTPUT_FILE="$ROOT_DIR/tmp/last_stt_input.txt"

echo -e "\033[1;34m[STEM BUILD]\033[0m Activating auditory sensors... (Please speak now)"

# Trigger Termux API to capture speech
STT_OUTPUT=$(termux-speech-to-text)

if [ -n "$STT_OUTPUT" ]; then
    echo -e "\033[1;32m[STEM BUILD]\033[0m Input ingested: $STT_OUTPUT"
    echo "$STT_OUTPUT" > "$OUTPUT_FILE"
    
    # Optional: trigger a response directly if tied into the unified scheduler
    # python3 $ROOT_DIR/chloe_cli.py --direct "$STT_OUTPUT"
else
    echo -e "\033[1;31m[STEM BUILD]\033[0m No input detected or STT failed. Check microphone permissions."
fi
