#!/bin/bash

echo "🚀 Starting ReelFlow Auto-Installer..."

# 1. Detect the Operating System / Environment
if [ -d "/data/data/com.termux/files/usr" ]; then
    echo "📱 Termux (Android) environment detected!"
    PKG_MANAGER="pkg"
    SUDO_CMD="" # Termux does not use sudo
else
    echo "💻 Linux/WSL environment detected!"
    PKG_MANAGER="apt"
    SUDO_CMD="sudo"
fi

# 2. Update System Packages
echo "🔄 Updating system packages..."
$SUDO_CMD $PKG_MANAGER update -y && $SUDO_CMD $PKG_MANAGER upgrade -y

# 3. Install Core System Dependencies
echo "🎥 Installing FFmpeg and Python..."
$SUDO_CMD $PKG_MANAGER install ffmpeg python -y

# 4. Install Python Libraries
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# 5. Launch the Engine
echo "✅ Setup Complete!"
echo "🤖 Booting up ReelFlow Engine..."
python bot.py