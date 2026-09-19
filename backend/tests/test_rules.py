import unittest

from app.curator.models import SavedTrackInventoryRecord
from app.curator.rules import classify_protected_purpose


def record(name, artist="Artist", album="Album"):
    return SavedTrackInventoryRecord(
        track_id="id", track_uri="spotify:track:id", track_name=name,
        artist_names=[artist], artist_ids=["artist"], album_name=album, album_id="album",
        release_date=None, duration_ms=None, explicit=False, popularity=0, saved_at="2026-09-19T00:00:00Z",
    )


class ClassificationRuleTests(unittest.TestCase):
    def test_arabic_script_routes_to_arabic_library(self):
        result = classify_protected_purpose(record("دعها الليلة تشتعل"))
        self.assertEqual("ARABIC", result.primary_language)
        self.assertEqual("Arabic — Liked Songs", result.recommended_language_library)

    def test_faith_is_protected_before_language_routing(self):
        result = classify_protected_purpose(record("سورة الفاتحة", artist="Quran Reciter"))
        self.assertEqual("FAITH", result.protected_purpose)
        self.assertIsNone(result.recommended_language_library)

    def test_kids_is_protected(self):
        result = classify_protected_purpose(record("Hush Little Baby Lullaby"))
        self.assertEqual("FAMILY_KIDS", result.protected_purpose)

    def test_unknown_requires_review(self):
        result = classify_protected_purpose(record("Beni Al"))
        self.assertEqual("REVIEW", result.primary_language)
