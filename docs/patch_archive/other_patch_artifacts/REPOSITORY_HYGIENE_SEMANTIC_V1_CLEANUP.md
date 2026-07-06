# Repository Hygiene Cleanup — Patch Notes Placement

Purpose:
- Reduce repository-root clutter.
- Preserve patch notes in the documentation/audit archive.
- Keep runtime source directories free of transient `PATCH_NOTES.md` files.

Changes:
- Removed duplicate root artifacts for Patch 189 through Patch 194; archived copies already exist under `docs/patch_archive/`.
- Moved transient semantic patch notes from root/core into `docs/patch_archive/other_patch_artifacts/SEMANTIC_V1_SESSION_PATCH_NOTES.md`.
- Added `docs/semantic_pressure_scanner_v1.md` as the stable reader-facing documentation for Semantic Pressure Scanner v1.
- Left the current latest numbered patch artifacts at root: `PATCH_195_MANIFEST.txt`, `PATCH_195_RECOVERY_NOTE.md`, and `PATCH_195_DELETE_LIST.txt`.

No changes to scoring, routing, receipt schema, semantic scanner logic, Streamlit UI behavior, telemetry, storage, certification, enforcement, or authority behavior.
