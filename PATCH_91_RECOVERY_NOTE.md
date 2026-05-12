# Patch 91 — AI Integrity Receipt Export Polish Recovery Note

Patch 91 polishes AI Integrity Mirror receipt exports while preserving the static mirror boundary.

## What changed

- Added `AI_INTEGRITY_RECEIPT_VERSION`.
- Added `build_ai_integrity_receipt_context(...)` for receipt-facing AI Integrity metadata.
- Added `render_ai_integrity_receipt_context_text(...)` so downloads include a readable AI Integrity section before the generic local witness receipt.
- The AI Integrity receipt now surfaces:
  - receipt header
  - review mode
  - artifact type
  - static review scope
  - privacy boundary
  - non-certification note
  - reliance boundary
  - finding summary
  - redacted evidence snippets
  - repair questions
  - optional batch summary

## Boundary preserved

The patch does not alter scoring math, verdict routing, signal weights, batch splitting, privacy architecture, or external behavior. It adds receipt readability only.

ALETHEIA still does not benchmark live models, call external APIs, crawl repositories, store pasted artifacts centrally, publish receipts to a ledger, sync Global ID, enforce action, approve vendors, certify models, or prove safety.

## Recovery

To recover, revert these files to the Patch 90 baseline:

- `core/ai_integrity_mirror.py`
- `app.py`
- `tests/test_patch_91_ai_integrity_receipt_export_polish.py`
- `docs/ai_integrity_mirror.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `PATCH_91_MANIFEST.txt`
- `PATCH_91_RECOVERY_NOTE.md`

## Verification

```bat
tools\run_patch_checks.bat 91
tools\run_patch_checks.bat 90
tools\run_patch_checks.bat 89
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```
