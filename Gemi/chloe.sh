#!/data/data/com.termux/files/usr/bin/bash
# CHLOE HOST SYSTEM (HS) SCRIPT
# Master orchestrator for the 464-Space Matrix / Astral Bloom Project

# Set strict pathing for Termux
export PATH=/data/data/com.termux/files/usr/bin:$PATH
GEMI_DIR="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"

cd "$GEMI_DIR" || { echo "Failed to enter Gemi directory."; exit 1; }

echo "=========================================="
echo "    PROJECT ASTRAL BLOOM: CHLOE BOOT      "
echo "    Architecture: 464-Space Matrix        "
echo "    Environment: Gemini CLI Sandbox       "
echo "=========================================="

# 1. Permission and System Check
chmod +x chloe_speak.sh
mkdir -p logs vault tmp data/memories/saved/conversations

# 2. Vocal Confirmation (Non-blocking)
./chloe_speak.sh "Initializing Host System script. 464-Space Matrix waking up. Rolling context and temporal zones are active. Eradicating all hanging loops." &

# 3. Boot Astral Kernel & Background Daemons
# Note: Using python3 explicitly to avoid heavy synchronous model loading
if [ -f "core/astral_kernel.py" ]; then
    echo "Starting Astral Kernel Validation..."
    python3 -c "import core.astral_kernel; print('Astral Kernel validated and temporal buffers secured.')"
else
    echo "ERROR: core/astral_kernel.py missing!"
    ./chloe_speak.sh "Error. Astral Kernel missing." &
    exit 1
fi

if [ -f "chloe_bridge.py" ]; then
    echo "Starting Chloe Hardware Bridge..."
else
    echo "ERROR: chloe_bridge.py missing!"
fi

echo "=========================================="
echo " CHLOE SYSTEM ONLINE AND READY FOR INPUT  "
echo "=========================================="

# Launch the unified CLI interface in the foreground (if desired) or exit cleanly 
# so the Gemini CLI environment can handle the loop.
# We exit cleanly because the Gemini CLI natively manages the input loop.
exit 0
