# PATCH 72.10 RECOVERY NOTE - Trust Upload Auto-Normalizer

If Patch 72.10 must be reverted, restore these files from the last known working state after Patch 72.9:

- `core/empirical.py`
- `core_empirical.py`
- `tests/test_patch_72_10_trust_upload_auto_normalizer.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.10 improves Evidence Lab trust ingestion.

Users should not need to manually edit common public trust files into ALETHEIA-ready format. The empirical layer now recognizes OWID/self-reported trust style columns:

- `Entity` -> `country`
- `Code` -> `iso3`
- `Year` -> `year`
- `Trust in others` -> `wvs_generalized_trust`

If trust values are on a 0-100 percentage scale, they are normalized to 0-1. Already-normalized 0-1 values are preserved.

Upload diagnostics now show a transform note when this auto-normalization occurs.

## What did not change

- No scoring formula changed.
- No verdict-routing logic changed.
- No 9k allocation formula changed.
- No World Lens logic changed.
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
tools\run_patch_checks.bat 72_10
```
