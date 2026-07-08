# Patch 229 — Threshold Metric Readability Follow-up

Patch 229 is a presentation-only follow-up to the Stage 2 metric-card modularization.

## Purpose

Patch 228 stabilized the extracted metric-card helper, but one Mirror Check panel still used native `st.metric` in a narrow four-column layout. Long values such as threshold-direction labels and Z-axis text were truncated into unreadable ellipses.

Patch 229 replaces that specific four-column native metric row with a readable dataframe summary and adds defensive CSS for native Streamlit metric labels/values.

## Scope

Changed:
- Mirror Check threshold-direction review presentation.
- Defensive CSS for native `st.metric` label/value wrapping.

Not changed:
- scanner logic
- semantic pressure scanner
- scoring
- MEI7 gate
- Z-axis calculations
- Stress Test math
- Evidence Lab calculations
- World Lens math
- receipts
- telemetry
- authority/boundary behavior

## Validation

Run:

```cmd
python -m py_compile app.py ui\components\metric_cards.py ui\components\semantic_pressure_panel.py
python -m pytest
python -m streamlit run app.py
```

Then inspect:
- Mirror Check → How to read this Mirror Check output → Threshold direction review.

Expected:
- No tiny unreadable metric cards.
- Threshold direction, Z-axis, repair questions, and confirmed repair appear as readable rows.
