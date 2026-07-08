# Patch 250 Recovery Note — Evidence Lab Bridge Removal

If Evidence Lab fails after applying this patch:

1. Confirm `app.py` imports both:

```python
from ui.pages.evidence_lab import evidence_lab_dependency_map, render_evidence_lab_page
```

2. Confirm the Evidence Lab call is:

```python
render_evidence_lab_page(evidence_lab_dependency_map(globals()))
```

3. Confirm `ui/pages/evidence_lab.py` contains:

```python
EVIDENCE_LAB_DEPENDENCIES = (...)
def evidence_lab_dependency_map(...): ...
def render_evidence_lab_page(deps): ...
```

4. Run:

```cmd
python -m py_compile app.py ui\pages\evidence_lab.py
python -m pytest
python -m streamlit run app.py
```

If a `RuntimeError` says the dependency map is incomplete, add the named missing dependency to `EVIDENCE_LAB_DEPENDENCIES` only if it already existed in the current app runtime and belongs to Evidence Lab behavior.

This patch should not alter Evidence Lab calculations, World Lens state sharing, scanner behavior, receipts, MEI7, Z-axis, or telemetry.
