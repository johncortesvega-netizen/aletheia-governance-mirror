# Patch 142 Recovery Note - Unit Preview Intent Router Calibration

Patch 142 calibrates Aletheia Unit Preview so the first-page prompt recognizes more specific user intent before falling back to Mirror Check.

## What changed

- Added `detect_unit_preview_route(text)` in `ui/unit_preview.py`.
- Unit Preview now displays:
  - `Suggested path: ...`
  - `Why: ...`
  - `Next step: ...`
- The router checks specific local phrase families first:
  - Receipt Reader - Standard View
  - AI Integrity Mirror
  - Privacy Audit
  - World Lens
  - Stress Test
  - Evidence Lab
  - Why ALETHEIA / guidance
  - Mirror Check fallback
- Added an internal batch-style test matrix in `tests/test_patch_142_unit_preview_intent_router.py`.

## What did not change

This patch does not change scoring, verdict routing, taxonomy, receipt schema, receipt generation, signal regexes or weights, AI Integrity scan behavior, Privacy Audit scan behavior, World Lens math, upload/download behavior, external calls, live model calls, embeddings, telemetry, analytics, storage, synchronization, certification, enforcement, approval/rejection behavior, privacy guarantees, or final-truth behavior.

The Unit Preview router is a local orientation helper only. Mirror Check is the fallback, not the universal answer. Human review remains required. ALETHEIA remains a mirror, not a throne.

## Recovery

To revert this patch, restore `ui/unit_preview.py` from Patch 141.3 and remove:

- `tests/test_patch_142_unit_preview_intent_router.py`
- `PATCH_142_MANIFEST.txt`
- `PATCH_142_RECOVERY_NOTE.md`
- Patch 142 entries in `PATCH_STATUS.md`, `docs/progress_database.md`, `docs/patch_index.md`, `docs/architecture.md`, and `data/protocol_baseline_manifest.json`.
