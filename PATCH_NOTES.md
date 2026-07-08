# PATCH NOTES

## Patch 246 — App-wide Copy Cleanup Pass

Patch 246 performs a conservative app-wide copy cleanup after modularization.

### Main changes

- Replaced stale/rebrand wording such as `Patrol guide panels` with `Protocol guide panels`.
- Clarified Receipt Reader placement as a support utility under Why ALETHEIA.
- Replaced overly broad or authority-sounding phrases with bounded review language.
- Rephrased several `proof` and `final truth` phrasings into `evidence`, `truth measurement`, or `final truth claim` depending on context.
- Kept the mirror-not-throne concept intact.

### Boundary

No runtime logic changed. No scoring, scanner, MEI7, Z-axis, receipt, World Lens, Evidence Lab, telemetry, storage, or routing behavior changed.

### Validation

- `python -m py_compile app.py ui/pages/*.py ui/components/*.py`
- `python -m pytest`

## Patch 247 — Mirror Check Bridge Removal

This patch removes the broad namespace bridge from the Mirror Check page by replacing the direct `globals()` page bridge with an explicit dependency map. This makes the Mirror Check page boundary inspectable while preserving current behavior.

No governance, scanner, scoring, receipt, Evidence Lab, World Lens, or telemetry behavior is changed.
