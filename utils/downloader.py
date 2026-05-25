import requests
import yt_dlp
import os
from datetime import datetime

def download_reel(url, save_path="downloads"):
    os.makedirs(save_path, exist_ok=True)
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M')}.mp4"
    filepath = os.path.join(save_path, filename)
    
    ydl_opts = {'outtmpl': filepath, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filepath