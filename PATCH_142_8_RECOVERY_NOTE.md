# Patch 142.8 Recovery Note — Receipt Reader World Lens Evidence Bundle Reader

If Patch 142.8 causes a Receipt Reader regression, revert these files:

- `ui/receipt_reader.py`
- `tests/test_patch_142_8_world_lens_evidence_bundle_reader.py`
- `PATCH_142_8_MANIFEST.txt`
- `PATCH_142_8_RECOVERY_NOTE.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `docs/patch_index.md`
- `data/protocol_baseline_manifest.json`

Expected restored behavior after reverting: World Lens ZIP uploads return to the previous generic batch ZIP rendering. Patch 142.8 does not alter World Lens math, receipt generation, scoring, routing, taxonomy, AI Integrity behavior, Privacy Audit behavior, Stress Test scoring behavior, telemetry, storage, external calls, or authority boundaries.

Human review remains required for any release decision.
