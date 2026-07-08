# Patch 242 — App Modularization Stage 10: Stress Test Page

## Purpose

This patch extracts the Stress Test page body from `app.py` into `ui/pages/stress_test.py` while preserving the existing behavior and state keys.

## What changed

- Added `ui/pages/stress_test.py`.
- Moved the Stress Test page rendering body into `render_stress_test_page(runtime_namespace)`.
- Updated `app.py` to import and call `render_stress_test_page(globals())` when the Stress Test module is selected.

## Why a namespace bridge is used

Stress Test currently depends on many shared helpers, constants, session-state keys, demo scenarios, receipt utilities, and visual components. A namespace bridge keeps this patch behavior-preserving and avoids a large dependency refactor in the same step.

Later stages may replace the bridge with explicit imports and narrower dependency injection.

## Boundary

This is a UI modularization patch only. It does not change:

- scenario scoring;
- Semantic Pressure Scanner behavior;
- MEI7 ethics gate behavior;
- Z-axis mapping;
- Stress Test metrics;
- batch testing;
- local witness receipt generation;
- Evidence Lab calculations;
- World Lens math;
- telemetry or storage posture;
- authority or certification boundaries.

## Manual checks

After applying:

```cmd
python -m py_compile app.py ui\pages\stress_test.py
python -m pytest
python -m streamlit run app.py
```

Then verify:

- Stress Test opens.
- Demo scenarios load.
- Manual test sliders still work.
- Run review works.
- Stress Test Tree renders.
- Batch testing expander opens.
- Semantic pressure signals render.
- Local witness receipt expander/download still works.
- Other modules remain one-at-a-time under navigation containment.
