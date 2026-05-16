from __future__ import annotations

from pathlib import Path

from ui.unit_preview import get_dao_governance_proof_of_concept_cases

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    direct = ROOT / path
    if direct.exists():
        return direct.read_text(encoding="utf-8")
    name = Path(path).name
    if name.endswith("_MANIFEST.txt"):
        return (ROOT / "docs" / "patch_archive" / "manifests" / name).read_text(encoding="utf-8")
    if name.endswith("_RECOVERY_NOTE.md"):
        return (ROOT / "docs" / "patch_archive" / "recovery_notes" / name).read_text(encoding="utf-8")
    return direct.read_text(encoding="utf-8")


def test_patch_149_adds_four_elaborated_dao_baseline_cases() -> None:
    cases = get_dao_governance_proof_of_concept_cases()

    assert [case["name"] for case in cases] == [
        "Major DAO governance tools",
        "Lido Snapshot proposal-threshold change",
        "Lido DAO meta-governance risks",
        "Lido Dual Governance mechanics",
    ]
    assert [case["reading"] for case in cases] == [
        "THRESHOLD",
        "THRESHOLD",
        "THRESHOLD / ASYLUM pressure under capture stress",
        "THRESHOLD",
    ]
    for case in cases:
        assert case["strengths"]
        assert case["risks"]
        assert "Grok-style" in str(case["grok_compare"])


def test_patch_149_puts_dao_cases_inside_side_by_side_proof_of_concept_dropdowns() -> None:
    source = read("ui/unit_preview.py")

    assert "Proof-of-concept mirrors" in source
    assert "render_unit_preview_proof_concepts_side_by_side(container)" in source
    assert "render_ai_audit_loop_evidence(ai_column)" in source
    assert "render_dao_governance_proof_of_concept(dao_column)" in source
    assert "container.columns(2)" in source
    assert 'with ai_column.expander("Proof of concept: AI audit-loop evidence", expanded=False):' in source
    assert 'with dao_column.expander("Proof of concept: DAO governance mirror cases", expanded=False):' in source
    assert "DAO tools propose / vote / delegate / execute" in source
    assert "Strengths / useful design signals" in source
    assert "Risk signals / review pressure" in source
    assert "Grok-comparison lens" in source


def test_patch_149_documents_dao_boundary_without_authority_claim() -> None:
    doc = read("docs/for-reviewers/dao_governance_proof_of_concept.md")
    combined = doc + "\n" + read("PATCH_149_2_MANIFEST.txt") + "\n" + read("PATCH_149_2_RECOVERY_NOTE.md")

    assert "Major DAO governance tools" in doc
    assert "Lido Snapshot proposal-threshold change" in doc
    assert "Lido DAO meta-governance risks" in doc
    assert "Lido Dual Governance mechanics" in doc
    assert "THRESHOLD — not failed, not safe, human review required" in doc
    assert "proof-of-concept dropdowns" in doc
    assert "Grok-comparison lens" in doc
    assert "not live DAO readings" in combined
    assert "not official ALETHEIA receipts" in combined
    assert "legal or investment advice" in combined or "legal findings, investment advice" in combined
    assert "Mirror, not throne" in combined


def test_patch_149_preserves_behavior_boundaries() -> None:
    manifest = read("PATCH_149_2_MANIFEST.txt")
    recovery = read("PATCH_149_2_RECOVERY_NOTE.md")
    combined = manifest + "\n" + recovery

    assert "ui/unit_preview.py" in manifest
    assert "docs/for-reviewers/dao_governance_proof_of_concept.md" in manifest
    assert "No app scoring change" in combined
    assert "No receipt schema or receipt generation change" in combined
    assert "No World Lens math change" in combined
    assert "No external calls" in combined
    assert "No certification" in combined
    assert "Human review remains required" in combined
