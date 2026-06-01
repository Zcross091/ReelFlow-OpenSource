import schedule
import time
import os
import logging
from datetime import datetime
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired

from config import INSTA_USER, INSTA_PASS, INSTA_PROXY
from utils.downloader import download_random_clip
from utils.caption_generator import generate_anime_caption
import schedule
import time
import os
import logging
from datetime import datetime
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired

from config import INSTA_USER, INSTA_PASS
from utils.downloader import download_random_clip
from utils.caption_generator import generate_anime_caption
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

# ── Login ─────────────────────────────────────────────────────────────────────
if os.path.exists(SESSION_FILE):
    log.info("🔄 Loading saved session...")
    cl.load_settings(SESSION_FILE)

try:
    cl.login(INSTA_USER, INSTA_PASS)
    cl.dump_settings(SESSION_FILE)
    log.info("✅ Login successful & session saved")
except ChallengeRequired:
    log.error("🔒 Instagram Challenge Required! Approve login from your phone app.")
    exit(1)
except Exception as e:
    log.error(f"❌ Login failed: {e}")
    exit(1)

# ── Main Job ──────────────────────────────────────────────────────────────────
def job():
    global _consecutive_failures
    log.info(f"🚀 Starting post job at {datetime.now().strftime('%H:%M')}")

    try:
        filepath, creator_name = download_random_clip()

        if filepath and os.path.exists(filepath):
            caption = generate_anime_caption(creator_name=creator_name or "Unknown Creator")
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

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(30)
