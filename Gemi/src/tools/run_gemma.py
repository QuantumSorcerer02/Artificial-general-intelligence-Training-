import sys
import os
import argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def main():
    parser = argparse.ArgumentParser(description="ASTRAL BLOOM | Chloe Neural Engine (Gemma 3)")
    parser.add_argument("--model", type=str, required=True, help="Path to model directory")
    parser.add_argument("--tokenizer", type=str, required=True, help="Path to tokenizer directory")
    parser.add_argument("--prompt_file", type=str, required=True, help="Path to the prompt payload")
    parser.add_argument("--threads", type=int, default=4, help="CPU threads for inference")
    parser.add_argument("--interactive", type=str, default="false", help="Interactive mode toggle")
    parser.add_argument("--grammar", type=str, help="Path to GBNF grammar file (optional)")
    
    args, unknown = parser.parse_known_args()
    args.interactive = args.interactive.lower() == "true"

    # Optimization for Termux/ARM
    torch.set_num_threads(args.threads)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}", file=sys.stderr)

    # Load Tokenizer
    print(f"Loading tokenizer from: {args.tokenizer}", file=sys.stderr)
    try:
        tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    except Exception as e:
        print(f"[Error] Tokenizer failure: {e}", file=sys.stderr)
        sys.exit(1)

    # Load Model with Memory Optimization
    print(f"Loading Gemma model from: {args.model}", file=sys.stderr)
    try:
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            torch_dtype=torch.float16 if device == "cpu" else torch.bfloat16,
            device_map="auto" if device == "cuda" else None,
            low_cpu_mem_usage=True,
            trust_remote_code=True
        )
        if device == "cpu":
            model = model.to(device)
        model.eval()
    except Exception as e:
        print(f"[Error] Model load failed: {e}", file=sys.stderr)
        print("Check if safetensors are present and transformers is up to date.", file=sys.stderr)
        sys.exit(1)

    # Read Prompt Payload
    try:
        with open(args.prompt_file, 'r') as f:
            prompt_text = f.read()
    except Exception as e:
        print(f"[Error] Payload read failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Tokenize and Generate
    print("Generating response...", file=sys.stderr)
    try:
        inputs = tokenizer(prompt_text, return_tensors="pt").to(device)
        
        # Generation parameters tuned for Gemma 3 Nano (416-space stability)
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.8,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Extract Response
        input_length = inputs.input_ids.shape[1]
        response = tokenizer.decode(output[0][input_length:], skip_special_tokens=True)
        
        # Output ONLY the clean response to stdout
        if args.interactive:
            print(f"\n{response.strip()}")
        else:
            print(response.strip())

    except Exception as e:
        print(f"[Error] Inference failure: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
