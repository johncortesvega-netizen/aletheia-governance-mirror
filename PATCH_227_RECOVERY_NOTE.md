# Patch 227 Recovery Note — Metric Card Component Extraction

If the app fails after applying this patch, restore the previous `app.py` and remove
`ui/components/metric_cards.py`.

Likely failure mode:
- `ModuleNotFoundError: No module named 'ui.components.metric_cards'`

Fix:
- Ensure `ui/components/metric_cards.py` exists.
- Ensure `ui/components/__init__.py` exists.
- Ensure `app.py` imports:

```python
from ui.components.metric_cards import metric_card, soft_card
```

Validation:

```cmd
python -m py_compile app.py ui\components\semantic_pressure_panel.py ui\components\metric_cards.py
python -m pytest
python -m streamlit run app.py
```

Manual validation:
- Stress Test metric cards render.
- World Lens metric/status cards render.
- No module renders outside the active navigation selection.
