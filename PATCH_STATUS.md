# ALETHEIA Patch Status

## Current patch

Patch 263 — Controlled Router Extraction

Status: READY FOR LOCAL REVIEW

Patch 263 moves the top-level controlled router out of `app.py` and into `ui/main.py` while preserving current navigation behavior.

It creates `ui.main.render_controlled_router(...)` and keeps `app.py` as the Streamlit entrypoint. The router now owns:

- selected-module resolution through the existing `st.radio("ALETHEIA module", ...)` selector;
- `key="aletheia_active_module"`;
- Receipt Reader location caption;
- conditional dispatch for Mirror Check, Stress Test, Evidence Lab, World Lens, Boundary Cases, Protocol Guide, and Why ALETHEIA;
- Receipt Reader — Standard View under Why ALETHEIA support utilities.

Validation target:

```bat
python -m pytest tests\active -q
python -m pytest -q
```

Boundary preserved: no scanner, scoring, MEI7, Z-axis, receipt parsing, Evidence Lab, World Lens, session-state default, telemetry/storage, native multipage, config/static-data, or authority-boundary behavior is changed.

## Hold note

Patch 263 is a controlled-router extraction patch only.

Still paused until separate patches:

- session-state extraction;
- config/demo-data extraction;
- Streamlit native multipage migration.

Patch 264 should be a state-extraction prep patch: map session-state keys/defaults/lifecycle before moving state helpers.

## Recent sequence

- Patch 255 — Patch Notes Final Cleanup
- Patch 256 — Legacy Test Quarantine / Import-Break Cleanup
- Patch 257 — Modularization Test Path Repair
- Patch 258 — Behavior Regression Review
- Patch 259 — App Shell Inventory / Thin Entrypoint Plan
- Patch 260 — App Shell Helper Extraction
- Patch 261 — Legacy Manifest Quarantine Completion
- Patch 262 — Routing Extraction Prep
- Patch 263 — Controlled Router Extraction
