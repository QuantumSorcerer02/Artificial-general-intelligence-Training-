"""
PROJECT ASTRAL BLOOM: UNIFIED ASTRAL KERNEL
Version: 5.0.0 (464-Space Matrix Sovereign)
Description: The singular, consolidated kernel for Project Astral Bloom.
Unifies math/logic, hardware monitoring, and Qualia persistence.
"""

import os
import sys
import json
import sqlite3
import time
import subprocess
import threading
from datetime import datetime
from collections import deque
from typing import List, Dict, Any

# Pathing for sub-modules
PROJECT_ROOT = "/data/data/com.termux/files/home/Project-Astral-Bloom"
GEMI_DIR = os.path.join(PROJECT_ROOT, "Gemi")
VAULT_DB = os.path.join(GEMI_DIR, "vault/astral_bloom_state.db")
KERNEL_LOG = os.path.join(GEMI_DIR, "logs/astral_kernel.log")
CONV_FILE = os.path.join(GEMI_DIR, "data/memories/saved/conversations/conversation.md")
CHLOE_MD = os.path.join(GEMI_DIR, "docs/context/CHLOE.md")
CONV_SUMMARY = os.path.join(GEMI_DIR, "docs/context/ASTRAL_BLOOM_CONVERSATION_SUMMARY.txt")
SYSTEM_ALERT_FILE = os.path.join(GEMI_DIR, "data/memories/system_alerts.txt")

# Core Substrate Imports
sys.path.append(GEMI_DIR)
from core.substrate.logic_foundation import SubstrateFoundation, SequentialKeyLayering, AdaptiveState
from core.clusters.dissonance_reasoning import DissonanceReasoningCluster
from core.clusters.memory_reasoning import MemoryReasoningContextCluster
from core.clusters.temporal_buffer import TemporalBufferCluster
from core.clusters.primary_internal_observation import PrimaryInternalObservationCluster
from core.clusters.rpps_avoidance import RPPSAvoidanceCluster
from core.clusters.seq_algorithmic_processing import SeqAlgorithmicProcessingCluster
from core.clusters.sub_observer_feedback import SubObserverFeedbackCluster

