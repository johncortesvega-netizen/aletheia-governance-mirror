# ALETHEIA Patch Notes

## Current patch

### Patch 255 — Patch Notes Final Cleanup

Patch 255 performs the final patch-note hygiene pass after the modularization and bridge-removal sequence.

It preserves the patch audit trail while keeping the repository root clean:

- current patch artifacts stay in root;
- older patch manifests move to `docs/patch_archive/manifests/`;
- older recovery notes move to `docs/patch_archive/recovery_notes/`;
- older delete lists move to `docs/patch_archive/delete_lists/`.

No runtime behavior changed.

## Recent architecture sequence

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

## Current architecture summary

The app has moved from one large Streamlit orchestrator toward a modular page/component structure:

- shared UI blocks are in `ui/components/`;
- major pages are in `ui/pages/`;
- broad page-level `globals()` handoffs have been replaced with dependency maps;
- patch artifacts are archived instead of cluttering root.

## Runtime boundary

Patch 255 is documentation and repository hygiene only. It does not change governance logic, scanner behavior, scoring, receipts, World Lens math, Evidence Lab calculations, telemetry, storage, or the mirror-not-throne boundary.
