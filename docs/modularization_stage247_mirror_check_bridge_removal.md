# Patch 247 — Mirror Check Bridge Removal

## Purpose
Remove the broad `globals()` namespace bridge from the Mirror Check page after the Stage 9 page extraction.

## What changed
- `ui/pages/mirror_check.py` now declares a narrow `MIRROR_CHECK_DEPENDENCIES` list.
- `app.py` now calls:

```python
render_mirror_check_page(mirror_check_dependency_map(globals()))
```

instead of passing the full app namespace directly.

## Boundary
This is an architectural cleanup only. It does not change:
- Mirror Check scoring;
- Semantic Pressure Scanner behavior;
- MEI7 / ethics calibration;
- Z-axis behavior;
- receipt generation;
- telemetry/storage;
- authority-boundary language.

## Why it matters
Mirror Check is now the first heavy page whose dependency surface is explicit and inspectable. The remaining bridge pages are still:
- Stress Test;
- Evidence Lab;
- World Lens.
