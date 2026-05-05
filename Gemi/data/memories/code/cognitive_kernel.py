"""
PROJECT ASTRAL BLOOM: COGNITIVE KERNEL
Architect: Clintin Brummer | Logic: 51 Formulas & Token Budgeting
"""
import os

from core.substrate.logic_foundation import SubstrateFoundation, SequentialKeyLayering, AdaptiveState

class Kernel:
    def __init__(self):
        self.substrate = SubstrateFoundation()
        self.unity_constant = 1.0
        self.spaces = 416
        self.formula_count = 51
        
    def generate_sequential_momentum(self, initiate_value: float):
        """Generates momentum using layered algorithmic keys instead of raw data."""
        states = [AdaptiveState(i) for i in range(1, 6)]
        key = SequentialKeyLayering.generate_layered_key(initiate_value, states)
        return key, self.substrate.unity_constant


    def calculate_token_budget(self, input_chars):
        """Amulet Guardrail: Protects physical RAM from OOM (Killed) error."""
        est_input_tokens = input_chars // 4
        available = self.max_context - est_input_tokens - self.response_reserve
        return max(available, 512)

# Global Engine for the Bridge
FORMULA_ENGINE = Kernel()
