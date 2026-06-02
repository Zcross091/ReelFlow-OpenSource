import schedule
import time
import os
import logging
from datetime import datetime
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, ClientError

from config import INSTA_USER, INSTA_PASS
from utils.downloader import download_random_clip
from utils.caption_generator import generate_caption_for_series # Swapped generator import
from utils.poster import post_to_instagram
from utils.cleaner import cleanup_downloads
from utils.proxy_rotator import PROXY_LIST, apply_next_proxy

# ── Logging ───────────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler("logs/bot.log"), logging.StreamHandler()],
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

SESSION_FILE = "session.json"
_consecutive_failures = 0
MAX_CONSECUTIVE_FAILURES = 3

# ── Instagram Client Setup ────────────────────────────────────────────────────
log.info("🔐 Initializing Instagram client...")
cl = Client()
cl.set_user_agent("Instagram 275.0.0.27.98 Android")
cl.set_locale("en_US")
cl.set_timezone_offset(19800)  # IST

if PROXY_LIST:
    apply_next_proxy(cl)
    log.info(f"🌍 Loaded {len(PROXY_LIST)} proxy(ies)")
else:
    log.warning("⚠️ No proxies configured — running without proxy rotation.")

# ── Login Logic ───────────────────────────────────────────────────────────────
def login_user(client):
    """Handles login logic and securely saves the session token."""
    if os.path.exists(SESSION_FILE):
        log.info("🔄 Loading saved session...")
        client.load_settings(SESSION_FILE)

    try:
        client.login(INSTA_USER, INSTA_PASS)
        client.dump_settings(SESSION_FILE)
        log.info("✅ Login successful & session saved")
        return True
    except ChallengeRequired:
        log.error("🔒 Instagram Challenge Required! Approve login from your phone app.")
        return False
    except Exception as e:
        log.error(f"❌ Login failed: {e}")
        return False

# Initial boot login
if not login_user(cl):
    exit(1)

# ── Main Job ──────────────────────────────────────────────────────────────────
def job():
    global _consecutive_failures
    log.info(f"🚀 Starting post job at {datetime.now().strftime('%H:%M')}")

    try:
        # Quick session check (Revives the session if Instagram dropped it)
        try:
            cl.get_timeline_feed()
        except (LoginRequired, ClientError):
            log.warning("⚠️ Session expired or invalid. Re-logging in...")
            if not login_user(cl):
                _consecutive_failures += 1
                return

        # Download & Post (Unpacks all 3 return values)
        filepath, creator_name, video_title = download_random_clip()

        if filepath and os.path.exists(filepath):
            # Pass the extracted title directly as the series hint
            caption = generate_caption_for_series(
                series_hint=video_title or "", 
                creator_name=creator_name or "Unknown Creator"
            )
            success = post_to_instagram(filepath, caption, cl)

            if success:
                log.info(f"✅ Post successful | Creator: {creator_name}")
                _consecutive_failures = 0
            else:
                log.error("❌ Post failed")
                _consecutive_failures += 1
                apply_next_proxy(cl)   # Rotate proxy on failure
        else:
            log.warning("⚠️ No clip available this cycle")

    except Exception as e:
        log.exception(f"Error during job: {e}")
        _consecutive_failures += 1
        apply_next_proxy(cl)

    # Safety pause after repeated failures
    if _consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
        log.error("🛑 Too many consecutive failures — pausing for 1 hour.")
        time.sleep(3600)
        _consecutive_failures = 0

# ── Schedule ──────────────────────────────────────────────────────────────────
schedule.every().day.at("08:00").do(job)
schedule.every().day.at("15:00").do(job)
schedule.every().day.at("22:00").do(job)
schedule.every().day.at("23:00").do(cleanup_downloads)

log.info("🤖 Bot Started | Posts at 08:00, 15:00, 22:00 | Cleanup at 23:00")

# ── Main Loop ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(30)