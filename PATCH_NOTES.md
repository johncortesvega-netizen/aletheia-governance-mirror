# Patch Notes

## Patch 252 — World Lens Bridge Inventory / Prep

Patch 252 prepares the final major modularization bridge removal by documenting the current World Lens dependency surface.

Added:
- `docs/world_lens_bridge_inventory_v1.md`
- `docs/world_lens_dependency_map_v1.md`

Purpose:
- Identify which dependencies World Lens still receives through the broad runtime namespace bridge.
- Document Evidence Lab state-sharing requirements.
- Preserve World Lens / 9k boundary language before making runtime changes.
- Define acceptance criteria for Patch 253.

Not changed:
- `app.py`
- `ui/pages/world_lens.py`
- scanner logic
- scoring
- MEI7 gate
- Z-axis
- Evidence Lab calculations
- World Lens math
- 9k allocation behavior
- receipts
- telemetry/storage
- authority-boundary behavior
