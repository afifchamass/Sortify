from fastapi import APIRouter, Depends, HTTPException

from .config import assert_read_only
from .service import run_liked_songs_audit

router = APIRouter(prefix="/curator", tags=["library-curator"])


def get_spotify_client():
    raise HTTPException(status_code=501, detail="Spotify client dependency is not configured.")


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
def audit_liked_songs(spotify_client=Depends(get_spotify_client)):
    assert_read_only()
    return run_liked_songs_audit(spotify_client)
