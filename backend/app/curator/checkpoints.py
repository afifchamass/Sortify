import json
from pathlib import Path
from typing import Dict, Optional


def write_checkpoint(path: str, payload: Dict) -> None:
    checkpoint = Path(path)
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    temporary = checkpoint.with_suffix(checkpoint.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    temporary.replace(checkpoint)


def read_checkpoint(path: str) -> Optional[Dict]:
    checkpoint = Path(path)
    if not checkpoint.exists():
        return None
    return json.loads(checkpoint.read_text(encoding="utf-8"))
