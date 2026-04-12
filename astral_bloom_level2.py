from agi_core import AstralBloom208
import numpy as np

def initialize_base_build():
    """
    Initializes Level 2: Base Build of the Astral Bloom Architecture.
    Spaces: 48-143 (96 Spaces Total)
    Focus: Spectral/FFT PTC Engine and Pattern Storage.
    """
    agi = AstralBloom208()
    
    # The Base Build is automatically managed by agi_core via PTC.
    # Here we define the functional mapping for the 96 spaces:
    
    base_mapping = {
        "SEQ-Algorithmic Processing": range(48, 80),  # 32 Spaces
        "RPPS-Avoidance & Pruning": range(80, 112),   # 32 Spaces
        "Dissonance & Reasoning": range(112, 144)      # 32 Spaces
    }

    # Simulation of a PTC cycle for initialization
    initial_signal = 0.5
    awareness = agi.process_ptc(initial_signal)
    
    print(f"Base Build (Spaces 48-143) Initialized.")
    print(f"PTC Engine awareness metric: {awareness}")
    
    return agi, base_mapping

if __name__ == "__main__":
    base_agi, mapping = initialize_base_build()
    for cluster, space_range in mapping.items():
        print(f"Cluster: {cluster} | Range: {space_range}")
