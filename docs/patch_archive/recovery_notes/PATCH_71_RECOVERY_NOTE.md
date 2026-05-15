# Patch 71 Recovery Note — Batch File Repository Consolidation

Patch 71 is documentation, fixture, and test consolidation only.

If the patch must be rolled back, restore the previous versions of:

- `docs/batch_file_catalog.md` if absent before the patch, remove it.
- `docs/mirror_check_batch_baselines.md`
- `docs/stress_test_batch_baselines.md`
- `README.md`
- `about_page.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `tests/test_patch_71_batch_file_catalog.py`
- new official batch-file copies added under `examples/batch_questions/` and `examples/batch_scenarios/`.

The patch does not change scoring, receipt generation, tree visualization, authority boundaries, storage behavior, or batch execution logic.

After recovery or re-application, run:

```bat
tools\run_patch_checks.bat 71
```

Expected boundary remains unchanged: local witness receipts only; no legal, political, institutional, religious, medical, or automated authority; no public ledger; no Global ID sync; no central storage; no enforcement; human review required.
