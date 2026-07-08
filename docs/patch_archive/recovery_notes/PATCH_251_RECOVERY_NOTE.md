# Patch 251 — Evidence Lab Bridge Removal Import Hotfix

## Issue
After Patch 250, Streamlit Cloud reported:

```text
NameError: name 'hashlib' is not defined
```

The error occurred in `ui/pages/evidence_lab.py` when `_empirical_active_input_signature(...)` called `hashlib.sha256()`.

## Cause
During Evidence Lab page extraction, the helper moved out of `app.py`, where `hashlib` was available indirectly through the root module context. The new page file needed an explicit import.

## Fix
Added:

```python
import hashlib
```

to `ui/pages/evidence_lab.py`.

## Recovery
Replace only:

```text
ui/pages/evidence_lab.py
```

Then run:

```cmd
python -m py_compile app.py ui\pages\evidence_lab.py
python -m pytest
python -m streamlit run app.py
```

For Streamlit Cloud, commit/push the changed file and reboot the app.

## Boundary
This patch does not change governance logic, scanner behavior, scoring, MEI7, Z-axis, Evidence Lab calculations, World Lens math, receipt behavior, telemetry, or authority-boundary behavior.
