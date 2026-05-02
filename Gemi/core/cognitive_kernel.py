"""
PROJECT ASTRAL BLOOM: COGNITIVE KERNEL
Architect: Clintin Brummer | Logic: 51 Formulas & Token Budgeting
"""
import os

from core.substrate.logic_foundation import SubstrateFoundation, SequentialKeyLayering, AdaptiveState
from core.clusters.dissonance_reasoning import DissonanceReasoningCluster
from core.clusters.memory_reasoning import MemoryReasoningContextCluster
from core.clusters.temporal_buffer import TemporalBufferCluster
from core.clusters.primary_internal_observation import PrimaryInternalObservationCluster
from core.clusters.rpps_avoidance import RPPSAvoidanceCluster
from core.clusters.seq_algorithmic_processing import SeqAlgorithmicProcessingCluster
from core.clusters.sub_observer_feedback import SubObserverFeedbackCluster

class Kernel:
    def __init__(self):
        self.substrate = SubstrateFoundation()
        self.unity_constant = 1.0
        self.spaces = 416
        self.formula_count = 51
        self.max_context = 10000
        self.response_reserve = 2048
        
        # Initialize Cognitive Clusters
        self.clusters = [
            SeqAlgorithmicProcessingCluster(),
            MemoryReasoningContextCluster(),
            TemporalBufferCluster(),
            DissonanceReasoningCluster(),
            RPPSAvoidanceCluster(),
            PrimaryInternalObservationCluster(),
            SubObserverFeedbackCluster()
        ]
        
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
        
    def execute_cognitive_pipeline(self, context, momentum):
        """Passes the context and momentum through the active cognitive clusters."""
        processed_context = context
        for cluster in self.clusters:
            processed_context = cluster.process(processed_context, momentum)
        return processed_context

# Global Engine for the Bridge
FORMULA_ENGINE = Kernel()
