from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_patch_73_1_scope_layers_are_about_level_and_collapsed_by_default():
    for path in ["app.py", "about_page.py"]:
        text = read(path)
        assert 'with st.expander("Scope layers: tool, research, vision, out of scope", expanded=False):' in text
        assert 'with st.expander("Scope layers: tool, research, vision, out of scope", expanded=True):' not in text


def test_patch_73_1_scope_boundary_text_remains_available_without_ui_overload():
    for path in ["app.py", "about_page.py"]:
        text = read(path)
        assert "corruption-pattern and governance-risk detection framework for human review" in text
        assert "theoretical horizon" in text
        assert "does not govern, enforce, allocate authority, select representatives" in text
        assert "create a real 9k body" in text


def test_patch_73_1_manifest_recovery_status_and_progress_present():
    for path in [
        "PATCH_73_1_MANIFEST.txt",
        "PATCH_73_1_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = read("PATCH_73_1_MANIFEST.txt")
    recovery = read("PATCH_73_1_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    assert "Scope Copy Trim / UI Minimalism" in manifest
    assert r"tools\run_patch_checks.bat 73_1" in recovery
    assert "Patch 73.1 - Scope Copy Trim / UI Minimalism" in status
    assert "Patch 73.1 - Scope Copy Trim / UI Minimalism" in progress
    assert "No scoring formula change" in status + progress
