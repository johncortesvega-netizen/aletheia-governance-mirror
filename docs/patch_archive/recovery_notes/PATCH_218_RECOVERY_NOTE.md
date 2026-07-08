# Patch 218 Recovery Note — Pytest Active Suite Configuration

## What changed

Patch 218 adds `pytest.ini` so default pytest collection points at `tests/active/`.

It also adds a small active semantic guardrail suite:

- opaque hidden-power claim routes to review;
- emergency power with weak safeguards routes to review;
- identity-gated public benefits routes to review;
- concrete appeal/audit/review language can remain low-pressure.

## Why

The repository contains historical patch tests and older regression tests that are useful for audit continuity but may not describe the current app. Default pytest collection should not accidentally treat that inventory as the active release gate.

## Recovery

If default pytest unexpectedly collects legacy files, confirm `pytest.ini` exists at the repository root and contains:

```ini
testpaths = tests/active
```

Then rerun:

```bat
python -m pytest
```

For legacy visibility, use:

```bat
python tools\run_legacy_test_inventory.py
```

## Boundary

This patch changes test collection configuration only. It does not change runtime behavior, scoring, semantic scanner logic, MEI7 gate, Z-axis behavior, Stress Test metrics, Evidence Lab calculations, World Lens math, receipts, storage, telemetry, certification, enforcement, or authority behavior.
