"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


USER_PROFILES = [
    # Late-night study session: low energy lofi, chilled out
    {"name": "Late-Night Studier", "genre": "lofi",     "mood": "chill",    "energy": 0.3},
    # High-intensity workout: hard rock, intense mood, max energy
    {"name": "Gym Grinder",        "genre": "rock",     "mood": "intense",  "energy": 0.9},
    # Sunday morning wind-down: jazz, relaxed vibe, moderate energy
    {"name": "Sunday Morning",     "genre": "jazz",     "mood": "relaxed",  "energy": 0.4},
    # ADVERSARIAL: genre/mood not in dataset — zero categorical hits, ranking falls to vibe only
    {"name": "Ghost Listener",     "genre": "trap",     "mood": "angry",    "energy": 0.5},
    # ADVERSARIAL: contradicts itself — lofi/chill genre+mood but max energy; categorical bonus (+3.0) drowns out vibe signal (+1.5 max)
    {"name": "Mismatch Maximizer", "genre": "kpop",     "mood": "chill",    "energy": 0.97},
]


def _print_recommendations(user_prfs: dict, recommendations: list) -> None:
    profile_label = f"{user_prfs['genre']}  ·  {user_prfs['mood']}  ·  energy {user_prfs['energy']}"
    name_label    = user_prfs.get("name", "User")
    header = f"  {name_label}  ·  Top {len(recommendations)}  ·  {profile_label}"

    width = max(
        len(header),
        max(
            len(f"  #{i}  {song['title']}   Score: {score:.2f}")
            for i, (song, score, _) in enumerate(recommendations, start=1)
        ),
        max(
            len(f"       {explanation}")
            for _, _, explanation in recommendations
        ),
    ) + 4

    print()
    print("─" * width)
    print(header)
    print("─" * width)

    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        title_line  = f"  #{i}  {song['title']}"
        score_label = f"Score: {score:.2f}"
        padding     = width - len(title_line) - len(score_label) - 2
        print(f"{title_line}{' ' * max(padding, 1)}{score_label}")
        print(f"       {song['artist']}  ·  {song['genre']}  ·  {song['mood']}")
        print(f"       {explanation}")

    print()
    print("─" * width)


def main() -> None:
    songs = load_songs("data/songs.csv")

    for user_prfs in USER_PROFILES:
        recommendations = recommend_songs(user_prfs, songs, k=5)
        _print_recommendations(user_prfs, recommendations)


if __name__ == "__main__":
    main()
