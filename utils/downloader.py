import os
import random
import yt_dlp
from datetime import datetime

def download_random_clip(save_dir="downloads"):
    os.makedirs(save_dir, exist_ok=True)
    
    # FIRST: Use manually downloaded files if available.
    existing_files = [f for f in os.listdir(save_dir) if f.endswith(('.mp4', '.mkv', '.mov'))]
    if existing_files:
        selected = random.choice(existing_files)
        filepath = os.path.join(save_dir, selected)
        print(f"✅ Using existing file: {selected}")
        return filepath, "Unknown Creator"

    # SECOND: Try an automated YouTube search download.
    print("📥 No local files found. Attempting YouTube download...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"anime_clip_{timestamp}.mp4"
    filepath = os.path.join(save_dir, filename)

    queries = [
        "anime edits shorts",
        "jujutsu kaisen amv short",
        "demon slayer edit short",
        "one piece shorts",
    ]
    search_query = random.choice(queries)

    ydl_opts = {
        'outtmpl': filepath,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'default_search': 'ytsearch5',
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'socket_timeout': 30,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            entries = info.get('entries') or []

            if not entries:
                print("⚠️ No search results found.")
                return None, None

            video = random.choice(entries)
            video_url = video.get('webpage_url') or f"https://www.youtube.com/watch?v={video.get('id')}"
            creator = video.get('uploader', 'Unknown Creator')

            print(f"🔍 Downloading video from: {video_url}")
            ydl.download([video_url])

            if os.path.exists(filepath) and os.path.getsize(filepath) > 500000:
                print(f"✅ Downloaded: {filepath}")
                return filepath, creator
            elif os.path.exists(filepath):
                os.remove(filepath)

    except Exception as e:
        print(f"Error downloading clip: {e}")

    print("⚠️ YouTube download failed. Add MP4 files to /downloads/ folder manually.")
    return None, None
