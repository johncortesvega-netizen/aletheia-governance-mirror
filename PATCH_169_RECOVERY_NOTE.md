# PATCH 169 Recovery Note

## Summary
Patch 169 is a UI/copy/layout cleanup for Evidence Lab. It restores readability by converting the top guidance into compact collapsed panels and by collapsing long template/source-map sections by default.

## Recovery steps
1. Restore `app.py` and `pages_ui/evidence_lab_page.py` from the pre-patch state if the Evidence Lab layout needs to be reverted.
2. Remove `tests/test_patch_169_evidence_lab_panel_layout.py` if reverting the patch completely.
3. Re-run `python tools/run_patch_checks.py 169` after applying or reverting changes.

## Boundary
This patch does not change empirical scoring, upload parsing, evidence mapping, World Lens math, routing, taxonomy, receipt schema/generation, protocol logic, telemetry, storage, certification, enforcement, or authority behavior. Human review remains required.
