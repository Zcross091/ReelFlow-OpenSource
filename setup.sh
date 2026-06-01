#!/bin/bash

echo "🔄 Updating system packages..."
sudo apt update -y

echo "🎥 Installing FFmpeg..."
sudo apt install ffmpeg -y

echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Setup Complete! You are ready to run the bot."

# RUN THE FOLLOWING:
#chmod +x setup.sh
#./setup.sh
