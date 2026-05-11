from pathlib import Path


def test_patch_72_1_hotfix_adds_threshold_mapping_summary_to_main_card():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "safe_threshold_direction = html.escape" in app_text
    assert "threshold_z_axis = float(threshold_mapping.get" in app_text
    assert "threshold_repair_index = float(threshold_mapping.get" in app_text
    assert "<strong>Threshold mapping:</strong>" in app_text
    assert "Z-axis {threshold_z_axis:.3f}" in app_text
    assert "Repair index {threshold_repair_index:.3f}" in app_text


def test_patch_72_1_hotfix_keeps_expander_preview_and_scan_path():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "Threshold mapping preview" in app_text
    assert "build_threshold_mapping_layer(" in app_text
    assert "scan=scan or {}" in app_text
    assert 'render_chat_judgment(latest["judgment"], latest["source"], latest["report"], latest.get("sim"), latest.get("scan"))' in app_text


def test_patch_72_1_hotfix_does_not_recompute_mapping_after_metrics():
    app_text = Path("app.py").read_text(encoding="utf-8")
    render_start = app_text.index("def render_chat_judgment")
    render_end = app_text.index("# Header", render_start)
    render_text = app_text[render_start:render_end]

    assert render_text.count("threshold_mapping = build_threshold_mapping_layer(") == 1
    assert render_text.index("threshold_mapping = build_threshold_mapping_layer(") < render_text.index("judgment_card_html = f")


def test_patch_72_1_hotfix_manifest_recovery_docs_present():
    for path in [
        "PATCH_72_1_HOTFIX_MANIFEST.txt",
        "PATCH_72_1_HOTFIX_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_1_HOTFIX_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_1_HOTFIX_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "app.py" in manifest
    assert "tools\\run_patch_checks.bat 72_1_hotfix" in recovery
    assert "Patch 72.1 Hotfix" in status
    assert "Patch 72.1 Hotfix" in progress
    assert "Threshold Mapping Card Summary" in status + progress
