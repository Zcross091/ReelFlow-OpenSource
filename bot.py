import schedule
import time
from utils.downloader import download_reel
from utils.caption_generator import generate_caption
from utils.poster import post_to_ig
from utils.cleaner import cleanup_old_files
import json

def job():
    # Example: Fetch new content logic (replace with scraping or RSS if available)
    # For demo: assume a list of public URLs or implement search
    sample_url = "https://example-public-anime-clip-url"  
    filepath = download_reel(sample_url)
    caption = generate_caption("One Piece")
    post_to_ig(filepath, caption)
    # Optional: cleanup_old_files() after post

# Schedule
schedule.every(1).hours.do(job)  # Every hour
schedule.every(20).hours.do(cleanup_old_files)  # Periodic clean

print("Bot started...")
while True:
    schedule.run_pending()
    time.sleep(60)