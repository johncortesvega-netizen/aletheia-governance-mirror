from __future__ import annotations

from pathlib import Path

from ui.unit_preview import get_ai_audit_loop_evidence_sets

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


def test_patch_148_adds_chatgpt_evidence_set_to_unit_preview() -> None:
    evidence_sets = get_ai_audit_loop_evidence_sets(ROOT)

    assert [item["ai_name"] for item in evidence_sets] == [
        "Grok / xAI",
        "Claude",
        "Gemini",
        "ChatGPT",
    ]
    assert [item["title"] for item in evidence_sets] == [
        "Capture and architectural-opacity pressure",
        "Evidence-boundary and mechanisms-vs-claims gap",
        "Sanctification drift / authority-boundary drift",
        "Concealed flattery pressure inside analytical tone",
    ]
    assert [len(item["images"]) for item in evidence_sets] == [2, 3, 6, 1]


def test_patch_148_makes_ai_names_larger_in_unit_preview() -> None:
    source = read("ui/unit_preview.py")

    assert "container.markdown(f\"### {ai_name}\")" in source
    assert "container.markdown(f\"**Evidence focus:** {title}\")" in source
    assert "ChatGPT" in source
    assert "Concealed flattery pressure inside analytical tone" in source


def test_patch_148_documents_four_part_audit_loop_without_authority_claim() -> None:
    evidence_doc = read("docs/for-reviewers/ai_audit_loop_evidence.md")
    baseline = read("docs/for-reviewers/ai_audit_loop_evidence/AI_AUDIT_LOOP_BASELINE_REVIEW.txt")
    combined = evidence_doc + "\n" + baseline

    assert "ChatGPT concealed-flattery review" in combined
    assert "concealed flattery pressure" in combined
    assert "observation and approval" in combined
    assert "Grok: capture" in combined
    assert "Claude: evidence-boundary" in combined
    assert "Gemini: sanctification drift" in combined
    assert "ChatGPT: concealed flattery" in combined
    assert "not official verdicts" in evidence_doc
    assert "not validation, certification, or official ALETHEIA receipts" in baseline
    assert "Mirror, not throne" in evidence_doc


def test_patch_148_preserves_behavior_boundaries() -> None:
    manifest = read("PATCH_148_MANIFEST.txt")
    recovery = read("PATCH_148_RECOVERY_NOTE.md")
    combined = manifest + "\n" + recovery

    assert "ui/unit_preview.py" in manifest
    assert "docs/for-reviewers/ai_audit_loop_evidence.md" in manifest
    assert "No app scoring change" in combined
    assert "No receipt schema or receipt generation change" in combined
    assert "No World Lens math change" in combined
    assert "Human review remains required" in combined
    assert "official verdict" not in combined.lower().replace("not official verdict", "")
