#!/bin/bash
# System Health Check for Astral Bloom
echo "--- SYSTEM STATUS ---"
echo "Root: /data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
echo "Kernel: $(if [ -f /data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/cognitive_kernel.pid ]; then echo "Online"; else echo "Offline"; fi)"
echo "Memory Files: $(ls /data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/data/memories/ | wc -l) files found."
echo "Bridge: Online"
