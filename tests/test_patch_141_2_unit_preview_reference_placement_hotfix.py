from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_reference_previews_render_below_unit_preview_actions():
    unit_preview = read("ui/unit_preview.py")
    assert "render_unit_preview_html_reference(container)" in unit_preview
    assert "Reference previews" in unit_preview
    assert "container.text_area(" in unit_preview
    prompt_index = unit_preview.index("preview_text = container.text_area")
    columns_index = unit_preview.index("action_columns = container.columns(2)")
    preview_button_index = unit_preview.index('container.button("Preview review path"')
    proceed_button_index = unit_preview.index('container.button(\n            "Proceed to ALETHEIA"')
    reference_index = unit_preview.index("render_unit_preview_html_reference(container)")
    assert prompt_index < columns_index < preview_button_index < proceed_button_index < reference_index


def test_reference_previews_remain_local_and_first_page_only():
    unit_preview = read("ui/unit_preview.py")
    assert "Sydney_Protocol_v3.2.html" in unit_preview
    assert "GPA_v8.2.html" in unit_preview
    assert "path.exists()" in unit_preview
    assert "components.html" in unit_preview
    for forbidden in ["requests.", "httpx.", "openai", "embedding", "telemetry", "analytics", "database"]:
        assert forbidden not in unit_preview.lower()


def test_patch_141_2_docs_record_visual_placement_only():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_141_2_MANIFEST.txt",
            "PATCH_141_2_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
        ]
    ).lower()
    assert "patch 141.2" in combined
    assert "reference previews" in combined
    assert "under the unit preview prompt" in combined
    for phrase in [
        "no scoring",
        "no verdict routing",
        "no receipt schema",
        "no receipt generation",
        "no external calls",
        "no telemetry",
        "no certification",
        "no final-truth",
    ]:
        assert phrase in combined
