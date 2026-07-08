# PATCH 231 RECOVERY NOTE

If Patch 231 causes UI issues, restore the previous `app.py` from Patch 230 and remove `ui/components/review_cards.py`.

Expected checks:

```cmd
python -m py_compile app.py ui\components\semantic_pressure_panel.py ui\components\metric_cards.py ui\components\review_cards.py
python -m pytest
python -m streamlit run app.py
```

Expected UI behavior:
- Stress Test "Why this result?" cards render normally.
- Stress Test repair questions render normally.
- No module renders inactive content from another module.
- No governance scores or labels change due to this patch.
