import schedule
import time
import os
import logging
from datetime import datetime

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

def job():
    print(f"\n🚀 Starting post job at {datetime.now()}")
    logging.info("Starting scheduled post job")
    
    filepath = download_random_clip()
    
    if filepath and os.path.exists(filepath):
        caption = generate_anime_caption()
        success = post_to_instagram(filepath, caption)
        if success:
            logging.info("✅ Post completed successfully")
        else:
            logging.error("❌ Post failed")
    else:
        logging.warning("⚠️ No file downloaded this cycle")

# Scheduling
schedule.every(1).hours.do(job)
schedule.every(22).hours.do(cleanup_downloads)

print("🤖 Anime Instagram Reels Bot Started!")
print(f"Current Time: {datetime.now()}")
print("→ Posting every 1 hour")
print("→ Auto cleanup every 22 hours")

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(30)
