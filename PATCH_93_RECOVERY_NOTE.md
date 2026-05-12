# Patch 93 Recovery Note — AI Integrity Batch Demo Pack

Patch 93 is safe to revert by removing the demo pack, documentation pointer, and patch-specific test files listed in `PATCH_93_MANIFEST.txt`.

## What changed

Patch 93 adds static, copy/paste-ready AI Integrity demo artifacts under `examples/ai_integrity/`, adds `docs/ai_integrity_demo_pack.md`, and updates README, AI Integrity Mirror docs, patch status, and the progress database.

## What did not change

No analyzer scoring changed. No signal patterns changed. No signal weights changed. No verdict routing changed. No UI behavior changed. No receipt generation changed. No live model calls, external calls, repository crawler, storage layer, public ledger sync, Global ID sync, enforcement, vendor ranking, model certification, approval, or final safety claim was added.

## Recovery procedure

1. Remove the Patch 93 files listed in `PATCH_93_MANIFEST.txt`.
2. Revert the Patch 93 sections in README, `docs/ai_integrity_mirror.md`, `PATCH_STATUS.md`, and `docs/progress_database.md`.
3. Run:

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

## Patch 93 verification

```bat
tools\run_patch_checks.bat 93
```
