# ReelFlow - Open Source

# Anime Instagram Reels Bot 🤖

**Want to run this yourself?** Follow the technical guide below to set up on Codespaces, configure mobile tunnels, and manage IP rotations.

**Don't want to deal with terminals, Termux, and IP bans?**

🚀 **[Click here to use our fully hosted 24/7 Cloud Service](https://discord.gg/hQn49uFsNS)** — Zero setup, fully managed automation.

---

Automated Instagram bot specialized in posting **viral anime reels** every hour.

Built for anime content creators who want consistent growth with minimal effort.

---

## ✨ Features

- **🎥 Automatic Content Downloading** — Pulls latest anime shorts from YouTube and public sources
- **✍️ AI-Powered Captions** — Generates engaging titles and trending hashtags
- **⏰ Hourly Auto Posting** — Posts Reels every hour consistently
- **🧹 Smart Storage Management** — Auto deletes old files every 22 hours
- **🔐 Session Management** — Saves sessions to reduce ban risk
- **☁️ Easy Deployment** — Works perfectly on VPS, or local machine

---

## 🚀 Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Setup your `.env` file with Instagram credentials
4. Run `python bot.py`

---

## 🤝 Community & Links

Need help with setup or want a **fully managed hosted version**?

[![Join Discord](https://img.shields.io/badge/Join_Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/hQn49uFsNS)
[![Visit Website](https://img.shields.io/badge/Visit_Website-00ff9d?style=for-the-badge&logo=globe&logoColor=black)](https://animereel-ai.gt.tc)

---
## Clone (PC/Phones)

```bash
git clone https://github.com/Zcross091/ReelFlow-OpenSource.git && cd ReelFlow-OpenSource && chmod +x setup.sh && ./setup.sh
```
## For Phones
**IF** the setup fails to automatically do the job, because you're not on a PC, then do this.
You phone can't run Rust files to Pydantic will crash and Setup.sh won't get to run properly and crash the whole program. To fix this
**Install the compilers (Run this in your terminal)**
This might take a few minutes to install as the Rust compiler is a large package.
```bash
pkg install rust clang make -y
```
**Run the Python installation**
```bash
pip install -r requirements.txt
```
**Run the bot**
```bash
python bot.py
```
### If you want to remove from Phone
Go to app settings and clear data then
Clear the Termux package cache:
(This deletes the invisible installer .deb files that Termux downloaded but no longer needs).

```bash
pkg clean
```

**Made for the Anime Community** 

© 2026 ReelFlow • AnimeReel AI
