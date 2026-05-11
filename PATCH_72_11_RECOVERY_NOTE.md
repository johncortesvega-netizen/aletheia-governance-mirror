# PATCH 72.11 RECOVERY NOTE - Mascot Logo Replacement

If Patch 72.11 must be reverted, restore these files from the last known working state after Patch 72.10:

- `app.py`
- `assets/aletheia_robot_laurel_logo.png`
- `tests/test_patch_72_11_mascot_logo_replacement.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

## What changed

Patch 72.11 is visual-only.

It replaces the two dove corner logos in the app with the new Aletheia cardboard robot mascot wearing a green laurel/leaf crown:

- header right circular emblem
- sidebar top circular emblem

The mascot is stored at:

```text
assets/aletheia_robot_laurel_logo.png
```

The app embeds the PNG as a data URI so it displays reliably inside Streamlit markdown HTML.

## What did not change

- No scoring formula changed.
- No verdict-routing logic changed.
- No Evidence Lab logic changed.
- No Stress Test logic changed.
- No Mirror Check logic changed.
- No Boundary Cases logic changed.
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
tools\run_patch_checks.bat 72_11
```
