"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prfs = {"genre": "lofi", "mood": "chill", "energy": 0.3}

    recommendations = recommend_songs(user_prfs, songs, k=5)

    profile_label = f"{user_prfs['genre']}  ·  {user_prfs['mood']}  ·  energy {user_prfs['energy']}"
    header = f"  Top {len(recommendations)} Recommendations  ·  {profile_label}"

    # Auto-size width to the longest line in the output
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
        title_line = f"  #{i}  {song['title']}"
        score_label = f"Score: {score:.2f}"
        padding = width - len(title_line) - len(score_label) - 2
        print(f"{title_line}{' ' * max(padding, 1)}{score_label}")
        print(f"       {song['artist']}  ·  {song['genre']}  ·  {song['mood']}")
        print(f"       {explanation}")

    print()
    print("─" * width)


if __name__ == "__main__":
    main()
