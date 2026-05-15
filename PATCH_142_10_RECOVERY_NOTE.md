# Patch 142.10 Recovery Note — Receipt Reader QUESTION_PROMPT Display Polish

Patch 142.10 is display/parsing polish for Receipt Reader batch and selected-detail views.

If the patch must be reverted, restore `ui/receipt_reader.py`, `tests/test_patch_142_9_receipt_reader_batch_per_receipt_summary.py`, `tests/test_patch_142_10_question_prompt_receipt_display.py`, `PATCH_STATUS.md`, `docs/progress_database.md`, `docs/patch_index.md`, and `data/protocol_baseline_manifest.json` from the pre-142.10 state.

Expected restored behavior after applying this patch:

- QUESTION_PROMPT receipts remain review-tool readings, not scored scenarios.
- Batch rows for QUESTION_PROMPT receipts show `Not applicable` for suppressed scored metrics.
- Selected QUESTION_PROMPT detail views show a calm not-applicable note instead of a table full of missing values.
- Receipt Reader remains upload-only and does not rescore, merge verdicts, override receipts, or create new receipts.

This patch does not change scoring, verdict routing, taxonomy, receipt schemas, receipt generation, World Lens math, AI Integrity behavior, Privacy Audit behavior, Stress Test scoring behavior, external calls, telemetry/storage, certification, enforcement, or final-truth boundaries.
