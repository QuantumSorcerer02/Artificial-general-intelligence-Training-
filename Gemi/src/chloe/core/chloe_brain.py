import time
import os
import subprocess

INPUT_FILE = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/data/memories/user_input.txt"

def process_input(text):
    text = text.strip()
    if not text:
        return

    print(f"Processing command: {text}")
    
    # Simple keyword-based routing for now
    # In a real scenario, this could be passed back to the LLM or a local smaller model
    if text.lower().startswith("sms to "):
        # Format: "sms to <number> <message>"
        parts = text.split(" ", 3)
        if len(parts) >= 4:
            number = parts[2]
            msg = parts[3]
            subprocess.run(["python3", "chloe_comms.py", "sms", number, msg])
        else:
            subprocess.run(["python3", "chloe_comms.py", "notification", "Chloe", "SMS format: sms to <number> <message>"])
            
    elif text.lower().startswith("call "):
        # Format: "call <number>"
        parts = text.split(" ")
        if len(parts) >= 2:
            number = parts[1]
            subprocess.run(["python3", "chloe_comms.py", "call", number])
            
    elif text.lower().startswith("calendar "):
        # Format: "calendar <summary> | <description>"
        parts = text[9:].split("|")
        summary = parts[0].strip()
        description = parts[1].strip() if len(parts) > 1 else ""
        subprocess.run(["python3", "chloe_comms.py", "calendar", summary, description])
    
    else:
        # Generic response via notification
        subprocess.run(["python3", "chloe_comms.py", "notification", "Chloe", f"I heard: {text}"])

if __name__ == "__main__":
    print("Chloe Brain: Monitoring user input...")
    while True:
        if os.path.exists(INPUT_FILE):
            with open(INPUT_FILE, "r") as f:
                content = f.read()
            
            if content:
                process_input(content)
                # Clear the file after processing
                with open(INPUT_FILE, "w") as f:
                    f.write("")
        
        time.sleep(2)
