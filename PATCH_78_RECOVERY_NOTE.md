# PATCH 78 RECOVERY NOTE — Capture Risk Checklist / Prompt Pack

Patch 78 is documentation, examples, About-copy, and tests only.

If the patch causes issues, remove or revert these files:

- `docs/capture_risk_checklist.md`
- `examples/capture_risk_prompts/`
- `tests/test_patch_78_capture_risk_checklist_prompt_pack.py`
- `PATCH_78_MANIFEST.txt`
- `PATCH_78_RECOVERY_NOTE.md`

Then revert the Patch 78 edits in:

- `README.md`
- `app.py`
- `about_page.py`
- `docs/capture_risk_framework.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

Run:

```bat
tools\run_patch_checks.bat 78
```

Expected recovery result: Patch 77 remains intact with the Capture Risk Signals Framework, and no scoring, routing, receipt, storage, or authority behavior has changed.

Patch 78 does not add enforcement, certification, punishment, legal authority, political authority, religious authority, public ledger, Global ID sync, central storage, or final judgment.
