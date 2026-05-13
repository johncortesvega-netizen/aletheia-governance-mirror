# Patch 115 Recovery Note — App Shell Router Refactor Step 4

Patch 115 is a static app-shell extraction. It does not change scoring or runtime analysis behavior.

## Recovery

If this patch needs to be reverted, remove:

- `tests/test_patch_115_app_shell_router_refactor_step_4.py`
- `PATCH_115_MANIFEST.txt`
- `PATCH_115_RECOVERY_NOTE.md`

Then restore the previous versions of:

- `app.py`
- `ui/app_shell.py`
- `README.md`
- `docs/architecture.md`
- `docs/patch_index.md`
- `docs/public_trust_package.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `data/protocol_baseline_manifest.json`

## Boundary

This patch only extracts static sidebar tuning-section copy into `ui/app_shell.py`. Interactive controls, session state, module routing, scoring, verdict routing, signal patterns, signal weights, receipt schemas, downloads, storage, external calls, live model calls, telemetry, analytics, Global ID sync, public ledger sync, certification, enforcement, privacy guarantees, and final-truth behavior remain unchanged.

ALETHEIA remains a mirror. Humans keep the judgment.
