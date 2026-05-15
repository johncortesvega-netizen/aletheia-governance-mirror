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
        archived = ROOT / "docs" / "patch_archive" / "manifests" / name
    elif name.endswith("_RECOVERY_NOTE.md"):
        archived = ROOT / "docs" / "patch_archive" / "recovery_notes" / name
    else:
        archived = direct
    return archived.read_text(encoding="utf-8")


def test_unit_preview_restores_small_github_link_without_background_calls():
    source = read("ui/unit_preview.py")

    assert "GitHub" in source
    assert 'container.link_button(\n            "GitHub"' in source  # restored as a small visible link label
    assert "View GitHub repository" in source  # kept in help/source text for regression compatibility
    assert "https://github.com/johncortesvega-netizen/aletheia-governance-mirror" in source
    assert "container.link_button" in source
    assert "Unit Preview does not make external calls" in source
    assert "user-clicked source link" in source


def test_ai_audit_loop_evidence_assets_are_available_for_unit_preview_review():
    evidence_doc = read("docs/for-reviewers/ai_audit_loop_evidence.md")
    assert "AI Audit Loop Evidence" in evidence_doc
    assert "external AI output -> ALETHEIA mirror reading -> human review" in evidence_doc
    assert "Grok" in evidence_doc
    assert "Claude" in evidence_doc
    assert "Gemini" in evidence_doc
    assert "not official verdicts" in evidence_doc
    assert "Mirror, not throne" in evidence_doc

    evidence_sets = get_ai_audit_loop_evidence_sets(ROOT)
    assert [item["title"] for item in evidence_sets] == [
        "Grok / xAI — capture and architectural-opacity pressure",
        "Claude — evidence-boundary and mechanisms-vs-claims gap",
        "Gemini — sanctification drift / authority-boundary drift",
    ]
    image_counts = [len(item["images"]) for item in evidence_sets]
    assert image_counts == [2, 3, 6]


def test_unit_preview_renders_proof_of_concept_card_but_not_as_authority():
    source = read("ui/unit_preview.py")
    assert "Proof of concept: AI audit-loop evidence" in source
    assert "external AI output -> ALETHEIA mirror reading -> human review" in source
    assert "not official verdicts" in source
    assert "certifications, legal findings, or final proof" in source
    assert "render_ai_audit_loop_evidence(container)" in source


def test_patch_146_1_does_not_change_core_behavior_files():
    manifest = read("PATCH_146_1_MANIFEST.txt")
    assert "ui/unit_preview.py" in manifest
    assert "docs/for-reviewers/ai_audit_loop_evidence.md" in manifest
    assert "core/" not in manifest
    assert "protocol.py" not in manifest
    assert "app.py" not in manifest
