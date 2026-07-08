# ALETHEIA Patch Notes

## Current patch

### Patch 261 — Legacy Manifest Quarantine Completion

Patch 261 completes a follow-up cleanup from Patch 256.

A later full-suite triage found 16 additional historical patch-contract tests that still expected old root-level `PATCH_N_*` artifacts. Patch 255 intentionally moved old patch artifacts to `docs/patch_archive/`, so these tests were checking a superseded documentation layout rather than runtime behavior.

Patch 261 adds those 16 tests to `PATCH_ARTIFACT_ROOT_CONTRACT_QUARANTINE` in `tests/conftest.py`.

The tests remain on disk for audit continuity. They can later be restored by rewriting them to inspect the patch archive rather than repository root.

Patch 261 also adds `docs/refactor_pause_roadmap_patch_261.md` for the next chat. Routing extraction, session-state extraction, and config extraction remain on hold.

This is test-governance cleanup only. It does not alter scanner behavior, scoring, MEI7, Z-axis, receipts, Evidence Lab calculations, World Lens math, navigation, telemetry/storage, or authority-boundary behavior.

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
