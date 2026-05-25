import os
from dotenv import load_dotenv

load_dotenv()

INSTA_USER = os.getenv("INSTAGRAM_USERNAME")
INSTA_PASS = os.getenv("INSTAGRAM_PASSWORD")

SOURCES = ["target_anime_account1", "target2"]  # Or load from JSON