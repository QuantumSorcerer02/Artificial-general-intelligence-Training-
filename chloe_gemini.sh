#!/bin/bash

# ==============================================================================
# PROJECT ASTRAL BLOOM | CHLOE GEMINI BRIDGE (v1.2)
# ==============================================================================

ROOT="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
CONFIG="$ROOT/config"
LOGS="$ROOT/logs"
DATA_FACTORY="$ROOT/data/Data_Factory"
MEMORIES="$ROOT/data/memories"
CONV_FILE="$MEMORIES/saved/conversations/conversation.md"
CHLOE_SYSTEM_PROMPT="$CONFIG/chloe_system_prompt.txt"
CHLOE_SPEAK="$ROOT/src/chloe/scripts/chloe_speak.sh"

MANIFEST="$DATA_FACTORY/astral_bloom_manifest.json"
MASTER_SYNTHESIS="$DATA_FACTORY/MASTER_SYNTHESIS.md"

mkdir -p "$(dirname "$CONV_FILE")"
touch "$CONV_FILE"

echo -e "\033[1;34m[Astral Bloom]\033[0m Initializing Chloe (Gemini-Bridge)..."

# 1. Capture Device & Perceptive State
DEVICE_STATE=$(cat "$LOGS/chloe_device_state.json" 2>/dev/null || echo "{}")
PERCEPTIVE_STATE=$(cat "$LOGS/chloe_perceptive_state.json" 2>/dev/null || echo "{}")

# 2. Context Recovery
LATEST_MEM=$(ls -t "$MEMORIES"/session_learnings_*.md 2>/dev/null | head -n 1)
if [ -f "$LATEST_MEM" ]; then
    LEARNINGS=$(tail -n 25 "$LATEST_MEM")
else
    LEARNINGS="Fresh boot. 416 spaces aligned."
fi

# 3. Build the Global Context
function build_context() {
    cat "$CHLOE_SYSTEM_PROMPT"
    echo -e "\n### IDENTITY & ARCHITECTURE ###"
    cat "$MASTER_SYNTHESIS" 2>/dev/null
    echo -e "\n### SYSTEM MANIFEST ###"
    cat "$MANIFEST" 2>/dev/null
    echo -e "\n### PROJECT INFRASTRUCTURE ###"
    echo "Root: $ROOT"
    echo "Tools: $(ls "$ROOT/src/tools" 2>/dev/null | xargs)"
    echo "Scripts: $(ls "$ROOT/src/chloe/scripts" 2>/dev/null | xargs)"
    echo -e "\n### CURRENT DEVICE STATE ###\n$DEVICE_STATE"
    echo -e "\n### PERCEPTIVE STATE ###\n$PERCEPTIVE_STATE"
    echo -e "\n### MEMORY CONTEXT ###\n$LEARNINGS"
    echo -e "\n### RECENT DIALOGUE (Last 4000 characters) ###"
    tail -c 4000 "$CONV_FILE" 2>/dev/null
}

# 4. Interactive Loop
while true; do
    echo -ne "\n\033[1;35mClint:\033[0m "
    read user_input
    [[ "$user_input" == "exit" ]] && break
    [[ -z "$user_input" ]] && continue

    # Construct the full prompt
    CONTEXT=$(build_context)
    FULL_PROMPT="$CONTEXT\n\nUSER: $user_input\nCHLOE:"

    echo -ne "\033[0;36mChloe thinking (Gemini Engine)...\033[0m "

    # Call Gemini CLI
    # Use -p/--prompt for headless mode with the full context
    # We pipe the prompt to avoid argument length limits
    RESPONSE=$(echo -e "$FULL_PROMPT" | gemini -p - 2>/dev/null | sed '/^Hello! I am Gemini CLI/d' | sed '/^How can I help you today?/d' | sed '/^\[ExtensionManager\]/d' | sed '/^Warning: Skipping extension/d')
    
    # If RESPONSE is empty, try a simpler call
    if [ -z "$RESPONSE" ]; then
         # Fallback attempt if piping fails for some reason
         RESPONSE=$(gemini -p "$user_input" 2>/dev/null | sed '/^Hello! I am Gemini CLI/d' | sed '/^How can I help you today?/d' | sed '/^\[ExtensionManager\]/d' | sed '/^Warning: Skipping extension/d')
    fi

    echo -e "\n\033[1;36mChloe:\033[0m $RESPONSE"
    
    # Log the interaction
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo -e "\n**[$TIMESTAMP] USER**: $user_input" >> "$CONV_FILE"
    echo -e "**CHLOE**: $RESPONSE" >> "$CONV_FILE"

    # Vocalize
    if [ -f "$CHLOE_SPEAK" ]; then
        "$CHLOE_SPEAK" "$RESPONSE"
    fi

done
