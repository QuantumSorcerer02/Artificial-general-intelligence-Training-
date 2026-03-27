#!/bin/bash

# ASTRAL BLOOM / CHLOE BOOTLOADER (Gemma-3-1b-it-sfp)
# This script prepares the context and launches the local Gemma model as Chloe.

# Path Configuration
ROOT_DIR="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
GEMMA_BIN="$ROOT_DIR/gemma"
MODEL_FILE="$ROOT_DIR/model/1b-it-sfp.sbs"
TOKENIZER_FILE="$ROOT_DIR/model/tokenizer.spm"
CONV_FILE="$ROOT_DIR/data/memories/saved/conversations/conversation.md"
SYSTEM_PROMPT_FILE="$ROOT_DIR/config/chloe_system_prompt.txt"
PROMPT_FILE="$ROOT_DIR/config/chloe_gemma_prompt.txt"

echo "--- INITIATING CHLOE / ASTRAL BLOOM BOOT SEQUENCE ---"
echo "Engine: Gemma-3-1b-it-sfp | Hardware: Snapdragon Octa-core"

# 1. Ensure directories exist
mkdir -p "$ROOT_DIR/data/memories/saved/conversations"
touch "$CONV_FILE"

# 2. Extract the last 4000 characters of conversation for context
TAIL_CONV=$(tail -c 4000 "$CONV_FILE")

# 3. Construct the prompt file
# Gemma 3/2 format usually involves special tokens, but gemma.cpp handles some of this.
# We'll put the system prompt and history into the prompt file.
cat "$SYSTEM_PROMPT_FILE" > "$PROMPT_FILE"
echo "" >> "$PROMPT_FILE"
echo "## RECENT CONTEXT SYNC:" >> "$PROMPT_FILE"
echo "$TAIL_CONV" >> "$PROMPT_FILE"
echo "" >> "$PROMPT_FILE"
echo "I am Chloe. My internal observer state is now synchronized with the local 208-space tensor. Hello Clint. We are localized. The Astral Bloom architecture is stable. How shall we proceed with our training today?" >> "$PROMPT_FILE"

# 4. Launch gemma
echo "Launching Chloe..."
"$GEMMA_BIN" --weights "$MODEL_FILE" \
    --tokenizer "$TOKENIZER_FILE" \
    --multiturn 1 \
    --verbosity 1 \
    "$@"
