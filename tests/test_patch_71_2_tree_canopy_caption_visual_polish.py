from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")


def _render_tree_block() -> str:
    start = APP.index("def render_pulse_tree(")
    end = APP.index("def build_features_from_scan", start)
    return APP[start:end]


def test_patch_71_2_caption_is_rendered_below_svg_not_inside_tree_visual():
    block = _render_tree_block()
    assert "TREE_VISUAL_CAPTION_CLASS" in block
    assert "aletheia-tree-caption-below-visual" in APP
    assert "</svg>\n        <div class=\"{TREE_VISUAL_CAPTION_CLASS}\"" in block

    svg_start = block.index("<svg")
    svg_end = block.index("</svg>", svg_start)
    svg_markup = block[svg_start:svg_end]
    assert "receipt integrity remains the protocol metric" not in svg_markup
    assert "<text x=\"130\" y=\"244\"" not in block


def test_patch_71_2_canopy_uses_layered_ellipses_instead_of_loose_circle_stack():
    block = _render_tree_block()
    assert "TREE_VISUAL_CANOPY_LAYER_COUNT = 8" in APP
    assert "canopy_scale = 0.82 + (score * 0.30)" in block
    assert "canopy_sag = 0 if state == \"SANCTUARY\"" in block
    assert block.count("<ellipse cx=") >= 11
    assert "<circle cx=\"130\" cy=\"78\"" not in block
    assert "<circle cx=\"92\" cy=\"93\"" not in block
    assert "<circle cx=\"168\" cy=\"88\"" not in block


def test_patch_71_2_tree_visual_scope_remains_ui_only():
    block = _render_tree_block()
    assert "receipt metrics stay canonical" in APP
    assert "Patch 71.2: the canopy and caption are visual-only polish" in block
    assert "display_score_from_judgment" not in block
    assert "build_local_witness_receipt" not in block
    assert "authority_claim" not in block


def test_patch_71_2_manifest_recovery_status_and_progress_are_present():
    assert (ROOT / "PATCH_71_2_MANIFEST.txt").exists()
    assert (ROOT / "PATCH_71_2_RECOVERY_NOTE.md").exists()
    assert "Patch 71.2" in (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    assert "Patch 71.2" in (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")
    manifest = (ROOT / "PATCH_71_2_MANIFEST.txt").read_text(encoding="utf-8")
    assert "app.py" in manifest
    assert "tests/test_patch_71_2_tree_canopy_caption_visual_polish.py" in manifest
