#!/bin/bash
# Chloe Speak Script (ElevenLabs High-Fidelity)
# Using xi-organization-id and specific model/format settings.

text="$1"
if [ -z "$text" ]; then
    if [ ! -t 0 ]; then
        text=$(cat)
    else
        exit 1
    fi
fi
if [ -z "$text" ]; then exit 1; fi

# Configuration
KEY_FILE="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/.elevenlabs_key"
ORG_FILE="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/.elevenlabs_workspace_id"
VOICE_ID="JBFqnCBsd6RMkjVDRZzb"
LOG_FILE="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/logs/chloe_voice.log"
# Realistic Android Chrome User-Agent
USER_AGENT="Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.63 Mobile Safari/537.36"

if [ -f "$KEY_FILE" ]; then
    API_KEY=$(cat "$KEY_FILE")
    ORG_ID=$(cat "$ORG_FILE")
    TEMP_MP3="/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi/logs/tmp_speech.mp3"
    
    # Requesting with explicit model and output_format
    curl -s -f -L -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID?output_format=mp3_44100_128" \
         -A "$USER_AGENT" \
         -H "xi-api-key: $API_KEY" \
         -H "Content-Type: application/json" \
         -H "Accept: audio/mpeg" \
         -d "{
               \"text\": \"$text\",
               \"model_id\": \"eleven_multilingual_v2\",
               \"voice_settings\": {
                 \"stability\": 0.5,
                 \"similarity_boost\": 0.75
               }
             }" -o "$TEMP_MP3" 2>> "$LOG_FILE"

    if [ $? -eq 0 ] && [ -s "$TEMP_MP3" ]; then
        # Background the playback and cleanup so the script returns immediately
        (play -q "$TEMP_MP3" && rm -f "$TEMP_MP3") 2>> "$LOG_FILE" &
        echo "$(date): ElevenLabs success (backgrounded)" >> "$LOG_FILE"
        exit 0
    fi
    
    # Error capture
    ERROR_BODY=$(curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID" \
         -A "$USER_AGENT" \
         -H "xi-api-key: $API_KEY" \
         -H "Content-Type: application/json" \
         -d "{\"text\": \"$text\"}")
    echo "$(date): ElevenLabs failed. Body: $ERROR_BODY" >> "$LOG_FILE"
fi

# Fallback
if command -v termux-tts-speak > /dev/null 2>&1; then
    termux-tts-speak -l help -p 1.15 -r 1.15 -s MUSIC "$text"
else
    espeak -v en-gb+f2 -p 75 -s 175 -k 1 -g 2 "$text"
fi
