# Patch 263 — Controlled Router Extraction

## Goal

Move the top-level ALETHEIA controlled router out of `app.py` without changing navigation behavior, page order, default state key, Receipt Reader placement, scoring, taxonomy, session-state defaults, or UI meaning.

## Runtime change

Patch 263 creates `ui/main.py` and introduces:

```python
render_controlled_router(...)
```

`app.py` remains the Streamlit entrypoint, but now delegates selected-page resolution and dispatch to `ui.main.render_controlled_router`.

## Moved from `app.py` into `ui/main.py`

- `st.radio("ALETHEIA module", ...)` selected-module resolution.
- `key="aletheia_active_module"` top-level module state key usage.
- Receipt Reader location caption.
- Conditional dispatch for:
  - Mirror Check;
  - Stress Test;
  - Evidence Lab;
  - World Lens;
  - Boundary Cases;
  - Protocol Guide;
  - Why ALETHEIA;
  - Receipt Reader — Standard View as a support utility under Why ALETHEIA.

## Explicitly not changed

- No Streamlit native multipage migration.
- No session-state extraction.
- No config/static-data extraction.
- No page rename, page reorder, or default module change.
- No scanner, scoring, taxonomy, Z-axis, receipt parsing, Evidence Lab, World Lens, or protocol behavior change.
- No routing behavior switch from the controlled router to automatic page discovery.

## Acceptance contract

- `app.py` still runs as the entrypoint.
- `APP_NAVIGATION_LABELS` stays in the same order.
- Receipt Reader remains under `Why ALETHEIA → Support utilities → Receipt Reader — Standard View`.
- `key="aletheia_active_module"` is preserved.
- Active tests target `ui/main.py` as the canonical router owner.

## Next patch boundary

Patch 264 should be a state-extraction prep patch only: map session-state keys/defaults/lifecycle before moving any state helpers.
