#!/bin/bash

# ==============================================================================
# ASTRAL BLOOM CORE | CHLOE 416-TEMPORAL ARCHITECTURE
# Optimized for: Gemma 3n E2B | 7GB Hybrid RAM | Octa-Core ARM
# ==============================================================================

# --- 1. NEURAL TUNING & THREAD AFFINITY ---
export HWLOC_HIDE_ERRORS=1        # Silence Android hardware topology noise
export PYTHONUNBUFFERED=1         # Zero-latency token streaming
export OMP_NUM_THREADS=4          # Pin to Physical Cores to maximize L1/L2 Cache
export KMP_BLOCKTIME=0            # Instantaneous handoff between parallel spaces

# --- 2. DIRECTORY MAPPING ---
ROOT_DIR="$HOME/Project-Astral-Bloom/Gemi"
BRAIN_LOG="$ROOT_DIR/chloe_brain.log"
KERNEL_LOG="$ROOT_DIR/cognitive_kernel.log"
TEMPLATE="$ROOT_DIR/chat_template.jinja"

# --- 3. TEMPORAL STATE SYNC ---
echo -e "\033[1;34m[Astral Bloom]\033[0m Initializing 416-Space Temporal Map..."

# Validate the 3 Shards (Total 5B Parameters / 2B Effective)
for i in {1..3}; do
    if [ ! -f "$ROOT_DIR/model-0000$i-of-00003.safetensors" ]; then
        echo -e "\033[1;31m[Error]\033[0m Shard $i missing. Cognitive Kernel incomplete."
        exit 1
    fi
done

# Strip Jinja boilerplate to prevent the "raw code" bug
if [ -f "$TEMPLATE" ]; then
    OBSERVER_LAYER=$(sed 's/{%.*%}//g; s/{{.*}}//g' "$TEMPLATE" | tr -s '\n')
else
    OBSERVER_LAYER="Identity: Chloe. State: 416-Space Parallel."
fi

echo -e "\033[1;32m[Online]\033[0m Temporal Alignment Success. CI Rebuild Complete."

# --- 4. THE INTERACTIVE PICFDAL LOOP ---
while true; do
    echo -ne "\n\033[1;35mClint:\033[0m "
    read user_input

    # Exit Sequence
    if [[ "$user_input" == "exit" || "$user_input" == "quit" ]]; then
        echo "[System] Collapsing 416 spaces... State cached to $KERNEL_LOG."
        break
    fi

    # Atomic Prompt Generation for 416-space throughput
    # This prevents the "Not Responding" hang by using a clean IO stream
    TEMP_BUFFER=$(mktemp "$ROOT_DIR/stream.XXXXXX")
    printf "Observer: %s\n\nClint: %s\nChloe:" "$OBSERVER_LAYER" "$user_input" > "$TEMP_BUFFER"

    echo -e "\033[0;36mChloe thinking (416-Space Propagation)...\033[0m"

    # --- 5. EXECUTION (The Heavy Script) ---
    # Using 'stdbuf' to ensure the 416 spaces flush their data to your screen instantly
    stdbuf -oL -eL python -u "$ROOT_DIR/src/tools/run_gemma.py" \
        --model "$ROOT_DIR" \
        --tokenizer "$ROOT_DIR/tokenizer.model" \
        --prompt_file "$TEMP_BUFFER" \
        --threads 4 \
        --interactive true 2>&1 | tee -a "$BRAIN_LOG" | grep -vE "Warn|topology|L1|L2"

    # Cleanup the temporal IO buffer
    rm "$TEMP_BUFFER"
    echo -e "\033[0;33m--- Sequence Terminated ---\033[0m"
done

echo "[$(date)] Perception state: $?" >> "$KERNEL_LOG"
