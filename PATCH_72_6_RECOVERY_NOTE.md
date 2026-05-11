# PATCH 72.6 RECOVERY NOTE - Why ALETHEIA Neutral Text Refresh

If Patch 72.6 must be reverted, restore these files from the last known working state after Patch 72.5:

- `about_page.py`
- `tests/test_patch_72_6_why_aletheia_neutral_text.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.6 refreshes the Why ALETHEIA / About page text so it is current with the neutral language standard from Patches 72-72.5.

It updates:
- main About intro
- Humility Protocol / Z-axis explanation
- 9k threshold-steward explanation
- Audit label explanation
- Boundary Cases explanation
- Evidence Lab extraordinary-claim language
- World Lens non-authority wording
- sample report and navigation boundary copy

## What did not change

- No scoring logic changed.
- No verdict-routing logic changed.
- No receipt schema changed.
- No Threshold Mapping math changed.
- No tree visual changed.
- No Stress Test logic changed.
- No Boundary Cases logic changed.
- No Evidence Lab logic changed.
- No World Lens logic changed.
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
tools\run_patch_checks.bat 72_6
```
