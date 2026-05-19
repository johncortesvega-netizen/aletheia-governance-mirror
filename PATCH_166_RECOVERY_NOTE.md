# PATCH 166 Recovery Note

## Summary
Patch 166 is a visible public rebrand patch. It changes copy/layout assets only and can be rolled back safely if the team wants to revisit wording or artwork. The engine boundary is preserved: no scoring, routing, taxonomy, World Lens math, receipt schema, or protocol logic changed.

## Recovery steps
1. Restore the files listed in `PATCH_166_MANIFEST.txt` from the pre-patch state if the AI Patrol branding needs to be reverted.
2. Re-run `python tools/run_patch_checks.py 166` after restoring any files to confirm the patch-specific copy/asset state is aligned.
3. If needed, verify the app boots and that the header/sidebar/about image load from the packaged PNG assets.

## Notes
- The new mascot outfit is packaged locally in `assets/aletheia_robot_laurel_logo.png`, `assets/aletheia_mascot.png`, and `assets/about_header.png`.
- Unit Preview wording now uses the `AI Patrol Preview Unit` public-facing label while preserving ALETHEIA as the underlying project identity.
- Human review remains required.
