import random
from datetime import datetime

# ── Themed caption pools ──────────────────────────────────────────────────────
_HOOKS = {
    "hype": [
        "This scene lives rent-free in my head 🔥",
        "The animation budget said GO OFF 😤",
        "Studio just said 'spend it all' 🤯",
        "Frame by frame perfection 👁️",
        "This is WHY we watch anime 🔥",
    ],
    "emotional": [
        "That piano drop hits every single time 💔",
        "I did NOT sign up to feel this today 😭",
        "The way this scene is perfectly written 🥺",
        "Living in my head at 3am rent-free 🌙",
        "Some scenes you never unsee 💔",
    ],
    "hype_short": [
        "Absolute cinema. No notes. 🎬",
        "IYKYK 👀🔥",
        "POV: Peak anime 🗿",
        "Not skippable. Ever. ⚡",
        "This scene broke the internet for a reason 💥",
    ],
    "question": [
        "Drop your favourite arc in the comments 👇",
        "Which scene hits harder? Comment below 🔥",
        "Who else had chills watching this? 👇",
        "What series are you watching right now? 👇",
        "Rate this scene 1-10 in the comments 👇",
    ],
}

_CTA = [
    "Follow for daily anime content 🔔",
    "Turn on notifications so you never miss a drop 🔔",
    "Save this for when you need serotonin ✨",
    "Share with someone who needs to start this series 👀",
    "Tag someone who hasn't watched this yet 👇",
]

_HASHTAG_POOLS = {
    "general": [
        "#Anime", "#AnimeReels", "#AnimeCommunity", "#AnimeEdit",
        "#AnimeLover", "#AnimeDaily", "#AnimeClips", "#Viral",
        "#FYP", "#ForYouPage", "#AnimeFan", "#OtakuLife",
    ],
    "series": [
        "#JujutsuKaisen", "#JJK", "#DemonSlayer", "#KimetsuNoYaiba",
        "#OnePiece", "#AttackOnTitan", "#SNK", "#Naruto",
        "#Bleach", "#HunterXHunter", "#HxH", "#MyHeroAcademia",
        "#MHA", "#TokyoRevengers", "#ChainsawMan", "#BlueLock",
    ],
    "meta": [
        "#AnimeRecommendations", "#MustWatch", "#AnimeMoments",
        "#BestAnime", "#TopAnime", "#AnimeScene",
    ],
}

# Day-of-week tone bias
_DAY_TONE = {
    0: "hype",      # Monday
    1: "emotional", # Tuesday
    2: "hype",      # Wednesday
    3: "question",  # Thursday
    4: "hype_short",# Friday
    5: "hype",      # Saturday
    6: "emotional", # Sunday
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def _pick_hashtags(n_general=5, n_series=5, n_meta=2) -> str:
    tags = (
        random.sample(_HASHTAG_POOLS["general"], min(n_general, len(_HASHTAG_POOLS["general"])))
        + random.sample(_HASHTAG_POOLS["series"], min(n_series, len(_HASHTAG_POOLS["series"])))
        + random.sample(_HASHTAG_POOLS["meta"], min(n_meta, len(_HASHTAG_POOLS["meta"])))
    )
    random.shuffle(tags)
    return " ".join(tags)

def _credit_line(creator_name: str) -> str:
    templates = [
        f"🎬 Credit: {creator_name} on YouTube (DM to remove)",
        f"✂️ Edit by {creator_name} — all credit to the original creator",
        f"📹 Original edit by {creator_name} on YouTube (DM for removal)",
    ]
    return random.choice(templates)

# ── Main Function ─────────────────────────────────────────────────────────────
def generate_anime_caption(
    creator_name: str = "Unknown Creator",
    tone: str | None = None,
) -> str:
    """
    Generate high-quality, varied Instagram captions.
    """
    if tone is None:
        tone = _DAY_TONE[datetime.now().weekday()]

    hook = random.choice(_HOOKS[tone])
    parts = [hook, ""]

    # Add engagement question (unless tone is already question)
    if tone != "question":
        parts.append(random.choice(_HOOKS["question"]))
        parts.append("")

    # Add CTA
    parts.append(random.choice(_CTA))
    parts.append("")

    # Hashtags
    parts.append(_pick_hashtags())
    parts.append("")

    # Credit line
    parts.append(_credit_line(creator_name))

    return "\n".join(parts)


# Optional: Series-aware version
def generate_caption_for_series(series_hint: str, creator_name: str = "Unknown Creator") -> str:
    base = generate_anime_caption(creator_name)
    hint_lower = series_hint.lower()

    series_tags = {
        "jujutsu": ["#JujutsuKaisen", "#JJK", "#GojouSatoru"],
        "demon slayer": ["#DemonSlayer", "#KimetsuNoYaiba"],
        "one piece": ["#OnePiece", "#Luffy"],
        "attack on titan": ["#AttackOnTitan", "#SNK"],
        "naruto": ["#Naruto", "#NarutoShippuden"],
    }

    for keyword, tags in series_tags.items():
        if keyword in hint_lower:
            lines = base.rsplit("\n", 2)
            lines[0] += " " + " ".join(tags)
            return "\n".join(lines)
    
    return base
