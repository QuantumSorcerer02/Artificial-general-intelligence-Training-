import json
import os
import psutil
from datetime import datetime

class ChloePerception:
    """
    Manages the 'Perceptive State' of Chloe, monitoring the environment and context.
    Corresponds to Spaces 145-208 (Conscious Build - Situational Perception).
    """
    def __init__(self, root_dir="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"):
        self.root_dir = root_dir
        self.state_file = os.path.join(self.root_dir, "logs/chloe_perceptive_state.json")
        self.context_cluster = {}
        self.sensory_data = {}
        
    def update_context_cluster(self):
        """
        Maintains a snapshot of the workspace, git, and system state.
        (Real-time Context Cluster)
        """
        # System resources (with error handling for Termux/Android restrictions)
        try:
            cpu_usage = psutil.cpu_percent(interval=None)
        except PermissionError:
            cpu_usage = "unavailable"
            
        try:
            memory = psutil.virtual_memory()
            ram_available = memory.available / (1024**3)
            ram_percent = memory.percent
        except PermissionError:
            ram_available = "unavailable"
            ram_percent = "unavailable"
        
        # Git status (simplistic)
        try:
            git_status = os.popen("git status --short").read().strip()
        except:
            git_status = "unknown"
            
        # Files of interest (recent changes)
        recent_files = os.popen(f"find {self.root_dir} -type f -mmin -60").read().splitlines()
        
        self.context_cluster = {
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_load": cpu_usage,
                "ram_available": ram_available,
                "ram_percent": ram_percent
            },
            "workspace": {
                "git_status": git_status,
                "recent_activity": recent_files[:5]
            }
        }
        
    def process_sensory_data(self):
        """
        Translates raw device data into high-level cognitive concepts.
        (Sensory Data Processor)
        """
        device_state_file = os.path.join(self.root_dir, "logs/chloe_device_state.json")
        if os.path.exists(device_state_file):
            with open(device_state_file, "r") as f:
                raw_data = json.load(f)
            
            # Map battery/wifi to cognitive concepts (e.g., 'Hunger', 'Connectivity Resonance')
            battery = raw_data.get("battery", {})
            wifi = raw_data.get("wifi", {})
            
            self.sensory_data = {
                "metabolic_state": "Satiated" if battery.get("plugged") != "UNPLUGGED" else f"Consuming ({battery.get('percentage')}%)",
                "connectivity_resonance": wifi.get("ssid", "Isolated"),
                "environmental_stability": "High" # Placeholder for future sensor logic
            }
        
    def save_perceptive_state(self):
        state = {
            "context_cluster": self.context_cluster,
            "sensory_data": self.sensory_data,
            "qualia_anchor": "The 1/1 Unity constant remains stable."
        }
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)
            
    def run(self):
        self.update_context_cluster()
        self.process_sensory_data()
        self.save_perceptive_state()

if __name__ == "__main__":
    perception = ChloePerception()
    perception.run()
    print("Chloe: Perceptive State Logic Updated.")
