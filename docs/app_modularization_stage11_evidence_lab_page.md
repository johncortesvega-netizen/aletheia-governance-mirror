# App Modularization Stage 11 — Evidence Lab Page

Patch 243 moves the Evidence Lab page body from `app.py` into:

```text
ui/pages/evidence_lab.py
```

The extraction uses a temporary runtime namespace bridge:

```python
render_evidence_lab_page(globals())
```

This keeps the current behavior stable while reducing the size of `app.py`. Future stages may replace the bridge with explicit imports once dependencies are isolated.

## Boundary

This patch does not change Evidence Lab scoring, semantic scanning, empirical calculations, World Lens data sharing, receipts, MEI7, Z-axis, telemetry, or authority posture.
