import json
import os
import subprocess
from datetime import datetime

REMINDERS_FILE = "data/memories/reminders.json"

def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return []
    with open(REMINDERS_FILE, "r") as f:
        return json.load(f)

def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)

def add_reminder(time_str, date_str, message):
    reminders = load_reminders()
    new_id = max([r["id"] for r in reminders] + [0]) + 1
    reminders.append({
        "id": new_id,
        "time": time_str,
        "date": date_str,
        "message": message,
        "status": "pending"
    })
    save_reminders(reminders)
    print(f"Reminder added: ID {new_id} - {date_str} {time_str}: {message}")

def list_reminders():
    reminders = load_reminders()
    if not reminders:
        print("No reminders found.")
        return
    for r in reminders:
        print(f"[{r['status'].upper()}] ID {r['id']}: {r['date']} {r['time']} - {r['message']}")

def trigger_notification(message):
    try:
        subprocess.run(["termux-notification", "--title", "Chloe: Reminder", "--content", message], check=True)
        subprocess.run(["bash", "chloe_speak.sh", message], check=True)
    except Exception as e:
        print(f"Error triggering notification: {e}")

def check_and_trigger():
    reminders = load_reminders()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    
    updated = False
    for r in reminders:
        if r["status"] == "pending" and r["date"] == current_date and r["time"] <= current_time:
            trigger_notification(r["message"])
            r["status"] = "completed"
            updated = True
            
    if updated:
        save_reminders(reminders)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "add" and len(sys.argv) == 5:
            add_reminder(sys.argv[2], sys.argv[3], sys.argv[4])
        elif cmd == "list":
            list_reminders()
        elif cmd == "check":
            check_and_trigger()
        else:
            print("Usage: python3 chloe_reminders.py [add TIME DATE MSG | list | check]")
