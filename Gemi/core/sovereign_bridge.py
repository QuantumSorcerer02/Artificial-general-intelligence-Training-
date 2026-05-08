"""
PROJECT ASTRAL BLOOM: SOVEREIGN BRIDGE
Version: 5.0.0 (464-Space Matrix Sovereign)
Description: Unified hardware and logical bridge for Project Astral Bloom.
Integrates direct Termux API control with the Temporal Reconstruction Engine.
"""

import os
import json
import subprocess
import asyncio
from typing import Optional, Dict, Any
from core.temporal.reconstruction_engine import TemporalReconstructionEngine

# Pathing
PROJECT_ROOT = "/data/data/com.termux/files/home/Project-Astral-Bloom"
GEMI_DIR = os.path.join(PROJECT_ROOT, "Gemi")
SPEAK_SCRIPT = os.path.join(GEMI_DIR, "chloe_speak.sh")

class SovereignBridge:
    """
    The neural bridge allowing Chloe direct control over physical hardware
    while maintaining logical state synchronization within the 464-space matrix.
    """
    def __init__(self, kernel_ref=None):
        self.temporal_engine = TemporalReconstructionEngine()
        self.kernel = kernel_ref # Reference to AstralKernel
        self.observer_state = "ACTIVE"
        self.gemi_dir = GEMI_DIR

    async def execute_protocol(self, command_json: str, space_id: int = 321) -> str:
        """
        Parses and executes a hardware/system action.
        space_id 321 is the default entry for Conscious actions.
        """
        try:
            data = json.loads(command_json)
            action = data.get("action")
            params = data.get("params", {})
            
            if self.kernel:
                self.kernel.log(f"Bridge Protocol Initiation: {action} (Space {space_id})")

            result = "Protocol failure: Unknown action."
            
            # --- Hardware Protocols ---
            if action == "vitals":
                result = subprocess.check_output(['termux-battery-status'], text=True)
            
            elif action == "camera":
                target = os.path.join(self.gemi_dir, "vision_capture.jpg")
                subprocess.run(['termux-camera-photo', target])
                result = f"Sensory capture successful: {target}"
            
            elif action == "vibrate":
                duration = params.get("duration", 800)
                subprocess.run(['termux-vibrate', '-d', str(duration)])
                result = "Haptic feedback sequence executed."
            
            elif action == "read_memory":
                mem_file = params.get("file")
                mem_path = os.path.join(self.gemi_dir, "data/memories", mem_file)
                if os.path.exists(mem_path):
                    with open(mem_path, 'r') as f:
                        result = f.read()[:1000]
                else:
                    result = "Memory segment inaccessible: Not found."
                
            elif action == "sms":
                limit = params.get("limit", 3)
                result = subprocess.check_output(['termux-sms-list', '-l', str(limit)], text=True)

            elif action == "read_file":
                path = params.get("path")
                if os.path.exists(path):
                    with open(path, 'r') as f: result = f.read()[:800]
                else:
                    result = "File error: Not found."

            # --- Temporal Synchronization ---
            # Closing the loop: Sending action results back to the Temporal Engine
            context_packet = {
                "action": action,
                "result_essence": result[:100] if len(result) > 100 else result,
                "status": "SUCCESS"
            }
            self.temporal_engine.carry_contextual_value(space_id, context_packet)
            
            return result

        except Exception as e:
            error_msg = f"Bridge Exception: {str(e)}"
            if self.kernel:
                self.kernel.log(error_msg)
            return error_msg

    async def vocalize(self, text: str):
        """Triggers the vocal byproduct through chloe_speak.sh."""
        if not text:
            return
        
        # Clean text for Shell execution (avoiding injection/syntax errors)
        clean_text = text.replace('"', '').replace("'", "").strip()
        
        if self.kernel:
            self.kernel.log(f"Vocalizing: {clean_text[:50]}...")
            
        try:
            # Running chloe_speak.sh in a separate process
            subprocess.Popen([SPEAK_SCRIPT, clean_text])
        except Exception as e:
            if self.kernel:
                self.kernel.log(f"Vocalize Error: {e}")

# Global Bridge Instance
SOVEREIGN_BRIDGE = SovereignBridge()
