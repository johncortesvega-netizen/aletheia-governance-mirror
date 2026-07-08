# Patch 238 Recovery Note

Patch 238 extracts Boundary Cases rendering into `ui/pages/boundary_cases.py`.

If Boundary Cases fails to open, restore the previous `app.py` and remove `ui/pages/boundary_cases.py`. No data schema or scoring migration is involved.

Validation:
```cmd
python -m py_compile app.py ui\pages\boundary_cases.py ui\pages\protocol_guide.py
python -m pytest
python -m streamlit run app.py
```

Manual UI check: open Boundary Cases, switch cases, open diagnostics expanders, and verify other modules still render one at a time.
