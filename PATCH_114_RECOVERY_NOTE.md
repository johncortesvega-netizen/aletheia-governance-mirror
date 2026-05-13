# Patch 114 Recovery Note — Public Release Polish v1

Patch 114 is documentation/release-surface polish. It does not change runtime behavior.

## Recovery

If this patch needs to be reverted, remove:

- `docs/public_release_polish_v1.md`
- `tests/test_patch_114_public_release_polish_v1.py`
- `PATCH_114_MANIFEST.txt`
- `PATCH_114_RECOVERY_NOTE.md`

Then restore the previous versions of:

- `README.md`
- `docs/public_release_notes.md`
- `docs/public_trust_package.md`
- `docs/patch_index.md`
- `docs/architecture.md`
- `examples/Trust_Package_README.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `data/protocol_baseline_manifest.json`

## Boundary

This patch does not alter `app.py`, runtime behavior, scanning, scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, downloads, storage, external calls, live model calls, telemetry, analytics, Global ID sync, public ledger sync, certification, enforcement, privacy guarantees, or final-truth behavior.

The public release polish is a clearer entry path, not an authority layer.

ALETHEIA remains a mirror. Humans keep the judgment.
