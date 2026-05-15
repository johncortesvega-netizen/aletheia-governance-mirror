# Patch 111 Recovery Note — Beginner Try This First UX

Patch 111 adds a small beginner-facing UX guide and documents the safe first path for new users.

## Files added

- `ui/beginner_guide.py`
- `docs/beginner_ux.md`
- `tests/test_patch_111_beginner_try_this_first_ux.py`
- `PATCH_111_MANIFEST.txt`
- `PATCH_111_RECOVERY_NOTE.md`

## Files updated

- `app.py`
- `README.md`
- `docs/architecture.md`
- `docs/patch_index.md`
- `docs/public_trust_package.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`
- `data/protocol_baseline_manifest.json`

## Recovery steps

If Patch 111 must be reverted, remove the `render_try_this_first_guide` import and call from `app.py`, delete `ui/beginner_guide.py`, delete `docs/beginner_ux.md`, and remove the Patch 111 documentation/status entries.

## Boundary preserved

Patch 111 is a small UX helper only. It does not change scoring, verdict routing, signal patterns, signal weights, receipt schemas, module routing, external calls, live model calls, telemetry, analytics, central storage, Global ID sync, public ledger sync, privacy guarantees, certification, enforcement, or final-truth behavior.

Human review remains required. ALETHEIA surfaces signals; humans keep the judgment.
