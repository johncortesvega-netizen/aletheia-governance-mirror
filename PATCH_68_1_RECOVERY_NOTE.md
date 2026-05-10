# Patch 68.1 Recovery Note — Asylum Label / Metric Consistency

If this patch causes issues, revert only these files:

- `protocol.py`
- `app.py`
- `docs/asylum_label_metric_consistency.md`
- `tests/test_patch_68_1_asylum_label_metric_consistency.py`
- `PATCH_68_1_MANIFEST.txt`
- `PATCH_68_1_RECOVERY_NOTE.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `README.md`
- `about_page.py`

Expected check:

```bat
tools\run_patch_checks.bat 68_1
```

This patch is display/receipt consistency only. It does not create authority, enforcement, public ledger, Global ID sync, or central storage.
