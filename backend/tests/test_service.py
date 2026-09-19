import csv
import tempfile
import unittest
from pathlib import Path

from app.curator.service import run_liked_songs_audit


class FakeSpotifyClient:
    def get_saved_tracks(self, limit, offset):
        if offset > 0:
            return {"total": 1, "items": []}
        return {
            "total": 1,
            "items": [{
                "added_at": "2026-09-19T00:00:00Z",
                "track": {
                    "id": "track-1", "uri": "spotify:track:track-1", "name": "دعها الليلة تشتعل",
                    "artists": [{"id": "artist-1", "name": "Ravena Beats"}],
                    "album": {"id": "album-1", "name": "Album", "release_date": "2026"},
                    "duration_ms": 1000, "explicit": False, "popularity": 50,
                },
            }],
        }


class AuditServiceTests(unittest.TestCase):
    def test_read_only_audit_exports_inventory_and_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_liked_songs_audit(FakeSpotifyClient(), directory)
            self.assertEqual("READ_ONLY", result["mode"])
            self.assertTrue(Path(result["inventory_csv"]).exists())
            self.assertTrue(Path(result["checkpoint"]).exists())
            with open(result["inventory_csv"], encoding="utf-8-sig") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(1, len(rows))
            self.assertEqual("ARABIC", rows[0]["classification_primary_language"])
