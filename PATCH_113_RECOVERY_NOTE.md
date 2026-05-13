# Patch 113 Recovery Note — Public Trust Package Consolidation

Patch 113 is a documentation/navigation consolidation patch. It does not change runtime behavior.

## Recovery

If this patch needs to be reverted, remove:

- `docs/public_review_checklist.md`
- `tests/test_patch_113_public_trust_package_consolidation.py`
- `PATCH_113_MANIFEST.txt`
- `PATCH_113_RECOVERY_NOTE.md`

Then restore the previous versions of:

- `README.md`
- `docs/architecture.md`
- `docs/patch_index.md`
- `docs/public_trust_package.md`
- `examples/Trust_Package_README.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `data/protocol_baseline_manifest.json`

## Boundary

This patch does not alter `app.py`, runtime behavior, scanning, scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, downloads, storage, external calls, live model calls, telemetry, analytics, Global ID sync, public ledger sync, compliance approval, certification, enforcement, privacy guarantees, or final-truth behavior.

The public trust package remains a review map, not an authority layer.

ALETHEIA remains a mirror. Humans keep the judgment.
