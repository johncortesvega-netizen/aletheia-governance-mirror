# PATCH 71.8 RECOVERY NOTE — Stress Test Review Band Card Polish

If Patch 71.8 must be reverted, restore these files from the last known working state after Patch 71.7:

- `app.py`
- `tests/test_patch_71_8_stress_review_band_card_polish.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 71.8 changes only the Stress Test result-card helper text for THRESHOLD outputs.

Before:

```text
Safety risk: Medium · Review band: Needs Review
```

After:

```text
Safety risk: Medium
Review band: Needs Review
```

## What did not change

- No receipt schema changed.
- No scoring logic changed.
- No verdict-routing logic changed.
- No taxonomy changed.
- No Mirror Check changed.
- No tree visual changed.
- No Boundary Cases changed.
- No World Lens changed.
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
tools\run_patch_checks.bat 71_8
```
