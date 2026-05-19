from pathlib import Path

from pages_ui.artificial_mind_formation_page import get_artificial_mind_formation_markdown

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_186_framework_balance_visible_on_app_and_doc_surfaces():
    required_phrase = (
        "Science is the investigative base. Philosophy is the interpretive structure. "
        "Theology is the humility boundary. Human review is the action layer."
    )
    surfaces = [
        read("pages_ui/about_page.py"),
        read("about_page.py"),
        read("README.md"),
        read("docs/BOUNDARY.md"),
        read("docs/architecture.md"),
        read("docs/artificial_mind_formation_theory.md"),
        read("docs/for-reviewers/tool_comparison.md"),
        read("docs/reviewer_start_here.md"),
        get_artificial_mind_formation_markdown(),
    ]
    for surface in surfaces:
        assert required_phrase in surface


def test_patch_186_defines_science_philosophy_theology_and_human_review_layers():
    combined = "\n".join([
        read("pages_ui/about_page.py"),
        read("README.md"),
        read("docs/BOUNDARY.md"),
        read("docs/architecture.md"),
        read("docs/for-reviewers/tool_comparison.md"),
        get_artificial_mind_formation_markdown(),
    ])
    required = [
        "science-grounded, philosophically structured governance mirror with theological humility boundaries",
        "does not replace evidence with faith",
        "does not claim final authority",
        "inspectable signals, heuristics, metrics, receipts, and repair questions",
        "power, capture, authority drift, evidence integrity, and self-certification",
        "soul, life, consciousness, dignity, and ultimate truth",
        "less compliance-centered",
        "upstream power, epistemic restraint",
        "preventing ethics itself from becoming a throne",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_186_is_copy_only_and_preserves_no_authority_boundary():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    assert "Patch 186 — Framework Balance Copy Alignment" in status
    assert "Patch 186 — Framework Balance Copy Alignment" in progress
    assert "Content/documentation copy only" in status
    assert "No scoring, routing, taxonomy, receipt" in status
    assert "Human review remains required" in status

    core_files = [
        "core/scoring.py",
        "core/world_lens.py",
        "core/ai_integrity_mirror.py",
        "protocol.py",
    ]
    for rel in core_files:
        assert "Patch 186" not in read(rel)
