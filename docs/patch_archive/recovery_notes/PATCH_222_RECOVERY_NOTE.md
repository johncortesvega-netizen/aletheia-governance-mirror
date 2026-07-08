# Patch 222 Recovery Note — Modularization Stage 1 Import Hotfix

## Symptom
After applying Patch 221 Stage 1, Streamlit may fail on startup with:

```text
NameError: name 'render_sydney_protocol_self_check_gate' is not defined
```

Trace points to:

```text
ui/components/semantic_pressure_panel.py
```

## Cause
A leftover top-level call to `render_sydney_protocol_self_check_gate()` was copied into the extracted semantic component. That function still belongs to `app.py`, and should not be executed during component import.

## Fix
Patch 222 removes the stray top-level call from:

```text
ui/components/semantic_pressure_panel.py
```

## Apply
Copy the patched file over the existing file:

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
No scoring, scanner, routing, MEI7, Z-axis, Evidence Lab, World Lens, receipt, telemetry, or authority behavior changes.
