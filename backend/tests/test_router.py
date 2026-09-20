import os
import unittest

os.environ.setdefault("SPOTIFY_CLIENT_ID", "test-client")
os.environ.setdefault("SPOTIFY_CLIENT_SECRET", "test-secret")

from fastapi.testclient import TestClient

from app.main import app


class CuratorRouterTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_audit_liked_songs_returns_audit(self):
        class FakeSpotifyClient:
            def get_saved_tracks(self, limit, offset):
                if offset > 0:
                    return {"total": 1, "items": []}
                return {
                    "total": 1,
                    "items": [{
                        "added_at": "2026-09-19T00:00:00Z",
                        "track": {
                            "id": "track-1",
                            "uri": "spotify:track:track-1",
                            "name": "دعها الليلة تشتعل",
                            "artists": [{"id": "artist-1", "name": "Ravena Beats"}],
                            "album": {"id": "album-1", "name": "Album", "release_date": "2026"},
                            "duration_ms": 1000,
                            "explicit": False,
                            "popularity": 50,
                        },
                    }],
                }

        async def fake_client_dependency():
            return FakeSpotifyClient()

        from app.curator.router import get_spotify_client
        app.dependency_overrides[get_spotify_client] = fake_client_dependency

        response = self.client.post("/curator/audit/liked-songs")
        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual("READ_ONLY", payload["mode"])
        self.assertEqual(1, payload["retrieved_unique_total"])
