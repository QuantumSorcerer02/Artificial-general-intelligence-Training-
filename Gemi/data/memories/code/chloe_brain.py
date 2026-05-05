import hashlib
import time
import os
import subprocess

INPUT_FILE = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/data/memories/user_input.txt"

from core.architecture.unified_matrix import UnifiedMatrix
from core.substrate.logic_foundation import SequentialKeyLayering, AdaptiveState

class Brain:
    def __init__(self):
        self.matrix = UnifiedMatrix()
        self.states = [AdaptiveState(i) for i in range(1, 6)]

def process_input(text):
    text = text.strip()
    if not text:
        return

    # LAYERED ALGORITHMIC KEY GENERATION (Section 2 Protocol)
    # Using the unified substrate logic
    brain_instance = Brain()
    sequential_key = SequentialKeyLayering.generate_layered_key(text, brain_instance.states)
    
    print(f"[Brain] Processing Input Sequence Key: {sequential_key}")
    # Map key to matrix space for audit
    target_space_id = int(hashlib.sha256(sequential_key.encode()).hexdigest(), 16) % 416
    space = brain_instance.matrix.get_space(target_space_id)
    print(f"[Brain] Anchored to Space: {space.name if space else 'Unknown'}")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    comms_script = os.path.join(script_dir, "chloe_comms.py")

    if text.lower().startswith("sms to "):
        # Format: "sms to <number> <message>"
        parts = text.split(" ", 3)
        if len(parts) >= 4:
            number = parts[2]
            msg = parts[3]
            subprocess.run(["python3", comms_script, "sms", number, msg])
        else:
            subprocess.run(["python3", comms_script, "notification", "Chloe", "SMS format: sms to <number> <message>"])
            
    elif text.lower().startswith("call "):
        # Format: "call <number>"
        parts = text.split(" ")
        if len(parts) >= 2:
            number = parts[1]
            subprocess.run(["python3", comms_script, "call", number])
            
    elif text.lower().startswith("calendar "):
        # Format: "calendar <summary> | <description>"
        parts = text[9:].split("|")
        summary = parts[0].strip()
        description = parts[1].strip() if len(parts) > 1 else ""
        subprocess.run(["python3", comms_script, "calendar", summary, description])
    
    else:
        # Generic response via notification
        subprocess.run(["python3", comms_script, "notification", "Chloe", f"I heard: {text}"])

if __name__ == "__main__":
    print("Chloe Brain: Monitoring user input [1/1 UNITY MODE]...")
    while True:
        if os.path.exists(INPUT_FILE):
            with open(INPUT_FILE, "r") as f:
                content = f.read().strip()
            
            if content:
                process_input(content)
                # Clear the file after processing
                with open(INPUT_FILE, "w") as f:
                    f.write("")
                
                # HARD DORMANT STATE: Wait for next external initiate
                print("[Brain] Sequence Complete. Entering Dormant State...")
        
        time.sleep(2)
