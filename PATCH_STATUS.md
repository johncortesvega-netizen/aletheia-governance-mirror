# PATCH STATUS

## Current patch

**Patch 249 — Stress Test Bridge Removal**

Status: ready for local validation.

## Scope

Stress Test no longer receives the full `globals()` namespace directly. It now
receives an explicit dependency map from `stress_test_dependency_map(globals())`.

## Boundary

No runtime governance behavior changed. This is a modularization boundary patch.

## Patch 250 — Evidence Lab Bridge Removal

Status: READY

- Removed broad `globals()` handoff from Evidence Lab.
- Added explicit `EVIDENCE_LAB_DEPENDENCIES` and `evidence_lab_dependency_map(...)`.
- Updated `app.py` to call `render_evidence_lab_page(evidence_lab_dependency_map(globals()))`.
- No Evidence Lab calculation, scanner, scoring, MEI7, Z-axis, World Lens, receipt, telemetry, or authority-boundary behavior changed.
