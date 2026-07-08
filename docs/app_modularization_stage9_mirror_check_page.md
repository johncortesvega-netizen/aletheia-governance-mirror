# Patch 239 — App Modularization Stage 9: Mirror Check Page

## Purpose

This patch extracts the Mirror Check page body from `app.py` into `ui/pages/mirror_check.py`.

## Files

- `app.py`
- `ui/pages/mirror_check.py`

## Boundary

This is a page-location refactor only. It does not change:

- governance scanner logic;
- semantic pressure scanner behavior;
- MEI7 ethics gate behavior;
- Z-axis repair-zone mapping;
- Mirror Check scoring;
- Stress Test metrics;
- Evidence Lab calculations;
- World Lens math;
- receipt schema or witness generation;
- telemetry, storage, or authority boundaries.

## Implementation note

Stage 9 uses a runtime-namespace bridge so Mirror Check can be moved out of `app.py` without changing all upstream dependencies at once. This is deliberate: it preserves behavior first, then allows later cleanup of explicit imports when the remaining modules are extracted.

## Manual checks

Run:

```cmd
python -m py_compile app.py ui\pages\mirror_check.py
python -m pytest
python -m streamlit run app.py
```

Then check:

- Mirror Check opens.
- Review idea works.
- Mirror Reading Tree renders.
- Semantic pressure panel renders.
- Batch testing expander opens.
- Support utilities remain visible.
- Other top-level modules still render one at a time.
