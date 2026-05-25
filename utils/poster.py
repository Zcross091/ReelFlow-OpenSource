from instagrapi import Client
from config import INSTA_USER, INSTA_PASS
import os

def post_to_instagram(filepath, caption):
    try:
        cl = Client()
        cl.set_user_agent("Instagram 275.0.0.27.98 Android")
        cl.set_locale('en_US')
        
        session_file = "session.json"
        if os.path.exists(session_file):
            cl.load_settings(session_file)

        # === ADD FREE/PROXY HERE ===
        # Example: cl.set_proxy("http://ip:port")   # or socks5://
        
        cl.login(INSTA_USER, INSTA_PASS)
        cl.dump_settings(session_file)
        
        if filepath.lower().endswith(('.mp4', '.mov')):
            cl.clip_upload(filepath, caption=caption)
        else:
            cl.photo_upload(filepath, caption=caption)
            
        print("🎉 Successfully posted!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)[:250]}")
        return False
