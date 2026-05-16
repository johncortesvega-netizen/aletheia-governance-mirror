# PATCH 149.2 RECOVERY NOTE — UNIT PREVIEW POC DROPDOWN RESTORE HOTFIX

## Intent

Patch 149.2 fixes the presentation misunderstanding from Patch 149.1. The proof-of-concept material should remain on the Unit Preview first page as two visible handles, but the detailed material should live inside dropdown/expander sections.

## Corrected behavior

The Unit Preview first page now shows two side-by-side proof-of-concept dropdowns:

1. **Proof of concept: AI audit-loop evidence**
2. **Proof of concept: DAO governance mirror cases**

Opening either dropdown reveals the richer content. The DAO/Lido side keeps the four baseline cases:

- Major DAO governance tools
- Lido Snapshot proposal-threshold change
- Lido DAO meta-governance risks
- Lido Dual Governance mechanics

Each case keeps internal reading, focus, useful design signals, risk signals/review pressure, and Grok-comparison lens.

## Boundaries preserved

This patch only changes Unit Preview presentation and related documentation/tests.

- No app scoring change.
- No receipt schema or receipt generation change.
- No World Lens math change.
- No external calls.
- No certification or DAO authority claim.
- Human review remains required.

The proof-of-concept material remains human-review evidence only: mirror, not throne.

## Recovery

If this patch needs to be reverted, restore `ui/unit_preview.py`, `docs/for-reviewers/dao_governance_proof_of_concept.md`, and `tests/test_patch_149_unit_preview_dao_proof_of_concept.py` from the previous working patch. No data migration or receipt cleanup is required.
