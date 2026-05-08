import os
import shutil
import re

IMPORT_DIR = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/tmp/imported_memories"
DATA_FACTORY = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/data/Data_Factory"
MEMORIES_DIR = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/data/memories"

# Categorization rules based on keywords
CATEGORIES = {
    "math": os.path.join(DATA_FACTORY, "Mathematical_Formulations"),
    "architecture": os.path.join(DATA_FACTORY, "Neural_Network_Architecture"),
    "observer": os.path.join(MEMORIES_DIR, "cognitive_map"),
    "business": os.path.join(MEMORIES_DIR, "business"),
    "pitch": os.path.join(MEMORIES_DIR, "investors"),
    "syndicate": os.path.join(MEMORIES_DIR, "business"),
    "qsp": os.path.join(DATA_FACTORY, "Quantum_State_Processing"),
    "asi-alpha": os.path.join(DATA_FACTORY, "Neural_Network_Architecture"),
    "code": os.path.join(MEMORIES_DIR, "code"),
    "python": os.path.join(MEMORIES_DIR, "code"),
    "landscape": os.path.join(MEMORIES_DIR, "knowledge_base"),
    "manifest": os.path.join(MEMORIES_DIR, "architecture"),
    "theory": os.path.join(MEMORIES_DIR, "knowledge_base"),
    "exploit": os.path.join(MEMORIES_DIR, "security"),
    "ledger": os.path.join(MEMORIES_DIR, "business"),
    "conversation": os.path.join(MEMORIES_DIR, "saved", "conversations"),
    "chat": os.path.join(MEMORIES_DIR, "saved", "conversations"),
}
DEFAULT_DIR = os.path.join(MEMORIES_DIR, "saved")

def clean_filename(filename):
    # Remove "Copy of " prefix
    cleaned = re.sub(r"^Copy of\s+", "", filename)
    # Remove numbering like "(1)", "(12)", etc. right before the extension
    cleaned = re.sub(r"\(\d+\)(?=\.[^.]+$)", "", cleaned)
    # Remove numbering at the end of files without extensions
    cleaned = re.sub(r"\(\d+\)$", "", cleaned)
    # Clean up double dots or space before dots
    cleaned = re.sub(r"\s+\.", ".", cleaned)
    cleaned = re.sub(r"\.\.+_", "_", cleaned)
    return cleaned.strip()

def determine_destination(filename):
    lower_name = filename.lower()
    for key, dest in CATEGORIES.items():
        if key in lower_name:
            return dest
    if filename.endswith(".py") or filename.endswith(".txt") and "code" in lower_name:
        return CATEGORIES["code"]
    return DEFAULT_DIR

def process_files():
    if not os.path.exists(IMPORT_DIR):
        print(f"Import directory not found: {IMPORT_DIR}")
        return

    processed = {}
    total_raw = 0

    # Recursively find all files
    for root, _, files in os.walk(IMPORT_DIR):
        for f in files:
            full_path = os.path.join(root, f)
            if os.path.isfile(full_path):
                total_raw += 1
                cleaned = clean_filename(f)
                if cleaned not in processed:
                    processed[cleaned] = []
                processed[cleaned].append(full_path)

    print(f"Found {total_raw} total raw files. Deduplicating to {len(processed)} unique documents.")

    moved_count = 0
    for cleaned_name, original_paths in processed.items():
        # If there are duplicates, take the one with the largest file size (most complete data)
        best_file = max(original_paths, key=os.path.getsize)
        
        dest_dir = determine_destination(cleaned_name)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, cleaned_name)
        
        try:
            shutil.copy2(best_file, dest_path)
            moved_count += 1
            
            # Clean up all the original raw files for this group
            for path in original_paths:
                try:
                    os.remove(path)
                except OSError:
                    pass
        except Exception as e:
            print(f"Error moving {cleaned_name}: {e}")

    print(f"Successfully processed, categorized, and distributed {moved_count} unique files.")

    # Clean up import directory
    shutil.rmtree(IMPORT_DIR, ignore_errors=True)
    print("Import directory cleaned up.")

if __name__ == "__main__":
    process_files()
