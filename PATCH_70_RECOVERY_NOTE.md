# PATCH 70 RECOVERY NOTE — Tree Visual Calibration

If Patch 70 needs to be rolled back, restore the previous versions of:

- app.py
- about_page.py
- README.md
- docs/progress_database.md
- PATCH_STATUS.md

Patch 70 adds the tree visual calibration documentation and test contract.

Expected check:

```bat
tools\run_patch_checks.bat 70
```

Expected result:

```text
4 passed
```

Patch purpose:

- Mirror Check tree is framed as evidence + accountability.
- Stress Test tree is framed as power under stress.
- QUESTION_PROMPT is displayed as Review Tool Mode.
- Visual tree score is not treated as protocol-adjusted integrity.
