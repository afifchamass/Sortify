from typing import Any, Dict


class SavedTracksSpotifyAdapter:
    """Read-only adapter for Spotify's saved-track endpoint."""

    def __init__(self, spotify_client: Any):
        self._spotify_client = spotify_client

    async def fetch_page(self, limit: int, offset: int) -> Dict:
        if limit < 1 or limit > 50:
            raise ValueError("Spotify saved-track page size must be between 1 and 50.")
        if offset < 0:
            raise ValueError("Spotify saved-track offset cannot be negative.")
        return await self._spotify_client.get_saved_tracks(limit=limit, offset=offset)
