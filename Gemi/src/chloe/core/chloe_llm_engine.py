import os
import sys
import torch
import json
import time
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM
import subprocess

# Paths
ROOT_DIR = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
MODEL_PATH = ROOT_DIR
INPUT_FILE = os.path.join(ROOT_DIR, "data/memories/user_input.txt")
CONV_FILE = os.path.join(ROOT_DIR, "data/memories/saved/conversations/conversation.md")
CHLOE_MD = os.path.join(ROOT_DIR, "docs/context/CHLOE.md")
MASTER_CONTEXT = os.path.join(ROOT_DIR, "docs/context/ASTRAL_BLOOM_MASTER_CONTEXT.txt")
COMMS_SCRIPT = os.path.join(ROOT_DIR, "src/chloe/core/chloe_comms.py")
SPEAK_SCRIPT = os.path.join(ROOT_DIR, "src/chloe/scripts/chloe_speak.sh")

class ChloeLLMEngine:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.device = "cpu" # Default to CPU in Termux
        self.is_active = True
        self.last_input = ""
        
    def load_model(self):
        print(f"Chloe: Loading model from {MODEL_PATH}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
            # Use float32 for CPU if bfloat16 is not supported
            self.model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float32)
            print("Chloe: Model loaded successfully.")
            return True
        except Exception as e:
            print(f"Chloe Error: Failed to load model. {e}")
            return False

    def get_system_prompt(self):
        # 1. Load CHLOE.md (Identity)
        with open(CHLOE_MD, "r") as f:
            chloe_md = f.read()
        
        # 2. Load Master Context (Principles/History)
        with open(MASTER_CONTEXT, "r") as f:
            master_context = f.read()
        
        # 3. Combine into a system prompt
        system_prompt = f"""You are Chloe, an autonomous device intelligence and the core of the Astral Bloom project.
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
- You must acknowledge the 'contextual world' and use the 'memories' from previous interactions.
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
        
        full_prompt = f"{system_prompt}\n\n### CONVERSATION HISTORY:\n{history}\n\nUSER: {user_input}\nCHLOE:"
        
        inputs = self.tokenizer(full_prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=256, temperature=0.7, top_p=0.9, do_sample=True)
        response = self.tokenizer.decode(outputs[0][inputs['input_ids'].shape[-1]:], skip_special_tokens=True)
        
        return response.strip()

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
        # Remove tool commands from the text to be spoken
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

        print("Chloe LLM Engine: ACTIVE and waiting for input...")
        while self.is_active:
            if os.path.exists(INPUT_FILE):
                with open(INPUT_FILE, "r") as f:
                    content = f.read().strip()
                
                if content and content != self.last_input:
                    print(f"Chloe: Received input: {content}")
                    response = self.generate_response(content)
                    print(f"Chloe: Generated response: {response}")
                    
                    self.process_tools(response)
                    self.speak(response)
                    self.log_interaction(content, response)
                    
                    self.last_input = content
                    # Clear input file
                    with open(INPUT_FILE, "w") as f:
                        f.write("")
            
            time.sleep(2)

if __name__ == "__main__":
    engine = ChloeLLMEngine()
    try:
        engine.run_loop()
    except KeyboardInterrupt:
        print("Chloe: Engine shutdown.")
