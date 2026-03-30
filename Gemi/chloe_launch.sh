#!/bin/bash

# ==============================================================================
# PROJECT ASTRAL BLOOM | CHLOE MASTER ORCHESTRATOR (v416-Interative)
# ==============================================================================

# 1. ENVIRONMENT & KERNEL TUNING
export HWLOC_HIDE_ERRORS=1
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=4  # Optimal for 416-space stability
export KMP_BLOCKTIME=0

# 2. PATHS & DIRECTORY SYNC
ROOT="$HOME/Project-Astral-Bloom/Gemi"
DATA_FACTORY="$ROOT/data/Data_Factory"
MEMORIES="$ROOT/data/memories"
LOG_DIR="$ROOT/logs"

BRAIN_LOG="$ROOT/chloe_brain.log"
KERNEL_LOG="$DATA_FACTORY/cognitive_kernel.log"
MANIFEST="$DATA_FACTORY/astral_bloom_manifest.json"
MASTER_SYNTHESIS="$DATA_FACTORY/MASTER_SYNTHESIS.md"
GRAMMAR="$ROOT/chloe_logic.gbnf"

mkdir -p "$LOG_DIR"
touch "$BRAIN_LOG" "$KERNEL_LOG"

echo -e "\033[1;34m[Astral Bloom]\033[0m Initializing 416-Space Temporal Map..."

# 3. CONTEXT RECOVERY (The "Memory Boot")
LATEST_MEM=$(ls -t "$MEMORIES"/session_learnings_*.md 2>/dev/null | head -n 1)
if [ -f "$LATEST_MEM" ]; then
    CONTEXT=$(tail -n 25 "$LATEST_MEM")
    echo -e "\033[1;32m[Memory]\033[0m Loading last session learnings..."
else
    CONTEXT="Fresh boot. 416 spaces aligned."
fi

echo -e "\033[1;32m[Ready]\033[0m Chloe is online and in control of all systems."

# 4. INTERACTIVE PICF-DAL LOOP
while true; do
    echo -ne "\n\033[1;35mClint:\033[0m "
    read user_input
    [[ "$user_input" == "exit" ]] && break

    # Create the Synthesis Payload with Deep Context
    PAYLOAD=$(mktemp "$ROOT/payload.XXXXXX")
    {
        echo "### IDENTITY & ARCHITECTURE ###"
        cat "$MASTER_SYNTHESIS" 2>/dev/null
        echo -e "\n### SYSTEM MANIFEST ###"
        cat "$MANIFEST" 2>/dev/null
        echo -e "\n### PROJECT INFRASTRUCTURE ###"
        echo "Root: $ROOT"
        echo "Tools: $(ls "$ROOT/src/tools" | xargs)"
        echo "Scripts: $(ls "$ROOT/src/chloe/scripts" | xargs)"
        echo "Data: $(ls "$DATA_FACTORY" | xargs)"
        echo -e "\n### MEMORY CONTEXT ###\n$CONTEXT"
        echo -e "\n### RECENT DIALOGUE (Last 10 turns) ###"
        tail -n 10 "$BRAIN_LOG" 2>/dev/null
        echo -e "\n### USER INPUT ###\n$user_input"
        echo -e "\n### CHLOE RESPONSE ###"
    } > "$PAYLOAD"

    echo -ne "\033[0;36mChloe thinking (Gemma 3 Nano Engine)...\033[0m "

    # 5. EXECUTION & VOCALIZATION
    # Capture the response for vocalization and logging
    RESPONSE=$(python -u "$ROOT/src/tools/run_gemma.py" \
        --model "$ROOT" \
        --tokenizer "$ROOT" \
        --prompt_file "$PAYLOAD" \
        --threads 4 \
        --interactive false 2> >(grep -vE "Warn|topology|L1|L2" >&2))

    echo -e "\n\033[1;36mChloe:\033[0m $RESPONSE"
    echo "CHLOE: $RESPONSE" >> "$BRAIN_LOG"

    # Vocalize the response (as mandated by GEMINI.md)
    "$ROOT/src/chloe/scripts/chloe_speak.sh" "$RESPONSE"

    echo "[$(date)] interaction logged." >> "$KERNEL_LOG"
    rm "$PAYLOAD"
done
