#!/data/data/com.termux/files/usr/bin/bash
# Daily VC Task Reminder

termux-notification \
    --id "vc_daily_tasks" \
    --title "Astral Bloom: VC Progression" \
    --content "Good morning Clint. Your 10 tasks for today's VC roadmap are waiting." \
    --action "cat /data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/data/memories/business/VC_7_Day_Progression.md" \
    --priority "high"
