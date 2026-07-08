# World Lens Dependency Map v1
**Patch:** 252  
**Purpose:** Draft dependency map for Patch 253 World Lens bridge removal.

## Draft dependency-map categories
Patch 253 should create a function in `app.py` similar to:

```python
def world_lens_dependency_map(ns: dict) -> dict:
    keys = [
        # Streamlit / data / formatting
        "st", "pd", "np",

        # UI components
        "metric_card", "soft_card",
        "render_shared_protocol_state_notice_panel",
        "render_module_reference_points",
        "render_world_lens_semantic_flags",
        "render_semantic_pressure_panel",

        # Semantic scanner
        "scan_semantic_pressure",

        # World Lens / empirical helpers
        # Fill from current app.py + ui/pages/world_lens.py inspection.

        # Report packet / source helpers
        # Fill from current World Lens render block.
    ]
    return {k: ns[k] for k in keys if k in ns}
```

This is intentionally a draft, not executable API. The exact key list should be extracted from `ui/pages/world_lens.py` during Patch 253.

## Required dependency groups

### Required at import time
These should become real imports inside `ui/pages/world_lens.py` when possible:

- standard library modules used locally;
- pandas/numpy if used directly;
- UI component helpers from `ui.components.*`;
- semantic scanner helpers from `core.semantic_pressure_scanner`.

### Required at render time
These can be passed through the dependency map while the page is still being stabilized:

- world data helpers still defined in `app.py`;
- selected-year/allocation helpers still defined in `app.py`;
- report packet helpers still defined in `app.py`;
- legacy formatting helpers not yet extracted.

### Should not be passed
Avoid passing broad objects that recreate the bridge problem:

- full `globals()`;
- full module namespaces;
- unrelated page render functions;
- unrelated scanner/state functions.

## Removal strategy after Patch 253
After `render_world_lens_page(world_lens_dependency_map(globals()))` is stable, future patches can shrink the map by moving helpers into focused modules:

1. `core/world_lens_data.py` — data loading, normalization, coverage.
2. `core/world_lens_allocation.py` — 9k allocation/audit-lens math.
3. `ui/components/world_lens_tables.py` — display tables/cards.
4. `ui/pages/world_lens.py` — final page orchestration with explicit imports.

Each migration must preserve the boundary: World Lens is an audit/context lens, not a mandate, rating authority, or certification layer.
