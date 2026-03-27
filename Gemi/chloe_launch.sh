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

    # Create the Synthesis Payload
    PAYLOAD=$(mktemp "$ROOT/payload.XXXXXX")
    {
        echo "### SYSTEM MANIFEST ###"
        cat "$MANIFEST" 2>/dev/null
        echo -e "\n### ARCHITECTURE RULES ###"
        cat "$MASTER_SYNTHESIS" 2>/dev/null
        echo -e "\n### MEMORY CONTEXT ###\n$CONTEXT"
        echo -e "\n### RECENT DIALOGUE ###"
        tail -n 10 "$BRAIN_LOG" 2>/dev/null
        echo -e "\n### INPUT ###\n$user_input"
        echo -e "\nCHLOE:"
    } > "$PAYLOAD"

    echo -ne "\033[0;36mChloe thinking...\033[0m "

    # 5. EXECUTION (The "Talk Back" Force)
    # We use 'stdbuf' to ensure the terminal flushes Chloe's voice instantly.
    stdbuf -oL -eL python -u "$ROOT/src/tools/run_gemma.py" \
        --model "$ROOT" \
        --tokenizer "$ROOT/tokenizer.model" \
        --prompt_file "$PAYLOAD" \
        --grammar "$GRAMMAR" \
        --threads 4 \
        --interactive true 2>&1 | tee -a "$BRAIN_LOG"

    echo "[$(date)] interaction logged." >> "$KERNEL_LOG"
    rm "$PAYLOAD"
done
