# Patch 230 Recovery Note

If the Stress Test protocol-reading card shows raw `<span ...>` HTML, ensure both files from this patch were applied:

- `ui/components/metric_cards.py`
- `app.py`

Then run:

```cmd
python -m py_compile app.py ui\components\metric_cards.py ui\components\semantic_pressure_panel.py
python -m pytest
python -m streamlit run app.py
```

Expected result: the protocol-reading card renders colored/line-broken text rather than visible HTML tags.
