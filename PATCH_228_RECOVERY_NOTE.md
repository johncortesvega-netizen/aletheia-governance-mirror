# Patch 228 Recovery Note — Metric Card Layout Stabilization

If Patch 228 causes unexpected UI issues, revert these files only:

- `app.py`
- `ui/components/metric_cards.py`

This patch only changes layout behavior for modularized metric/soft cards. It does not change scoring, scanner logic, semantic pressure behavior, receipts, World Lens calculations, Evidence Lab calculations, or navigation routing.

## Validation commands

```cmd
python -m py_compile app.py ui\components\metric_cards.py ui\components\semantic_pressure_panel.py
python -m pytest
python -m streamlit run app.py
```

## Manual checks

- Mirror Check opens and result cards wrap normally.
- Stress Test status card is no longer extremely narrow.
- Stress Test metric cards remain aligned.
- World Lens metric/status cards still render.
- Only one top-level module body is visible at a time.
