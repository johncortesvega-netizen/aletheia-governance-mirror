# Patch 253 — World Lens Bridge Removal

## Purpose

This patch removes the broad `globals()` handoff from the World Lens page and replaces it with an explicit dependency map.

World Lens remains behaviorally unchanged. The patch only makes the page boundary more inspectable by listing the runtime helpers and constants it currently receives.

## Changed files

- `app.py`
- `ui/pages/world_lens.py`

## New page boundary

Before:

```python
render_world_lens_page(globals())
```

After:

```python
render_world_lens_page(world_lens_dependency_map(globals()))
```

The page now declares `WORLD_LENS_DEPENDENCIES` and fails loudly if a required dependency is missing.

## Preserved behavior

This patch does not change:

- World Lens math
- 9k allocation behavior
- selected-year handling
- Evidence Lab state sharing
- semantic pressure integration
- report packet generation
- scanner logic
- scoring
- MEI7 gate
- Z-axis
- receipt schema
- telemetry/storage behavior

## Follow-up

Later cleanup can replace injected helpers with direct imports where safe. World Lens should be handled carefully because it touches selected-year data, coverage diagnostics, 9k allocation, report packets, and Evidence Lab state.
