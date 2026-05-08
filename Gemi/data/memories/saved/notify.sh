#!/bin/bash
# Chloe Notification Tool
# Usage: ./notify.sh "Title" "Content"
termux-notification --title "$1" --content "$2" --id 101 --ongoing
