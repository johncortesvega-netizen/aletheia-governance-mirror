# ALETHEIA Patch Status

## Current Patch
Patch 226 — Navigation Containment Refactor

## Status
Ready for local validation.

## Summary
Top-level navigation no longer uses Streamlit tabs. It uses a single active-module selector and renders only the selected module body. This prevents inactive modules from leaking into one long page after reruns.

## Boundary
No changes to scanner logic, scoring, MEI7 gate, Z-axis, receipts, Evidence Lab calculations, World Lens math, semantic pressure logic, tests, telemetry, or authority behavior.

## Validation
- `python -m py_compile app.py`
- `python -m pytest`
- `python -m streamlit run app.py`

## Patch 227 — App Modularization Stage 2: Metric Cards
Status: READY
Type: modularization / UI helper extraction

Summary:
- Moved shared `metric_card` and `soft_card` presentation helpers from `app.py` to `ui/components/metric_cards.py`.
- Updated `app.py` to import these helpers from the new component module.
- Added Stage 2 modularization documentation.

Boundary:
- No scoring, scanner logic, MEI7 gate behavior, Z-axis mapping, Stress Test math, Evidence Lab calculations, World Lens math, receipts, telemetry, storage, or authority behavior changed.


## Patch 228 — Metric Card Layout Stabilization
Status: READY
Type: modularization stabilization / UI layout

Summary:
- Stabilizes `metric_card(...)` and `soft_card(...)` after Stage 2 extraction.
- Adds full-width block behavior and safer wrapping inside Streamlit columns.
- Targets narrow status-card collapse in Stress Test and awkward explanatory-card wrapping in Mirror Check.

Boundary:
- UI layout only.
- No scoring, scanner logic, semantic pressure logic, MEI7 gate behavior, Z-axis mapping, Stress Test math, Evidence Lab calculations, World Lens math, receipts, telemetry, storage, or authority behavior changed.

Validation:
- `python -m py_compile app.py ui\components\metric_cards.py ui\components\semantic_pressure_panel.py`
- `python -m pytest`
- `python -m streamlit run app.py`

## Patch 229 — Threshold Metric Readability Follow-up

Status: READY
Type: UI readability stabilization after modularization Stage 2

Summary:
- Replaces a narrow native `st.metric` row in Mirror Check's Threshold direction review with a readable summary table.
- Adds defensive wrapping CSS for native Streamlit metric labels and values.
- Presentation-only; no scoring, scanner, MEI7, Z-axis calculation, Evidence Lab math, World Lens math, receipt, telemetry, or authority behavior changes.

Validation:
- `python -m py_compile app.py ui\components\metric_cards.py ui\components\semantic_pressure_panel.py`
- `python -m pytest`
- Manual check: Mirror Check → Threshold direction review values remain readable.


## Patch 230 — Protocol Metric HTML Rendering Fix
Status: READY
Type: presentation hotfix after Stage 2 modularization
Files: app.py; ui/components/metric_cards.py; docs/app_modularization_stage2_protocol_metric_html_fix.md
Boundary: no scoring, scanner, MEI7, Z-axis, Stress Test math, Evidence Lab math, World Lens math, receipt, telemetry, or authority behavior changes.

## Patch 231 — App Modularization Stage 3: Review Cards
Status: READY

- Extracted shared review-card rendering helpers into `ui/components/review_cards.py`.
- Stress Test result explanation and repair/recommendation cards now use shared component helpers.
- Presentation-only modularization; no scanner, scoring, MEI7, Z-axis, World Lens, Evidence Lab, receipt, telemetry, or authority behavior changed.

## Patch 232 — App Modularization Stage 4: Tree Visuals
Status: READY

- Extracted Mirror/Stress tree visual renderer into `ui/components/tree_visuals.py`.
- `app.py` now imports `render_pulse_tree` from the component module.
- No governance logic, scoring, MEI7 gate, Z-axis, receipts, Evidence Lab math, or World Lens math changed.



## Patch 233 — App Modularization Stage 5: Receipt Blocks
- Extracted shared receipt visual panel rendering into `ui/components/receipt_blocks.py`.
- Reused helper in Stress Test receipt download and Protocol Guide receipt example.
- Visual-only; no receipt schema or scoring changes.


