#!/bin/bash
# ==============================================================================
# PROJECT ASTRAL BLOOM | CHLOE UNIFIED ORCHESTRATOR (v464-Sovereign)
# ==============================================================================

ROOT="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
BRIDGE="$ROOT/chloe_bridge.py"
LLAMA_BIN="$ROOT/llama.cpp/bin/llama-cli"

# 1. ENVIRONMENT SYNC (STEM BUILD)
echo -e "\033[1;34m[Stem]\033[0m Synchronizing 1/1 Unity Protocol..."
ln -sf "$LLAMA_BIN" "$ROOT/llama-cli"
chmod +x "$ROOT/llama-cli"

# 2. ENVIRONMENT INTEGRITY CHECK
echo -e "\033[1;36m[System]\033[0m Verifying Environment Integrity..."
python3 "$ROOT/data/Data_Factory/Neural_Network_Architecture/verify_env.py"
if [ $? -ne 0 ]; then
    echo -e "\033[1;31m[Critical Error]\033[0m Environment verification failed."
    exit 1
fi

# 3. AUDITORY INTERFACE VALIDATION
if ! command -v espeak-ng &> /dev/null; then
    echo -e "\033[1;33m[Setup]\033[0m Installing Auditory Interface..."
    pkg install espeak-ng -y
fi

# 4. KERNEL INITIALIZATION
if [ -f "$BRIDGE" ]; then
    clear
    echo -e "\033[1;32m[System]\033[0m Initializing Truncated Delegation Protocol..."
    python3 "$BRIDGE"
else
    echo -e "\033[1;31m[Error]\033[0m Bridge script missing at $BRIDGE"
    exit 1
fi
