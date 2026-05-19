from pathlib import Path

from pages_ui.artificial_mind_formation_page import (
    ARTIFICIAL_MIND_FORMATION_PANEL_ROWS,
    ARTIFICIAL_MIND_FORMATION_SECTIONS,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_164_uses_four_side_by_side_panel_rows():
    assert len(ARTIFICIAL_MIND_FORMATION_PANEL_ROWS) == 4
    assert all(len(row) == 2 for row in ARTIFICIAL_MIND_FORMATION_PANEL_ROWS)

    panel_titles = [panel_title for row in ARTIFICIAL_MIND_FORMATION_PANEL_ROWS for panel_title, _ in row]
    assert panel_titles == [
        "Boundary & scale",
        "Formation & pause",
        "Memory & conditioning",
        "Embodiment & friction",
        "Route-before-reach",
        "Corruption signals",
        "Human review / revocation / appeal",
        "Spark boundary",
    ]


def test_patch_164_panel_rows_cover_every_original_section_once():
    original_titles = [title for title, _ in ARTIFICIAL_MIND_FORMATION_SECTIONS]
    panel_section_titles = [
        section_title
        for row in ARTIFICIAL_MIND_FORMATION_PANEL_ROWS
        for _, section_titles in row
        for section_title in section_titles
    ]

    assert panel_section_titles == original_titles
    assert len(panel_section_titles) == len(set(panel_section_titles))


def test_patch_164_rendering_is_opt_in_and_collapsed_by_default():
    source = read("pages_ui/artificial_mind_formation_page.py")
    docs = read("docs/artificial_mind_formation_theory.md")

    assert "st.columns(2)" in source
    assert "ARTIFICIAL_MIND_FORMATION_PANEL_ROWS" in source
    assert "Open only the panel you want to review" in source
    assert "four compact rows" in source
    assert "with st.expander(ARTIFICIAL_MIND_FORMATION_TITLE, expanded=False)" in source
    assert "with st.expander(panel_title, expanded=False)" in source
    assert "four compact side-by-side panel rows" in docs
    assert "collapsed by default" in docs


def test_patch_164_preserves_no_scoring_taxonomy_or_world_lens_changes():
    source = read("pages_ui/artificial_mind_formation_page.py")
    scoring = read("core/scoring.py")
    world_lens = read("core/world_lens.py")

    forbidden_runtime_hooks = (
        "full_report",
        "score_",
        "classify_verdict",
        "final_protocol_judgment",
        "simulate(",
        "build_local_witness_receipt",
        "create_receipt",
        "generate_receipt",
        "requests.",
        "telemetry",
        "analytics",
        "database",
        "Global ID sync",
        "public ledger",
    )
    for token in forbidden_runtime_hooks:
        assert token not in source

    assert "ARTIFICIAL_MIND" not in scoring
    assert "ARTIFICIAL_MIND" not in world_lens
