# Patch 268 — Native Multipage Decision

Status: READY FOR LOCAL REVIEW

Patch 268 is a decision-only patch. It documents the decision to keep the current controlled router for now and defer Streamlit native multipage migration.

Added:

- `docs/native_multipage_decision_patch_268.md`
- `docs/native_multipage_decision_patch_268_summary.md`
- `tests/active/test_patch_268_native_multipage_decision.py`
- `PATCH_268_MANIFEST.txt`
- `PATCH_268_RECOVERY_NOTE.md`
- `PATCH_268_DELETE_LIST.txt`

Preserved:

- no runtime file changes;
- No root `pages/` directory is added.;
- `ui/main.py` remains the controlled router owner;
- `app.py` still delegates to `render_controlled_router(...)`;
- navigation labels/order/default behavior remain unchanged;
- Receipt Reader remains under `Why ALETHEIA → Support utilities`;
- no scoring, taxonomy, Z-axis, receipt, state, Evidence Lab, World Lens, Mirror Check, or Stress Test behavior changes.

Decision:

- Keep controlled router for now.
- Reconsider native multipage or hybrid only after a separate prep patch proves lower complexity, preserved framing, and protected state lifecycle.

Tests expected:

```bash
python -m pytest tests/active -q
python -m pytest -q
```

---

# Patch 267 — Safe Config Extraction

Status: READY FOR LOCAL REVIEW

Patch 267 performs the first narrow config/static-data extraction prepared by Patch 266. It adds canonical static owners for low-risk UI/demo values and updates `app.py` to import them without changing runtime behavior.

Added:

- `ui/config.py`
- `ui/examples.py`
- `docs/config_extraction_patch_267.md`
- `docs/config_extraction_patch_267_summary.md`
- `tests/active/test_patch_267_safe_config_extraction.py`
- `PATCH_267_MANIFEST.txt`
- `PATCH_267_RECOVERY_NOTE.md`
- `PATCH_267_DELETE_LIST.txt`

Updated:

- `app.py` now imports `APP_VERSION` and `SUPPORTED_INPUT_LANGUAGE_NOTE` from `ui.config`.
- `app.py` now imports `APP_UX_POLISH_SUMMARY` and `DEMO_INPUT_FILES` from `ui.examples`.
- Patch 266 active test was adjusted so it remains a historical inventory contract after Patch 267 creates the config/example modules.

Preserved:

- no scoring/taxonomy/Z-axis movement;
- no allocation constant movement;
- no receipt-semantics movement;
- no navigation-label movement;
- no demo-scenario movement;
- `load_demo_input()` behavior remains in `app.py`.

Tests expected:

```bash
python -m pytest tests/active -q
python -m pytest -q
```

---

# Patch 266 — Config Extraction Inventory

Status: READY FOR LOCAL REVIEW

Patch 266 is a prep-only inventory patch for future config/static-data extraction. It adds docs and active tests that classify safe static candidates versus behavior-sensitive constants. No runtime constants are moved and no `ui/config.py`, `ui/constants.py`, `ui/examples.py`, or `ui/labels.py` module is created yet.

Added:

- `docs/config_extraction_inventory_patch_266.md`
- `docs/config_extraction_inventory_patch_266_summary.md`
- `tests/active/test_patch_266_config_extraction_inventory.py`
- `PATCH_266_MANIFEST.txt`
- `PATCH_266_RECOVERY_NOTE.md`
- `PATCH_266_DELETE_LIST.txt`

Boundary:

- Safe-first future candidates: `APP_VERSION`, `SUPPORTED_INPUT_LANGUAGE_NOTE`, `APP_UX_POLISH_SUMMARY`, `DEMO_INPUT_FILES`, and possibly demo scenario maps with exact-content tests.
- Out of scope for Patch 267: `TOTAL_9K`, `DEMOGRAPHIC_BRACKETS`, `WORLD_BANK_AGGREGATE_ISO3`, `REVIEW_BAND_LABELS`, `MISSING_SAFEGUARD_NEGATION_PATTERNS`, `MIN_FULL_GRID_COUNTRIES`, scoring/taxonomy/Z-axis thresholds, allocation logic, and receipt semantics.

Tests expected:

```bash
python -m pytest tests/active -q
python -m pytest -q
```

---

# ALETHEIA Patch Notes

## Current patch

### Patch 264 — State Extraction Prep

Patch 264 prepares the future state extraction without moving runtime code. It maps the current Streamlit `st.session_state` ownership surface and records key names, owners, lifecycles, and extraction risk.

Added:

- `docs/state_extraction_prep_patch_264.md`
- `docs/state_extraction_prep_patch_264_summary.md`
- `tests/active/test_patch_264_state_extraction_prep.py`
- `PATCH_264_MANIFEST.txt`
- `PATCH_264_RECOVERY_NOTE.md`
- `PATCH_264_DELETE_LIST.txt`

Preserved:

- no `ui/state.py` yet;
- no runtime state movement;
- no state key renames;
- no default/lifecycle changes;
- router key `aletheia_active_module` remains owned by `ui/main.py`;
- sidebar defaults/reset behavior remains in `app.py`;
- Evidence Lab, World Lens, Mirror Check, Stress Test, Unit Preview, and Sydney Protocol self-check state remain in current owners.

Next patch guidance:

- Patch 265 may create `ui/state.py`;
- first extraction should be narrow, preferably sidebar defaults/reset helpers;
- do not move Evidence/World Lens sync state, dataframe caches, batch state, Unit Preview, router selection, or Sydney Protocol self-check caching without separate focused tests.


### Patch 265 — State Extraction

Patch 265 performs the first narrow runtime state extraction prepared by Patch 264. It creates `ui/state.py` and moves only the sidebar review-lens normalization/reset defaults out of `app.py`.

Added:

- `ui/state.py`
- `docs/state_extraction_patch_265.md`
- `docs/state_extraction_patch_265_summary.md`
- `tests/active/test_patch_265_state_extraction.py`
- `PATCH_265_MANIFEST.txt`
- `PATCH_265_RECOVERY_NOTE.md`
- `PATCH_265_DELETE_LIST.txt`

Updated:

- `app.py` delegates the legacy sidebar profile normalization to `normalize_sidebar_lens_state(st.session_state)`.
- `app.py` delegates the Reset lens state mutation to `reset_sidebar_lens_state(st.session_state)`.
- Patch 264 tests now recognize `ui/state.py` as the canonical owner of the moved sidebar reset defaults.
- `PATCH_STATUS.md` records Patch 265 as current.

Preserved:

- exact sidebar widget keys;
- exact sidebar default values;
- legacy `Default` → `Starting preset` normalization;
- controlled-router ownership in `ui/main.py`;
- app.py as Streamlit entrypoint.

Not changed:

- no router/session key rename;
- no Unit Preview or Sydney Protocol self-check state movement;
- no shared `protocol_state` extraction;
- no Evidence Lab/World Lens/Mirror Check/Stress Test state movement;
- no scanner/scoring/taxonomy/Z-axis/receipt behavior changes.

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
