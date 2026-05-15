# PATCH 49 RECOVERY NOTE — Full Test Suite / Legacy Test Cleanup

Patch 49 hardens local testing by separating current safe checks from legacy full-suite cleanup.

## Added / changed

- `tools/run_current_suite.py` — runs current patch tests from Patch 33 onward and compile checks.
- `tools/run_checks.bat` — now calls the current safe suite and prints a non-blocking legacy inventory.
- `tools/run_full_checks.bat` — explicit full-suite command for later cleanup work.
- `tools/run_legacy_test_inventory.py` — lists legacy tests and known blockers without deleting them.
- `pytest.ini` — ignores nested duplicate `tests/tests` collection by default.
- `docs/legacy_test_cleanup.md` — explains current checks vs legacy cleanup.
- `PATCH_STATUS.md`, `docs/progress_database.md`, `docs/patch_workflow.md`, `README.md`, and `about_page.py` — updated to surface the Patch 49 workflow.
- `tests/test_patch_49_legacy_test_cleanup.py` — patch contract tests.

## Known legacy blockers documented

- `tests/tests/test_patch_29_hard_capture_receipt_trace.py`
- `tests/test_patch_20_1_batch_question_upload_mode.py`
- `tests/test_scoring_repair_questions.py`

## Recovery

If Patch 49 fails, restore the files listed in `PATCH_49_MANIFEST.txt` from the last passing project state, then re-apply only Patch 49.

## Authority boundary

Patch 49 changes developer workflow only. It adds no governance authority, no Global ID sync, no public ledger, no real 9k selection, no World Leader logic, no automatic reset, no neural data, no memory extraction, no spiritual validation, and no automated enforcement.
