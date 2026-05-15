# Patch 116 Recovery Note — App Shell Router Refactor Step 5

Patch 116 is a narrow, behavior-preserving app-shell extraction.

## What changed

- `ui/app_shell.py` now contains `render_app_footer_banner(app_version, container=None)`.
- `app.py` imports and calls `render_app_footer_banner(APP_VERSION, st)` instead of rendering the footer banner inline.
- Documentation, status, progress, tests, and the baseline manifest were updated to record the patch.

## What did not change

Patch 116 does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, interactive controls, session state, downloads, analysis behavior, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, certification, enforcement, or final-truth behavior.

## Recovery steps

If the patch needs to be rolled back:

1. Restore `app.py` from the pre-Patch-116 baseline.
2. Restore `ui/app_shell.py` from the pre-Patch-116 baseline.
3. Remove `tests/test_patch_116_app_shell_router_refactor_step_5.py`.
4. Restore `README.md`, `docs/architecture.md`, `docs/patch_index.md`, `docs/public_trust_package.md`, `PATCH_STATUS.md`, `docs/progress_database.md`, and `data/protocol_baseline_manifest.json` from the pre-Patch-116 baseline.
5. Re-run the most recent passing patch checks.

## Local validation

Run:

```bat
tools\run_patch_checks.bat 116
tools\run_patch_checks.bat 115
tools\run_patch_checks.bat 114
python tools\run_protocol_baseline_self_audit.py
```

ALETHEIA remains a mirror, not a throne. Humans keep the judgment.
