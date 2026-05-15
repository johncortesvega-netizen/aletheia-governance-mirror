# PATCH 72.18 RECOVERY NOTE - World Lens Receipt Naming and Sanctuary Humility Export Guard

If Patch 72.18 must be reverted, restore these files from the last known working state after Patch 72.17:

- `app.py`
- `tests/test_patch_72_18_world_lens_receipt_naming_and_humility_export.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.18 fixes two World Lens receipt issues:

1. The complete receipt button and filenames now use current World Lens naming instead of older Grid wording.

2. World Lens receipt/export narrative fields now neutralize old absolute Sanctuary wording:

```text
SANCTUARY evidence pattern: strong public-data baseline, still subject to protocol guardrails
```

is replaced in export narrative fields with humble low-risk/internal-taxonomy wording.

Raw/internal taxonomy values such as `SANCTUARY` remain available for compatibility and aggregation.

## What did not change

- No scoring formula changed.
- No verdict-routing logic changed.
- No 9k allocation formula changed.
- No Evidence Lab data model changed.
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
tools\run_patch_checks.bat 72_18
```
