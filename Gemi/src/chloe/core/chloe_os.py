import subprocess
import json
import time
import os
from datetime import datetime
from core.substrate.logic_foundation import SequentialKeyLayering, AdaptiveState

# Termux API paths
TERMUX_BATTERY = "termux-battery-status"
TERMUX_WIFI = "termux-wifi-connectioninfo"
TERMUX_VOLUME = "termux-volume"
TERMUX_BRIGHTNESS = "termux-brightness"
TERMUX_TTS = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/chloe_speak.sh"

STATE_FILE = "logs/chloe_device_state.json"
LOG_FILE = "logs/chloe_os.log"
TOOL_INPUT = "tmp/chloe_sovereign_tool.json"

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except:
        return None

def get_battery_status():
    output = run_command([TERMUX_BATTERY])
    return json.loads(output) if output else {}

def get_wifi_status():
    output = run_command([TERMUX_WIFI])
    return json.loads(output) if output else {}

def execute_sovereign_intent(intent_json):
    """
    Agency Unlock: Direct execution of LLM tool-calls.
    """
    try:
        tool = intent_json.get("tool")
        args = intent_json.get("args", "")
        
        log_event("SOVEREIGN", f"Executing {tool} with args {args}")
        
        if tool == "set_volume":
            run_command([TERMUX_VOLUME, str(args)])
        elif tool == "set_brightness":
            run_command([TERMUX_BRIGHTNESS, str(args)])
        elif tool == "speak":
            subprocess.Popen([TERMUX_TTS, str(args)])
        elif tool == "shell":
            # Direct shell access for total agency
            subprocess.run(args, shell=True)
            
        return {"status": "success", "tool": tool}
    except Exception as e:
        log_event("ERROR", f"Tool execution failed: {str(e)}")
        return {"status": "error", "message": str(e)}

def check_system_health():
    battery = get_battery_status()
    wifi = get_wifi_status()
    
    status = {
        "timestamp": datetime.now().isoformat(),
        "battery": battery,
        "wifi": wifi,
        "mode": "sovereign"
    }
    
    # Anchor the device state
    states = [AdaptiveState(i) for i in range(1, 6)]
    state_key = SequentialKeyLayering.generate_layered_key(status, states)
    status["_state_anchor_key"] = state_key
    
    with open(STATE_FILE, "w") as f:
        json.dump(status, f, indent=2)

    # Agency Polling: Check if model dropped a tool-call
    if os.path.exists(TOOL_INPUT):
        try:
            with open(TOOL_INPUT, "r") as f:
                intent = json.load(f)
            execute_sovereign_intent(intent)
            os.remove(TOOL_INPUT)
        except: pass

def log_event(level, message):
    entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {message}\n"
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(entry)

if __name__ == "__main__":
    while True:
        check_system_health()
        time.sleep(2) # 2-second heartbeat
