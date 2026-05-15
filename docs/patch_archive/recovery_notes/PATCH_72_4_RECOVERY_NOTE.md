# PATCH 72.4 RECOVERY NOTE - Neutral Text Refresh

If Patch 72.4 must be reverted, restore these files from the last known working state after Patch 72.3:

- `app.py`
- `about_page.py`
- `README.md`
- `core/witness.py`
- `docs/threshold_mapping_layer.md`
- `tests/test_patch_72_4_neutral_text_refresh.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.4 updates textual framing across the app and docs.

The intent is to keep the Humility Protocol current while making the user-facing tone neutral and friendly:

- Z-axis = boundary of what human/system tools may responsibly claim
- Z=0.9999 = highest review boundary shown by ALETHEIA
- Z=1.0000 = outside ALETHEIA's claim
- 9k = anti-tyranny scaffold / threshold steward
- no final safety, final truth, final authority, or perfection claim

## What did not change

- No scoring logic changed.
- No verdict-routing logic changed.
- No receipt schema changed.
- No Threshold Mapping math changed.
- No tree visual changed.
- No Stress Test logic changed.
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
tools\run_patch_checks.bat 72_4
```
