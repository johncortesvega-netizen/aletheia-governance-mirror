# ALETHEIA Patch 22.3 — Mirror Tree Wording Polish

Type: UI wording only.

## Intent
Rename the visible Mirror Check tree title so the interface matches the current app language.

## Touched files
- app.py
- tests/test_patch_22_3_mirror_tree_wording.py
- PATCH_22_3_RECOVERY_NOTE.md

## Not touched
- protocol.py
- core/ethics.py
- core/scoring.py
- core/simulation.py
- core/parser.py
- core/witness.py
- core/empirical.py
- verdict logic
- scoring formulas
- witness hashing
- batch UI behavior
- Global Grid behavior

## Expected behavior
- The latest Mirror Check graphic is titled "Mirror Reading Tree".
- The empty-state copy says: "No reading yet. Share one idea above to generate a Mirror Reading Tree."
- All metrics, receipts, and verdicts remain unchanged.

## Rollback
Revert the two wording strings in app.py and remove this test/recovery note.
