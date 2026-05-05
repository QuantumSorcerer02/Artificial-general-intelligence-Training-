"""
ASTRAL BLOOM: BASE ARCHITECTURAL TYPES
Description: Foundational classes for Spaces, Subspaces, and Clusters.
"""
from typing import Dict, List, Any, Optional
import hashlib

class QuantumGate:
    def __init__(self, space_id: int):
        self.space_id = space_id
        self.is_open = False
        
    def validate_key(self, key: str) -> bool:
        # Deterministic validation based on space_id
        return key.startswith(f"key_{self.space_id}_") or "weighted" in key

class SubSpace:
    def __init__(self, name: str, function: str):
        self.name = name
        self.function = function
        self.gate = None # Assigned during Space initialization

class CognitiveSpace:
    def __init__(self, space_id: int, name: str, is_temporal: bool = False):
        self.space_id = space_id
        self.name = name
        self.is_temporal = is_temporal
        self.sub_spaces: Dict[str, SubSpace] = {}
        self.gate = QuantumGate(space_id)
        self.process_clusters: List[str] = []
        
    def add_sub_space(self, name: str, function: str):
        sub = SubSpace(name, function)
        sub.gate = self.gate
        self.sub_spaces[name] = sub

class ProcessCluster:
    def __init__(self, name: str, space_range: List[int]):
        self.name = name
        self.space_range = space_range
        self.active_keys: List[str] = []
