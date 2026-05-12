# Patch 73 Recovery Note - Layered Scope Clarification

## What changed

Patch 73 adds a visible layered-scope clarification to README, Why ALETHEIA / About, and documentation.

The patch separates:

1. Current operational layer — corruption-pattern and governance-risk detection framework for human review.
2. Research layer — hypotheses, benchmarks, empirical mappings, scenario tests, and validation work.
3. Vision layer — the incorruptible-system idea as a long-term theoretical horizon.
4. Out-of-scope layer — no governing, enforcement, representative selection, real 9k body, mandates, authority validation, or replacement of human judgment.

## Files touched

- `README.md`
- `about_page.py`
- `app.py`
- `docs/scope_layers.md`
- `docs/progress_database.md`
- `PATCH_STATUS.md`
- `PATCH_73_MANIFEST.txt`
- `PATCH_73_RECOVERY_NOTE.md`
- `tests/test_patch_73_layered_scope_clarification.py`

## Invariant preserved

No scoring formula, verdict routing, witness receipt schema, empirical data model, World Lens behavior, Evidence Lab behavior, authority boundary, storage, public ledger, Global ID sync, central storage, real 9k body, or enforcement behavior changed.

## Check

```bat
tools\run_patch_checks.bat 73
```

If the patch must be reverted, remove the Scope Layers copy from README, `app.py`, and `about_page.py`; remove `docs/scope_layers.md`; remove the Patch 73 entries from `PATCH_STATUS.md` and `docs/progress_database.md`; then remove this manifest, recovery note, and the Patch 73 test file.
