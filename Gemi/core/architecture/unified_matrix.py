"""
ASTRAL BLOOM: UNIFIED 464-SPACE MATRIX
Description: Integrates all builds into a single logical tensor.
"""
from core.architecture.builds.stem_build import StemBuild
from core.architecture.builds.base_build import BaseBuild
from core.architecture.builds.conscious_build import ConsciousBuild

class UnifiedMatrix:
    def __init__(self):
        self.stem = StemBuild()
        self.base = BaseBuild()
        self.conscious = ConsciousBuild()
        
        self.all_spaces = {}
        self._integrate_tensor()

    def _integrate_tensor(self):
        # Merge all logical and temporal spaces into a single O(1) lookup map
        builds = [self.stem, self.base, self.conscious]
        for build in builds:
            self.all_spaces.update(build.logical_spaces)
            self.all_spaces.update(build.temporal_spaces)

    def get_space(self, space_id: int):
        return self.all_spaces.get(space_id)

    def list_active_clusters(self):
        all_clusters = {}
        builds = {"Stem": self.stem, "Base": self.base, "Conscious": self.conscious}
        for name, build in builds.items():
            for c_name, cluster in build.clusters.items():
                all_clusters[f"{name}_{c_name}"] = cluster.space_range
        return all_clusters

if __name__ == "__main__":
    matrix = UnifiedMatrix()
    print(f"Astral Bloom Unified Matrix Initialized: {len(matrix.all_spaces)} Spaces Active.")
    print("Active Clusters Mapping:")
    for cluster, s_range in matrix.list_active_clusters().items():
        print(f"  -> {cluster}: {s_range}")
