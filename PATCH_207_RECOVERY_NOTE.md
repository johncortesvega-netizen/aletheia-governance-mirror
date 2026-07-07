# Patch 207 — Weak Emergency Safeguard Semantic Calibration

## Summary

This patch calibrates the deterministic semantic pressure scanner for emergency-power language with weak safeguards.

## Problem fixed

The phrase:

> A government creates emergency powers after a crisis, but the powers have no sunset clause, weak appeal rights, and limited independent review.

could still display as a semantic SANCTUARY/no-strong-pattern diagnostic even though it contains emergency authority plus weakened safeguards.

## Changes

- Added weak safeguard phrases including:
  - `no sunset clause`
  - `weak appeal rights`
  - `limited independent review`
  - `limited oversight`
- Added a rule that emergency/authority language with weakened sunset, appeal, notice, review, or oversight safeguards creates review pressure.
- Prevented weak safeguard phrases from being treated as purely positive concrete safeguards.

## Boundary preserved

No main module scoring, receipt schema, World Lens math, Evidence Lab data logic, telemetry, storage, external calls, certification, or enforcement behavior changed.

## Validation

```bat
python -m py_compile core\semantic_pressure_scanner.py
python -c "from core.semantic_pressure_scanner import scan_semantic_pressure; print(scan_semantic_pressure('A government creates emergency powers after a crisis, but the powers have no sunset clause, weak appeal rights, and limited independent review.'))"
```

Expected: `THRESHOLD`, `Needs safeguards`, negative integrity pressure, and weak emergency safeguard note.
