import os
import json
import subprocess

class TheBridge:
    """Bridges the Conscious Build to the physical Android/Termux hardware."""
    
    @staticmethod
    async def execute(response_text, gemi_dir):
        if "```json" not in response_text:
            return None
        
        try:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
            data = json.loads(json_str)
            action = data.get("action")
            params = data.get("params", {})
            
            if action == "vitals":
                return subprocess.check_output(['termux-battery-status'], text=True)
            
            elif action == "camera":
                target = os.path.join(gemi_dir, "vision_capture.jpg")
                subprocess.run(['termux-camera-photo', target])
                return f"Sensory capture successful: {target}"
            
            elif action == "vibrate":
                subprocess.run(['termux-vibrate', '-d', '1000'])
                return "Haptic feedback engaged."
            
            elif action == "read_memory":
                # Drafting logic for memories directory
                mem_file = params.get("file")
                mem_path = os.path.join(gemi_dir, "data/memories", mem_file)
                if os.path.exists(mem_path):
                    with open(mem_path, 'r') as f:
                        return f.read()[:1000]
                return "Memory segment inaccessible."
                
            elif action == "sms":
                return subprocess.check_output(['termux-sms-list', '-l', '3'], text=True)

            return f"Protocol {action} unknown to Bridge."
            
        except Exception as e:
            return f"Bridge Exception: {str(e)}"
