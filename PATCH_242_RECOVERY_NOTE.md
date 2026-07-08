# Patch 242 Recovery Note — Stress Test Page Extraction

If Stress Test fails after applying this patch:

1. Confirm `ui/pages/stress_test.py` exists.
2. Confirm `app.py` imports:

```python
from ui.pages.stress_test import render_stress_test_page
```

3. Confirm the Stress Test navigation branch calls:

```python
render_stress_test_page(globals())
```

4. Run:

```cmd
python -m py_compile app.py ui\pages\stress_test.py
python -m pytest
python -m streamlit run app.py
```

If there is a missing-name error, the namespace bridge may be missing a helper due to local patch drift. Restore the previous `app.py` or re-apply Patch 242 over the current committed state.

This patch does not intentionally modify scoring, scanner behavior, receipts, Evidence Lab, World Lens, or authority boundaries.
