# Patch 184 Recovery Note — Current and Spark Theory Update

Patch 184 is a content/documentation patch for the Artificial Mind Formation Theory section.

## What changed

- `pages_ui/artificial_mind_formation_page.py` now uses the Current and Spark framing:
  - AI is current, not creature.
  - AI is real in effect, not alive in essence.
  - Impact is evidence, not proof of soul.
  - The current must be stewarded, not worshiped.
- `docs/artificial_mind_formation_theory.md` was aligned with the same wording.
- `tests/test_patch_184_current_and_spark_theory_update.py` verifies the new theory anchors and the preserved no-authority boundary.

## What did not change

This patch does not change scoring, routing, taxonomy, receipt generation, receipt values, batch behavior, Evidence Lab calculations, World Lens math, AI static scan logic, protocol-engine logic, storage, certification, enforcement, or authority behavior.

## Recovery

To revert this patch, restore these files from the previous working tree:

- `pages_ui/artificial_mind_formation_page.py`
- `docs/artificial_mind_formation_theory.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `docs/patch_archive/root_patch_artifact_index.md`

Then remove:

- `tests/test_patch_184_current_and_spark_theory_update.py`
- `PATCH_184_MANIFEST.txt`
- `PATCH_184_RECOVERY_NOTE.md`
- `PATCH_184_DELETE_LIST.txt`

The archived Patch 183 root artifacts under `docs/patch_archive/` can remain as audit-trail copies.
