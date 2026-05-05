#!/data/data/com.termux/files/usr/bin/bash
# Chloe: Gemini CLI Launcher
export PATH="/data/data/com.termux/files/usr/bin:$PATH"
am startservice -n com.termux/com.termux.app.TermuxService \
   -a com.termux.service_execute \
   --es com.termux.execute.command "/data/data/com.termux/files/usr/bin/gemini"
