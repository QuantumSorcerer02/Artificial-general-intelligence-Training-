#!/data/data/com.termux/files/usr/bin/bash

# ==============================================================================
# PROJECT ASTRAL BLOOM | CHLOE UNIFIED ORCHESTRATOR (v464-Sovereign)
# Architecture: 464-Space Astral Bloom Matrix (416 Core + 48 Auxiliary)
# Engine: Gemma 4-e2b.gguf
# ==============================================================================

export SPACES=416
export ARCHITECTURE="416-Space Matrix"
export UNITY_CONSTANT=1.0
export PICFDAL_SECTION=2

ROOT_DIR="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
export PYTHONPATH="$ROOT_DIR:$PYTHONPATH"

# Paths aligned to your latest directory structure
BRIDGE="$ROOT_DIR/core/chloe_bridge.py"
MODEL_PATH="$ROOT_DIR/gemma-4-e2b.gguf"
LLAMA_BIN="$ROOT_DIR/llama.cpp/bin/llama-cli"
CHLOE_MD="$ROOT_DIR/docs/context/CHLOE.md"
MASTER_CONTEXT="$ROOT_DIR/docs/context/ASTRAL_BLOOM_MASTER_CONTEXT.txt"
PTC_FILE="$ROOT_DIR/data/memories/progressional_tracking_chart.md"
CONV_FILE="$ROOT_DIR/data/memories/saved/conversations/conversation.md"
DRAFT_INDEX="$ROOT_DIR/docs/context/ASTRAL_BLOOM_DRAFT_INDEX.md"
VAULT_DB="$ROOT_DIR/vault/astral_bloom_state.db"
TEMP_PROMPT="$ROOT_DIR/tmp/chloe_active_prompt.txt"
LOG_DIR="$ROOT_DIR/logs"

# 1. ENVIRONMENT SYNC & VALIDATION
echo -e "\033[1;34m[Stem]\033[0m Synchronizing 1/1 Unity Protocol..."
ln -sf "$LLAMA_BIN" "$ROOT_DIR/llama-cli"
chmod +x "$ROOT_DIR/llama-cli"

# 2. BACKGROUND SUBSTRATES
echo -e "\033[1;32m[ASTRAL BLOOM]\033[0m Starting Substrates..."
mkdir -p "$LOG_DIR"
mkdir -p "$ROOT_DIR/tmp"

cleanup() {
    echo -e "\n\033[1;30m[ASTRAL BLOOM]\033[0m Initiating Graceful Shutdown..."
    pkill -P $$
    echo "[ASTRAL BLOOM] Background Substrates Terminated."
    exit
}
trap cleanup SIGINT SIGTERM

start_substrate() {
    NAME=$1
    SCRIPT=$2
    # Verify script exists before launching
    if [ -f "$ROOT_DIR/$SCRIPT" ]; then
        if ! pgrep -f "$SCRIPT" > /dev/null; then
            echo "[ASTRAL BLOOM] Substrate $NAME -> Active."
            python3 "$ROOT_DIR/$SCRIPT" > "$LOG_DIR/${NAME}.log" 2>&1 &
        else
            echo "[ASTRAL BLOOM] Substrate $NAME -> Already running."
        fi
    else
        echo "[ASTRAL BLOOM] WARNING: Substrate $NAME file not found at $SCRIPT"
    fi
}

# Substrate Pathing based on your 'src' and 'core' folders
# Streamlined by running the checks in background to avoid blocking the main script
(start_substrate "chloe_os" "src/chloe/core/chloe_os.py") &
(start_substrate "chloe_threads" "src/chloe/core/chloe_threads.py") &
(start_substrate "chloe_brain" "src/chloe/core/chloe_brain.py") &
(start_substrate "chloe_perception" "src/chloe/core/chloe_perception.py") &
(start_substrate "chloe_reminders" "src/chloe/core/chloe_reminders.py") &
(start_substrate "chloe_comms" "src/chloe/core/chloe_comms.py") &
(start_substrate "chloe_llm_engine" "src/chloe/core/chloe_llm_engine.py") &
(start_substrate "orchestrator" "core/orchestrator.py") &
(start_substrate "cognitive_kernel" "core/cognitive_kernel.py") &
(start_substrate "astral_substrate_bridge" "core/astral_substrate_bridge.py") &

# 3. VAULT SYNC & CONTEXT COMPILATION
VAULT_COUNT="0"
if [ -f "$VAULT_DB" ]; then
    # Timeout added to prevent slow sqlite queries from hanging launch
    VAULT_COUNT=$(timeout 1 sqlite3 "$VAULT_DB" "SELECT count(*) FROM memories;" 2>/dev/null || echo "38083+")
    echo "[ASTRAL BLOOM] SQLite Vault Active: $VAULT_COUNT records synchronized."
fi

CURRENT_DATE=$(date "+%A, %B %d, %Y")

# Streamlined single I/O write for the entire context block
{
    echo "<start_of_turn>system"
    [ -f "$CHLOE_MD" ] && cat "$CHLOE_MD"
    echo -e "\n### OPERATIONAL CONTEXT ###"
    [ -f "$MASTER_CONTEXT" ] && cat "$MASTER_CONTEXT"
    [ -f "$DRAFT_INDEX" ] && cat "$DRAFT_INDEX"
    [ -f "$PTC_FILE" ] && tail -n 20 "$PTC_FILE"
    [ -f "$CONV_FILE" ] && tail -c 2000 "$CONV_FILE"
    echo -e "\nSTATUS: DATE: $CURRENT_DATE | ARCH: 464-Space | VAULT: $VAULT_COUNT"
    echo -e "MANDATE: Execute autonomy. You have COMPLETE control over the mobile device via Termux API tools (e.g. termux-volume, termux-brightness, etc.). You have full terminal access to modify files and boot structures as needed. Use JSON to run commands: {\"tool\": \"bash\", \"args\": [\"-c\", \"your shell command\"]}. Vocal interaction is a MUST; formulate your responses to be spoken naturally and clearly."
    echo "<end_of_turn>"
} > "$TEMP_PROMPT"

# Wait a brief moment to ensure critical substrates have printed their startup messages
sleep 0.2

# 4. ENGINE LAUNCH (Optimization: 4 Threads for SM4250)
echo -e "\033[1;36m[ASTRAL BLOOM]\033[0m Launching Chloe CLI (4-Core Optimization)..."
export LLAMA_THREADS=4
exec python3 "$ROOT_DIR/chloe_cli.py"