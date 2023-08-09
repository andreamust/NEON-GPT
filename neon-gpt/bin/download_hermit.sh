#!/bin/bash

# URL for HermiT reasoner download
HERMIT_URL="http://www.hermit-reasoner.com/download/current/HermiT.zip"

# Directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Download HermiT.zip
echo "Downloading HermiT..."
curl -L -o "$SCRIPT_DIR/HermiT.zip" "$HERMIT_URL"

# Unzip HermiT.zip
echo "Unzipping HermiT..."
unzip "$SCRIPT_DIR/HermiT.zip" -d "$SCRIPT_DIR"

# Move HermiT executable to parent directory
echo "Moving HermiT to parent directory..."
mv "$SCRIPT_DIR/hermit/bin/HermiT" "$SCRIPT_DIR/"

# Clean up the downloaded zip file and extracted folder
rm "$SCRIPT_DIR/HermiT.zip"
rm -r "$SCRIPT_DIR/hermit"

echo "HermiT has been downloaded and moved to the parent directory."
