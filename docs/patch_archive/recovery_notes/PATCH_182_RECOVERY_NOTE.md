# PATCH 182 Recovery Note

## Summary
Patch 182 is the second visual patch for the sky-blue / gold / white-pillars AI Patrol direction. It does not rewrite app logic. It adds small visual anchor cards to Patrol Guide, Why AI Patrol, and Evidence Lab, and extends the existing sky/gold styling to review expanders, blockquotes, tables, and subordinate AI static scan context panels.

## Recovery steps
1. Revert `app.py` to remove the Patch 182 CSS override, restore `APP_VERSION = "v1.0-ai-patrol-sky-theme"`, and remove the Patrol Guide anchor plus the two AI static scan styling comments.
2. Revert `pages_ui/about_page.py` to remove the Why AI Patrol visual anchor.
3. Revert `pages_ui/evidence_lab_page.py` to remove the Evidence Lab visual anchor.
4. Remove `tests/test_patch_182_sky_gold_module_alignment.py` if the patch is fully rolled back.
5. Keep archived patch artifacts in `docs/patch_archive/` unless deliberately restoring root-level historical patch files.
6. Re-run `python tools/run_patch_checks.py 181` after rollback, or `python tools/run_patch_checks.py 182` if keeping the patch.

## Boundary
Visual/CSS and page-anchor copy only. No scoring, routing, taxonomy, receipt, Evidence Lab calculation, World Lens, AI static scan logic, protocol logic, storage, telemetry, certification, enforcement, or authority behavior was changed. Human review remains required.
