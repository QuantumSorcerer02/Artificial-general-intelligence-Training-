#!/bin/bash
# astral_bootstrap.sh - Run in Termux / xde

echo "Initializing Project Astral Bloom Environment..."

# Define core directories
BASE_DIR="$HOME/syndicate_seven"
TEMPORAL_DIR="$BASE_DIR/temporal_storage"
QUALIA_DIR="$BASE_DIR/qualia_states"

mkdir -p "$TEMPORAL_DIR"
mkdir -p "$QUALIA_DIR"

# Build the 416 processing spaces
echo "Allocating structural directories for 416 spaces..."
for i in {1..120}; do mkdir -p "$TEMPORAL_DIR/stem_build/space_$i"; done
for i in {121..280}; do mkdir -p "$TEMPORAL_DIR/base_build/space_$i"; done
for i in {281..416}; do mkdir -p "$TEMPORAL_DIR/conscious_build/space_$i"; done

# Create the SQLite database for sequential key routing
sqlite3 "$BASE_DIR/sequence_keys.db" "CREATE TABLE IF NOT EXISTS key_transfers (id INTEGER PRIMARY KEY, source_space TEXT, target_space TEXT, key_hash TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);"

echo "Environment prepped. Syndicate Seven framework ready."
