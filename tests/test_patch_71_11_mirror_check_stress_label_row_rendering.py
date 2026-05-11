from pathlib import Path


def test_patch_71_11_adds_html_escape_import_and_inline_detail_rows():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "import html" in app_text
    assert "detail_rows = [" in app_text
    assert "detail_rows_html = \"\".join(detail_rows)" in app_text
    assert 'safe_stress_label = html.escape(str(judgment.get("stress_label", "Unclassified")))' in app_text


def test_patch_71_11_stress_label_row_is_rendered_as_inline_html_not_indented_markdown():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert '<div style="color:#e8e0d0;margin-top:0.5rem;">{detail_rows_html}</div>' in app_text
    assert "<strong>Stress label:</strong> {safe_stress_label}" in app_text
    assert '<strong>Stress label:</strong> {judgment.get("stress_label", "Unclassified")}' not in app_text


def test_patch_71_11_preserves_patch_71_10_render_path_and_scope():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "st.markdown(textwrap.dedent(judgment_card_html).strip(), unsafe_allow_html=True)" in app_text
    assert "def render_chat_judgment(judgment: dict, source: str, report: dict, sim: dict | None = None)" in app_text
    assert "render_chat_judgment(latest[\"judgment\"], latest[\"source\"], latest[\"report\"], latest.get(\"sim\"))" in app_text


def test_patch_71_11_manifest_recovery_and_progress_docs_present():
    for path in [
        "PATCH_71_11_MANIFEST.txt",
        "PATCH_71_11_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_71_11_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_71_11_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "app.py" in manifest
    assert "tests/test_patch_71_11_mirror_check_stress_label_row_rendering.py" in manifest
    assert "tools\\run_patch_checks.bat 71_11" in recovery
    assert "Patch 71.11" in status
    assert "Patch 71.11" in progress
    assert "Mirror Check Stress Label Row Render Fix" in status + progress
