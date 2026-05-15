# Patch 108 Recovery Note — App Shell Router Refactor Step 1

Patch 108 begins the gradual `app.py` router/shell refactor by extracting static top-of-app boundary notices into `ui/app_shell.py`.

## What changed

- Added `ui/__init__.py`.
- Added `ui/app_shell.py` with `render_app_boundary_notices(...)`.
- Updated `app.py` to import and call the helper instead of rendering those three notices inline.

## What did not change

- No scoring change.
- No verdict-routing change.
- No signal-pattern or signal-weight change.
- No receipt schema change.
- No external calls or live model calls.
- No telemetry, analytics, backend upload endpoint, central storage, Global ID sync, or public ledger sync.
- No certification, enforcement, privacy guarantee, security guarantee, or final-truth claim.

## Rollback

To roll back Patch 108, remove the import:

```python
from ui.app_shell import render_app_boundary_notices
```

Then replace this call:

```python
render_app_boundary_notices(SUPPORTED_INPUT_LANGUAGE_NOTE, st)
```

with the three previous inline `st.markdown(...)` top-of-app boundary notices from the Patch 107 version of `app.py`.

Human review remains required.
