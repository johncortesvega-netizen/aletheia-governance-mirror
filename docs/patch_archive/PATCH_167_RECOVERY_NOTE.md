# PATCH 167 Recovery Note

## Summary
Patch 167 restores the Patrol Guide formatting after the AI Patrol rebrand. It converts the guide back into compact, opt-in side-by-side panels and restores the Artificial Mind Formation Theory explainer into the guide flow.

## Recovery steps
1. Restore `app.py` from the pre-Patch-167 state if the compact panel layout needs to be reverted.
2. Restore `pages_ui/artificial_mind_formation_page.py` and `docs/artificial_mind_formation_theory.md` if the Artificial Mind explainer should be removed again.
3. Re-run `python tools/run_patch_checks.py 167` and `python tools/run_patch_checks.py 166`.

## Boundary
This patch is UI/copy/layout restoration only. It does not alter scoring, routing, taxonomy, receipt logic, World Lens math, protocol logic, external calls, telemetry/storage, certification, enforcement, or final authority behavior. Human review remains required.
