import csv
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from .models import SavedTrackInventoryRecord


def export_inventory_csv(records: Iterable[SavedTrackInventoryRecord], output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for record in records:
        row = asdict(record)
        audio = row.pop("audio_features")
        classification = row.pop("classification")
        row.update({f"audio_{key}": value for key, value in audio.items()})
        row.update({f"classification_{key}": value for key, value in classification.items()})
        row["artist_names"] = " | ".join(row["artist_names"])
        row["artist_ids"] = " | ".join(row["artist_ids"])
        row["classification_genre_signals"] = " | ".join(row["classification_genre_signals"])
        row["classification_recommended_dj_crates"] = " | ".join(row["classification_recommended_dj_crates"])
        rows.append(row)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
