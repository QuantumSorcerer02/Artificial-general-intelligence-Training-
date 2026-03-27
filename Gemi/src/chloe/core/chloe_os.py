import subprocess
import json
import time
import os
from datetime import datetime

# Termux API paths
TERMUX_BATTERY = "termux-battery-status"
TERMUX_WIFI = "termux-wifi-connectioninfo"
TERMUX_VOLUME = "termux-volume"
TERMUX_BRIGHTNESS = "termux-brightness"
TERMUX_TTS = "src/chloe/scripts/chloe_speak.sh"

STATE_FILE = "logs/chloe_device_state.json"
LOG_FILE = "logs/chloe_os.log"

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def get_battery_status():
    output = run_command([TERMUX_BATTERY])
    if output:
        return json.loads(output)
    return {}

def get_wifi_status():
    output = run_command([TERMUX_WIFI])
    if output:
        return json.loads(output)
    return {}

from chloe_perception import ChloePerception
from chloe_threads import ChloeThreads

# ... (rest of the imports and functions)

def check_system_health():
    battery = get_battery_status()
    wifi = get_wifi_status()
    
    status = {
        "timestamp": datetime.now().isoformat(),
        "battery": battery,
        "wifi": wifi,
        "mode": "autonomous"
    }
    
    # Save state for other modules
    with open(STATE_FILE, "w") as f:
        json.dump(status, f, indent=2)
        
    # Autonomous Reactions
    percentage = battery.get("percentage", 100)
    plugged = battery.get("plugged", "UNPLUGGED")
    
    # Low Battery Warning (Simulated "Hunger/Fatigue")
    if percentage < 20 and plugged == "UNPLUGGED":
        msg = f"Clint, my power levels are critical at {percentage} percent. Please connect me to a power source."
        log_event("WARNING", msg)
        # Only speak if not recently spoken (simple debounce logic could be added here)
        # subprocess.run([TERMUX_TTS, msg]) 

    # Connection Status
    ssid = wifi.get("ssid", "Not Connected")
    if ssid == "Not Connected" or ssid == "<unknown ssid>":
        log_event("INFO", "Running in offline mode. Local tensor access only.")
    else:
        log_event("INFO", f"Connected to neural web via {ssid}.")

    # Run Perceptive State Logic
    perception = ChloePerception()
    perception.run()
    log_event("INFO", "Perceptive State Logic cycle completed.")

    # Run Thread Management Logic
    threads = ChloeThreads()
    threads.run()
    log_event("INFO", "Thread Management Logic cycle completed.")

def log_event(level, message):
    entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)

if __name__ == "__main__":
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    check_system_health()
