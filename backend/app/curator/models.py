from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class AudioFeatures:
    tempo: Optional[float] = None
    energy: Optional[float] = None
    danceability: Optional[float] = None
    valence: Optional[float] = None
    acousticness: Optional[float] = None
    instrumentalness: Optional[float] = None
    loudness: Optional[float] = None
    key: Optional[int] = None
    mode: Optional[int] = None
    time_signature: Optional[int] = None


@dataclass
class Classification:
    primary_language: str = "UNCLASSIFIED"
    language_confidence: float = 0.0
    protected_purpose: Optional[str] = None
    genre_signals: List[str] = field(default_factory=list)
    recommended_language_library: Optional[str] = None
    recommended_dj_crates: List[str] = field(default_factory=list)
    explanation: str = ""
    manual_override: Optional[str] = None


@dataclass
class SavedTrackInventoryRecord:
    track_id: str
    track_uri: str
    track_name: str
    artist_names: List[str]
    artist_ids: List[str]
    album_name: Optional[str]
    album_id: Optional[str]
    release_date: Optional[str]
    duration_ms: Optional[int]
    explicit: Optional[bool]
    popularity: Optional[int]
    saved_at: str
    source: str = "LIKED_SONGS"
    audio_features: AudioFeatures = field(default_factory=AudioFeatures)
    classification: Classification = field(default_factory=Classification)
