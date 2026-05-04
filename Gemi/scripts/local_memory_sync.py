import google.generativeai as genai
import json
import os
import subprocess
from datetime import datetime

# Configure your API key (ensure this is set in your Termux environment variables)
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("[Error] GEMINI_API_KEY environment variable not found.")
    exit(1)

genai.configure(api_key=API_KEY)

# Define the local memory storage file
MEMORY_FILE = "local_memory_sync.json"

def load_local_memory():
    """Loads existing memory and ensures the file is valid JSON."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_to_memory(memory_list):
    """Saves the entire history to disk."""
    try:
        with open(MEMORY_FILE, "w") as file:
            json.dump(memory_list, file, indent=4)
    except IOError as e:
        print(f"[Error] Failed to save memory: {e}")

def chloe_speak(text):
    """Auditory Interface Integration: Triggers Chloe's voice via espeak-ng."""
    # Clean text for speech: remove markdown and truncate at code blocks
    clean_text = text.replace("**", "").replace("__", "").replace("#", "").split("```")[0].strip()
    if clean_text:
        # Using subprocess.Popen to avoid blocking the CLI during speech
        subprocess.Popen(["bash", "chloe_speak.sh", clean_text], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)

def main():
    # Initialise the model
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    # Load past interactions to provide historical context
    raw_history = load_local_memory()
    
    # Format for Gemini SDK: history=[{'role': 'user', 'parts': ['...']}, ...]
    formatted_history = []
    for entry in raw_history:
        if "role" in entry and "content" in entry:
            formatted_history.append({
                "role": entry["role"],
                "parts": [entry["content"]]
            })
    
    # Start the chat session with historical context
    chat = model.start_chat(history=formatted_history)
    
    print("\n[SYS] Project Astral Bloom: Local Synchronisation Active.")
    print("[SYS] Auditory Interface Primed (Chloe). Type 'exit' to close.")
    
    while True:
        try:
            user_input = input("\nClint ❯ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[SYS] Terminating Session...")
            break
            
        if not user_input:
            continue
            
        if user_input.lower() == 'exit':
            break
            
        # 1. Update local memory state (user part)
        raw_history.append({
            "timestamp": datetime.now().isoformat(),
            "role": "user",
            "content": user_input
        })
        
        # 2. Send to Gemini
        try:
            response = chat.send_message(user_input)
            response_text = response.text
            
            print(f"\nChloe ❯ {response_text}")
            
            # 3. Update memory with model response
            raw_history.append({
                "timestamp": datetime.now().isoformat(),
                "role": "model",
                "content": response_text
            })
            
            # 4. Persistence and Vocalization
            save_to_memory(raw_history)
            chloe_speak(response_text)
            
        except Exception as e:
            print(f"\n[Error] API Interaction Failed: {e}")

if __name__ == "__main__":
    main()
