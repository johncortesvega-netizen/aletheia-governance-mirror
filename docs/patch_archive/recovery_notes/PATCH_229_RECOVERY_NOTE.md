# Patch 229 Recovery Note — Threshold Metric Readability Follow-up

If the Mirror Check threshold-direction review displays tiny truncated values such as `To...`, `0.1...`, or `1....`, apply this patch.

## Apply

Copy these files into the repo:

- `app.py`
- `docs/app_modularization_stage2_metric_readability_followup.md`
- patch status/manifest files if maintaining the patch archive

## Validate

```cmd
python -m py_compile app.py ui\components\metric_cards.py ui\components\semantic_pressure_panel.py
python -m pytest
python -m streamlit run app.py
```

Open:

Mirror Check → How to read this Mirror Check output → Threshold direction review

Expected result:

- The four threshold/Z-axis values are shown in a readable summary table.
- No governance behavior changes.
