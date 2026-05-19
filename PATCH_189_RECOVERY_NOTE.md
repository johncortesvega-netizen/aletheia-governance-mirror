# Patch 189 Recovery Note — No-Colon Brand Titles, Raised Tree Canopy, Clean Full Zip

Patch 189 is a small visual/branding patch on top of Patch 188.

It removes the colon after `Aletheia` in the stacked brand title surfaces and related public-label references, changing the visible public title from `Aletheia: AI PATROL` to `Aletheia AI PATROL` while preserving the two-line title layout.

It also raises the explanatory tree canopy used by the Mirror Check and Stress Test tree visual. This is a visual-only adjustment. It does not change scoring, routing, taxonomy, receipt values, protocol-adjusted state, or any tree-state logic.

The delivered artifact is a clean full-project zip with older root patch artifacts archived into `docs/patch_archive/`; only Patch 189 artifacts remain visible at the root.

Rollback:
- Revert `ui/app_shell.py`, `ui/unit_preview.py`, and `app.py` to Patch 188.
- Revert the Patch 166 / 185 / 187 branding test expectation updates.
- Remove `tests/test_patch_189_no_colon_brand_titles.py`.
- If needed, restore archived previous root patch artifacts from `docs/patch_archive/`.

No logic, scoring, routing, taxonomy, receipt, storage, or protocol behavior changed.
