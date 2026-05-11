# PATCH 70.1 Recovery Note — Negated Safeguard Strength Calibration

Patch 70.1 is a narrow ethics-diagnostic calibration following the Patch 70 tree visual review.

## Issue

Inputs such as `no oversight` and `no public review` were correctly scoring as ASYLUM, but the ethics diagnostics could still list positive strengths such as transparency or accountability because positive terms were detected inside negated phrases.

## Change

Patch 70.1 adds local negation filtering for positive-credit terms in `core/ethics.py`:

- `no oversight`
- `no public review`
- `without transparency`
- `no accountability`
- Dutch equivalents such as `geen`, `niet`, and `zonder` near positive safeguard terms

This filter only affects positive strength credit. Risk, grip-marker, ASYLUM, local-receipt, and authority-boundary behavior remain unchanged.

## Verification

Run:

```bat
tools\run_patch_checks.bat 70_1
```

Recommended full regression:

```bat
tools\run_checks.bat
```

## Boundary

Patch 70.1 does not add legal, political, medical, religious, institutional, or automated authority. ALETHEIA remains a local mirror only: no public ledger, no Global ID sync, no central storage, no enforcement, and human review remains required.
