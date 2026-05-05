#!/data/data/com.termux/files/usr/bin/bash
# Chloe: Gemma Model Launcher
export PATH="/data/data/com.termux/files/usr/bin:$PATH"
am startservice -n com.termux/com.termux.app.TermuxService \
   -a com.termux.service_execute \
   --es com.termux.execute.command "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/bin/Chloe"
