# PATCH 149.1 RECOVERY NOTE — Unit Preview Proof-of-Concept Visibility Hotfix

## What this patch fixes

Patch 149 placed the AI audit-loop and DAO/Lido proof-of-concept mirrors side by side, but each side was still hidden behind a collapsed dropdown. Patch 149.1 makes both proof-of-concept mirrors visible directly on the Unit Preview first page.

It also expands the DAO/Lido proof-of-concept content so the four baseline locks are not reduced to short paragraph summaries. Each case now shows:

- internal reading;
- focus;
- strengths / useful design signals;
- risk signals / review pressure;
- Grok-comparison lens.

## Files to restore to roll back this hotfix

Restore the previous Patch 149 versions of:

- `ui/unit_preview.py`
- `docs/for-reviewers/dao_governance_proof_of_concept.md`
- `tests/test_patch_149_unit_preview_dao_proof_of_concept.py`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `docs/patch_index.md`

Patch 149 root manifest/recovery files are archived under:

- `docs/patch_archive/manifests/PATCH_149_MANIFEST.txt`
- `docs/patch_archive/recovery_notes/PATCH_149_RECOVERY_NOTE.md`

## Boundary

This is a Unit Preview display/content hotfix only. It does not change scoring, routing, taxonomy, receipts, signal detection, World Lens math, AI Integrity behavior, Privacy Audit behavior, Evidence Lab behavior, upload/download behavior, storage, telemetry, Global ID sync, public ledger sync, certification, enforcement, approval/rejection authority, official authority, or final-truth behavior.

Human review remains required. Mirror, not throne.

## Validation

Run:

```bat
python tools\run_patch_checks.py 149
python -m py_compile ui\unit_preview.py
```

If full baseline self-audit reports differences, review them as expected changed files for this hotfix rather than treating them as scoring drift.
