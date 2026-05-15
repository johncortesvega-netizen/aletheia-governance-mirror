# Patch 87 - AI Integrity Mirror Demo Examples and Static Smoke Coverage

## Purpose

Patch 87 keeps building on the AI Integrity Mirror module by centralizing its demo examples in the analyzer module and adding smoke coverage for those examples.

The goal is usability and regression safety: users should see clearer paste-ready examples, while tests confirm the examples remain auditable without live model benchmarking, external calls, certification language, or analyzer overreach. AI Integrity Mirror does not certify models, vendors, codebases, prompts, agents, or outputs; this patch is not certification.

## Files touched

- `core/ai_integrity_mirror.py`
- `app.py`
- `docs/ai_integrity_mirror.md`
- `tests/test_patch_87_ai_integrity_demo_examples.py`
- `PATCH_87_MANIFEST.txt`
- `PATCH_87_RECOVERY_NOTE.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## Boundary preserved

- No scoring-math change.
- No verdict-routing change.
- No Mirror Check, Stress Test, Boundary Cases, Evidence Lab, or World Lens logic change.
- No live model benchmarking.
- No external calls.
- No repository crawler.
- No public ledger.
- No Global ID sync.
- No central storage.
- No enforcement, punishment, model certification, vendor approval, legal authority, political authority, religious authority, medical authority, moral finality, or final safety claim.

## Verification

Run:

```bat
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```
