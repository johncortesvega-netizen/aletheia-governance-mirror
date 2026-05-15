# Patch 90 Recovery Note — AI Integrity Batch Review Scaffold

Patch 90 adds a small batch-review layer to AI Integrity Mirror.

## What changed

- `core/ai_integrity_mirror.py` now includes:
  - `AI_INTEGRITY_BATCH_VERSION`
  - `split_ai_integrity_batch_input`
  - `summarize_ai_integrity_batch`
  - `audit_ai_integrity_batch`
- `app.py` now exposes batch review mode in the AI Integrity Mirror tab.
- The batch UI shows per-item readings and a compact summary.
- Documentation and patch ledgers were updated.
- Patch-specific regression tests were added.

## Recovery / rollback

To roll back Patch 90, remove the batch helper functions from `core/ai_integrity_mirror.py`, remove the batch checkbox/summary block from the AI Integrity tab in `app.py`, and remove `tests/test_patch_90_ai_integrity_batch_review.py` plus this manifest/recovery note. Patch 85-89 single-artifact AI Integrity behavior should remain intact.

## Boundary

This patch does not create live model benchmarking, external calls, repository crawling, public ledger sync, Global ID sync, central storage, enforcement, vendor ranking, certification, approval, or a final safety claim. It reviews pasted artifacts only.

## Validation

```bat
tools\run_patch_checks.bat 90
tools\run_patch_checks.bat 89
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```
