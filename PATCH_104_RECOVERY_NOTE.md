# Patch 104 Recovery Note — Boundary, Privacy, and Hosted-Use Transparency

Patch 104 is a small structural/documentation patch. It should be safe to revert by removing the added boundary/privacy helper files and restoring the updated documentation/status files from the previous patch.

## What changed

Patch 104 added:

- `docs/BOUNDARY.md`
- `docs/hosting_limits.md`
- `core/boundary.py`
- `core/privacy_panel.py`
- `tests/test_patch_104_boundary_privacy_hosting.py`
- `PATCH_104_MANIFEST.txt`
- `PATCH_104_RECOVERY_NOTE.md`

Patch 104 updated:

- `README.md`
- `CONTRIBUTING.md`
- `docs/architecture.md`
- `docs/privacy_boundary.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `data/protocol_baseline_manifest.json`

## Recovery action

If the patch causes problems:

1. Remove the added Patch 104 files listed above.
2. Restore the updated files from the Patch 103 working state.
3. Run:

```bat
tools\run_patch_checks.bat 103
tools\run_patch_checks.bat 102
tools\run_patch_checks.bat 101
```

## Boundary confirmation

Patch 104 does not wire the new helper modules into `app.py`. It does not change runtime scoring, verdict routing, signal patterns, signal weights, receipt schemas, Streamlit page behavior, external calls, telemetry, analytics, storage, Global ID sync, public ledger sync, certification behavior, enforcement behavior, or final-truth claims.

The privacy language is intentionally bounded: ALETHEIA is local-first by design, but hosted deployments may have platform-level logs outside ALETHEIA's application code. This patch must not be interpreted as a privacy guarantee, security guarantee, hosting audit, compliance approval, or certification.
