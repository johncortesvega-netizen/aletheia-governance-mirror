# Patch 238 — App Modularization Stage 8: Boundary Cases Page

This patch extracts the Boundary Cases surface from `app.py` into `ui/pages/boundary_cases.py`.

## Scope
- Moves Boundary Cases rendering into a dedicated page module.
- Keeps Boundary Cases as a calibration/reference surface.
- Preserves protocol-state updates by passing `update_protocol_state` from `app.py`.
- Preserves the shared protocol-state notice by passing the existing renderer from `app.py`.

## Boundary
No scanner logic, scoring, MEI7 gate, Z-axis, Stress Test math, Evidence Lab calculations, World Lens math, receipt schema, telemetry, or authority behavior is changed.

## Manual checks
- Boundary Cases opens from the module selector.
- Case selection works.
- Boundary diagnostics expander opens.
- Consent audit, mechanism scan, semantic pressure scan, self-audit, and receipt example still render.
- Navigation containment still renders one top-level module at a time.
