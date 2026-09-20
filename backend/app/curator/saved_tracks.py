import asyncio
from typing import Awaitable, Callable, Dict, List, Optional

from .config import SETTINGS, assert_read_only
from .models import SavedTrackInventoryRecord


def _to_record(item: Dict) -> Optional[SavedTrackInventoryRecord]:
    track = item.get("track") or {}
    track_id = track.get("id")
    track_uri = track.get("uri")
    if not track_id or not track_uri:
        return None
    artists = track.get("artists") or []
    album = track.get("album") or {}
    return SavedTrackInventoryRecord(
        track_id=track_id,
        track_uri=track_uri,
        track_name=track.get("name") or "",
        artist_names=[artist.get("name", "") for artist in artists],
        artist_ids=[artist.get("id", "") for artist in artists if artist.get("id")],
        album_name=album.get("name"),
        album_id=album.get("id"),
        release_date=album.get("release_date"),
        duration_ms=track.get("duration_ms"),
        explicit=track.get("explicit"),
        popularity=track.get("popularity"),
        saved_at=item.get("added_at") or "",
    )


async def retrieve_all_saved_tracks(
    fetch_page: Callable[[int, int], Awaitable[Dict]],
    checkpoint: Optional[Callable[[Dict], None]] = None,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> List[SavedTrackInventoryRecord]:
    """Read every saved track using offset pagination; this function never writes to Spotify."""
    assert_read_only()
    offset = 0
    expected_total = None
    records: List[SavedTrackInventoryRecord] = []
    seen = set()

    while True:
        response = None
        for attempt in range(SETTINGS.max_retries):
            try:
                response = await fetch_page(SETTINGS.page_size, offset)
                break
            except Exception:
                if attempt == SETTINGS.max_retries - 1:
                    raise
                await sleep(min(2 ** attempt, 16))
        if response is None:
            raise RuntimeError("Saved-track response was empty.")

        if expected_total is None:
            expected_total = int(response.get("total", 0))
        items = response.get("items") or []
        if not items:
            break

        for item in items:
            record = _to_record(item)
            if record and record.track_uri not in seen:
                seen.add(record.track_uri)
                records.append(record)

        offset += len(items)
        if checkpoint:
            checkpoint({
                "offset": offset,
                "expected_total": expected_total,
                "retrieved_unique": len(records),
            })
        if offset >= expected_total:
            break

    if expected_total is not None and len(records) != expected_total:
        raise RuntimeError(
            f"Liked Songs reconciliation failed: Spotify reported {expected_total}, "
            f"but {len(records)} unique playable tracks were retrieved."
        )
    return records
