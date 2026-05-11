# PATCH 72.13 RECOVERY NOTE - Evidence Lab Year Selector and Trust Diagnostic Guard

If Patch 72.13 must be reverted, restore these files from the last known working state after Patch 72.12:

- `app.py`
- `tests/test_patch_72_13_evidence_lab_year_trust_guard.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.13 fixes two Evidence Lab UI/diagnostic issues.

1. The Country-Year Explorer year dropdown no longer snaps back to a synced/default year such as 2024 after the user manually selects another available year.

2. Direct merged-upload diagnostics no longer present `empirical_trust_prior` as a missing upload source. Trust prior is a derived/scoring field. Raw trust should be read from `wvs_generalized_trust` when available; the trust prior is computed during scoring or falls back neutrally when raw trust is unavailable.

## What did not change

- No scoring formula changed.
- No verdict-routing logic changed.
- No 9k allocation formula changed.
- No World Lens logic changed.
- No Evidence Lab data model changed.
- No receipt schema changed.
- No authority-boundary logic changed.

ALETHEIA remains:

- Authority claim: `False`
- Human review required: `True`
- Public ledger: `False`
- Global ID sync: `False`
- Central storage: `False`
- Dataflow boundary: `Power -> Mirror. Never Mirror -> Power.`

## Validation

Run:

```bat
tools\run_patch_checks.bat 72_13
```
