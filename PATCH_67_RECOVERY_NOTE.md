# Patch 67 — Stress Test Threshold Repair + Metric Softening

## Purpose

Patch 67 makes medium-risk Stress Test results more actionable. Patch 66 correctly moved subtle governance-risk scenarios out of SANCTUARY and into THRESHOLD / Needs Safeguards. Patch 67 adds repair questions and light metric softening for those Threshold outputs.

## Changes

- Added Threshold repair-question helpers in `protocol.py`.
- Added Threshold metric-softening guard in `protocol.py`.
- Wired the calibration into Stress Test / Simulation paths in `app.py`.
- Added documentation in `docs/stress_test_threshold_repair_calibration.md`.
- Added regression tests in `tests/test_patch_67_threshold_repair_metric_softening.py`.

## Boundary

Diagnostic only. No governance authority, no enforcement, no automatic reset, no Global ID sync, no public ledger, and no central storage. ALETHEIA remains a mirror for human review.

## Check

```bat
tools\run_patch_checks.bat 67
```
