# PATCH 109 RECOVERY NOTE — App Shell Router Refactor Step 2

Patch 109 is a small behavior-preserving app-shell extraction.

## What changed

The stable sidebar identity card and static sidebar context copy were moved from `app.py` into `ui/app_shell.py`:

- `render_sidebar_brand(...)`
- `render_sidebar_context(...)`

`app.py` now imports and calls those helpers while keeping all interactive controls and behavior in place.

## What did not change

This patch does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, navigation, downloads, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, certification, enforcement, or final truth claims.

`app.py` remains the orchestrator for session state, controls, module routing, analysis calls, receipts, and downloads.

## Recovery

To revert Patch 109:

1. Restore the previous inline sidebar identity/context block in `app.py`.
2. Remove `render_sidebar_brand` and `render_sidebar_context` calls from `app.py`.
3. Remove the Patch 109 additions from `ui/app_shell.py` or leave them unused if a later patch depends on them.
4. Remove `tests/test_patch_109_app_shell_router_refactor_step_2.py`, `PATCH_109_MANIFEST.txt`, and this recovery note if reverting fully.
5. Re-run:

```bat
tools\run_patch_checks.bat 108
tools\run_patch_checks.bat 107
python tools\run_protocol_baseline_self_audit.py
```

## Human boundary

ALETHEIA remains a mirror, not a throne. The shell refactor is maintainability work only. Human review remains required.


App.py remains the orchestrator for behavior; Patch 109 only extracts sidebar shell copy.
