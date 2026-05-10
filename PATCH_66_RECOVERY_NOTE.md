# Patch 66 — Stress Test Risk Sensitivity Calibration

Patch 66 raises the Stress Test's sensitivity for subtle governance-risk scenarios.

## What changed

- Added soft stress-test sensitivity markers in `protocol.py`.
- Scenarios with missing appeal, no term limits, biometric access pressure, forced consent, fallback-data confusion, founder control, surveillance, or non-meaningful human review now route to `THRESHOLD / Needs Safeguards` unless explicit safeguards are present.
- Hard capture cases still route to `ASYLUM / High`.
- Added tests for the official 50-scenario Stress Test batch baseline.

## Safety boundary

This patch does not add authority, enforcement, Global ID sync, central storage, public ledger behavior, or automated decisions. It only adjusts the mirror signal and keeps human review required.

## Check

```bat
tools\run_patch_checks.bat 66
```
