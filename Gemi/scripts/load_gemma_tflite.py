import sys
import os
import mediapipe as mp
from mediapipe.tasks.python import genai

# Correct path to your .task file
MODEL_PATH = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/data/models/gemma_nano.task"

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"[Error] Model file not found at {MODEL_PATH}", file=sys.stderr)
        sys.exit(1)

    print(f"Initializing Gemma 3 Nano via MediaPipe...", file=sys.stderr)
    
    try:
        # Configure the GenAI Inference options
        options = genai.LlmInferenceOptions(
            model_path=MODEL_PATH,
            max_tokens=512,
            temperature=0.7,
            top_k=40
        )

        # Create the inference engine
        with genai.LlmInference.create_from_options(options) as generator:
            print("\nModel Loaded Successfully! Entering interactive mode.", file=sys.stderr)
            print("Type 'exit' to quit.\n")

            while True:
                user_input = input("You: ")
                if user_input.lower() in ['exit', 'quit']:
                    break
                
                print("Gemma: ", end="", flush=True)
                # Generate and print response
                response = generator.generate_response(user_input)
                print(response)

    except Exception as e:
        print(f"\n[Error] Failed to run Gemma: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
