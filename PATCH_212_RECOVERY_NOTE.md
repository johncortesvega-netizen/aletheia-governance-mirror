# Patch 212 — Recovery Note

If this patch causes an issue, restore these files from the previous working tree or the last patch package:

- `core/semantic_pressure_scanner.py`
- `app.py`
- `ui/receipt_reader.py`
- `PATCH_STATUS.md`

Then rerun:

```bat
python -m py_compile app.py core\semantic_pressure_scanner.py ui\receipt_reader.py
python -m streamlit run app.py
```

Patch 212 is display/guidance only. It should not affect scoring, routing, receipts, World Lens math, Evidence Lab calculations, or Stress Test metrics.
