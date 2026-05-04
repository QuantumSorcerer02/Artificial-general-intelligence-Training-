import os
import sys
import time
import json
from datetime import datetime

# Adjust Python path to load local modules
ROOT_DIR = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
sys.path.append(ROOT_DIR)

from src.chloe.core.chloe_os import check_system_health
from src.chloe.core.chloe_perception import ChloePerception
from src.chloe.core.chloe_llm_engine import ChloeLLMEngine
from src.chloe.core.chloe_reminders import check_and_trigger
from core.architecture.unified_matrix import UnifiedMatrix

INPUT_FILE = os.path.join(ROOT_DIR, "data/memories/user_input.txt")
STATE_FILE = os.path.join(ROOT_DIR, "logs/unified_scheduler.log")

class UnifiedAutonomyScheduler:
    def __init__(self):
        self.llm_engine = ChloeLLMEngine()
        self.perception = ChloePerception()
        self.matrix = UnifiedMatrix()
        self.tick = 0
        
    def log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(STATE_FILE, "a") as f:
            f.write(f"[{timestamp}] [UAS] {msg}\n")
        print(f"[UAS] {msg}")

    def run(self):
        self.log("Booting Unified Autonomy Scheduler (UAS)...")
        
        if not self.llm_engine.load_model():
            self.log("CRITICAL: Failed to connect to unified llama-server.")
            return

        self.log("UAS 1/1 Unity Handshake Established. Entering main autonomous loop.")

        while True:
            # 1. High-Frequency Tick (every 2 seconds)
            # Check physical device health (battery, wifi, tools)
            try:
                check_system_health()
            except Exception as e:
                self.log(f"OS Health Check Error: {e}")
                
            # Check pending user inputs (Replaces chloe_brain and chloe_llm_engine overlap)
            if os.path.exists(INPUT_FILE):
                try:
                    with open(INPUT_FILE, "r") as f:
                        content = f.read().strip()
                        
                    if content and content != self.llm_engine.last_input:
                        self.log(f"Origin Initiate Received: {content}")
                        response = self.llm_engine.generate_response(content)
                        self.log("Sequence Resolve Produced.")
                        
                        # Route through deterministic tool processor
                        self.llm_engine.process_tools(response)
                        self.llm_engine.speak(response)
                        self.llm_engine.log_interaction(content, response)
                        
                        self.llm_engine.last_input = content
                        # Clear to enter dormant state
                        with open(INPUT_FILE, "w") as f:
                            f.write("")
                except Exception as e:
                    self.log(f"Input Processing Error: {e}")

            # 2. Medium-Frequency Tick (every 10 seconds)
            if self.tick % 5 == 0:
                try:
                    check_and_trigger() # Check pending reminders
                except Exception as e:
                    pass

            # 3. Low-Frequency Tick (every 60 seconds)
            if self.tick % 30 == 0:
                try:
                    self.perception.run() # Update perceptive world state
                except Exception as e:
                    self.log(f"Perception Update Error: {e}")
            
            time.sleep(2)
            self.tick += 1

if __name__ == "__main__":
    scheduler = UnifiedAutonomyScheduler()
    try:
        scheduler.run()
    except KeyboardInterrupt:
        print("\n[UAS] Graceful shutdown.")
