# Patch 117 Recovery Note — Refactor Stabilization Checkpoint

Patch 117 is a stabilization checkpoint after the app-shell router refactor sequence through Patch 116.

## Scope

- Adds `docs/refactor_stabilization_checkpoint.md`.
- Adds `tests/test_patch_117_refactor_stabilization_checkpoint.py`.
- Updates public/docs/status/progress references for Patch 117.
- Updates the local protocol baseline manifest for the changed review files.

## Boundary

This patch makes no runtime UI change and no behavior change.

No scoring, verdict-routing, signal-pattern, signal-weight, receipt schema, module routing, external call, live model call, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantee, certification, enforcement, or final-truth behavior is changed.

`app.py` remains the orchestrator for interactive controls, session state, module routing, scoring, receipts, downloads, and analysis behavior. `ui/app_shell.py` remains a static shell-copy helper module.

## Recovery

If Patch 117 causes local test failure, remove the files listed in `PATCH_117_MANIFEST.txt` and restore the previous versions of updated docs/status/progress/manifest files from the Patch 116-passed baseline.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.
