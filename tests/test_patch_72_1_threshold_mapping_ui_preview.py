from pathlib import Path


def test_patch_72_1_imports_public_threshold_mapping_helper():
    app_text = Path("app.py").read_text(encoding="utf-8")
    witness_text = Path("core/witness.py").read_text(encoding="utf-8")

    assert "build_threshold_mapping_layer" in app_text
    assert "def build_threshold_mapping_layer(" in witness_text
    assert "return _threshold_mapping_layer(" in witness_text


def test_patch_72_1_render_chat_judgment_accepts_scan_and_builds_preview():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "def render_chat_judgment(judgment: dict, source: str, report: dict, sim: dict | None = None, scan: dict | None = None)" in app_text
    assert "threshold_mapping = build_threshold_mapping_layer(" in app_text
    assert "scan=scan or {}" in app_text
    assert "Threshold mapping preview" in app_text
    assert "Threshold direction" in app_text
    assert "Z-axis" in app_text
    assert "Repair index" in app_text


def test_patch_72_1_preview_is_explicitly_receipt_only_and_not_new_verdict():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "Receipt preview only: this maps THRESHOLD direction" in app_text
    assert "It does not create a new verdict or enforcement path." in app_text
    assert "THRESHOLD-" not in app_text
    assert "THRESHOLD+" not in app_text


def test_patch_72_1_latest_reading_passes_scan_into_judgment_renderer():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert 'render_chat_judgment(latest["judgment"], latest["source"], latest["report"], latest.get("sim"), latest.get("scan"))' in app_text


def test_patch_72_1_manifest_recovery_docs_present():
    for path in [
        "PATCH_72_1_MANIFEST.txt",
        "PATCH_72_1_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_1_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_1_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "app.py" in manifest
    assert "core/witness.py" in manifest
    assert "tests/test_patch_72_1_threshold_mapping_ui_preview.py" in manifest
    assert "tools\\run_patch_checks.bat 72_1" in recovery
    assert "Patch 72.1" in status
    assert "Patch 72.1" in progress
    assert "Threshold Mapping UI Preview" in status + progress
