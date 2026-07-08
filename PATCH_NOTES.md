# Patch 257 — Modularization Test Path Repair

Patch 257 adds `tests/active/test_modularization_current_paths.py`, an active
release-gate contract for the new modularized layout. It replaces stale
historical assumptions that page/component strings must still live directly in
`app.py`.

The new test checks extracted page modules, shared component modules, dependency
map usage, app orchestration imports/calls, and absence of the broad direct
`render_*_page(globals())` calls for the core pages.

No runtime logic changed.

# ALETHEIA Patch Notes

## Current patch

### Patch 256 — Legacy Test Quarantine / Import-Break Cleanup

Patch 256 performs the first concrete legacy-test cleanup step after the active-suite split, modularization sequence, and Patch 255 patch-archive cleanup.

It adds `tests/conftest.py` with explicit `collect_ignore` quarantine entries for:

- two historical test files with imports to helpers that no longer exist in the current codebase;
- historical patch-contract files that still expect old root-level `PATCH_N_*` artifacts after those artifacts were intentionally archived under `docs/patch_archive/`.

The quarantined files are retained on disk for audit continuity. This patch does not rewrite them as passing tests and does not claim they validate the current release surface.

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

## Runtime boundary

Patch 256 is test-collection and documentation hygiene only. It does not change governance logic, scanner behavior, scoring, receipts, World Lens math, Evidence Lab calculations, telemetry, storage, or the mirror-not-throne boundary.
