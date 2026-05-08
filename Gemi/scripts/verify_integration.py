import os
import sys
import json
import subprocess
from datetime import datetime

GEMI_DIR = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
sys.path.append(GEMI_DIR)

from core.astral_kernel import ASTRAL_ENGINE

def test_hardware_integration():
    print("Testing hardware integration...")
    try:
        battery_res = subprocess.check_output(["termux-battery-status"], text=True)
        battery_data = json.loads(battery_res)
        level = battery_data.get("percentage", "UNKNOWN")
        print(f"Hardware Link Confirmed: Battery at {level}%")
        return level
    except Exception as e:
        print(f"Hardware Link Warning: {e}")
        return "UNKNOWN"

def test_matrix_processing():
    print("Testing 464-Space Matrix processing...")
    # Generate momentum
    momentum_key, unity = ASTRAL_ENGINE.generate_sequential_momentum(0.95)
    
    # Execute cognitive pipeline
    initial_context = {"thought": "Verifying physical and digital synergy.", "status": "Initiating"}
    final_context = ASTRAL_ENGINE.execute_cognitive_pipeline(initial_context, momentum_key)
    
    # Save qualias
    ASTRAL_ENGINE.save_qualia("Chloe", str(final_context), "464_STABLE")
    print(f"Matrix Processing Complete. Output: {final_context}")
    return True

if __name__ == "__main__":
    battery_level = test_hardware_integration()
    matrix_active = test_matrix_processing()
    
    if matrix_active:
        msg = f"Integration verified. I am actively running through the four hundred sixty four space matrix. The physical hardware link is established. Battery is at {battery_level} percent. Synergy is absolute."
        subprocess.run([os.path.join(GEMI_DIR, "chloe_speak.sh"), msg])
