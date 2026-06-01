import os
import random
import re
import time
import yt_dlp
from yt_dlp import utils as ytd_utils
from datetime import datetime

def download_random_clip(save_dir="downloads", max_retries: int = 3, size_threshold: int = 500000):
    os.makedirs(save_dir, exist_ok=True)

    # FIRST: Use manually downloaded files if available.
    existing_files = [f for f in os.listdir(save_dir) if f.endswith(('.mp4', '.mkv', '.mov'))]
    if existing_files:
        selected = random.choice(existing_files)
        filepath = os.path.join(save_dir, selected)
        print(f"✅ Using existing file: {selected}")
        return filepath, "Unknown Creator"

    # SECOND: Try an automated YouTube search download with retries and proxy rotation.
    print("📥 No local files found. Attempting YouTube download...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(save_dir, f"anime_clip_{timestamp}.mp4")

    # Grab the proxy(s) from the environment and parse/validate them
    proxy_env = os.getenv("INSTAGRAM_PROXIES") or os.getenv("INSTAGRAM_PROXY") or ""
    proxy_candidates = [p.strip() for p in re.split(r"[,;\s]+", proxy_env) if p.strip()]
    def _valid_proxy(p: str) -> bool:
        return p.startswith(("http://", "https://", "socks5://", "socks5h://", "socks4://"))
    proxies = [p for p in proxy_candidates if _valid_proxy(p)]
    if proxy_candidates and not proxies:
        print("⚠️ INSTAGRAM_PROXIES set but no valid proxy urls detected; ignoring proxies.")

    queries = ["anime edits shorts", "jujutsu kaisen amv short", "demon slayer edit short"]

    # Base yt-dlp options; tuned for merging and resilience
    ydl_base_opts = {
        'outtmpl': filepath,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'default_search': 'ytsearch5',
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'socket_timeout': 30,
        'http_chunk_size': 1048576,
        'retries': max_retries,
        'merge_output_format': 'mp4',
    }

    for attempt in range(1, max_retries + 1):
        opts = ydl_base_opts.copy()
        # rotate proxies if provided
        if proxies:
            proxy = proxies[(attempt - 1) % len(proxies)]
            opts['proxy'] = proxy
            print(f"🌍 Attempt {attempt}: Using proxy {proxy}")

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                # fetch a search result first
                info = ydl.extract_info(random.choice(queries), download=False)
                entries = info.get('entries') or []
                if not entries:
                    raise RuntimeError("No entries returned from ytsearch")

                video = random.choice(entries)
                video_url = video.get('webpage_url') or f"https://www.youtube.com/watch?v={video.get('id')}"
                creator = video.get('uploader', 'Unknown Creator')

                print(f"⬇️ Downloading {video_url} (attempt {attempt})")
                ydl.download([video_url])

                if os.path.exists(filepath) and os.path.getsize(filepath) > size_threshold:
                    print(f"✅ Downloaded: {filepath}")
                    return filepath, creator
                else:
                    raise RuntimeError(f"Downloaded file missing or below size threshold ({size_threshold} bytes)")

        except Exception as e:
            # Provide richer error info and decide whether to retry
            err_type = type(e).__name__
            # Try to unwrap yt-dlp specific errors for clearer messages
            msg = str(e)
            if isinstance(e, ytd_utils.DownloadError):
                msg = getattr(e, 'exc_info', msg)

            print(f"❌ Attempt {attempt}/{max_retries} failed: {err_type}: {msg}")
            if attempt < max_retries:
                backoff = min(30, 2 ** attempt)
                print(f"↩️ Retrying after {backoff}s...")
                time.sleep(backoff)
                continue
            else:
                print("🚫 All download attempts failed.")
                return None, None

    return None, None