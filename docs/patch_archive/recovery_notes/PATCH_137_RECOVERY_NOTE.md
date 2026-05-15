# Patch 137 Recovery Note - Validation Alignment After Unit Preview

Patch 137 only updates validation and documentation after the Unit Preview sequence.

## Recovery

If Patch 137 causes a problem, revert these files:

- `tests/test_patch_131_start_page_gate.py`
- `tests/test_patch_131_test_check_hygiene.py`
- `tests/test_patch_132_start_page_stabilization_checkpoint.py`
- `docs/validation_alignment_after_unit_preview.md`
- `tests/test_patch_137_validation_alignment_after_unit_preview.py`
- `PATCH_137_MANIFEST.txt`
- `PATCH_137_RECOVERY_NOTE.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `docs/patch_index.md`
- `docs/architecture.md`
- `README.md`
- `data/protocol_baseline_manifest.json`

## Boundary

Patch 137 does not change app runtime behavior. It does not change scoring, verdict routing, taxonomy, receipt schemas, receipt generation, signal regexes, signal weights, AI Integrity scan behavior, Privacy Audit scan behavior, World Lens math, uploads, downloads, batch behavior, external calls, telemetry, analytics, storage, identity sync, certification, enforcement, privacy guarantees, or final-truth behavior.

Humans keep the judgment.
