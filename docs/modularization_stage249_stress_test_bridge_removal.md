# Patch 249 — Stress Test Bridge Removal

## Purpose

Patch 249 removes the broad `globals()` handoff from the Stress Test page.

Before this patch, `app.py` called:

```python
render_stress_test_page(globals())
```

That kept behavior stable during page extraction, but it also meant the page
could access the entire app runtime namespace. Patch 249 replaces that with an
explicit dependency map:

```python
render_stress_test_page(stress_test_dependency_map(globals()))
```

## What changed

- `ui/pages/stress_test.py` now declares `STRESS_TEST_DEPENDENCIES`.
- `stress_test_dependency_map(...)` validates that all required dependencies are present.
- `render_stress_test_page(...)` receives only the curated dependency dictionary.
- `app.py` imports and uses the dependency-map helper.

## What did not change

- No Stress Test scoring changes.
- No semantic pressure scanner changes.
- No MEI7 gate changes.
- No Z-axis changes.
- No receipt schema or witness logic changes.
- No batch behavior changes.
- No Evidence Lab or World Lens math changes.
- No telemetry/storage behavior changes.

## Remaining bridge work

Stress Test still uses an injected dependency map. Later cleanup can convert
stable utilities to direct imports one group at a time, but this patch avoids
that risk and only removes the broad namespace bridge.
