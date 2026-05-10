# Patch 67.1 — Dutch Stress Test Lexicon + Threshold Receipt Enforcement

## Status
Ready for local verification.

## Summary
Adds Dutch Stress Test risk-sensitivity triggers so Dutch governance scenarios no longer get washed into Sanctuary because the lexicon was English-heavy.

## What changed
- Added Dutch Stress Test risk rules in `protocol.py`.
- Added Dutch 50-scenario batch baseline under `examples/batch_scenarios/`.
- Added documentation for Dutch stress calibration.
- Added tests for Dutch crisis authority, biometric/basic-services pressure, fallback-data confusion, forced consent, and threshold repair/metric softening.

## Safety boundary
This patch does not add enforcement authority.

ALETHEIA remains:
- mirror-only
- local receipt only
- no public ledger
- no Global ID sync
- no central storage
- human review required

## Check
```bat
tools\run_patch_checks.bat 67_1
```
