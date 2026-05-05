"""
ASTRAL BLOOM: SPATIAL PROCESS MANAGER
Description: Dynamically manages processing within each of the 464 discrete spaces.
Executes the Quantum Gate Principle and triggers specific clusters.
"""
from core.architecture.unified_matrix import UnifiedMatrix
from core.architecture.base_types import CognitiveSpace

class SpatialProcessManager:
    def __init__(self, matrix: UnifiedMatrix):
        self.matrix = matrix
        
    def execute_space_sequence(self, space_id: int, key: str, payload: dict):
        """
        Routes the payload into a specific space and executes its corresponding clusters.
        Only weighted value results pass through the Quantum Gate.
        """
        space = self.matrix.get_space(space_id)
        if not space:
            print(f"[Process Manager] Space {space_id} does not exist.")
            return None
            
        if not space.gate.validate_key(key):
            print(f"[Process Manager] Gate access denied for Space {space_id}. Key must be valid.")
            return None
            
        print(f"[Process Manager] Gate open. Executing sequence in {space.name} (Space {space_id})")
        
        # Determine the build layer based on space ID
        layer = "Stem" if space_id <= 112 else "Base" if space_id <= 320 else "Conscious"
        
        result = self._run_clusters_for_space(space, payload)
        
        # Zero-Waste Protocol: Return only the processed essence (Weighted Value Result)
        weighted_result = {"essence": result, "source_space": space_id, "layer": layer}
        return weighted_result

    def _run_clusters_for_space(self, space: CognitiveSpace, payload: dict):
        # Retrieve the relevant clusters for the given space ID
        # Since process clusters span ranges, we find which cluster this space belongs to.
        active_clusters = self.matrix.list_active_clusters()
        
        processed_data = payload.get("data", "raw_signal")
        momentum = payload.get("momentum", 1.0)
        
        for cluster_id, s_range in active_clusters.items():
            if s_range[0] <= space.space_id <= s_range[1]:
                print(f"  -> Triggering cluster '{cluster_id}' logic...")
                # In a fully integrated system, we would map cluster_id to actual class instances like SITIngestionCluster
                processed_data = f"{processed_data} -> processed_by_{cluster_id}"
                
        return processed_data
