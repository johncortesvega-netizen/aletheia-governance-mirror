# Patch 141.2 Recovery Note — Unit Preview Reference Placement Hotfix

If this patch needs to be reverted, restore `ui/unit_preview.py`, `tests/test_patch_141_v1_ui_receipt_upload_cleanup.py`, `tests/test_patch_141_2_unit_preview_reference_placement_hotfix.py`, `PATCH_STATUS.md`, `docs/progress_database.md`, `docs/patch_index.md`, `docs/architecture.md`, and `data/protocol_baseline_manifest.json` from the prior Patch 141.1 state.

This hotfix only changes Unit Preview placement: packaged local reference previews now render under the Unit Preview prompt on the first app page. The previews remain local packaged HTML, stay outside the full module app, and fail gracefully when files are missing.

No scoring, routing, taxonomy, receipt schema, receipt generation, signal, AI Integrity, Privacy Audit, World Lens, upload/download, storage, telemetry, external-call, or authority behavior is changed.
