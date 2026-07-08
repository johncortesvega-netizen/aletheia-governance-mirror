# Patch 232 — App Modularization Stage 4: Tree Visuals

## Purpose
Move the shared Mirror/Stress tree visual renderer out of `app.py` into a reusable UI component without changing governance logic or scoring.

## Extracted component

`ui/components/tree_visuals.py`

Contains:
- `tree_copy_for_state(...)`
- `visual_review_band_for_tree(...)`
- `render_pulse_tree(...)`
- tree visual constants

## Runtime boundary
This patch is UI-structure only. It does not modify:
- scanner logic
- MEI7 gate
- Z-axis mapping
- semantic pressure behavior
- Stress Test scoring
- Mirror Check scoring
- Evidence Lab calculations
- World Lens math
- receipts or telemetry

## Expected behavior
Mirror Check and Stress Test should render the same tree visuals as before, but the renderer now lives in `ui/components/tree_visuals.py`.

## Validation
Run:

```cmd
python -m py_compile app.py ui\components\tree_visuals.py ui\components\metric_cards.py ui\components\semantic_pressure_panel.py ui\components\review_cards.py
python -m pytest
python -m streamlit run app.py
```

Manual checks:
- Mirror Check → run one idea → Mirror Reading Tree renders.
- Stress Test → run one scenario → Stress Test Tree renders.
- Navigation containment remains stable: only one module body appears at a time.
