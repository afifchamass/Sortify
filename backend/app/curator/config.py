from dataclasses import dataclass


@dataclass(frozen=True)
class CuratorSettings:
    write_enabled: bool = False
    export_directory: str = "exports"
    page_size: int = 50
    max_retries: int = 5
    checkpoint_file: str = "curator_checkpoints/liked_songs.json"


SETTINGS = CuratorSettings()


def assert_read_only() -> None:
    if SETTINGS.write_enabled:
        raise RuntimeError("Library Curator write mode is prohibited in the foundation release.")
