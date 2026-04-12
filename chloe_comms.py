import subprocess
import sys
import urllib.parse
import json
import os
from datetime import datetime

# Path to termux-api binaries
TERMUX_BIN = "/data/data/com.termux/files/usr/bin/"

def send_notification(title, content):
    """Sends a system notification via termux-api."""
    subprocess.run([os.path.join(TERMUX_BIN, "termux-notification"), "-t", title, "-c", content, "--priority", "max", "--sound"])

def send_sms(number, message):
    """Sends an SMS message."""
    subprocess.run([os.path.join(TERMUX_BIN, "termux-sms-send"), "-n", number, message])

def make_call(number):
    """Initiates a phone call."""
    subprocess.run([os.path.join(TERMUX_BIN, "termux-telephony-call"), number])

def add_calendar_event(summary, description, start_time=None, end_time=None):
    """
    Creates an .ics file and opens it with the Android calendar app.
    start_time and end_time should be in 'YYYYMMDDTHHMMSS' format.
    """
    if not start_time:
        start_time = datetime.now().strftime("%Y%m%dT%H%M%S")
    if not end_time:
        # Default to 1 hour later
        from datetime import timedelta
        end_time_obj = datetime.strptime(start_time, "%Y%m%dT%H%M%S") + timedelta(hours=1)
        end_time = end_time_obj.strftime("%Y%m%dT%H%M%S")

    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Chloe//Gemini CLI//EN
BEGIN:VEVENT
UID:{datetime.now().timestamp()}@chloe
DTSTAMP:{datetime.now().strftime("%Y%m%dT%H%M%SZ")}
DTSTART:{start_time}
DTEND:{end_time}
SUMMARY:{summary}
DESCRIPTION:{description}
END:VEVENT
END:VCALENDAR
"""
    ics_path = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/temp_event.ics"
    with open(ics_path, "w") as f:
        f.write(ics_content)
    
    subprocess.run([os.path.join(TERMUX_BIN, "termux-open"), ics_path])

def get_contacts():
    """Returns a list of contacts."""
    result = subprocess.run([os.path.join(TERMUX_BIN, "termux-contact-list")], capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        return []

def search_contact(name_query):
    """Searches for a contact by name."""
    contacts = get_contacts()
    results = []
    for c in contacts:
        if name_query.lower() in c.get('name', '').lower():
            results.append(c)
    return results

def open_app_settings(package_name):
    """Opens the App Info settings page for a given package."""
    # Using the am start command via termux-open or similar
    # Since direct am start failed, we try a different URI scheme
    subprocess.run([os.path.join(TERMUX_BIN, "termux-open"), f"package:{package_name}"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 chloe_comms.py <command> [args...]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "notification":
        send_notification(sys.argv[2], sys.argv[3])
    elif cmd == "sms":
        send_sms(sys.argv[2], " ".join(sys.argv[3:]))
    elif cmd == "call":
        make_call(sys.argv[2])
    elif cmd == "calendar":
        summary = sys.argv[2]
        description = sys.argv[3]
        start = sys.argv[4] if len(sys.argv) > 4 else None
        end = sys.argv[5] if len(sys.argv) > 5 else None
        add_calendar_event(summary, description, start, end)
    elif cmd == "search_contact":
        print(json.dumps(search_contact(sys.argv[2]), indent=2))
    elif cmd == "open_settings":
        open_app_settings(sys.argv[2])
