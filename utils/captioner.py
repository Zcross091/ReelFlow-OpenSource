import random

def generate_caption(niche="Demon Slayer"):
    templates = [
        f"🔥 Epic {niche} moment! Which scene is your favorite? 💥 #Anime # {niche.replace(' ', '')}",
        # Add more
    ]
    hashtags = "#Anime #Naruto #OnePiece #JujutsuKaisen #Reels"  # Rotate smartly
    return random.choice(templates) + "\n\n" + hashtags