import random

def generate_anime_caption():
    templates = [
        "🔥 This scene hit different! 😱\n\n",
        "💥 Absolute cinema! Tag your squad 👇\n\n",
        "🌟 Anime peak moment 🔥\n\n"
    ]
    hashtags = "#Anime #JujutsuKaisen #DemonSlayer #OnePiece #AttackOnTitan #Naruto #AnimeReels #Viral"
    return random.choice(templates) + hashtags
