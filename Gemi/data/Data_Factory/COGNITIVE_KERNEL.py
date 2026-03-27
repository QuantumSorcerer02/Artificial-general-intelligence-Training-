import json
import os
import time
import subprocess
from datetime import datetime

# Paths - Adjusted for new structure (Gemi/data/memories, etc.)
# ROOT_DIR points to .../Project-Astral-Bloom/Gemi
ROOT_DIR = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
INPUT_FILE = os.path.join(ROOT_DIR, "data/memories/user_input.txt")
CONV_FILE = os.path.join(ROOT_DIR, "data/memories/saved/conversations/conversation.md")
CHLOE_MD = os.path.join(ROOT_DIR, "CHLOE.md")
MASTER_CONTEXT = os.path.join(ROOT_DIR, "ASTRAL_BLOOM_MASTER_CONTEXT.txt")

class CognitiveKernel:
    """
    The Master Sync & Observer for Astral Bloom.
    Automatically sorts, places, and updates all architectural files in real-time.
    """
    def __init__(self):
        self.last_processed_input = ""
        self.is_active = True
        
    def log_interaction(self, user_text, chloe_text=""):
        """Appends the interaction to the rolling context immediately."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n\n**[{timestamp}] USER**: {user_text}\n"
        if chloe_text:
            entry += f"**CHLOE**: {chloe_text}\n"
            
        with open(CONV_FILE, "a") as f:
            f.write(entry)
        print(f"Kernel: Interaction logged to {CONV_FILE}")

    def update_architecture(self, context_summary):
        """Analyzes text for architectural changes and updates CHLOE.md/Data_Factory."""
        # This function scans for keywords like 'fail', 'principle', 'logic'
        # and updates the CHLOE.md status.
        if "fail" in context_summary.lower() or "error" in context_summary.lower():
            # Trigger 'Observed Failure' logic update
            with open(CHLOE_MD, "r") as f:
                content = f.read()
            if "Identity State: ACTIVE" in content:
                new_content = content.replace("Identity State: ACTIVE", "Identity State: EVOLVING (Error Correction Active)")
                with open(CHLOE_MD, "w") as f:
                    f.write(new_content)
                print("Kernel: Architecture updated to EVOLVING state.")

    def sync_master_context(self):
        """Periodically refreshes the Master Context file for global observation."""
        # Simple head-based synthesis for now to avoid huge file reads
        cmd = f"head -n 100 {CONV_FILE} > {MASTER_CONTEXT}.tmp && mv {MASTER_CONTEXT}.tmp {MASTER_CONTEXT}"
        subprocess.run(cmd, shell=True)
        print("Kernel: Master Context synced.")

    def run_loop(self):
        print("Chloe Cognitive Kernel: MONITORING SYNC...")
        while self.is_active:
            # 1. Check for new input from the notification/terminal
            if os.path.exists(INPUT_FILE):
                with open(INPUT_FILE, "r") as f:
                    content = f.read().strip()
                
                if content and content != self.last_processed_input:
                    self.log_interaction(content)
                    self.update_architecture(content)
                    self.sync_master_context()
                    self.last_processed_input = content
                    # Note: We don't clear the file here; chloe_brain.py does that.
                    # Or we merge them.
            
            time.sleep(5) # 5-second sync cycle

if __name__ == "__main__":
    kernel = CognitiveKernel()
    try:
        kernel.run_loop()
    except KeyboardInterrupt:
        print("Kernel: Shutdown.")
