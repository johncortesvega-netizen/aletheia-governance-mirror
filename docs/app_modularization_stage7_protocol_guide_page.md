# Patch 236 — App Modularization Stage 7: Protocol Guide Page

## Scope
Stage 7 extracts the mostly static Protocol Guide surface from `app.py` into a page-level renderer:

- `ui/pages/protocol_guide.py`

The top-level app now calls `render_protocol_guide_page()` when the Protocol Guide module is selected.

## Boundary
This is a structural refactor only.

No changes were made to:

- scanner logic
- scoring
- MEI7 / ethics gate behavior
- Z-axis mapping
- Stress Test math
- Evidence Lab calculations
- World Lens math
- receipt schema or witness logic
- telemetry/storage behavior
- module navigation containment

## Why this slice
The Protocol Guide is a safe first page extraction because it is mostly static guidance/copy and has limited runtime state. This reduces `app.py` size without changing behavior.

## Manual checks
- Protocol Guide renders.
- All Protocol Guide expanders open.
- Public trust package expander renders.
- Receipt Reader remains visible as a top-level module.
- Navigation containment remains single-module.
