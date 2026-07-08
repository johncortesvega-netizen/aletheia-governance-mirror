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
