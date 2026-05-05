"""
ASTRAL BLOOM: BASE BUILD (LEVEL 2)
Range: [113-320] (104 Logical, 104 Temporal)
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
        self.clusters["SEQ_Processing"] = ProcessCluster("SEQ-Algorithmic Processing", [113, 147])
        self.clusters["RPPS_Avoidance"] = ProcessCluster("RPPS-Avoidance & Pruning", [148, 182])
        self.clusters["Dissonance_Reasoning"] = ProcessCluster("Dissonance & Reasoning", [183, 216])

        # 2. Build Logical Spaces
        space_names = {
            113: "System processing", 120: "Clusters", 130: "Creation",
            148: "Pro monitoring", 158: "Alteration", 168: "Det(usage)",
            183: "Reduction", 196: "Mitigation"
        }
        
        for i in range(113, 217):
            name = space_names.get(i, f"Base_Logical_{i}")
            space = CognitiveSpace(i, name)
            # Add Standard Base Sub-spaces
            space.add_sub_space("Default State", "Standard base processing")
            space.add_sub_space("Emulation", "Solution mirroring")
            space.add_sub_space("Quarantine", "Dissonant thread isolation")
            space.add_sub_space("inception", "Inception of Conception trigger")
            self.logical_spaces[i] = space

        # 3. Build Temporal Counterparts
        for i in range(217, 321):
            self.temporal_spaces[i] = CognitiveSpace(i, f"Base_Temporal_{i}", is_temporal=True)
