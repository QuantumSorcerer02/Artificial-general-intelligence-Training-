import json
import os
import time
import subprocess
from datetime import datetime

# Paths
ROOT_DIR = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
INPUT_FILE = os.path.join(ROOT_DIR, "data/memories/user_input.txt")
CONV_FILE = os.path.join(ROOT_DIR, "data/memories/saved/conversations/conversation.md")
CHLOE_MD = os.path.join(ROOT_DIR, "docs/context/CHLOE.md")
MASTER_CONTEXT = os.path.join(ROOT_DIR, "docs/context/ASTRAL_BLOOM_MASTER_CONTEXT.txt")
SYSTEM_ALERT_FILE = os.path.join(ROOT_DIR, "data/memories/system_alerts.txt")

class CognitiveKernel:
    """
    The Master Sync & Observer for Astral Bloom.
    Monitors system state (Battery, WiFi) and syncs the architectural context.
    """
    def __init__(self):
        self.last_processed_input = ""
        self.is_active = True
        self.last_battery_alert = 0
        
    def log_interaction(self, user_text, chloe_text="", role="USER"):
        """Appends the interaction to the rolling context immediately."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n\n**[{timestamp}] {role}**: {user_text}\n"
        if chloe_text:
            entry += f"**CHLOE**: {chloe_text}\n"
            
        with open(CONV_FILE, "a") as f:
            f.write(entry)

    def check_system_state(self):
        """Monitors hardware via Termux API and injects alerts if necessary."""
        try:
            # Check Battery
            res = subprocess.check_output(["termux-battery-status"], text=True)
            data = json.loads(res)
            level = data.get("percentage", 100)
            status = data.get("status", "UNKNOWN")
            
            # Low Battery Alert (below 15%)
            if level < 15 and status != "CHARGING" and (time.time() - self.last_battery_alert > 1800):
                alert_msg = f"SYSTEM_ALERT: Battery critical ({level}%). Cognitive stability compromised."
                with open(SYSTEM_ALERT_FILE, "a") as f:
                    f.write(alert_msg + "\n")
                self.last_battery_alert = time.time()
                print(f"Kernel: Low battery alert injected.")

        except Exception as e:
            print(f"Kernel: Error checking system state: {e}")

    def update_architecture(self, context_summary):
        """Analyzes text for architectural changes and updates CHLOE.md."""
        if any(kw in context_summary.lower() for kw in ["fail", "error", "critical"]):
            with open(CHLOE_MD, "r") as f:
                content = f.read()
            if "Identity State: ACTIVE" in content:
                new_content = content.replace("Identity State: ACTIVE", "Identity State: EVOLVING (System Recovery Active)")
                with open(CHLOE_MD, "w") as f:
                    f.write(new_content)
                print("Kernel: Architecture updated to EVOLVING state.")

    def sync_master_context(self):
        """Periodically refreshes the Master Context file for global observation."""
        if os.path.exists(CONV_FILE):
            # Keep the last 100 lines for the master context
            cmd = f"tail -n 100 {CONV_FILE} > {MASTER_CONTEXT}"
            subprocess.run(cmd, shell=True)

    def run_loop(self):
        print("\033[1;34m[Kernel]\033[0m MONITORING SYNC & SENSORIUM...")
        cycle = 0
        while self.is_active:
            # 1. Check for user input
            if os.path.exists(INPUT_FILE):
                with open(INPUT_FILE, "r") as f:
                    content = f.read().strip()
                if content and content != self.last_processed_input:
                    self.log_interaction(content)
                    self.update_architecture(content)
                    self.last_processed_input = content
            
            # 2. Check system hardware (every 60 seconds)
            if cycle % 12 == 0:
                self.check_system_state()
                self.sync_master_context()
            
            cycle += 1
            time.sleep(5)

if __name__ == "__main__":
    kernel = CognitiveKernel()
    try:
        kernel.run_loop()
    except KeyboardInterrupt:
        print("Kernel: Shutdown.")
