"""
ASTRAL BLOOM: CONSCIOUS BUILD (LEVEL 3)
Range: Logical [145-208] | Temporal [353-416]
"""
from core.architecture.base_types import CognitiveSpace, ProcessCluster

class ConsciousBuild:
    def __init__(self):
        self.logical_spaces = {}
        self.temporal_spaces = {}
        self.clusters = {}
        self._build_infrastructure()

    def _build_infrastructure(self):
        # 1. Define Clusters (Sub-tiers)
        self.clusters["Internal_Observation"] = ProcessCluster("Primary Internal Observation", [145, 164])
        self.clusters["Memory_Reasoning"] = ProcessCluster("Memory-Reasoning & Context", [165, 184])
        self.clusters["Observer_Feedback"] = ProcessCluster("Sub-Observer Feedback", [185, 196])
        self.clusters["Temporal_Buffer"] = ProcessCluster("Temporal Buffer", [197, 208])

        # 2. Build Logical Spaces
        space_names = {
            145: "Analytical", 154: "Reasoning", 165: "Observe",
            174: "Comparative", 185: "Identification", 197: "Response Gen",
            208: "Recursive Gate" # Space 416 equivalent
        }
        
        for i in range(145, 209):
            name = space_names.get(i, f"Conscious_Logical_{i}")
            space = CognitiveSpace(i, name)
            # Add Standard Conscious Sub-spaces
            space.add_sub_space("Critical", "High-fidelity logic review")
            space.add_sub_space("Observer state", "The monitoring layer")
            space.add_sub_space("Situation analytics", "Reverse order anchor points")
            self.logical_spaces[i] = space

        # 3. Build Temporal Counterparts
        for i in range(353, 417):
            self.temporal_spaces[i] = CognitiveSpace(i, f"Conscious_Temporal_{i}", is_temporal=True)
