# Patch 142.3 Recovery Note — Receipt Reader Module Receipt Calibration and Stress Batch Tree Reset

Patch 142.3 is a bounded UI/parser calibration patch.

If it needs to be reverted, restore these files from the pre-142.3 project state:

- `ui/receipt_reader.py`
- `app.py`
- `tests/test_patch_142_3_receipt_reader_module_receipts_and_stress_batch_tree_reset.py`
- `PATCH_142_3_MANIFEST.txt`
- `PATCH_142_3_RECOVERY_NOTE.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `docs/patch_index.md`
- `data/protocol_baseline_manifest.json`

Expected behavior after the patch:

- Receipt Reader remains upload-only.
- World Lens receipts are displayed as selected-year evidence-distribution receipts, including selected year, 9k seat allocation, weighted integrity/friction/collapse, empirical coverage, and trust-prior/raw-trust coverage notes when present.
- AI Integrity Mirror receipts are displayed as static artifact review receipts and do not imply live model, vendor, deployment, training-data, hidden-prompt, or future-behavior testing.
- Stress Test / Simulation receipts remain receipt readings only; the reader does not re-run scenarios.
- Running Stress Test batch after a single scenario closes the single-scenario tree/result state so the old tree does not remain under the batch output.

Boundary reminder:

Patch 142.3 does not change scoring, verdict routing, taxonomy, QUESTION_PROMPT handling, receipt schema, receipt generation, signals, weights, AI Integrity scan behavior, Privacy Audit scan behavior, World Lens math, uploads/downloads, external calls, telemetry, analytics, storage, certification, enforcement, approval/rejection behavior, privacy guarantees, legal/official authority, or final-truth claims. Human review remains required.
