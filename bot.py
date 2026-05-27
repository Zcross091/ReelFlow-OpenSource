import schedule
import time
import os
import logging
from datetime import datetime

from instagrapi import Client
from config import INSTA_USER, INSTA_PASS, INSTA_PROXY
from utils.downloader import download_random_clip
from utils.caption_generator import generate_anime_caption
from utils.poster import post_to_instagram
from utils.cleaner import cleanup_downloads

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    filename='logs/bot.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("🔐 Initializing Instagram client...")
cl = Client()
cl.set_user_agent("Instagram 275.0.0.27.98 Android")
cl.set_locale('en_US')
session_file = "session.json"

# 1. Try to load an existing session first
if os.path.exists(session_file):
    print("🔄 Loading saved session settings...")
    cl.load_settings(session_file)

if INSTA_PROXY:
    print(f"🌍 Using proxy for safer login...")
    cl.set_proxy(INSTA_PROXY)

try:
    # 2. Login (If a valid session was loaded, this will safely bypass a fresh login)
    cl.login(INSTA_USER, INSTA_PASS)

    # 3. Save the fresh session data for next time
    cl.dump_settings(session_file)
    print("✅ Login successful & session saved!")

except Exception as e:
    print(f"❌ Login failed: {e}")
    print("Try logging into the app manually to clear any security checks.")
    exit(1)

def job():
    print(f"\n🚀 Starting post job at {datetime.now()}")
    logging.info("Starting scheduled post job")

    try:
        filepath, creator_name = download_random_clip()

        if filepath and os.path.exists(filepath):
            caption = generate_anime_caption(creator_name)
            success = post_to_instagram(filepath, caption, cl)
            if success:
                logging.info(f"✅ Post completed successfully. Credited: {creator_name}")
            else:
                logging.error("❌ Post failed")
        else:
            logging.warning("⚠️ No file downloaded this cycle")
    except Exception as e:
        logging.exception(f"Unexpected error during scheduled post job: {e}")

# Scheduling - Post 3x daily at 7-hour intervals (8 AM, 3 PM, 10 PM) and clean disk at 11 PM
schedule.every().day.at("08:00").do(job)
schedule.every().day.at("15:00").do(job)
schedule.every().day.at("22:00").do(job)
schedule.every().day.at("23:00").do(cleanup_downloads)

print("🤖 Anime Instagram Reels Bot Started!")
print(f"Current Time: {datetime.now()}")
print("→ Posting at 8:00 AM, 3:00 PM, 10:00 PM")
print("→ Cleaning disk at 11:00 PM")

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(30)
