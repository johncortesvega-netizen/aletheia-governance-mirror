# Patch 32.2 — Mascot Logo Replacement

Type: UI asset patch only.

## Goal

Replace the two dove emoji logo marks in the app shell with the ALETHEIA cardboard robot mascot:

- hero/top-right emblem
- sidebar/top-left emblem

## Files touched

- `app.py`
- `assets/aletheia_mascot.png`
- `tests/test_patch_32_2_mascot_logo_replacement.py`
- `PATCH_32_2_RECOVERY_NOTE.md`

## Behavior

- The mascot is loaded from a bundled local asset.
- The logo spots keep the same round botanical-civic frame.
- No product logic, scoring, ethics, witness, or World Lens code changed.
- App version updates to `v9.6.14-patch32-2-mascot-logo`.

## Test

```cmd
set PYTHONPATH=.
python -m pytest tests/test_patch_32_2_mascot_logo_replacement.py -q
```

Expected:

```text
5 passed
```

## Recovery

If the mascot fails to display, confirm `assets/aletheia_mascot.png` exists and rerun the static test above. Revert this patch to restore the prior dove emoji marks.
