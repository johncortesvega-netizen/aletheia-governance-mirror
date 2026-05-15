# Patch 142.12 Recovery Note — Receipt Reader Standard View Copy Polish

Patch 142.12 is a Receipt Reader copy/label polish patch. It only changes how already-parsed uploaded receipt values are described and displayed.

Rollback steps:
1. Restore `ui/receipt_reader.py` from the previous working Patch 142.11 state.
2. Remove `tests/test_patch_142_12_receipt_reader_standard_view_copy_polish.py`.
3. Restore the Patch 142.11 versions of:
   - `tests/test_patch_142_4_receipt_reader_narrative_output.py`
   - `tests/test_patch_142_7_receipt_reader_world_lens_zip_selection.py`
   - `PATCH_STATUS.md`
   - `docs/progress_database.md`
   - `docs/patch_index.md`
   - `data/protocol_baseline_manifest.json`
4. Re-run:
   - `python tools/run_patch_checks.py 142_11`
   - `python tools/run_patch_checks.py 142_10`
   - `python tools/run_protocol_baseline_self_audit.py`

No scoring, verdict routing, taxonomy, receipt schema, receipt generation, signal behavior, World Lens math, AI Integrity behavior, Privacy Audit behavior, Stress Test scoring behavior, telemetry/storage, external calls, certification, enforcement, or final-truth behavior was changed by this patch.
