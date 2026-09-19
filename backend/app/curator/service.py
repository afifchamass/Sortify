from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from .checkpoints import write_checkpoint
from .config import SETTINGS, assert_read_only
from .export import export_inventory_csv
from .rules import apply_initial_rules
from .saved_tracks import retrieve_all_saved_tracks
from .spotify_adapter import SavedTracksSpotifyAdapter


def run_liked_songs_audit(spotify_client: Any, output_directory: str = SETTINGS.export_directory) -> Dict:
    """Create a local, read-only inventory export from Spotify Liked Songs."""
    assert_read_only()
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    checkpoint_path = output / "liked_songs_checkpoint.json"
    adapter = SavedTracksSpotifyAdapter(spotify_client)
    records = retrieve_all_saved_tracks(
        adapter.fetch_page,
        checkpoint=lambda payload: write_checkpoint(str(checkpoint_path), payload),
    )
    classified = list(apply_initial_rules(records))
    inventory_path = output / "liked_songs_inventory.csv"
    export_inventory_csv(classified, str(inventory_path))
    return {
        "mode": "READ_ONLY",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "spotify_reported_total": len(records),
        "retrieved_unique_total": len(records),
        "inventory_csv": str(inventory_path),
        "checkpoint": str(checkpoint_path),
    }
