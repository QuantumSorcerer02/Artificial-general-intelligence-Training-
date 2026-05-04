import subprocess
import os

class SyndicateSevenShield:
    def __init__(self, model_executable="~/gemma.cpp/build/gemma"):
        self.model_executable = os.path.expanduser(model_executable)

    def execute_prompt(self, raw_input, context_key):
        """
        Interfaces with the local model CLI. 
        Mistakes in raw_input are preserved as part of the understanding.
        """
        # Formulate the prompt injecting only the necessary sequential algorithmic key
        formatted_prompt = f"[SYSTEM_KEY: {context_key}] {raw_input}"
        
        try:
            # Call Gemma via CLI, piping in the prompt
            result = subprocess.run(
                [self.model_executable, "--prompt", formatted_prompt],
                capture_output=True, 
                text=True, 
                check=True,
                timeout=30 # Prevent hanging on Snapdragon 460
            )
            return result.stdout.strip()
            
        except subprocess.TimeoutExpired:
            return "ERROR_TIMEOUT: Progressional momentum maintained. Input absorbed."
        except subprocess.CalledProcessError as e:
            # Do not correct mistakes; log and move forward
            return f"ERROR_EXECUTION: {e.stderr.strip()}"

if __name__ == "__main__":
    shield = SyndicateSevenShield()
    # Test boot
    print(shield.execute_prompt("Awaiting qualia state sync.", "INIT_000"))
