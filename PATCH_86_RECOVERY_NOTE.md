# Patch 86 Recovery Note — AI Integrity Mirror Copy & Receipt Polish

Patch 86 is a small polish patch on top of Patch 85. AI Integrity Mirror does not certify models, vendors, prompts, agents, codebases, or outputs.

## What changed

- `core/ai_integrity_mirror.py`
  - Rubric version updated to `ai-integrity-v0.2-static-receipt-polish`.
  - Added static scope, receipt, and reliance notes.
  - Added those notes to the top-level analyzer result and to scan/report dictionaries.

- `app.py`
  - AI Integrity Mirror heading now emphasizes static review and non-certification.
  - Metric labels now read as risk reading, integrity reading, and capture pressure.
  - Added a "How to read this result" expander.
  - Receipt expander now displays a receipt note before the local witness receipt text.

- `docs/ai_integrity_mirror.md`
  - Added Patch 86 notes and clarified the pasted-artifact-only boundary.

- `tests/test_patch_86_ai_integrity_copy_receipt_polish.py`
  - Verifies the new copy, notes, analyzer metadata, ledgers, and non-certification boundary.

## Boundary preserved

Patch 86 does not change ALETHEIA scoring math, verdict routing, receipt schema, Mirror Check, Stress Test, Evidence Lab, World Lens, Boundary Cases, live model benchmarking, repository scanning, external calls, public ledger behavior, Global ID sync, central storage, enforcement, punishment, certification, vendor approval, legal authority, political authority, religious authority, medical authority, moral finality, or final safety claims.

## Verification

```bat
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```

If recovery is needed, restore the Patch 85 baseline and reapply only the Patch 86 files listed in `PATCH_86_MANIFEST.txt`.