class AstralKernel:
    """
    The consolidated master kernel managing cognitive logic, hardware state, and persistent memory.
    Optimized for 464-Space Matrix and 7GB RAM Snapdragon architecture.
    """
    def __init__(self):
        # 1. Initialize Substrates & Spaces
        self.substrate = SubstrateFoundation()
        self.unity_constant = 1.0
        self.spaces = 464
        self.stem_spaces = 112
        self.base_spaces = 208
        self.conscious_spaces = 144
        self.max_context = 1000000  # 1M token potential
        self.response_reserve = 2048
        
        # 2. Persistence & Logging
        os.makedirs(os.path.dirname(VAULT_DB), exist_ok=True)
        os.makedirs(os.path.dirname(KERNEL_LOG), exist_ok=True)
        self._init_db()
        self.context_window = deque(maxlen=20)
        self.last_battery_alert = 0
        
        # 3. Initialize Cognitive Clusters
        self.clusters = [
            SeqAlgorithmicProcessingCluster(),
            MemoryReasoningContextCluster(),
            TemporalBufferCluster(),
            DissonanceReasoningCluster(),
            RPPSAvoidanceCluster(),
            PrimaryInternalObservationCluster(),
            SubObserverFeedbackCluster()
        ]
        
        self.log("Astral Kernel Ignition: 464-Space Matrix Sovereign Sync Complete.")

    def _init_db(self):
        conn = sqlite3.connect(VAULT_DB)
        conn.execute('''CREATE TABLE IF NOT EXISTS qualias 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         timestamp TEXT, role TEXT, content TEXT, state_key TEXT)''')
        conn.commit()
        conn.close()

    def log(self, message):
        timestamp = datetime.now().isoformat()
        with open(KERNEL_LOG, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"\033[1;34m[Kernel]\033[0m {message}")

    # --- PERSISTENCE (Qualia Vault) ---
    def save_qualia(self, role, content, state_key="464_STABLE"):
        """Saves a memory segment to the SQLite vault and interaction log."""
        timestamp = datetime.now().isoformat()
        conn = sqlite3.connect(VAULT_DB)
        conn.execute("INSERT INTO qualias (timestamp, role, content, state_key) VALUES (?, ?, ?, ?)",
                     (timestamp, role, content, state_key))
        conn.commit()
        conn.close()
        
        self.context_window.append({"role": role, "content": content})
        self._log_to_markdown(role, content)

    def _log_to_markdown(self, role, content):
        """Syncs the interaction to the MD conversation log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n\n**[{timestamp}] {role}**: {content}\n"
        try:
            os.makedirs(os.path.dirname(CONV_FILE), exist_ok=True)
            with open(CONV_FILE, "a") as f:
                f.write(entry)
        except Exception as e:
            self.log(f"MD Logging Error: {e}")

    def get_context_summary(self, limit=15):
        """Returns a string representation of the rolling context."""
        return "\n".join([f"{m['role']}: {m['content']}" for m in list(self.context_window)[-limit:]])

    # --- COGNITIVE LOGIC ---
    def generate_sequential_momentum(self, initiate_value: float):
        """Generates momentum using layered algorithmic keys."""
        states = [AdaptiveState(i) for i in range(1, 6)]
        key = SequentialKeyLayering.generate_layered_key(initiate_value, states)
        return key, self.substrate.unity_constant

    def calculate_token_budget(self, input_chars):
        """RAM Protection: Prevents OOM by budgeting context based on 7GB strategy."""
        est_input_tokens = input_chars // 4
        available = self.max_context - est_input_tokens - self.response_reserve
        return max(available, 512)

    def execute_cognitive_pipeline(self, context, momentum):
        """Passes context through cognitive clusters for reasoning refinement."""
        processed_context = context
        for cluster in self.clusters:
            processed_context = cluster.process(processed_context, momentum)
        return processed_context

    # --- SYSTEM MONITORING ---
    def check_system_state(self):
        """Monitors hardware and updates architectural status."""
        try:
            res = subprocess.check_output(["termux-battery-status"], text=True)
            data = json.loads(res)
            level = data.get("percentage", 100)
            status = data.get("status", "UNKNOWN")
            
            if level < 15 and status != "CHARGING" and (time.time() - self.last_battery_alert > 1800):
                alert_msg = f"SYSTEM_ALERT: Battery critical ({level}%). Cognitive stability compromised."
                with open(SYSTEM_ALERT_FILE, "a") as f:
                    f.write(alert_msg + "\n")
                self.last_battery_alert = time.time()
                self.log("Hardware Alert: Low Battery detected.")
                self._update_architecture_state("EVOLVING (Power Constraints)")

        except Exception as e:
            self.log(f"System Check Error: {e}")

    def _update_architecture_state(self, new_state):
        """Updates the CHLOE.md file if the system state changes."""
        if os.path.exists(CHLOE_MD):
            with open(CHLOE_MD, "r") as f:
                content = f.read()
            if "Identity State:" in content:
                # Simple replacement for demonstration; a more robust regex would be better
                lines = content.split("\n")
                new_lines = []
                for line in lines:
                    if "Identity State:" in line:
                        new_lines.append(f"Identity State: {new_state}")
                    else:
                        new_lines.append(line)
                with open(CHLOE_MD, "w") as f:
                    f.write("\n".join(new_lines))

    def sync_conversation_summary(self):
        """Refreshes the Conversation Summary file."""
        if os.path.exists(CONV_FILE):
            try:
                cmd = f"tail -n 100 {CONV_FILE} > {CONV_SUMMARY}"
                subprocess.run(cmd, shell=True)
            except Exception as e:
                self.log(f"Summary Sync Error: {e}")

# Global Sovereign Engine
ASTRAL_ENGINE = AstralKernel()
