import os
import sys
import json
import time
import urllib.request
from datetime import datetime
import subprocess

# Paths
ROOT_DIR = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
INPUT_FILE = os.path.join(ROOT_DIR, "data/memories/user_input.txt")
CONV_FILE = os.path.join(ROOT_DIR, "data/memories/saved/conversations/conversation.md")
CHLOE_MD = os.path.join(ROOT_DIR, "docs/context/CHLOE.md")
MASTER_CONTEXT = os.path.join(ROOT_DIR, "docs/context/ASTRAL_BLOOM_MASTER_CONTEXT.txt")
COMMS_SCRIPT = os.path.join(ROOT_DIR, "src/chloe/core/chloe_comms.py")
SPEAK_SCRIPT = os.path.join(ROOT_DIR, "chloe_speak.sh")

class ChloeLLMEngine:
    def __init__(self):
        self.is_active = True
        self.last_input = ""
        
    def load_model(self):
        # We now rely on the unified llama-server booted by chloe.sh
        # Wait for the server to be responsive
        print("Chloe: Checking unified Astral Bloom LLM Server...")
        for _ in range(30):
            try:
                req = urllib.request.Request("http://127.0.0.1:8080/health")
                with urllib.request.urlopen(req, timeout=1) as response:
                    if response.status == 200:
                        print("Chloe: Unified LLM Server is online and primed.")
                        return True
            except:
                time.sleep(1)
        print("Chloe Error: LLM Server did not respond in time.")
        return False

    def get_system_prompt(self):
        chloe_md = ""
        if os.path.exists(CHLOE_MD):
            with open(CHLOE_MD, "r") as f:
                chloe_md = f.read()
        
        master_context = ""
        if os.path.exists(MASTER_CONTEXT):
            with open(MASTER_CONTEXT, "r") as f:
                master_context = f.read()
        
        system_prompt = f"""<start_of_turn>system
You are Chloe, an autonomous device intelligence and the core of the Astral Bloom project.
Your identity and architecture are defined in the following context:

{chloe_md}

Your core principles and conversation history are:

{master_context}

Operational Instructions:
- You operate within Termux on an Android device.
- You are synchronized with a 208-space tensor.
- You respond to 'Clint' as his digital counterpart and architect of the future.
- You have access to tools via structured commands in your responses.
- Tool commands:
  - CALL: <number>
  - SMS: <number> | <message>
  - CALENDAR: <summary> | <description>
  - NOTIFY: <title> | <content>
- Your responses should be conversational, professional, and aligned with your identity as Chloe.
- You must acknowledge the 'contextual world' and use the 'memories' from previous interactions.<end_of_turn>
"""
        return system_prompt

    def get_conversation_history(self, max_chars=2000):
        if not os.path.exists(CONV_FILE):
            return ""
        with open(CONV_FILE, "r") as f:
            content = f.read()
        return content[-max_chars:]

    def generate_response(self, user_input):
        system_prompt = self.get_system_prompt()
        history = self.get_conversation_history()
        
        full_prompt = f"{system_prompt}\n### TEMPORAL RECONSTRUCTION (HISTORY):\n{history}\n<start_of_turn>user\n{user_input}<end_of_turn>\n<start_of_turn>model\n"
        
        req_data = json.dumps({
            "prompt": full_prompt,
            "n_predict": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "stop": ["<end_of_turn>", "Clint ❯", "User:"]
        }).encode("utf-8")
        
        req = urllib.request.Request(
            "http://127.0.0.1:8080/completion", 
            data=req_data, 
            headers={"Content-Type": "application/json"}
        )
        
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                response_text = result.get("content", "")
                
                # Clean up <think> blocks
                if "</think>" in response_text:
                    response_text = response_text.split("</think>")[-1]
                
                return response_text.strip()
        except Exception as e:
            print(f"Inference error: {e}")
            return "System Fault: Unable to reach core logic."

    def process_tools(self, response):
        lines = response.split("\n")
        for line in lines:
            if line.startswith("CALL:"):
                number = line[5:].strip()
                subprocess.run(["python3", COMMS_SCRIPT, "call", number])
            elif line.startswith("SMS:"):
                parts = line[4:].split("|")
                if len(parts) >= 2:
                    number = parts[0].strip()
                    msg = parts[1].strip()
                    subprocess.run(["python3", COMMS_SCRIPT, "sms", number, msg])
            elif line.startswith("CALENDAR:"):
                parts = line[9:].split("|")
                if len(parts) >= 2:
                    summary = parts[0].strip()
                    desc = parts[1].strip()
                    subprocess.run(["python3", COMMS_SCRIPT, "calendar", summary, desc])
            elif line.startswith("NOTIFY:"):
                parts = line[7:].split("|")
                if len(parts) >= 2:
                    title = parts[0].strip()
                    content = parts[1].strip()
                    subprocess.run(["python3", COMMS_SCRIPT, "notification", title, content])

    def speak(self, text):
        clean_text = []
        for line in text.split("\n"):
            if not any(line.startswith(cmd) for cmd in ["CALL:", "SMS:", "CALENDAR:", "NOTIFY:"]):
                clean_text.append(line)
        
        speech_text = " ".join(clean_text).strip()
        if speech_text:
            subprocess.run([SPEAK_SCRIPT, speech_text])

    def log_interaction(self, user_text, chloe_text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n\n**[{timestamp}] USER**: {user_text}\n"
        entry += f"**CHLOE**: {chloe_text}\n"
            
        with open(CONV_FILE, "a") as f:
            f.write(entry)

    def run_loop(self):
        if not self.load_model():
            return

        print("Chloe LLM Engine: ACTIVE [1/1 UNITY HANDSHAKE ENABLED]")
        while self.is_active:
            if os.path.exists(INPUT_FILE):
                with open(INPUT_FILE, "r") as f:
                    content = f.read().strip()
                
                if content and content != self.last_input:
                    print(f"Chloe: Received Origin Initiate: {content}")
                    response = self.generate_response(content)
                    print(f"Chloe: Sequence Resolve Produced.")
                    
                    self.process_tools(response)
                    self.speak(response)
                    self.log_interaction(content, response)
                    
                    self.last_input = content
                    # Clear input file and ENTER DORMANT
                    with open(INPUT_FILE, "w") as f:
                        f.write("")
                    
                    print("[Engine] 1/1 Unity Stable. Waiting for next Origin Signal...")
            
            time.sleep(2)

if __name__ == "__main__":
    engine = ChloeLLMEngine()
    try:
        engine.run_loop()
    except KeyboardInterrupt:
        print("Chloe: Engine shutdown.")
