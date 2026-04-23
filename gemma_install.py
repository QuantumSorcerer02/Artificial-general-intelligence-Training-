import kagglehub
import os

print("Downloading Gemma 4 E2B-it model...")
try:
    # Assuming the path for Gemma 4 based on previous patterns
    path = kagglehub.model_download("google/gemma-4/gemmaCpp/e2b-it-sfp")
    print(f"Model downloaded to: {path}")
    
    # Create a symlink or copy to the project directory for easier access
    target_dir = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/data/models"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    # Find the .sfp or .sbs file in the downloaded path
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".sfp") or file.endswith(".sbs"):
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_dir, file)
                if not os.path.exists(target_file):
                    os.symlink(source_file, target_file)
                    print(f"Symlinked {source_file} to {target_file}")

except Exception as e:
    print(f"Error downloading model: {e}")
    print("\nIMPORTANT: To download models from Kaggle, you need to set up your API keys.")
    print("1. Go to https://www.kaggle.com/settings")
    print("2. Click 'Create New Token' to download kaggle.json")
    print("3. Place the file at ~/.kaggle/kaggle.json")
    print("4. Ensure permissions are correct: chmod 600 ~/.kaggle/kaggle.json")
