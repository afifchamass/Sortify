from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException

from .config import assert_read_only
from .service import run_liked_songs_audit

router = APIRouter(prefix="/curator", tags=["library-curator"])


class SpotifySavedTracksClient:
    def __init__(self, session: dict[str, Any]) -> None:
        self._session = session

    async def get_saved_tracks(self, limit: int, offset: int) -> dict[str, Any]:
        import httpx
        from app.playlists.spotify_client import _bearer, _ensure_fresh_token

        self._session = await _ensure_fresh_token(self._session)
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.spotify.com/v1/me/tracks",
                headers=_bearer(self._session["access_token"]),
                params={"limit": limit, "offset": offset},
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Spotify saved-track request failed ({response.status_code}).",
            )

        return response.json()


async def get_spotify_client(
    session: Annotated[dict[str, Any], Depends(__import__("app.auth.session", fromlist=["require_session"]).require_session)],
) -> SpotifySavedTracksClient:
    assert_read_only()
    return SpotifySavedTracksClient(session)


@router.get("/audit-capabilities")
def audit_capabilities():
    assert_read_only()
    return {
        "mode": "READ_ONLY",
        "source": "LIKED_SONGS",
        "spotify_write_operations_enabled": False,
        "supported_outputs": ["CSV"],
    }


@router.post("/audit/liked-songs")
async def audit_liked_songs(
    spotify_client: SpotifySavedTracksClient = Depends(get_spotify_client),
):
    assert_read_only()
    return await run_liked_songs_audit(spotify_client)
