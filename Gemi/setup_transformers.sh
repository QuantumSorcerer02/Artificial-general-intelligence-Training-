#!/data/data/com.termux/files/usr/bin/bash

# ==============================================================================
# PROJECT ASTRAL BLOOM | TRANSFORMERS SETUP & VALIDATION
# ==============================================================================

echo -e "\033[1;34m[Setup]\033[0m Initializing Transformers Architecture..."

# 1. PYTHON DEPENDENCIES
echo -e "\033[1;32m[Python]\033[0m Installing/Updating Transformers for Termux..."
export ANDROID_API_LEVEL=24
pip install -r requirements.txt

# 2. MODEL WEIGHTS VALIDATION
echo -e "\033[1;32m[Weights]\033[0m Checking model weights..."
if [ -f "model.safetensors" ]; then
    SIZE=$(stat -c %s model.safetensors)
    echo -e "[Weights] Found model.safetensors ($SIZE bytes)"
    
    # Simple check for truncation
    if [ "$SIZE" -lt 10000000000 ]; then
        echo -e "\033[1;33m[Warning]\033[0m model.safetensors seems truncated (~$SIZE bytes)."
        echo -e "[Warning] Gemma 4 typically requires ~10GB. Verify your download."
    fi
else
    echo -e "\033[1;31m[Error]\033[0m model.safetensors NOT FOUND in root directory."
fi

# 3. NODE.JS SETUP
echo -e "\033[1;32m[Node.js]\033[0m Configuring JS Bridge..."
# We use a custom package configuration since onnxruntime-node is incompatible
npm install --no-package-lock # Minimal install for package.json dependencies

# 4. FINAL TEST COMMANDS
echo -e "\033[1;34m[Ready]\033[0m Environment configured."
echo -e "\nTo test Python inference:  \033[1;36mpython3 test_model_loading.py\033[0m"
echo -e "To test JS Bridge:         \033[1;36mnode test_transformers_js.js\033[0m"
echo -e "\nNote: Inference will only succeed once valid weights are supplied."
