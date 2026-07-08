# PATCH NOTES

## Patch 249 — Stress Test Bridge Removal

- Removed broad `globals()` handoff from Stress Test page call.
- Added explicit Stress Test dependency inventory in code.
- Added documentation for the bridge-removal step.
- No scoring, scanner, MEI7, Z-axis, receipt, Evidence Lab, World Lens, telemetry, or authority-boundary behavior changed.

# Patch 250 — Evidence Lab Bridge Removal

Patch 250 replaces the broad Evidence Lab `globals()` bridge with an explicit dependency map. This keeps the page functional while making its dependency surface reviewable for later cleanup. Runtime logic is unchanged.
