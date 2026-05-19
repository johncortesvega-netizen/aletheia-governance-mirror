# Patch 164 Recovery Note — Artificial Mind Formation Compact Opt-In Panels

Patch 164 is a small layout-only follow-up to Patch 163.

## Intent

The Protocol Guide became too visually crowded when the Artificial Mind Formation Theory explainer exposed a long stack of sections. Patch 164 keeps the explainer opt-in: the main module remains collapsed by default, and internal subsections are grouped into four side-by-side rows of collapsed panels.

## Recovery / rollback

To revert this patch only:

1. Restore `pages_ui/artificial_mind_formation_page.py` to the Patch 163 version, removing `ARTIFICIAL_MIND_FORMATION_PANEL_ROWS`, `_section_map()`, and the nested `st.columns(2)` / panel-expander rendering loop.
2. Remove `tests/test_patch_164_artificial_mind_opt_in_panel_layout.py`.
3. Remove Patch 164 entries from `PATCH_STATUS.md` and `docs/progress_database.md`.
4. Remove `PATCH_164_MANIFEST.txt` and this recovery note.

## Boundaries preserved

Patch 164 does not change scoring, taxonomy, World Lens, receipt generation, routing, external calls, telemetry/storage, certification, enforcement, or authority behavior. It only changes presentation/layout for a static explainer.
