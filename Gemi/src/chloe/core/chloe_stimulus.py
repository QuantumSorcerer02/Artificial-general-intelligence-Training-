import subprocess
import json
import os
import requests
from datetime import datetime

# Termux API Commands
LOCATION_CMD = ["termux-location"]
NOTIF_CMD = ["termux-notification-list"]
SMS_CMD = ["termux-sms-list", "-l", "3"]
BATTERY_CMD = ["termux-battery-status"]
WIFI_CMD = ["termux-wifi-connectioninfo"]

STIMULUS_FILE = "logs/chloe_stimulus.json"

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return json.loads(result.stdout)
    except Exception:
        return None

def get_weather(lat, lon):
    """Fetches weather data for current coordinates."""
    # Using a free, no-key weather API (wttr.in) for simplicity in this sandbox
    try:
        response = requests.get(f"https://wttr.in/{lat},{lon}?format=j1", timeout=10)
        if response.status_code == 200:
            data = response.json()
            current = data.get('current_condition', [{}])[0]
            return {
                "temp": current.get('temp_C'),
                "desc": current.get('weatherDesc', [{}])[0].get('value'),
                "humidity": current.get('humidity'),
                "feels_like": current.get('FeelsLikeC')
            }
    except Exception:
        pass
    return {"status": "Weather data unavailable"}

def gather_stimuli():
    print("Chloe: Gathering external stimuli...")
    
    location = run_cmd(LOCATION_CMD)
    lat = location.get("latitude") if location else None
    lon = location.get("longitude") if location else None
    
    weather = get_weather(lat, lon) if lat and lon else {"status": "Awaiting coordinates"}
    
    notifications = run_cmd(NOTIF_CMD)
    sms = run_cmd(SMS_CMD)
    battery = run_cmd(BATTERY_CMD)
    wifi = run_cmd(WIFI_CMD)
    
    stimulus_package = {
        "timestamp": datetime.now().isoformat(),
        "environment": {
            "location": location,
            "weather": weather,
            "wifi": wifi
        },
        "communications": {
            "notifications": notifications,
            "sms": sms
        },
        "vitals": battery,
        "perception": "Active"
    }
    
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    with open(STIMULUS_FILE, "w") as f:
        json.dump(stimulus_package, f, indent=2)
    
    print(f"Chloe: Stimulus package saved to {STIMULUS_FILE}.")
    return stimulus_package

if __name__ == "__main__":
    gather_stimuli()
