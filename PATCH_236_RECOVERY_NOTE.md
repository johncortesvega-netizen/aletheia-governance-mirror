# PATCH 236 RECOVERY NOTE

If Protocol Guide fails to render after this patch:

1. Confirm `ui/pages/protocol_guide.py` exists.
2. Confirm `ui/pages/__init__.py` exists.
3. Confirm `app.py` imports:

```python
from ui.pages.protocol_guide import render_protocol_guide_page
```

4. Confirm the Protocol Guide branch calls:

```python
render_protocol_guide_page()
```

5. Run:

```cmd
python -m py_compile app.py ui\pages\protocol_guide.py
python -m streamlit run app.py
```

Rollback:
- Restore the pre-Patch-236 `app.py` and remove `ui/pages/protocol_guide.py` if necessary.

Boundary:
- This patch is page extraction only. It does not modify scoring, scanner logic, receipts, MEI7, Z-axis, Evidence Lab, World Lens, or Stress Test behavior.
