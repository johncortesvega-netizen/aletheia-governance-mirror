from pathlib import Path


def test_patch_71_12_review_band_visual_line_is_inline_html():
    app_text = Path("app.py").read_text(encoding="utf-8")

    expected = '''<div style="color:#d4b88a;font-size:1.05rem;font-weight:800;margin-top:0.2rem;">'''
    assert "review_band_line = (" in app_text
    assert expected in app_text
    assert "f'{safe_review_band_label}'" in app_text
    assert "'</div>'" in app_text


def test_patch_71_12_removes_multiline_indented_review_band_html_from_card():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert 'review_band_line = f"""' not in app_text
    assert 'review_band_detail_line = f"<strong>Review band:</strong> {review_band_label}<br>"' not in app_text


def test_patch_71_12_preserves_detail_rows_and_render_path():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert 'detail_rows_html = "".join(detail_rows)' in app_text
    assert '<div style="color:#e8e0d0;margin-top:0.5rem;">{detail_rows_html}</div>' in app_text
    assert "st.markdown(textwrap.dedent(judgment_card_html).strip(), unsafe_allow_html=True)" in app_text


def test_patch_71_12_manifest_recovery_and_progress_docs_present():
    for path in [
        "PATCH_71_12_MANIFEST.txt",
        "PATCH_71_12_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_71_12_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_71_12_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "app.py" in manifest
    assert "tests/test_patch_71_12_mirror_check_review_band_row_rendering.py" in manifest
    assert "tools\\run_patch_checks.bat 71_12" in recovery
    assert "Patch 71.12" in status
    assert "Patch 71.12" in progress
    assert "Mirror Check Review Band Row Render Fix" in status + progress
