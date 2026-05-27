import os
from dotenv import load_dotenv

load_dotenv()

INSTA_USER = os.getenv("INSTAGRAM_USERNAME")
INSTA_PASS = os.getenv("INSTAGRAM_PASSWORD")
INSTA_PROXY = os.getenv("INSTAGRAM_PROXY")