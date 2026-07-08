## Current patch

Patch 268 — Native Multipage Decision

## Status: READY FOR LOCAL REVIEW

Patch 268 records the native multipage decision after the controlled router, state-prep/state-extraction, and safe config extraction sequence.

Decision: keep the current controlled router for now.

Runtime behavior: no intended behavior change. No Streamlit native multipage migration is performed.

## Preserved

- `app.py` still imports and calls `render_controlled_router(...)` from `ui/main.py`.
- `ui/main.py` remains the canonical top-level router owner.
- no root `pages/` directory is added.
- navigation labels/order/default behavior are unchanged.
- `key="aletheia_active_module"` is unchanged.
- Receipt Reader remains under `Why ALETHEIA → Support utilities`.
- no scoring/taxonomy/Z-axis/receipt behavior changes.
- no state lifecycle changes.

## Active suite

Expected local check:

```bash
python -m pytest tests/active -q
python -m pytest -q
```

## Next patch boundary

Patch 269 should not start native multipage migration unless a separate migration prep patch first proves that the migration reduces complexity, preserves protocol framing, and protects session-state lifecycle with focused tests.

## Patch history

- Patch 255 — Patch Notes Final Cleanup
- Patch 256 — Legacy Test Quarantine / Import-Break Cleanup
- Patch 257 — Modularization Test Path Repair
- Patch 258 — Behavior Regression Review
- Patch 259 — App Shell Inventory / Thin Entrypoint Plan
- Patch 260 — App Shell Helper Extraction
- Patch 261 — Legacy Manifest Quarantine Completion
- Patch 262 — Routing Extraction Prep
- Patch 263 — Controlled Router Extraction
- Patch 264 — State Extraction Prep
- Patch 265 — State Extraction
- Patch 266 — Config Extraction Inventory
- Patch 267 — Safe Config Extraction
