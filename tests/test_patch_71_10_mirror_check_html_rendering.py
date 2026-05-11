
from pathlib import Path


def test_patch_71_10_mirror_check_judgment_card_uses_dedented_html():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "import textwrap" in app_text
    assert "judgment_card_html = f" in app_text
    assert "st.markdown(textwrap.dedent(judgment_card_html).strip(), unsafe_allow_html=True)" in app_text

    start = app_text.index("def render_chat_judgment")
    end = app_text.index("# Header", start)
    judgment_section = app_text[start:end]

    old_fragment = 'st.markdown(\n        f"""\n        <div class="soft-card">'
    assert old_fragment not in judgment_section


def test_patch_71_10_review_band_line_is_precomputed_not_nested_inside_html_expression():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert 'review_band_detail_line = ""' in app_text
    assert 'review_band_detail_line = f"<strong>Review band:</strong> {review_band_label}<br>"' in app_text
    assert '{f"<strong>Review band:</strong> {review_band_label}<br>" if verdict == "THRESHOLD" else ""}' not in app_text


def test_patch_71_10_scope_is_mirror_check_display_only():
    app_text = Path("app.py").read_text(encoding="utf-8")

    assert "def render_chat_judgment(judgment: dict, source: str, report: dict, sim: dict | None = None)" in app_text
    assert "render_chat_judgment(latest[\"judgment\"], latest[\"source\"], latest[\"report\"], latest.get(\"sim\"))" in app_text

    assert "review_band" not in Path("core/witness.py").read_text(encoding="utf-8")


def test_patch_71_10_manifest_recovery_and_progress_docs_present():
    for path in [
        "PATCH_71_10_MANIFEST.txt",
        "PATCH_71_10_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_71_10_MANIFEST.txt").read_text(encoding="utf-8")
    assert "app.py" in manifest
    assert "tests/test_patch_71_10_mirror_check_html_rendering.py" in manifest

    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")
    assert "Patch 71.10" in status
    assert "Patch 71.10" in progress
    assert "Mirror Check HTML Rendering Fix" in status + progress
