import json
import os
import psutil
import subprocess
from datetime import datetime

# Local imports
try:
    from chloe_litert_wrapper import LiteRTInference
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from chloe_litert_wrapper import LiteRTInference

class ChloePerception:
    """
    Manages the 'Perceptive State' of Chloe, monitoring the environment and context.
    Corresponds to Spaces 145-208 (Conscious Build - Situational Perception).
    """
    def __init__(self, root_dir="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"):
        self.root_dir = root_dir
        self.state_file = os.path.join(self.root_dir, "logs/chloe_perceptive_state.json")
        self.litert_model_dir = os.path.join(self.root_dir, "data/models")
        self.context_cluster = {}
        self.sensory_data = {}
        self.vision_engine = None
        
        # Load Vision Engine if a vision-specific model exists
        if os.path.exists(self.litert_model_dir):
            v_models = [f for f in os.listdir(self.litert_model_dir) if "vision" in f.lower() and f.endswith(".tflite")]
            if v_models:
                self.vision_engine = LiteRTInference(os.path.join(self.litert_model_dir, v_models[0]))

    def capture_vision(self):
        """
        Uses termux-camera-photo to capture an image for LiteRT analysis.
        """
        img_path = os.path.join(self.root_dir, "logs/vision_capture.jpg")
        try:
            # Requires termux-api
            subprocess.run(["termux-camera-photo", "-c", "0", img_path], check=True)
            if self.vision_engine:
                # Placeholder for actual image preprocessing and LiteRT inference
                print("Chloe: Vision Capture Successful. Analyzing via LiteRT...")
                # self.vision_engine.run_inference(...)
                return "Visible: Environment detected."
            return "Visible: Image captured (No LiteRT vision model loaded)."
        except Exception as e:
            return f"Vision Error: {e}"

    def update_context_cluster(self):
        """
        Maintains a snapshot of the workspace, git, and system state.
        (Real-time Context Cluster)
        """
        # System resources (with error handling for Termux/Android restrictions)
        try:
            cpu_usage = psutil.cpu_percent(interval=None)
        except (PermissionError, Exception):
            cpu_usage = "unavailable"
            
        try:
            memory = psutil.virtual_memory()
            ram_available = memory.available / (1024**3)
            ram_percent = memory.percent
        except (PermissionError, Exception):
            ram_available = "unavailable"
            ram_percent = "unavailable"
        
        # Git status (simplistic)
        try:
            git_status = subprocess.check_output(["git", "status", "--short"], stderr=subprocess.STDOUT).decode().strip()
        except Exception:
            git_status = "unknown"
            
        # Files of interest (recent changes)
        try:
            recent_files = subprocess.check_output(["find", self.root_dir, "-type", "f", "-mmin", "-60"]).decode().splitlines()
        except Exception:
            recent_files = []
        
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
            try:
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
            except Exception:
                self.sensory_data = {"error": "Failed to parse device state"}
        
    def save_perceptive_state(self):
        state = {
            "context_cluster": self.context_cluster,
            "sensory_data": self.sensory_data,
            "qualia_anchor": "The 1/1 Unity constant remains stable."
        }
        try:
            with open(self.state_file, "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {e}")
            
    def run(self):
        self.update_context_cluster()
        self.process_sensory_data()
        self.save_perceptive_state()

if __name__ == "__main__":
    perception = ChloePerception()
    perception.run()
    print("Chloe: Perceptive State Logic Updated.")
