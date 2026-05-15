# ALETHEIA Patch 20.8 — Batch Table Narrow Panel Polish

Purpose:
- Improve the Batch Testing summary table in the narrow side panel.
- Keep the table readable by showing only `#`, `Type`, and `Reading`.
- Fold the former `Role` value into `Reading` so the rightmost column is no longer hidden.

Touched:
- `app.py`
- `tests/test_patch_20_8_batch_table_narrow_panel_polish.py`
- `PATCH_20_8_RECOVERY_NOTE.md`

Not touched:
- protocol logic
- scoring formulas
- witness hashing
- batch receipt generation
- parser behavior
- empirical / Global Grid logic

Rollback:
- Revert the display mapping block in `app.py` to the Patch 20.7 table configuration.
- Remove this test file and recovery note.
