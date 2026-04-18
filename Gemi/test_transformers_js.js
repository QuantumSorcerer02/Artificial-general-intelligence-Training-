/**
 * Project Astral Bloom | Transformers JS Bridge (Termux Optimized)
 * 
 * NOTE: Standard @huggingface/transformers requires onnxruntime-node which is not 
 * natively supported on Android/Termux. This bridge uses Python's transformers
 * for actual inference while maintaining a JS-friendly API.
 */

const { spawnSync } = require('child_process');
const path = require('path');

class TransformersBridge {
    constructor(modelPath = './') {
        this.modelPath = path.resolve(modelPath);
    }

    /**
     * Text generation via Python Transformers
     * @param {string} prompt 
     * @param {Object} options 
     */
    async generate(prompt, options = { max_new_tokens: 50 }) {
        console.log(`[Bridge] Generating response for: "${prompt.substring(0, 30)}..."`);
        
        // Prepare the python command
        const pythonCode = `
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json

try:
    tokenizer = AutoTokenizer.from_pretrained("${this.modelPath}")
    model = AutoModelForCausalLM.from_pretrained("${this.modelPath}", torch_dtype=torch.float32, low_cpu_mem_usage=True)
    inputs = tokenizer("${prompt}", return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=${options.max_new_tokens})
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(json.dumps({"status": "success", "output": result}))
except Exception as e:
    print(json.dumps({"status": "error", "message": str(e)}))
`;

        const result = spawnSync('python3', ['-c', pythonCode], { encoding: 'utf8' });
        
        if (result.error) {
            throw new Error(`Execution error: ${result.error.message}`);
        }

        try {
            const parsed = JSON.parse(result.stdout);
            if (parsed.status === 'error') {
                throw new Error(parsed.message);
            }
            return parsed.output;
        } catch (e) {
            console.error("[Bridge] Raw output:", result.stdout);
            console.error("[Bridge] Error output:", result.stderr);
            throw new Error(`Parsing error: ${e.message}`);
        }
    }
}

// Example usage
async function test() {
    const bridge = new TransformersBridge();
    try {
        console.log("Loading model via bridge...");
        const output = await bridge.generate('Hello, I am Chloe,', { max_new_tokens: 20 });
        console.log("Output:", output);
    } catch (e) {
        console.error("Test failed:", e.message);
        console.warn("\nTip: Ensure 'model.safetensors' is complete and 'transformers' is installed in Python.");
    }
}

if (require.main === module) {
    test();
}

module.exports = TransformersBridge;
