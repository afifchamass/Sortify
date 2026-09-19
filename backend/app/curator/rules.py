import re
from typing import Iterable

from .models import Classification, SavedTrackInventoryRecord

ARABIC_RE = re.compile(r"[\u0600-\u06FF]")
FAITH_TERMS = ("quran", "quraan", "qur'an", "dua", "doaa", "adhkar", "adhan", "surah", "sorat", "تلاوة", "دعاء", "اذكار", "أذكار", "قرآن", "القرآن")
KIDS_TERMS = ("cocomelon", "lullaby", "baby", "bedtime", "kids", "children")


def classify_protected_purpose(record: SavedTrackInventoryRecord) -> Classification:
    text = " ".join([record.track_name, *record.artist_names, record.album_name or ""]).lower()
    result = Classification()
    if any(term in text for term in FAITH_TERMS):
        result.protected_purpose = "FAITH"
        result.explanation = "Matched faith/recitation keywords."
        return result
    if any(term in text for term in KIDS_TERMS):
        result.protected_purpose = "FAMILY_KIDS"
        result.explanation = "Matched family/kids keywords."
        return result
    if ARABIC_RE.search(" ".join([record.track_name, *record.artist_names])):
        result.primary_language = "ARABIC"
        result.language_confidence = 0.90
        result.recommended_language_library = "Arabic — Liked Songs"
        result.explanation = "Arabic script detected in track or artist metadata."
    else:
        result.primary_language = "REVIEW"
        result.explanation = "No deterministic language signal; send to review/enrichment."
    return result


def apply_initial_rules(records: Iterable[SavedTrackInventoryRecord]) -> Iterable[SavedTrackInventoryRecord]:
    for record in records:
        record.classification = classify_protected_purpose(record)
        yield record
