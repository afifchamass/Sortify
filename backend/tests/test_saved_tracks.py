import unittest

from app.curator.saved_tracks import retrieve_all_saved_tracks


def item(track_id, uri=None):
    return {
        "added_at": "2026-09-19T00:00:00Z",
        "track": {
            "id": track_id,
            "uri": uri or f"spotify:track:{track_id}",
            "name": f"Track {track_id}",
            "artists": [{"id": f"artist-{track_id}", "name": "Artist"}],
            "album": {"id": f"album-{track_id}", "name": "Album", "release_date": "2026"},
            "duration_ms": 1000,
            "explicit": False,
            "popularity": 50,
        },
    }


class SavedTrackRetrievalTests(unittest.TestCase):
    def test_retrieves_all_pages_and_reconciles(self):
        pages = {
            0: {"total": 3, "items": [item("1"), item("2")]},
            2: {"total": 3, "items": [item("3")]},
        }
        checkpoints = []
        records = retrieve_all_saved_tracks(lambda limit, offset: pages[offset], checkpoints.append, sleep=lambda _: None)
        self.assertEqual(3, len(records))
        self.assertEqual(3, checkpoints[-1]["retrieved_unique"])

    def test_duplicate_uri_fails_reconciliation(self):
        pages = {
            0: {"total": 2, "items": [item("1"), item("2", "spotify:track:1")]},
        }
        with self.assertRaises(RuntimeError):
            retrieve_all_saved_tracks(lambda limit, offset: pages[offset], sleep=lambda _: None)

    def test_retries_transient_error(self):
        attempts = {"count": 0}
        def fetch(limit, offset):
            attempts["count"] += 1
            if attempts["count"] == 1:
                raise ConnectionError("temporary")
            return {"total": 1, "items": [item("1")]}
        records = retrieve_all_saved_tracks(fetch, sleep=lambda _: None)
        self.assertEqual(1, len(records))
        self.assertEqual(2, attempts["count"])
