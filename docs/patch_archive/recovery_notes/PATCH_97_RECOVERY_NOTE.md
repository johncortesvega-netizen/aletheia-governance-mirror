# Patch 97 Recovery Note — AI Integrity Comparison View v1

If Patch 97 needs to be reverted, remove the files listed in `PATCH_97_MANIFEST.txt` and restore the previous Patch 96 versions of:

- `core/ai_integrity_mirror.py`
- `app.py`
- `docs/ai_integrity_mirror.md`
- `README.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

Patch 97 is intentionally small. It adds comparison metadata and UI presentation for AI Integrity batch results only. It should not affect analyzer scoring, signal weights, signal patterns, verdict routing, receipts, code-integrity scanning, privacy-boundary scanning, or any non-AI-Integrity module.

Boundary reminder: Comparison View is artifact-level review support. It is not model-wide certification, not a vendor ranking, not live model benchmarking, not approval, and not a final truth claim.

Suggested checks after recovery or reapply:

```bat
tools\run_patch_checks.bat 97
tools\run_patch_checks.bat 96
tools\run_patch_checks.bat 95
```
