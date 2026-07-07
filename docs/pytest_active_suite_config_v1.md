# Pytest Active Suite Configuration
**Patch:** 218  
**Status:** Current release-gate configuration  
**Scope:** Test collection behavior only

## Purpose

ALETHEIA keeps a long historical test tree because old patch contracts are part of the development receipt chain. That history is useful for audit continuity, but it should not be confused with the active release gate.

Patch 218 makes the default `pytest` behavior explicit:

```bat
python -m pytest
```

now collects only the active suite under:

```text
tests/active/
```

This prevents the default test command from accidentally collecting stale historical tests that were written against older module names, earlier UI layouts, or removed helper functions.

## What the default active suite means

A passing default pytest run means:

- the current active smoke/regression checks passed;
- the active semantic guardrails still route known pressure cases to review;
- concrete safeguard language can still remain low-pressure;
- the repository did not accidentally collect the legacy inventory as if it were current.

It does **not** mean:

- every historical patch test passes;
- every archived contract still describes the current app;
- ALETHEIA is production-certified;
- the scoring is statistically predictive;
- the mirror has authority.

## Legacy tests

Legacy tests remain in the repository as cleanup inventory. They should be handled deliberately through triage, not accidentally through default collection.

Use the existing inventory tool for visibility:

```bat
python tools\run_legacy_test_inventory.py
```

Full historical test attempts are explicit and may fail until tests are deleted, restored, or updated:

```bat
tools\run_full_checks.bat
```

## Boundary note

This patch changes pytest collection defaults only. It does not change runtime behavior, scanner logic, scoring, MEI7 routing, Z-axis behavior, Evidence Lab calculations, World Lens math, receipts, storage, telemetry, or authority boundaries.
