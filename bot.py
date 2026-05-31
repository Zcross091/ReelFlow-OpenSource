import schedule
import time
import os
import logging
from datetime import datetime
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, ClientError

from config import INSTA_USER, INSTA_PASS, INSTA_PROXY
from utils.downloader import download_random_clip
from utils.caption_generator import generate_anime_caption
from utils.poster import post_to_instagram
from utils.cleaner import cleanup_downloads

# ── Logging Setup ─────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler(),
    ],
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

SESSION_FILE = "session.json"
MAX_LOGIN_RETRIES = 3
_consecutive_failures = 0
MAX_CONSECUTIVE_FAILURES = 3

# ── Client Setup ─────────────────────────────────────────────────────────────
def build_client() -> Client:
    cl = Client()
    cl.set_user_agent("Instagram 275.0.0.27.98 Android")
    cl.set_locale("en_US")
    cl.set_timezone_offset(19800)  # IST (India)
    if INSTA_PROXY:
        log.info(f"🌍 Using proxy: {INSTA_PROXY}")
        cl.set_proxy(INSTA_PROXY)
    return cl

def login(cl: Client) -> bool:
    """Attempt login with session reuse first"""
    # Try existing session
    if os.path.exists(SESSION_FILE):
        log.info("🔄 Loading existing session...")
        cl.load_settings(SESSION_FILE)
        try:
            cl.get_timeline_feed()
            log.info("✅ Session is still valid")
            return True
        except (LoginRequired, ClientError):
            log.warning("⚠️ Session expired, trying fresh login...")

    # Fresh login with retries
    for attempt in range(1, MAX_LOGIN_RETRIES + 1):
        try:
            cl.login(INSTA_USER, INSTA_PASS)
            cl.dump_settings(SESSION_FILE)
            log.info("✅ Login successful & session saved")
            return True
        except ChallengeRequired:
            log.error("🔒 Instagram Challenge Required! Please approve login from your phone.")
            return False
        except Exception as e:
            log.warning(f"Login attempt {attempt} failed: {e}")
            if attempt < MAX_LOGIN_RETRIES:
                time.sleep(30 * attempt)

    log.error("❌ All login attempts failed.")
    return False

# ── Initialize Client ────────────────────────────────────────────────────────
log.info("🔐 Initializing Instagram client...")
cl = build_client()

if not login(cl):
    log.error("Cannot start bot - login failed. Fix credentials/challenge and restart.")
    exit(1)

# ── Main Job ─────────────────────────────────────────────────────────────────
def job():
    global _consecutive_failures
    log.info(f"🚀 Starting post job at {datetime.now().strftime('%H:%M')}")

    try:
        # Quick session check
        try:
            cl.get_timeline_feed()
        except (LoginRequired, ClientError):
            log.warning("Session expired. Re-logging in...")
            if not login(cl):
                _consecutive_failures += 1
                return

        filepath, creator_name = download_random_clip()

        if filepath and os.path.exists(filepath):
            caption = generate_anime_caption(creator_name=creator_name)
            success = post_to_instagram(filepath, caption, cl)

            if success:
                log.info(f"✅ Post successful | Creator: {creator_name}")
                _consecutive_failures = 0
            else:
                log.error("❌ Post failed")
                _consecutive_failures += 1
        else:
            log.warning("⚠️ No clip available this cycle")

    except Exception as e:
        log.exception(f"Unexpected error in job: {e}")
        _consecutive_failures += 1

    # Safety pause after repeated failures
    if _consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
        log.error(f"🛑 {MAX_CONSECUTIVE_FAILURES} consecutive failures. Pausing for 1 hour.")
        time.sleep(3600)
        _consecutive_failures = 0

# ── Scheduling ───────────────────────────────────────────────────────────────
schedule.every().day.at("08:00").do(job)
schedule.every().day.at("15:00").do(job)
schedule.every().day.at("22:00").do(job)
schedule.every().day.at("23:00").do(cleanup_downloads)

log.info("🤖 Anime Instagram Reels Bot Started Successfully!")
log.info("Posting times → 08:00 | 15:00 | 22:00")
log.info(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ── Main Loop ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(30)
