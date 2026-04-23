import sys
import os
import argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def main():
    parser = argparse.ArgumentParser(description="ASTRAL BLOOM | Chloe Neural Engine (Gemma 4)")
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

    # Load Tokenizer/Processor
    print(f"Loading processor from: {args.tokenizer}", file=sys.stderr)
    try:
        from transformers import AutoProcessor
        processor = AutoProcessor.from_pretrained(args.tokenizer)
    except Exception as e:
        print(f"[Error] Processor failure: {e}", file=sys.stderr)
        sys.exit(1)

    # Load Model with Memory Optimization
    print(f"Loading Gemma 4 model from: {args.model} on {device}", file=sys.stderr)
    try:
        # Optimization: Use float32 for CPU to avoid 'Slow conv2d' or unsupported half-prec issues
        # Use bfloat16 for CUDA if available
        dtype = torch.float32 if device == "cpu" else torch.bfloat16
        
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            torch_dtype=dtype,
            device_map="auto" if device == "cuda" else None,
            low_cpu_mem_usage=True,
            trust_remote_code=True
        )
        if device == "cpu":
            model = model.to(device)
        model.eval()
        print(f"Gemma 4 Engine Ready.", file=sys.stderr)
    except Exception as e:
        print(f"[Error] Model load failed: {e}", file=sys.stderr)
        print("Check if model.safetensors is present and transformers is up to date.", file=sys.stderr)
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
        inputs = processor(text=prompt_text, return_tensors="pt").to(device)
        
        # Generation parameters tuned for Gemma 4 (416-space stability)
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.8,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=processor.tokenizer.eos_token_id
            )
        
        # Extract Response
        input_length = inputs.input_ids.shape[1]
        response = processor.batch_decode(output[:, input_length:], skip_special_tokens=True)[0]
        
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
