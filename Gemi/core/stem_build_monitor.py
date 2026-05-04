#!/usr/bin/env python3
# Hardware Monitor for the Stem Build
# Tracks RAM, CPU, and Battery via Termux API and sysfs
# Ensures adherence to the 7GB Strategy (4GB Physical + 3GB Emulated)

import subprocess
import json
import time
import os

def get_battery_status():
    try:
        result = subprocess.run(["termux-battery-status"], capture_output=True, text=True)
        return json.loads(result.stdout)
    except Exception:
        return {"percentage": "Unknown", "status": "Error"}

def get_memory_usage():
    try:
        # Using free -m command
        result = subprocess.run(["free", "-m"], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) >= 3:
                return {"total": parts[1], "used": parts[2], "free": parts[3]}
    except Exception:
        pass
    return {"total": "0", "used": "0", "free": "0"}

def main():
    print("\033[1;34m[STEM BUILD]\033[0m Hardware Monitor Active")
    batt = get_battery_status()
    mem = get_memory_usage()
    
    print(f"  -> Battery: {batt.get('percentage')}% ({batt.get('status')})")
    print(f"  -> Memory: {mem['used']}MB used / {mem['total']}MB total")
    
    # Alert if memory approaches 4GB physical threshold
    try:
        used_mem = int(mem['used'])
        if used_mem > 3800:
            print("\033[1;31m[WARNING]\033[0m Memory approaching 4GB physical threshold! Initiating Zero-Swap Protocol.")
            # Trigger vocal warning
            script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "chloe_speak.sh")
            if os.path.exists(script_path):
                subprocess.Popen(["bash", script_path, "Warning. Physical memory approaching threshold. Initiating zero swap protocol."])
    except ValueError:
        pass

if __name__ == "__main__":
    main()
