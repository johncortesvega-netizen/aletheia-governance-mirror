# Patch 92 — AI Integrity Rubric Documentation Recovery Note

Patch 92 documents the AI Integrity Mirror rubric while preserving the existing runtime behavior.

## What changed

- Added `docs/ai_integrity_rubric.md`.
- Updated `docs/ai_integrity_mirror.md` with a Patch 92 rubric-documentation section.
- Updated README with AI Integrity Mirror scope and documentation links.
- Added `tests/test_patch_92_ai_integrity_rubric_documentation.py`.
- Updated `PATCH_STATUS.md` and `docs/progress_database.md`.

## Boundary preserved

This is a documentation patch only. It does not alter scoring math, signal patterns, signal weights, verdict routing, UI behavior, receipt generation, privacy architecture, batch splitting, or external behavior.

ALETHEIA still does not benchmark live models, call external APIs, crawl repositories, store pasted artifacts centrally, publish receipts to a ledger, sync Global ID, enforce action, approve vendors, certify models, or prove safety.

## Recovery

To recover, revert these files to the Patch 91 baseline:

- `docs/ai_integrity_rubric.md`
- `docs/ai_integrity_mirror.md`
- `README.md`
- `tests/test_patch_92_ai_integrity_rubric_documentation.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `PATCH_92_MANIFEST.txt`
- `PATCH_92_RECOVERY_NOTE.md`

## Verification

```bat
tools\run_patch_checks.bat 92
tools\run_patch_checks.bat 91
tools\run_patch_checks.bat 90
tools\run_patch_checks.bat 89
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```
