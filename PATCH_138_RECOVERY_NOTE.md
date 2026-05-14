# Patch 138 Recovery Note — Single Unit Preview Entry Hotfix

If Patch 138 needs to be reverted, restore the pre-Patch-138 versions of:

- `ui/start_page.py`
- `tests/test_patch_131_start_page_gate.py`
- `tests/test_patch_132_start_page_stabilization_checkpoint.py`
- `tests/test_patch_137_validation_alignment_after_unit_preview.py`
- `tests/test_patch_138_single_unit_preview_entry_hotfix.py`
- `docs/single_unit_preview_entry_hotfix.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `docs/patch_index.md`
- `docs/architecture.md`
- `README.md`
- `data/protocol_baseline_manifest.json`

Patch 138 is a wiring/validation hotfix only. It keeps Aletheia Unit Preview as the single active pre-app gate and prevents the retired Start Page from rendering before the full app.

No scoring, verdict routing, taxonomy, receipts, signals, privacy scan behavior, AI Integrity behavior, World Lens math, uploads, downloads, external calls, telemetry, storage, certification, enforcement, privacy guarantee, or final-truth behavior changed.

Humans keep the judgment.
