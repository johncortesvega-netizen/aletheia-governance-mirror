# Patch 249 Recovery Note — Stress Test Bridge Removal

If Stress Test fails to open after this patch, check the traceback for:

```text
Stress Test page dependency map is incomplete
```

If that appears, add the missing dependency name to `STRESS_TEST_DEPENDENCIES`
only if the page actually still uses it.

Rollback path:

1. Restore the previous `app.py` call:

```python
render_stress_test_page(globals())
```

2. Restore the previous `ui/pages/stress_test.py` header that accepted the full runtime namespace.

Expected checks:

```cmd
python -m py_compile app.py ui\pages\stress_test.py
python -m pytest
python -m streamlit run app.py
```
