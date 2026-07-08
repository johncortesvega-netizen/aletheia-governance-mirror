# Patch 243 Recovery Note — Evidence Lab Page Extraction

If this patch fails, restore the previous `app.py` and remove `ui/pages/evidence_lab.py`.

Expected validation:

```cmd
python -m py_compile app.py ui\pages\evidence_lab.py
python -m pytest
python -m streamlit run app.py
```

Manual checks:
- Evidence Lab opens.
- Semantic claim/mechanism evidence check works.
- Synthetic demo works.
- CSV upload/synthetic table path still renders.
- Evidence Lab output tables, score cards, and Method note still render.
- World Lens still reads active Evidence Lab state.
- Navigation containment remains one module at a time.
