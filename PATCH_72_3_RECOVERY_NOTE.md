# PATCH 72.3 RECOVERY NOTE - Humility Protocol / Sanctuary Asymptote

If Patch 72.3 must be reverted, restore these files from the last known working state after Patch 72.2:

- `core/witness.py`
- `app.py`
- `docs/threshold_mapping_layer.md`
- `tests/test_patch_72_3_sanctuary_asymptote.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.3 adds the Humility Protocol: Sanctuary as Asymptote.

The Z-axis no longer means progress toward perfection. It means proximity to the boundary of human/system authority.

- `Z=0.0000`: full ASYLUM pressure.
- `Z=0.9999`: maximum human/system Threshold+ humility boundary.
- `Z=1.0000`: OUTSIDE SYSTEM CLAIM.

Human, political, algorithmic, institutional, or governance scenarios must not receive Z=1.0000.

Receipts now include:
- Asymptote Note
- Outside System Claim note
- 9k threshold-steward note

## What did not change

- No scoring logic changed.
- No verdict-routing logic changed.
- No canonical taxonomy changed.
- No religious authority claim was added.
- No legal, political, medical, institutional, or automated authority claim was added.
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
tools\run_patch_checks.bat 72_3
```
