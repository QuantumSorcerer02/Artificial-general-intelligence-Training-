"""
ASTRAL BLOOM: BASE BUILD (LEVEL 2)
Range: Logical [49-144] | Temporal [257-352]
"""
from core.architecture.base_types import CognitiveSpace, ProcessCluster

class BaseBuild:
    def __init__(self):
        self.logical_spaces = {}
        self.temporal_spaces = {}
        self.clusters = {}
        self._build_infrastructure()

    def _build_infrastructure(self):
        # 1. Define Clusters (Sub-tiers)
        self.clusters["SEQ_Processing"] = ProcessCluster("SEQ-Algorithmic Processing", [49, 80])
        self.clusters["RPPS_Avoidance"] = ProcessCluster("RPPS-Avoidance & Pruning", [81, 112])
        self.clusters["Dissonance_Reasoning"] = ProcessCluster("Dissonance & Reasoning", [113, 144])

        # 2. Build Logical Spaces
        space_names = {
            49: "System processing", 56: "Clusters", 66: "Creation",
            81: "Pro monitoring", 91: "Alteration", 101: "Det(usage)",
            113: "Reduction", 126: "Mitigation"
        }
        
        for i in range(49, 145):
            name = space_names.get(i, f"Base_Logical_{i}")
            space = CognitiveSpace(i, name)
            # Add Standard Base Sub-spaces
            space.add_sub_space("Default State", "Standard base processing")
            space.add_sub_space("Emulation", "Solution mirroring")
            space.add_sub_space("Quarantine", "Dissonant thread isolation")
            space.add_sub_space("inception", "Inception of Conception trigger")
            self.logical_spaces[i] = space

        # 3. Build Temporal Counterparts
        for i in range(257, 353):
            self.temporal_spaces[i] = CognitiveSpace(i, f"Base_Temporal_{i}", is_temporal=True)
