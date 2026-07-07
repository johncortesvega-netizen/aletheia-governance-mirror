# PATCH 214 RECOVERY NOTE

## Patch
Patch 214 — Regression Guardrails / Mirror Boundary Test Pack

## Purpose
This patch adds documentation and regression tests after the UI and semantic-layer expansion in patches 210–213.

It does not modify runtime scoring, routing, UI, semantic scanner logic, receipt structure, MEI7 gate behavior, World Lens math, or Evidence Lab calculations.

## Added files
- `docs/architecture_review_v1_boundary_and_regression.md`
- `tests/test_patch_214_regression_guardrails.py`
- `manifest/patch_214.json`

## Boundary rule
Every patch must prove again that the mirror did not become a throne.

## Test command
```cmd
python -m py_compile tests\test_patch_214_regression_guardrails.py
python -m pytest tests\test_patch_214_regression_guardrails.py
```

If pytest is not installed locally, run:

```cmd
python -m py_compile tests\test_patch_214_regression_guardrails.py
```

and then run the full suite in the normal repo environment.

## Rollback
Remove the added Patch 214 files:
- `docs/architecture_review_v1_boundary_and_regression.md`
- `tests/test_patch_214_regression_guardrails.py`
- `manifest/patch_214.json`
- `PATCH_214_MANIFEST.txt`
- `PATCH_214_RECOVERY_NOTE.md`
- `PATCH_214_DELETE_LIST.txt`

No runtime source files need rollback.
