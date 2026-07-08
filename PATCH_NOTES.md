# ALETHEIA Patch Notes

## Current patch

### Patch 260 — App Shell Helper Extraction

Patch 260 is the first implementation step after the Patch 259 app-shell
inventory.

It moves the global Streamlit page setup and large CSS theme block out of
`app.py` and into `ui/app_shell.py`:

- `ALETHEIA_GLOBAL_CSS`
- `apply_app_page_config_and_theme(st)`

`app.py` now calls the helper instead of carrying the full inline setup block.

This is a shell extraction only. It does not alter scanner behavior, scoring,
MEI7, Z-axis, receipts, Evidence Lab calculations, World Lens math, navigation,
telemetry/storage, or authority-boundary behavior.

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
