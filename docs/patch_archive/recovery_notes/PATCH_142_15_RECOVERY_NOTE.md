# Patch 142.15 Recovery Note - Receipt Reader Verbal Micro-Polish Across Receipts

If Patch 142.15 causes Receipt Reader display problems, revert these files:

- `ui/receipt_reader.py`
- `tests/test_patch_142_15_receipt_reader_verbal_micro_polish.py`
- `tests/test_patch_142_12_receipt_reader_standard_view_copy_polish.py`
- `PATCH_142_15_MANIFEST.txt`
- `PATCH_142_15_RECOVERY_NOTE.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `docs/patch_index.md`
- `data/protocol_baseline_manifest.json`

This patch is presentation/copy only. It does not change scoring, routing, taxonomy, receipt schema, receipt generation, scan behavior, World Lens math, upload/download behavior, or any authority boundary. Uploaded receipt values remain the source of truth; the verbal layer does not infer missing values, rescore, or create a new verdict.

Suggested validation after revert or reapply:

```bat
python tools\run_patch_checks.py 142_15
python tools\run_patch_checks.py 142_13
python tools\run_patch_checks.py 142_12
python tools\run_patch_checks.py 142_11
python tools\run_patch_checks.py 142_10
python tools\run_protocol_baseline_self_audit.py
```
