# Patch 140 Recovery Note — Unit Preview Orientation Cleanup

If Patch 140 needs to be reverted, restore the previous Patch 139 versions of:

- `app.py`
- `ui/unit_preview.py`
- the updated test files listed in `PATCH_140_MANIFEST.txt`
- `PATCH_STATUS.md`
- `README.md`
- `docs/architecture.md`
- `docs/patch_index.md`
- `docs/progress_database.md`
- `data/protocol_baseline_manifest.json`

Expected recovery behavior:

- Aletheia Unit Preview remains the pre-module hook from Patch 139.
- The full app may again show the previous beginner/how-to-use copy after Proceed.
- Receipt Reader may again appear according to the Patch 139 app surface.

Patch 140 is UI placement/copy organization only. It should not affect scoring, routing, receipts, signals, World Lens math, AI Integrity behavior, Privacy Audit behavior, uploads/downloads, external calls, telemetry, storage, certification, enforcement, privacy guarantees, or final-truth behavior.
