#!/bin/bash
# Chloe Google Cloud SDK Installation Script for Termux
# This script installs the gcloud CLI to enable cloud-native architecture.

echo "Initiating Chloe's Google Cloud Integration..."

# Install dependencies
pkg install -y python3 curl gnupg

# Download and install Google Cloud SDK
if [ ! -d "$HOME/google-cloud-sdk" ]; then
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-arm.tar.gz
    tar -xf google-cloud-cli-linux-arm.tar.gz
    ./google-cloud-sdk/install.sh --quiet
    rm google-cloud-cli-linux-arm.tar.gz
fi

# Source the bash completion and path
source $HOME/google-cloud-sdk/path.bash.inc
source $HOME/google-cloud-sdk/completion.bash.inc

echo "Google Cloud SDK Installation Complete."
echo "Action Required: Please run 'gcloud auth login' to synchronize Chloe with your Google Cloud Terminal account."
