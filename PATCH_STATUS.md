# ALETHEIA Patch Status

## Current Patch
Patch 245 — Repository Hygiene / Patch Archive Consolidation

## Status
Ready for local validation.

## Summary
The repository has been cleaned after the modularization round. Active runtime files remain in place, while old root-level patch artifacts have been moved into `docs/patch_archive/`. The distributable package excludes `.git/`, bytecode caches, and local pytest caches.

## Current Architecture Snapshot
Shared UI components now live under `ui/components/`:
- `semantic_pressure_panel.py`
- `metric_cards.py`
- `review_cards.py`
- `tree_visuals.py`
- `receipt_blocks.py`
- `module_headers.py`

Extracted pages now live under `ui/pages/`:
- `protocol_guide.py`
- `boundary_cases.py`
- `mirror_check.py`
- `stress_test.py`
- `evidence_lab.py`
- `world_lens.py`

The extracted high-dependency pages still use a temporary runtime namespace bridge where needed. That is intentional and should be treated as the next cleanup target, not as a behavior change.

## Boundary
No scanner logic, scoring, MEI7 gate behavior, Z-axis mapping, Stress Test math, Evidence Lab calculations, World Lens math, receipt schema, telemetry, storage, certification, enforcement, or authority behavior changed.

## Validation
Recommended local checks:

```bat
python -m py_compile app.py ui\components\*.py ui\pages\*.py
python -m pytest
python -m streamlit run app.py
```

Manual smoke check:
- Mirror Check opens and runs.
- Stress Test opens and runs.
- Evidence Lab opens and runs.
- World Lens opens and all internal tabs render.
- Boundary Cases opens.
- Protocol Guide opens.
- Receipt Reader is clearly indicated under Why ALETHEIA → Support utilities.
- Only one top-level module body renders at a time.
