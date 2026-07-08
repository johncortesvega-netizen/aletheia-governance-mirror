# Patch 250 — Evidence Lab Bridge Removal

## Purpose

Patch 250 removes the broad `globals()` handoff from the Evidence Lab page.

Before this patch, `app.py` called:

```python
render_evidence_lab_page(globals())
```

That made the page functional, but the page boundary remained unclear because it could access the full application namespace.

After this patch, `app.py` calls:

```python
render_evidence_lab_page(evidence_lab_dependency_map(globals()))
```

The page now declares an explicit `EVIDENCE_LAB_DEPENDENCIES` tuple and receives only those dependencies.

## Scope

Changed files:

- `app.py`
- `ui/pages/evidence_lab.py`

Added documentation:

- `docs/modularization_stage250_evidence_lab_bridge_removal.md`

## Boundary

This patch is a modularization boundary cleanup only.

It does not change:

- semantic scanner logic
- Evidence Lab scoring/calculations
- public-data ingestion logic
- World Lens math or 9k allocation logic
- MEI7 ethics gate
- Z-axis routing
- receipts/witness schema
- telemetry/storage behavior
- authority-boundary copy

## Notes

This is still an intermediate stage. Some dependencies are still passed through the explicit map. Later cleanup patches can replace injected helpers with direct imports where appropriate.
