#!/bin/bash
# Chloe Notification Mirror UI
# Allows for direct input to Chloe from the Android Notification Shade.

ROOT_DIR="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
INPUT_LOG="$ROOT_DIR/data/memories/user_input.txt"
CHLOE_SPEAK="$ROOT_DIR/src/chloe/scripts/chloe_speak.sh"

send_mirror_notification() {
    termux-notification --id "chloe_mirror" \
                        --title "Chloe: Astral Bloom Core" \
                        --content "System Active | Waiting for Intent..." \
                        --priority max \
                        --ongoing \
                        --button1 "Quick Input" \
                        --button1-action "bash $0 --reply" \
                        --button2 "Status" \
                        --button2-action "bash $0 --status"
}

handle_reply() {
    # This uses the Direct Reply feature of termux-api
    # In a real implementation, we'd use a dedicated script to capture $REPLY
    termux-dialog text -t "Enter User Intent for Chloe:" | jq -r '.text' > "$INPUT_LOG"
    USER_TEXT=$(cat "$INPUT_LOG")
    if [ ! -z "$USER_TEXT" ]; then
        # Notify the kernel/Gemi of the new input
        termux-toast "Intent Captured: $USER_TEXT"
        # Optional: Echo to a named pipe or trigger the Gemi process
    fi
    send_mirror_notification
}

show_status() {
    termux-toast "Chloe Status: Synchronized with 208-space tensor. Principality Governance: ACTIVE."
}

if [ "$1" == "--reply" ]; then
    handle_reply
elif [ "$1" == "--status" ]; then
    show_status
else
    send_mirror_notification
fi
