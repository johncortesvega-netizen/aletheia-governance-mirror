# Patch 68 — Advanced English Stress Lexicon + Asylum Metric Enforcement

## Summary

Patch 68 expands Stress Test calibration for advanced English governance-risk language and fixes Asylum metric enforcement for non-malicious Asylum labels.

## Added

- `ADVANCED_ENGLISH_STRESS_TEST_RISK_SENSITIVITY_RULES` in `protocol.py`
- Advanced English 50-scenario batch baseline
- Documentation for advanced English stress calibration
- Patch-specific tests

## Behavior

- Advanced English stress scenarios no longer wash into Sanctuary.
- Hard-capture advanced cases route to `ASYLUM / High`.
- Medium advanced cases route to `THRESHOLD / Needs Safeguards`.
- Any explicit Asylum label receives metric enforcement even when not phrased as malicious leadership.

## Authority boundary

No enforcement, no public ledger, no Global ID sync, no automated authority, no leader removal, and no replacement of human review.
