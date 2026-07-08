# ALETHEIA Patch Notes

## Current patch

### Patch 263 — Controlled Router Extraction

Patch 263 performs the runtime move prepared by Patch 262: the top-level controlled router is now owned by `ui/main.py`, while `app.py` remains the Streamlit entrypoint.

Added:

- `ui/main.py`
- `docs/controlled_router_extraction_patch_263.md`
- `docs/controlled_router_extraction_patch_263_summary.md`
- `PATCH_263_MANIFEST.txt`
- `PATCH_263_RECOVERY_NOTE.md`
- `PATCH_263_DELETE_LIST.txt`

Updated:

- `app.py` now delegates to `render_controlled_router(...)`.
- `tests/active/test_patch_262_routing_extraction_prep.py` now treats `ui/main.py` as the canonical router owner after Patch 263.
- `PATCH_STATUS.md` records Patch 263 as current.

Preserved:

- exact top-level navigation labels and order;
- `key="aletheia_active_module"`;
- Receipt Reader placement under Why ALETHEIA support utilities;
- controlled-router dispatch targets;
- app.py as the entrypoint.

Not changed:

- no Streamlit native multipage migration;
- no session-state extraction;
- no config/static-data extraction;
- no scanner/scoring/taxonomy/Z-axis/receipt behavior changes.

## Previous patch

### Patch 262 — Routing Extraction Prep

Patch 262 prepares the next architecture step without moving runtime code.

The current build already completed the app-shell inventory/extraction sequence in Patches 259–260 and the legacy manifest quarantine completion in Patch 261. Patch 262 therefore does not repeat inventory or shell work. Instead, it records the current `app.py` controlled-router contract so the next patch can extract routing deliberately.

Added:

- `docs/routing_extraction_prep_patch_262.md`
- `docs/routing_extraction_prep_patch_262_summary.md`
- `tests/active/test_patch_262_routing_extraction_prep.py`

The new active tests protect:

- exact top-level navigation labels and order;
- the `st.radio` selector contract;
- `key="aletheia_active_module"`;
- the Receipt Reader location hint and support-utility placement;
- the current dispatch targets for Mirror Check, Stress Test, Evidence Lab, World Lens, Boundary Cases, Protocol Guide, and Why ALETHEIA.

This is a no-runtime-move patch. It does not create `ui/main.py`, switch to native multipage, alter session-state defaults, move config/static values, or change scanner/scoring/taxonomy/Z-axis/receipt behavior.

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
- Patch 260 — App Shell Helper Extraction
- Patch 261 — Legacy Manifest Quarantine Completion
- Patch 262 — Routing Extraction Prep
- Patch 263 — Controlled Router Extraction
