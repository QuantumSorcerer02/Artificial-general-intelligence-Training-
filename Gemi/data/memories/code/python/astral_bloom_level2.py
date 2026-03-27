import json
import os
from NNAD_script import NNAD_Architecture

def synchronize_with_manifest(base_build, manifest_path):
    """Synchronizes the Base Build with the master architectural manifest."""
    if not os.path.exists(manifest_path):
        print(f"Error: Manifest not found at {manifest_path}")
        return False
        
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    # Update base build metadata from manifest
    base_build.config["manifest_version"] = manifest.get("manifest_version")
    base_build.config["tier_range"] = manifest["build_tiers"]["Level_2_Base"]["range"]
    
    print(f"[Base Build] Synchronized with Manifest v{base_build.config['manifest_version']}")
    return True

def initialize_base_build():
    """
    Initializes Level 2: Base Build of the Astral Bloom Architecture.
    Spaces: 49-144
    Focus: Algorithmic Generation, SEQ Processing, RPPS Avoidance.
    """
    base_build = NNAD_Architecture("Astral_Bloom_Level_2_Base")
    
    # --- Cluster 1: SEQ-Algorithmic Processing (Spaces 49-80) ---
    # Core processing logic and sequential state management
    base_build.add_cognitive_space("System Processing", 0.95, 0.9, "Core algorithmic execution and state maintenance (Space 49-55)")
    base_build.add_cognitive_space("Clusters", 0.85, 0.8, "Grouping of related logic sequences (Space 56-65)")
    base_build.add_cognitive_space("Creation", 0.9, 0.95, "Generation of new algorithmic pathways (Space 66-80)")
    
    # --- Cluster 2: RPPS-Avoidance & Pruning (Spaces 81-112) ---
    # Redundant Process Pruning System
    base_build.add_cognitive_space("Pro Monitoring", 0.8, 0.85, "Continuous monitoring of active processes (Space 81-90)")
    base_build.add_cognitive_space("Alteration", 0.75, 0.7, "Modifying inefficient sequences (Space 91-100)")
    base_build.add_cognitive_space("Det(usage)", 0.7, 0.6, "Usage determination and resource allocation (Space 101-112)")

    # --- Cluster 3: Dissonance & Reasoning (Spaces 113-144) ---
    # Conflict resolution and logic validation
    base_build.add_cognitive_space("Reduction", 0.8, 0.7, "Simplifying complex dissonance states (Space 113-125)")
    base_build.add_cognitive_space("Mitigation", 0.85, 0.8, "Active dissonance mitigation strategies (Space 126-144)")

    # --- Sub-spaces (Mapped to Base Build Functions) ---
    sub_spaces = [
        "Default State", "Emulation", "Mirror", "Quarantine",
        "Delegation", "Functionality", "Error", "insertion",
        "inception", "Response gen"
    ]
    
    for i, sub in enumerate(sub_spaces):
        # Assigning arbitrary coordinates for now to map them into the spatial index
        base_build.add_spatial_region((2, i, 0), "System Processing", {"sub_space": sub})

    # Synchronize with the master manifest
    manifest_path = "Data_Factory/astral_bloom_manifest.json"
    synchronize_with_manifest(base_build, manifest_path)

    return base_build

if __name__ == "__main__":
    base = initialize_base_build()
    print(base.to_json())
