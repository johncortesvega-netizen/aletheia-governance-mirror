# Patch 89 Recovery Note — Privacy Boundary Visibility

## What this patch changes

Patch 89 adds visible privacy-by-design language to ALETHEIA without changing any review logic.

It states that ALETHEIA's repository includes no built-in telemetry, trackers, analytics SDKs, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database. Inputs are processed in the running app session and receipts are user-held downloads.

## Files touched

- `app.py`
- `about_page.py`
- `README.md`
- `docs/ai_integrity_mirror.md`
- `docs/privacy_boundary.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `tests/test_patch_89_privacy_boundary_visibility.py`
- `PATCH_89_MANIFEST.txt`
- `PATCH_89_RECOVERY_NOTE.md`

## Important limitation

The privacy claim is limited to ALETHEIA's app code and repository design. If ALETHEIA is deployed on a third-party host, that host may keep server logs, access logs, crash logs, request metadata, or operational monitoring outside ALETHEIA's code boundary.

## Recovery steps

If Patch 89 causes trouble:

1. Restore the touched files from the previous passing Patch 88 baseline.
2. Re-run:

```bat
tools\run_patch_checks.bat 88
```

3. Re-apply only the privacy-copy changes after confirming the host/deployment wording is still accurate.

## Validation

```bat
tools\run_patch_checks.bat 89
tools\run_patch_checks.bat 88
tools\run_patch_checks.bat 87
tools\run_patch_checks.bat 86
tools\run_patch_checks.bat 85
```

## Boundary preserved

No scoring-math change, verdict-routing change, AI Integrity rubric change, live model benchmarking, external calls, repository crawler, storage layer, public ledger, Global ID sync, enforcement, certification, or authority claim.
