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

