from instagrapi import Client

def post_to_ig(filepath, caption):
    cl = Client()
    cl.login(INSTA_USER, INSTA_PASS)  # Session persistence better in prod
    if filepath.endswith('.mp4'):
        cl.clip_upload(filepath, caption)
    else:
        cl.photo_upload(filepath, caption)
    print("Posted!")