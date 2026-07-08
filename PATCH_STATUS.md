## Current patch

Patch 266 — Config Extraction Inventory

## Status: READY FOR LOCAL REVIEW

Patch 266 maps app-level constants/static-data surfaces before any config extraction. It is a prep-only patch: no runtime constants are moved, no config modules are created, and scoring/taxonomy/allocation/receipt behavior remains untouched.

It adds active tests that protect the Patch 266 boundary:

- config extraction inventory exists;
- `ui/config.py`, `ui/constants.py`, `ui/examples.py`, and `ui/labels.py` are not created yet;
- behavior-sensitive constants still live in `app.py`;
- Patch 267 has a narrow safe-first boundary.

## Runtime behavior

No runtime behavior changes.

## Active suite

Expected local check:

```bash
python -m pytest tests/active -q
python -m pytest -q
```

## Next patch boundary

Patch 267 may perform a narrow safe config extraction. It should prefer static UI/demo surfaces first and must not move `TOTAL_9K`, demographic allocation data, World Bank aggregate filtering, review-band labels, missing-safeguard patterns, World Lens minimum grid thresholds, scoring/taxonomy/Z-axis logic, allocation logic, or receipt semantics.

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
