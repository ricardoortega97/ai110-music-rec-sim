from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Returns the top k songs ranked by score for the given user profile.
        Delegates to score_song() for scoring logic.
        """
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Returns a human-readable string explaining why the song matches the user.
        Example: "Matches your lofi genre preference and chill mood. Close energy and acousticness."
        """
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Casts numeric fields: id (int), energy/tempo_bpm/valence/danceability/acousticness (float).
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded {len(songs)} songs:")
    for song in songs:
        print(f"  [{song['id']}] {song['title']} — {song['artist']} ({song['genre']}, {song['mood']})")
    return songs


def vibe_closeness(user_prfs: Dict, song: Dict, tempo_min: float, tempo_max: float) -> float:
    """
    Returns a score from 0.0 to 1.5 based on how close the song's sonic
    fingerprint is to the user's preferences.
    Normalizes tempo_bpm using tempo_min/tempo_max from the catalog.
    Computes mean absolute distance across: energy, tempo_bpm, valence, acousticness.
    vibe_score = 1.5 * (1 - mean_distance)
    Only compares features present in user_prfs — missing features are skipped.
    """
    tempo_range = tempo_max - tempo_min
    song_tempo_norm = (song["tempo_bpm"] - tempo_min) / tempo_range if tempo_range > 0 else 0.5

    comparisons = []

    if "energy" in user_prfs:
        comparisons.append((song["energy"], float(user_prfs["energy"])))

    if "tempo_bpm" in user_prfs:
        user_tempo_norm = (float(user_prfs["tempo_bpm"]) - tempo_min) / tempo_range if tempo_range > 0 else 0.5
        comparisons.append((song_tempo_norm, user_tempo_norm))

    if "valence" in user_prfs:
        comparisons.append((song["valence"], float(user_prfs["valence"])))

    if "acousticness" in user_prfs:
        comparisons.append((song["acousticness"], float(user_prfs["acousticness"])))

    if not comparisons:
        return 0.0

    mean_distance = sum(abs(sv - uv) for sv, uv in comparisons) / len(comparisons)
    return round(1.5 * (1 - mean_distance), 4)


def score_song(user_prfs: Dict, song: Dict, session_state: Dict, tempo_min: float, tempo_max: float) -> float:
    """
    Computes the full point-weight score for one song against the user profile.
    +2.0 if song genre matches user genre
    +1.0 if song mood matches user mood
    +0.0 to +1.5 vibe closeness (calls vibe_closeness)
    -0.5 if session_state skip_count for this song is 1 (first strike)
    """
    score = 0.0

    if song["genre"] == user_prfs.get("genre", ""):
        score += 2.0

    if song["mood"] == user_prfs.get("mood", ""):
        score += 1.0

    score += vibe_closeness(user_prfs, song, tempo_min, tempo_max)

    song_state = session_state.get(song["id"], {})
    if song_state.get("skip_count", 0) == 1:
        score -= 0.5

    return round(score, 4)


def init_session_state(songs: List[Dict]) -> Dict:
    """
    Returns a fresh session state dict for a new listening session.
    Structure:
      {
        "queue_position": 0,
        <song_id>: { "skip_count": 0, "disqualified": False, "cooldown_until": 0 },
        ...
      }
    """
    state: Dict = {"queue_position": 0}
    for song in songs:
        state[song["id"]] = {
            "skip_count":    0,
            "disqualified":  False,
            "cooldown_until": 0,
        }
    return state


def is_eligible(song: Dict, session_state: Dict) -> bool:
    """
    Returns True if a song can enter the scoring loop this cycle.
    A song is ineligible if:
      - session_state[song_id]["disqualified"] is True, OR
      - session_state["queue_position"] < session_state[song_id]["cooldown_until"]
    """
    song_state = session_state.get(song["id"], {})
    if song_state.get("disqualified", False):
        return False
    if session_state.get("queue_position", 0) < song_state.get("cooldown_until", 0):
        return False
    return True


def apply_feedback(song_id: int, signal: str, session_state: Dict) -> None:
    """
    Updates session state after a song plays based on the user's feedback signal.
    signal values:
      "play" — no change to song state
      "skip" — skip_count += 1
               if skip_count == 1: cooldown_until = queue_position + 25
               if skip_count >= 2: disqualified = True
      "off"  — disqualified = True immediately, regardless of skip_count
    Always increments session_state["queue_position"] by 1.
    """
    song_state = session_state.get(song_id, {})

    if signal == "off":
        song_state["disqualified"] = True
    elif signal == "skip":
        song_state["skip_count"] = song_state.get("skip_count", 0) + 1
        if song_state["skip_count"] == 1:
            song_state["cooldown_until"] = session_state.get("queue_position", 0) + 25
        elif song_state["skip_count"] >= 2:
            song_state["disqualified"] = True

    session_state[song_id] = song_state
    session_state["queue_position"] = session_state.get("queue_position", 0) + 1


def recommend_songs(user_prfs: Dict, songs: List[Dict], k: int = 5, session_state: Optional[Dict] = None) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    1. Filter eligible songs using is_eligible()
    2. Score each eligible song using score_song()
    3. Sort by score descending, return top k as (song_dict, score, explanation)
    """
    if session_state is None:
        session_state = init_session_state(songs)

    tempo_min = min(s["tempo_bpm"] for s in songs)
    tempo_max = max(s["tempo_bpm"] for s in songs)

    scored = sorted(
        [
            (song, score_song(user_prfs, song, session_state, tempo_min, tempo_max))
            for song in songs
            if is_eligible(song, session_state)
        ],
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        (song, score, _build_explanation(user_prfs, song, tempo_min, tempo_max))
        for song, score in scored[:k]
    ]


def _build_explanation(user_prfs: Dict, song: Dict, tempo_min: float, tempo_max: float) -> str:
    """Builds a human-readable explanation of why a song was recommended."""
    reasons = []
    if song["genre"] == user_prfs.get("genre", ""):
        reasons.append(f"genre match ({song['genre']})")
    if song["mood"] == user_prfs.get("mood", ""):
        reasons.append(f"mood match ({song['mood']})")
    vibe = vibe_closeness(user_prfs, song, tempo_min, tempo_max)
    reasons.append(f"vibe score {vibe:.2f}/1.5")
    return ", ".join(reasons)
