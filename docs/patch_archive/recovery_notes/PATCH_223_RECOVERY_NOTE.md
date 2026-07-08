# Patch 223 Recovery Note — Modularization Stage 1 Missing Imports Hotfix

## Problem
After Patch 221/222, modules that rendered the shared semantic pressure panel could crash with:

```text
NameError: name 're' is not defined
```

The extracted module also used `hashlib.sha1(...)`, so both `re` and `hashlib` need to live inside the component module itself.

## Fix
Patch 223 adds the missing imports to:

```text
ui/components/semantic_pressure_panel.py
```

```python
import hashlib
import re
```

## Apply
Replace only:

```text
ui/components/semantic_pressure_panel.py
```

Then run:

```cmd
python -m py_compile app.py ui\components\semantic_pressure_panel.py
python -m pytest
python -m streamlit run app.py
```

## Boundary
This is an import hotfix only. It does not change app behavior, scoring, scanner logic, MEI7 gate, Z-axis, Evidence Lab, World Lens, receipts, or telemetry.
