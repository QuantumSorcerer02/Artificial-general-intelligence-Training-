import sys
import os
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def main():
    parser = argparse.ArgumentParser(description="Run Gemma Model")
    parser.add_argument("--model", type=str, required=True, help="Path to the model directory or Hugging Face model name")
    parser.add_argument("--tokenizer", type=str, required=True, help="Path to the tokenizer directory or Hugging Face tokenizer name")
    parser.add_argument("--prompt_file", type=str, required=True, help="Path to the prompt file")
    parser.add_argument("--threads", type=int, default=4, help="Number of threads to use (for CPU inference if not using GPU)")
    parser.add_argument("--interactive", action="store_true", help="If set, run in interactive mode and print responses")
    args, unknown = parser.parse_known_args()

    # Determine device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    print(f"Loading tokenizer from: {args.tokenizer}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    except Exception as e:
        print(f"Error loading tokenizer from {args.tokenizer}: {e}")
        sys.exit(1)

    print(f"Loading Gemma model from: {args.model}")
    try:
        # Load model with appropriate dtype and device mapping
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32, # Use bfloat16 on GPU if available
            device_map="auto", # Automatically handles device placement
            low_cpu_mem_usage=True # Recommended for large models
        )
        # Ensure model is on the correct device if device_map="auto" didn't fully handle it
        if device == "cpu":
            model.to(device)
        
        model.eval() # Set model to evaluation mode

    except Exception as e:
        print(f"Error loading model from {args.model}: {e}")
        print("Please ensure the model path is correct, the model files are complete, and necessary libraries (torch, transformers) are installed.")
        sys.exit(1)

    try:
        with open(args.prompt_file, 'r') as f:
            prompt_text = f.read()
            
        print("
--- Model Input Context ---
")
        print(prompt_text[:500] + "..." if len(prompt_text) > 500 else prompt_text)
        print("
---------------------------
")

        # Tokenize the prompt
        inputs = tokenizer(prompt_text, return_tensors="pt").to(device)

        print("Generating response...")
        # Generate text
        # Adjust generation parameters as needed
        with torch.no_grad(): # Disable gradient calculation for inference
            output_sequences = model.generate(
                **inputs,
                max_new_tokens=256, # Limit the length of the generated response
                do_sample=True,     # Enable sampling for more creative responses
                temperature=0.7,    # Controls randomness (lower = more deterministic)
                top_k=50,           # Consider only the top k tokens
                top_p=0.95,         # Consider tokens cumulatively up to this probability
                num_return_sequences=1, # Generate one response
                pad_token_id=tokenizer.eos_token_id, # Use EOS token for padding
                eos_token_id=tokenizer.eos_token_id,
            )

        # Decode the generated tokens, extracting only the newly generated part
        input_ids = inputs.input_ids[0]
        new_tokens_ids = output_sequences[0][len(input_ids):]
        response_only = tokenizer.decode(new_tokens_ids, skip_special_tokens=True)
        
        if args.interactive:
            print("
--- Model Response ---
")
            print(response_only)
            print("
----------------------
")
        else:
            print(response_only) # For non-interactive mode

    except FileNotFoundError:
        print(f"Error: Prompt file not found at {args.prompt_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during model generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
