# Patch 255 — Patch Notes Final Cleanup

**Status:** Applied  
**Type:** Repository documentation hygiene / patch archive cleanup  
**Runtime impact:** None

## Purpose

Patch 255 performs the final patch-note hygiene pass after the modularization and bridge-removal sequence.
It keeps the repository root clean while preserving the patch record as an audit trail.

## What changed

- Moved root-level patch artifacts for recent patches into `docs/patch_archive/`:
  - manifests → `docs/patch_archive/manifests/`
  - recovery notes → `docs/patch_archive/recovery_notes/`
  - delete lists → `docs/patch_archive/delete_lists/`
- Normalized older loose patch artifacts that were still directly under `docs/patch_archive/`.
- Updated `PATCH_STATUS.md` as the current root status file.
- Rebuilt `PATCH_NOTES.md` as the current readable patch summary.
- Added this cleanup note as the final patch-note hygiene record.

## Boundary

This patch does **not** change application behavior.
It does not modify scanner logic, scoring, MEI7 gates, Z-axis mapping, receipts, Evidence Lab calculations, World Lens math, navigation, telemetry, or storage.

## Intended root policy after this patch

The repository root should contain only the current patch artifacts:

- `PATCH_255_MANIFEST.txt`
- `PATCH_255_RECOVERY_NOTE.md`
- `PATCH_255_DELETE_LIST.txt`
- `PATCH_STATUS.md`
- `PATCH_NOTES.md`

Older patch artifacts should remain preserved under `docs/patch_archive/`.
