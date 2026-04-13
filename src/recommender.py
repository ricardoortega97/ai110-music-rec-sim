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
        raise NotImplementedError

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Returns a human-readable string explaining why the song matches the user.
        Example: "Matches your lofi genre preference and chill mood. Close energy and acousticness."
        """
        raise NotImplementedError

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Casts numeric fields: id (int), energy/tempo_bpm/valence/danceability/acousticness (float).
    Required by src/main.py
    """
    raise NotImplementedError


def vibe_closeness(user_prfs: Dict, song: Dict, tempo_min: float, tempo_max: float) -> float:
    """
    Returns a score from 0.0 to 1.5 based on how close the song's sonic
    fingerprint is to the user's preferences.
    Normalizes tempo_bpm using tempo_min/tempo_max from the catalog.
    Computes mean absolute distance across: energy, tempo_bpm, valence, acousticness.
    vibe_score = 1.5 * (1 - mean_distance)
    """
    raise NotImplementedError


def score_song(user_prfs: Dict, song: Dict, session_state: Dict, tempo_min: float, tempo_max: float) -> float:
    """
    Computes the full point-weight score for one song against the user profile.
    +2.0 if song genre matches user genre
    +1.0 if song mood matches user mood
    +0.0 to +1.5 vibe closeness (calls vibe_closeness)
    -0.5 if session_state skip_count for this song is 1 (first strike)
    """
    raise NotImplementedError


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
    raise NotImplementedError


def is_eligible(song: Dict, session_state: Dict) -> bool:
    """
    Returns True if a song can enter the scoring loop this cycle.
    A song is ineligible if:
      - session_state[song_id]["disqualified"] is True, OR
      - session_state["queue_position"] < session_state[song_id]["cooldown_until"]
    """
    raise NotImplementedError


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
    raise NotImplementedError


def recommend_songs(user_prfs: Dict, songs: List[Dict], k: int = 5, session_state: Optional[Dict] = None) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    1. Filter eligible songs using is_eligible()
    2. Score each eligible song using score_song()
    3. Sort by score descending, return top k as (song_dict, score, explanation)
    """
    raise NotImplementedError
