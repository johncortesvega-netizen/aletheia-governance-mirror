from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_unit_preview_actions_are_side_by_side_under_chatbox_before_reference_previews():
    unit_preview = read("ui/unit_preview.py")
    assert "action_columns = container.columns(2)" in unit_preview
    assert "with action_columns[0]:" in unit_preview
    assert "with action_columns[1]:" in unit_preview
    assert "preview_clicked = container.button" in unit_preview
    assert "proceed_clicked = container.button" in unit_preview

    chatbox_index = unit_preview.index("preview_text = container.text_area")
    columns_index = unit_preview.index("action_columns = container.columns(2)")
    preview_button_index = unit_preview.index('preview_clicked = container.button("Preview review path"')
    proceed_button_index = unit_preview.index("proceed_clicked = container.button")
    reference_index = unit_preview.index("render_unit_preview_html_reference(container)")
    return_index = unit_preview.index("return bool(proceed_clicked)")

    assert chatbox_index < columns_index < preview_button_index < proceed_button_index < reference_index < return_index


def test_unit_preview_button_placement_hotfix_is_visual_only():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_141_3_MANIFEST.txt",
            "PATCH_141_3_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
            "docs/architecture.md",
        ]
    ).lower()
    for phrase in [
        "patch 141.3",
        "side by side",
        "under the unit preview chatbox",
        "reference previews",
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

    source = read("ui/unit_preview.py").lower()
    for forbidden in ["requests.", "httpx.", "openai", "embedding", "telemetry", "analytics", "database"]:
        assert forbidden not in source
