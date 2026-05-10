# Patch 34 — Boundary Cases Matrix

Status: reviewable patch

## What changed

- Added `docs/boundary_cases_matrix.md` with the first 10 core boundary cases.
- Added `prompts/boundary_case_prompt.md` for consistent boundary-case analysis.
- Added a new `Boundary Cases` app tab as a calibration center.
- Updated `README.md` and `about_page.py` to reference Boundary Cases.
- Added `tests/test_patch_34_boundary_cases.py`.

## Safety posture

Boundary Cases are calibration tools, not command mechanisms.

No Global ID sync, no real 9k selection, no public ledger, no neural data, no automatic reset, no leader deactivation, and no spiritual validation were added.

## Recovery

If this patch causes UI trouble, remove the `Boundary Cases` tab block from `app.py`. The documentation and prompt files can remain safely as reference material.
