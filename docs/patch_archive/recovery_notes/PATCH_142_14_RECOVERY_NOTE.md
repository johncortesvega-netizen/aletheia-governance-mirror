# Patch 142.14 Recovery Note — Receipt Reader Verbal Standard View Polish

Patch 142.14 changes Receipt Reader presentation only. It adds a warmer verbal Standard View layer above the native record table and reframes repair questions as human-review questions.

To revert this patch:

1. Restore `ui/receipt_reader.py` from the pre-142.14 version.
2. Remove `tests/test_patch_142_14_receipt_reader_verbal_standard_view.py`.
3. Remove `PATCH_142_14_MANIFEST.txt` and this recovery note.
4. Remove the Patch 142.14 entries from `PATCH_STATUS.md`, `docs/progress_database.md`, and `docs/patch_index.md`.
5. Restore `data/protocol_baseline_manifest.json` to the previous baseline.

No scoring, routing, receipt schema, receipt generation, taxonomy, World Lens math, signal behavior, telemetry/storage, or authority-boundary behavior is intentionally changed by this patch.
