# PATCH 149.4 RECOVERY NOTE — Unit Preview DAO Grok Comparison Intro Hotfix

## Purpose

Patch 149.4 clarifies the DAO governance proof-of-concept introduction on the Unit Preview first page.

The previous patch already restored the correct first-page dropdown behavior. This hotfix keeps that behavior and adds one missing framing point requested during review: Grok-style review should be mentioned in the expanded DAO proof-of-concept introduction as a comparison lens / external reviewer pressure input.

## What changed

- The DAO proof-of-concept intro now states that Grok-style review can sharpen centralization, capture, and hypocrisy concerns, but it is not validation, certification, or a final judge.
- The reviewer documentation now carries the same boundary.

## What did not change

- No scoring logic changed.
- No receipt logic changed.
- No World Lens math changed.
- No AI Integrity, Evidence Lab, Stress Test, Mirror Check, or Receipt Reader behavior changed.
- No external calls were added.
- No telemetry, central storage, public ledger, identity sync, or automation authority was added.

## Validation

Recommended checks:

```bash
python -m py_compile ui/unit_preview.py
PYTHONPATH=. pytest -q tests/test_patch_149_unit_preview_dao_proof_of_concept.py
```

## Recovery

To revert Patch 149.4, restore `ui/unit_preview.py` and `docs/for-reviewers/dao_governance_proof_of_concept.md` from Patch 149.3.

Human review remains required. Mirror, not throne.
