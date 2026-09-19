# Regression Testing and Release Gate

## Required checks for every change

From `backend/` run:

```bash
python -m compileall -q app
pytest
```

GitHub Actions runs the same checks for pushes to `master` and `feature/**`, plus pull requests targeting `master`.

## Mandatory regression coverage

- Existing backend behavior remains importable and routable.
- Liked Songs retrieval paginates, retries transient failures, de-duplicates records, and reconciles the Spotify-reported total.
- Faith and family/kids material remains protected from general music/DJ routing.
- Read-only mode remains enabled and audit capabilities expose no Spotify write operations.
- Audit output produces a checkpoint and inventory CSV using fake Spotify data only.

## Real-account acceptance test

Before any production library audit, use a Spotify app with `user-library-read` only. Verify the application exports an inventory and that the reported total equals the retrieved unique total. Confirm there are no playlist creations, additions, removals, edits, or Liked Songs modifications.
