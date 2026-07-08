# Patch 234 — App Modularization Stage 6: Module Headers

Stage 6 extracts shared module/header notice rendering from `app.py` into `ui/components/module_headers.py`.

## Scope
- Adds `render_shared_protocol_state_notice_panel(...)`.
- Keeps `update_protocol_state(...)` and session-state mutation in `app.py`.
- Adds `render_module_reference_points(...)` as a safe UI-only helper for later page extraction.

## Boundary
This patch changes presentation ownership only. It does not change shared-state calculation, scoring, scanner logic, MEI7 gate, Z-axis, World Lens math, Evidence Lab calculations, receipts, telemetry, or authority boundaries.
