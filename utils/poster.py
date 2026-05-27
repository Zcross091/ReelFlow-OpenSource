import os

def post_to_instagram(filepath, caption, cl):
    try:
        if filepath.lower().endswith(('.mp4', '.mov')):
            cl.clip_upload(filepath, caption=caption)
        else:
            cl.photo_upload(filepath, caption=caption)

        print("🎉 Successfully posted!")
        return True

    except Exception as e:
        print(f"❌ Error: {str(e)[:250]}")
        print("💡 Tip: Try logging into Instagram manually to clear security checks.")
        return False
