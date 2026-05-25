import os
from datetime import datetime, timedelta

def cleanup_downloads(directory="downloads", hours=22):
    if not os.path.exists(directory):
        return
    now = datetime.now()
    cutoff = now - timedelta(hours=hours)
    
    deleted = 0
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if datetime.fromtimestamp(os.path.getmtime(filepath)) < cutoff:
                try:
                    os.remove(filepath)
                    deleted += 1
                except:
                    pass
    print(f"🗑️ Cleanup completed. Deleted {deleted} old files.")