## Patch 234 — App Modularization Stage 6: Module Headers
- Extracted shared protocol-state notice rendering into `ui/components/module_headers.py`.
- Kept protocol-state computation in `app.py` to avoid behavior changes.
- Added module reference helper for later page extraction.

## Patch 235 — Receipt Reader Navigation Restore
Status: ready

Restores Receipt Reader as a top-level single-module navigation item. Receipt Reader remains read-only and does not rescore or certify receipts.

## Patch 236 — App Modularization Stage 7: Protocol Guide Page

Status: ready.

- Extracted Protocol Guide rendering from `app.py` into `ui/pages/protocol_guide.py`.
- Added `ui/pages/__init__.py`.
- Added documentation for Stage 7 modularization.
- No scoring, scanner, MEI7, Z-axis, Evidence Lab, World Lens, Stress Test, receipt, telemetry, or authority behavior changes.

## Patch 237 — Receipt Reader Support Utility Placement Clarification
Status: Ready
Type: UI copy / navigation placement clarification

Summary:
- Clarifies that Receipt Reader is available under Why ALETHEIA → Support utilities.
- Keeps Receipt Reader framed as a read-only support utility rather than a main decision module.
- Adds docs/receipt_reader_support_utility_placement_v1.md.

Boundary:
- No runtime governance logic changes.
- No receipt schema/parser/witness changes.
- No scanner, scoring, MEI7, Z-axis, Evidence Lab, or World Lens math changes.

## Patch 238 — App Modularization Stage 8: Boundary Cases Page
- Extracted Boundary Cases rendering from `app.py` into `ui/pages/boundary_cases.py`.
- Kept Boundary Cases as reference/calibration surface; no scoring or governance logic changed.
- Added `docs/app_modularization_stage8_boundary_cases_page.md`.


## Patch 239 — App Modularization Stage 9: Mirror Check Page

Status: READY. Extracts Mirror Check page body into `ui/pages/mirror_check.py` using a behavior-preserving runtime namespace bridge. No scoring, scanner, receipt, MEI7, Z-axis, World Lens, Evidence Lab, telemetry, or authority-boundary behavior changed.


## Patch 240 — Receipt Reader Placement Rebase After Stage 9

Receipt Reader placement copy re-applied after Stage 9. Current intended location: Why ALETHEIA → Support utilities → Receipt Reader — Standard View. Documentation-only/navigation-copy clarification; no runtime governance behavior changes.

## Patch 241 — Mirror Check Layout Cleanup and Receipt Reader Header Hint
Status: READY
Type: UI readability / placement clarification

- Mirror Check explanation panels changed to full-width sequential expanders.
- Receipt Reader location added as a global header caption.
- No scoring, scanner, MEI7, Z-axis, Evidence Lab, World Lens, receipt, telemetry, or authority-boundary changes.

## Patch 242 — App Modularization Stage 10: Stress Test Page
Status: READY
Type: page extraction / behavior-preserving modularization

- Extracted Stress Test rendering from `app.py` into `ui/pages/stress_test.py`.
- Uses the same temporary runtime namespace bridge pattern as Stage 9 to avoid changing scenario scoring, batch behavior, receipts, semantic diagnostics, or UI state keys.
- `app.py` now delegates Stress Test rendering to `render_stress_test_page(globals())`.
- No scanner, scoring, MEI7, Z-axis, Evidence Lab, World Lens, receipt schema, telemetry, or authority-boundary behavior changed.

## Patch 243 — App Modularization Stage 11: Evidence Lab Page
Status: ready

- Extracts the Evidence Lab page from `app.py` into `ui/pages/evidence_lab.py`.
- Keeps behavior stable through a temporary runtime namespace bridge.
- Does not change scoring, scanner logic, Evidence Lab calculations, World Lens data, receipts, MEI7, Z-axis, telemetry, or authority boundaries.


## Patch 244 — App Modularization Stage 12: World Lens Page

Status: ready for local validation.

Summary: extracted the World Lens page into `ui/pages/world_lens.py` using a transitional runtime namespace bridge. This reduces `app.py` size while preserving existing World Lens behavior, internal tabs, Evidence Lab integration, selected-year allocation, and report packet behavior.

Boundary: no scanner, scoring, MEI7, Z-axis, Evidence Lab calculation, World Lens math, receipt schema, 9k allocation rule, telemetry, or authority-boundary behavior changed.
