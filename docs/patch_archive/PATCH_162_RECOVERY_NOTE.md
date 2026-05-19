# PATCH 162 RECOVERY NOTE - Artificial Mind Formation Theory Explainer

Patch 162 adds a static Protocol Guide explainer called **Artificial Mind Formation Theory**.

## What changed

- Added a new copy-only renderer: `pages_ui/artificial_mind_formation_page.py`.
- Wired the explainer into the Protocol Guide as a collapsed expander.
- Added `docs/artificial_mind_formation_theory.md` as the documentation source for the theory/explainer text.
- Added patch-specific tests for required sections, boundary language, and absence of scoring/taxonomy/World Lens hooks.

## Core line

> ALETHEIA cannot build the spark. It can inspect the hands reaching for it.

## What did not change

- No core scoring changed.
- No taxonomy state was added.
- No World Lens logic changed.
- No receipt schema or generation changed.
- No protocol routing changed.
- No sentience, consciousness, personhood, soul, life, legal status, safety, or spiritual authority certification was added.

## Rollback

Remove the import and `render_artificial_mind_formation_page(st)` call from `app.py`, then delete:

- `pages_ui/artificial_mind_formation_page.py`
- `docs/artificial_mind_formation_theory.md`
- `tests/test_patch_162_artificial_mind_formation_theory.py`
- `PATCH_162_MANIFEST.txt`
- `PATCH_162_RECOVERY_NOTE.md`

Human review remains required.
