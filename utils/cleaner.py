import os
import shutil
from datetime import datetime, timedelta

def cleanup_old_files(directory="downloads", hours=24):
    now = datetime.now()
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if os.path.getmtime(path) < (now - timedelta(hours=hours)).timestamp():
            os.remove(path)
    print("Cleanup done.")