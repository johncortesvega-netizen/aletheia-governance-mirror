# Patch 107 Recovery Note — Boundary and Privacy UI Wiring

Patch 107 is a narrow runtime UI wiring patch.

## What changed

- `app.py` imports `render_boundary_statement` from `core.boundary`.
- `app.py` imports `render_privacy_panel` from `core.privacy_panel`.
- The Streamlit sidebar renders the existing privacy/local-first expander and compact boundary footer.

## What did not change

- No scoring change.
- No verdict-routing change.
- No signal-pattern or signal-weight change.
- No receipt schema change.
- No external calls or live model calls.
- No telemetry, analytics, backend upload endpoint, central storage, Global ID sync, or public ledger sync.
- No certification, enforcement, privacy guarantee, security guarantee, or final-truth claim.

## Rollback

To roll back Patch 107, remove the two helper imports from `app.py` and remove the two sidebar calls:

```python
render_privacy_panel(st, expanded=False)
render_boundary_statement("footer", st)
```

The helper modules and documentation from earlier patches can remain in place.

Human review remains required.
