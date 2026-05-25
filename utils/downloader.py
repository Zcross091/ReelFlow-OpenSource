import os
import random
import yt_dlp
from datetime import datetime

def download_random_clip(save_dir="downloads"):
    os.makedirs(save_dir, exist_ok=True)
    
    # FIRST: Check if there are manually downloaded files in /downloads/
    existing_files = [f for f in os.listdir(save_dir) if f.endswith(('.mp4', '.mkv', '.mov'))]
    if existing_files:
        selected = random.choice(existing_files)
        filepath = os.path.join(save_dir, selected)
        print(f"✅ Using existing file: {selected}")
        return filepath
    
    # SECOND: Try automated download from YouTube
    print("📥 No local files found. Attempting YouTube download...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"anime_clip_{timestamp}.mp4"
    filepath = os.path.join(save_dir, filename)

    sources = [
        "https://www.youtube.com/results?search_query=one+piece+shorts",
        "https://www.youtube.com/results?search_query=jujutsu+kaisen+shorts",
        "https://www.youtube.com/results?search_query=demon+slayer+shorts",
    ]

    random.shuffle(sources)

    ydl_opts = {
        'outtmpl': filepath,
        'format': 'best[height<=1080]/best',
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'playlistend': 2,
        'socket_timeout': 30,
    }

    for attempt, url in enumerate(sources, 1):
        try:
            print(f"🔍 Attempt {attempt}: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if os.path.exists(filepath) and os.path.getsize(filepath) > 500000:
                print(f"✅ Downloaded: {filepath}")
                return filepath
            elif os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            pass
    
    print("⚠️ YouTube downloads blocked. Add MP4 files to /downloads/ folder manually.")
    return None
