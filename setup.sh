#!/bin/bash

echo "🚀 Starting ReelFlow Auto-Installer..."

# 1. Detect the Operating System / Environment
if [ -d "/data/data/com.termux/files/usr" ]; then
    echo "📱 Termux (Android) environment detected!"
    PKG_MANAGER="pkg"
    SUDO_CMD=""
else
    echo "💻 Linux/WSL environment detected!"
    PKG_MANAGER="apt"
    SUDO_CMD="sudo"
fi

# 2. Update System Packages
echo "🔄 Updating system packages..."
$SUDO_CMD $PKG_MANAGER update -y && $SUDO_CMD $PKG_MANAGER upgrade -y

# 3. Install Core System Dependencies
echo "🎥 Installing system tools and compilers..."
$SUDO_CMD $PKG_MANAGER install ffmpeg python rust clang make -y

# 4. Install Python Libraries
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# 5. Account Configuration (THE FIX)
echo ""
echo "========================================"
echo "      ⚙️  ACCOUNT CONFIGURATION ⚙️      "
echo "========================================"
echo "Please enter the Instagram account details for the bot."

read -p "👤 Instagram Username: " INSTA_USER

# The -s flag hides the password as they type it for security
read -s -p "🔑 Instagram Password: " INSTA_PASS
echo ""

read -p "🌍 (Optional) Enter proxy URL (or press Enter to skip): " INSTA_PROXY

# Create the .env file automatically
echo "INSTAGRAM_USERNAME=$INSTA_USER" > .env
echo "INSTAGRAM_PASSWORD=$INSTA_PASS" >> .env
echo "INSTAGRAM_PROXIES=$INSTA_PROXY" >> .env

echo "✅ Credentials saved securely to .env!"
echo ""

# 6. Launch the Engine
echo "✅ Setup Complete!"
echo "🤖 Booting up ReelFlow Engine..."
python bot.py