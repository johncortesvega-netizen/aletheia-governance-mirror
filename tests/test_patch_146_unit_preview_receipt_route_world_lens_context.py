from pathlib import Path

from ui.unit_preview import detect_unit_preview_route, get_unit_preview_how_to_use_markdown

ROOT = Path(__file__).resolve().parents[1]


def test_unit_preview_routes_receipt_without_active_receipt_textbox_label():
    source = (ROOT / "ui" / "unit_preview.py").read_text(encoding="utf-8")
    assert '"Short text, question, or scenario"' in source
    assert '"Short text, question, scenario, or receipt"' not in source
    assert "Unit Preview can suggest **Receipt Reader — Standard View**" in get_unit_preview_how_to_use_markdown()

    suggestion = detect_unit_preview_route("ALETHEIA LOCAL WITNESS RECEIPT\nRubric version: v0.1")
    assert suggestion["module"] == "Receipt Reader — Standard View"
    assert "Receipt Reader" in suggestion["next_step"]


def test_world_lens_context_note_and_dial_copy_are_bounded():
    app_source = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "Optional context note" in app_source
    assert "World Lens context dial" in app_source
    assert "Review pressure lens" in app_source
    assert "World Lens context reflection" in app_source
    assert "Scenario or proposal to review" not in app_source
    assert "#### Simulation report" not in app_source
    assert "does not change country-year data, World Lens math, 9k allocation, receipts" in app_source
    assert "does not create a World Lens verdict, rescore country-year data, or certify" in app_source


def test_patch_146_no_forbidden_behavior_claims_added_to_world_lens_context():
    app_source = (ROOT / "app.py").read_text(encoding="utf-8")
    wl_block = app_source[app_source.index('with tab_grid:'):]
    assert "external call" not in wl_block.lower()
    assert "telemetry" not in wl_block.lower()
    assert "certify any country, government, institution, or policy" in wl_block
    assert "make a final decision" in wl_block
