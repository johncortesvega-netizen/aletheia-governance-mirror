# Patch 227 — App Modularization Stage 2: Metric Cards

## Purpose

Stage 2 continues the app modularization effort with a small, low-risk extraction.
It moves the shared metric/status card presentation helpers out of `app.py` and into
`ui/components/metric_cards.py`.

## What moved

- `metric_card(...)`
- `soft_card(...)`

These functions are presentation helpers only. They render HTML cards from values
that have already been computed elsewhere. They do not calculate scores, change
routing, classify readings, alter semantic pressure results, or modify receipts.

## Why this slice

Metric cards are reused in the Stress Test and World Lens result surfaces, but the
helpers do not contain domain logic. That makes them a safe second modularization
slice after the semantic pressure panel extraction.

## Boundary

This patch does not change:

- scanner logic;
- scoring formulas;
- MEI7 Ethics Gate behavior;
- Z-axis mapping;
- Stress Test metrics;
- Evidence Lab calculations;
- World Lens math;
- receipt creation or parsing;
- telemetry, storage, or authority behavior.

## Test commands

```cmd
python -m py_compile app.py ui\components\semantic_pressure_panel.py ui\components\metric_cards.py
python -m pytest
python -m streamlit run app.py
```

## Manual checks

- Mirror Check opens.
- Stress Test result metric cards render.
- World Lens result cards render.
- No duplicate module rendering appears.
- No import errors occur.
