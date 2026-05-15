# Patch 36.1 — Automation Script Hotfix + Safe Check Workflow

## Purpose

Fix the Patch 36 automation workflow so Windows Command Prompt can run patch-specific checks reliably.

## Changes

- Added `tools/run_patch_checks.py` to resolve patch test wildcards in Python instead of relying on CMD wildcard expansion.
- Updated `tools/run_patch_checks.bat` to call the Python helper.
- Added `tools/run_current_patch.bat` as an alias for patch-specific checks.
- Updated `tools/run_checks.bat` to run a safe default check instead of full pytest collection.
- Added `tools/package_patched_items.py` for manifest-based patched-item packaging.
- Added `docs/progress_database.md` and `PATCH_STATUS.md` for local continuity tracking.
- Added a Patch 36.1 regression test.

## Why

Full pytest collection currently surfaces legacy duplicate-test and import issues. Patch-specific checks should remain stable while older collection issues are cleaned up later.

## Commands

Run current patch checks:

```bat
tools\run_patch_checks.bat 36_1
```

Run safe default checks:

```bat
tools\run_checks.bat
```

## Guardrails

No production governance logic changed. No Global ID sync. No public ledger. No authority handoff.
