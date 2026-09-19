# Spotify Library Curator — Read-Only Foundation

## Purpose

This foundation retrieves the complete Spotify Liked Songs library, normalizes a track-level inventory, applies only initial protected-purpose and Arabic-script rules, and exports the result for human review. It does not create, modify, delete, or reorder Spotify playlists.

## Safety contract

- Liked Songs is the immutable master source.
- `write_enabled` is hard-coded to `False` in the foundation release.
- The retrieval function raises an error if the retrieved unique-track count differs from Spotify's reported total.
- Classification decisions include an explanation and are intended for review.
- Quran, du'a, adhkar, adhan, and children/bedtime signals are protected-purpose categories and are excluded from general music/DJ curation by default.

## Required Spotify scopes

Audit mode requires the least-privilege scope `user-library-read`; `playlist-read-private` is optional for reading existing playlists. Do not add playlist-modify scopes until the approval-based sync release.

## Initial outputs

The foundation exports a UTF-8 CSV containing Spotify metadata, saved date, audio-feature placeholders, classification fields, reasons, and manual-override placeholders. Excel/XLSX output, audio-feature enrichment, language enrichment, dashboarding, and playlist sync are subsequent increments.

## Acceptance criteria

1. Spotify-reported saved-track count equals the retrieved unique-track count.
2. The output is read-only and reviewable before any Spotify write capability exists.
3. Every record has a source, saved date, unique Spotify URI, and a classification explanation.
4. Protected-purpose material is never assigned to a general music or DJ crate by the initial rules.
