# Patch 221 Recovery Note — App Modularization Stage 1

Patch 221 moves shared Semantic Pressure UI helpers out of `app.py` into:

```text
ui/components/semantic_pressure_panel.py
```

## If the app fails to start

Check that this import block exists near the top of `app.py`:

```python
from ui.components.semantic_pressure_panel import (
    choose_stress_semantic_scan,
    choose_strongest_semantic_scan,
    render_semantic_evidence_check,
    render_semantic_pressure_panel,
    render_semantic_stress_triggers,
    render_world_lens_semantic_flags,
    semantic_evidence_implication_rows,
    semantic_stress_trigger_rows,
    semantic_world_lens_flag_rows,
)
```

Then run:

```bat
python -m py_compile app.py ui\components\semantic_pressure_panel.py
python -m pytest
```

## If semantic panels disappear

Restore the previous `app.py`, or verify that `ui/components/semantic_pressure_panel.py` was copied into the repository and that `ui/components/__init__.py` exists.

## Boundary note

This is a component extraction patch only. It should not change ALETHEIA readings, pressure codes, scoring, MEI7 routing, Z-axis behavior, receipts, Evidence Lab calculations, World Lens math, telemetry, storage, or authority boundaries.
