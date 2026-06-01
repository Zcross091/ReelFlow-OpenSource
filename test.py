import os
from instagrapi import Client
from config import INSTA_USER, INSTA_PASS
from utils.downloader import download_random_clip
from utils.caption_generator import generate_anime_caption
from utils.poster import post_to_instagram

print("🧪 Starting Manual Post Test...")

# 1. Initialize Client
cl = Client()

# FIX: Only load the session if the file actually exists
if os.path.exists("session.json"):
    print("🔄 Loading saved session...")
    cl.load_settings("session.json")

# 2. Login and save session
try:
    cl.login(INSTA_USER, INSTA_PASS)
    cl.dump_settings("session.json") # This creates the file!
    print("✅ Logged in successfully!")
except Exception as e:
    print(f"❌ Login failed: {e}")
    exit(1)

# 3. Get the video and post
filepath, creator_name = download_random_clip()

if filepath and os.path.exists(filepath):
    print(f"✅ Ready to post: {filepath}")
    
    # FIX: Satisfies Pylance type checker by ensuring a string
    safe_creator = creator_name if creator_name else "Unknown Creator" 
    
    caption = generate_anime_caption(safe_creator)
    post_to_instagram(filepath, caption, cl)
else:
    print("❌ No file available to post.")