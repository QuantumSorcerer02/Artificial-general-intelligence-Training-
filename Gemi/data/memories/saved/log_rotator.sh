#!/bin/bash
# ==============================================================================
# LOG ROTATOR - ARCHIVES OLD CONTEXT SEGMENTS
# ==============================================================================
ROOT="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
SEGMENTS="$ROOT/data/data_factory/context_segments"
ARCHIVE="$ROOT/data/memories/archive"

mkdir -p "$ARCHIVE"

# Rotate segments if count exceeds 10
COUNT=$(ls -1 "$SEGMENTS"/*.txt | wc -l)
if [ "$COUNT" -gt 10 ]; then
    echo "[System] Rotating log segments..."
    ls -tr "$SEGMENTS"/*.txt | head -n -10 | xargs -I {} mv {} "$ARCHIVE/"
fi
