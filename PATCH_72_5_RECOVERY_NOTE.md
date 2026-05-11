# PATCH 72.5 RECOVERY NOTE - Boundary Cases Neutral Text Refresh

If Patch 72.5 must be reverted, restore these files from the last known working state after Patch 72.4:

- `app.py`
- `tests/test_patch_72_5_boundary_cases_neutral_text.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.5 updates Boundary Cases wording to match the neutral Patch 72.4 standard.

It changes:
- "turn the mirror into a throne" -> "does not create authority, enforcement, or final decisions"
- "before any Sanctuary reading" -> "before any low-risk internal reading"
- "approach Sanctuary" -> "approach the review boundary"
- "spiritual validation" -> "extraordinary-claim validation"
- "spiritual authority leakage" -> "unverified authority leakage"

## What did not change

- No scoring logic changed.
- No verdict-routing logic changed.
- No receipt schema changed.
- No Threshold Mapping math changed.
- No tree visual changed.
- No Stress Test logic changed.
- No Evidence Lab logic changed.
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
tools\run_patch_checks.bat 72_5
```
