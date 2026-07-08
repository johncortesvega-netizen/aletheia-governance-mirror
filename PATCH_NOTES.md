# ALETHEIA Patch Notes

## Current patch

### Patch 259 — App Shell Inventory / Thin Entrypoint Plan

Patch 259 documents what still lives in `app.py` after the modularization and
bridge-removal sequence.

It adds:

- `docs/app_shell_inventory_patch_259.md`
- `docs/thin_entrypoint_refactor_plan_patch_259.md`

The patch defines the safe next direction:

1. extract shell helpers first;
2. move routing to `ui/main.py` later;
3. extract shared session state only after routing is stable;
4. delay native Streamlit multipage until the controlled single-app shell is thin.

No runtime behavior changed.

## Recent architecture and cleanup sequence

- Patch 245 — Modularization Bridge Inventory
- Patch 246 — App-wide Copy Cleanup Pass
- Patch 247 — Mirror Check Bridge Removal
- Patch 248 — Stress Test Bridge Inventory / Prep
- Patch 249 — Stress Test Bridge Removal
- Patch 250 — Evidence Lab Bridge Removal
- Patch 251 — Evidence Lab `hashlib` Import Hotfix
- Patch 252 — World Lens Bridge Inventory / Prep
- Patch 253 — World Lens Bridge Removal
- Patch 254 — Modularization Final Audit
- Patch 255 — Patch Notes Final Cleanup
- Patch 256 — Legacy Test Quarantine / Import-Break Cleanup
- Patch 257 — Modularization Test Path Repair
- Patch 258 — Behavior Regression Review
- Patch 259 — App Shell Inventory / Thin Entrypoint Plan

## Runtime boundary

Patch 259 is documentation and refactor planning only. It does not change
governance logic, scanner behavior, scoring, receipts, World Lens math, Evidence
Lab calculations, telemetry, storage, navigation behavior, or the
mirror-not-throne boundary.
