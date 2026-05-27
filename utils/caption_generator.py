import random

def generate_anime_caption(creator_name="Unknown Creator"):
    templates = [
        "🔥 This scene hit different! 😱\n\n",
        "💥 Absolute cinema! Tag your squad 👇\n\n",
        "🌟 Anime peak moment 🔥\n\n"
    ]
    hashtags = "#Anime #JujutsuKaisen #DemonSlayer #OnePiece #AttackOnTitan #Naruto #AnimeReels #Viral"
    credit = f"\n\nCredit to {creator_name} on YouTube for the original edit! (DM for removal)"
    return random.choice(templates) + hashtags + credit
