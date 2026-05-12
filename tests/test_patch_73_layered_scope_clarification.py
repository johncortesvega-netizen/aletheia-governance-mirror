from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_patch_73_readme_defines_scope_layers():
    text = read("README.md")

    assert "## Scope layers" in text
    assert "Current operational layer" in text
    assert "corruption-pattern and governance-risk detection framework for human review" in text
    assert "Research layer" in text
    assert "Vision layer" in text
    assert "Out-of-scope layer" in text
    assert "The incorruptible-system framing is a theory horizon, not a present capability claim." in text
    assert "docs/scope_layers.md" in text


def test_patch_73_scope_layers_doc_states_theory_vs_tool_boundary():
    text = read("docs/scope_layers.md")

    assert "# ALETHEIA Scope Layers" in text
    assert "ALETHEIA is currently a corruption-pattern and governance-risk detection framework" in text
    assert "This vision layer is a theoretical horizon" in text
    assert "The incorruptible system is the theory horizon. The current tool is the mirror." in text
    assert "replace human judgment" in text
    assert "create a real 9k body" in text


def test_patch_73_about_surfaces_layered_scope_in_app_and_standalone_about():
    for path in ["app.py", "about_page.py"]:
        text = read(path)
        assert "Scope layers: tool, research, vision, out of scope" in text
        assert "Current operational layer" in text
        assert "corruption-pattern and governance-risk detection framework for human review" in text
        assert "Vision layer" in text
        assert "theoretical horizon" in text
        assert "does not govern, enforce, allocate authority, select representatives" in text
        assert "create a real 9k body" in text


def test_patch_73_manifest_recovery_status_and_progress_present():
    for path in [
        "PATCH_73_MANIFEST.txt",
        "PATCH_73_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = read("PATCH_73_MANIFEST.txt")
    recovery = read("PATCH_73_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    assert "Layered Scope Clarification" in manifest
    assert r"tools\run_patch_checks.bat 73" in recovery
    assert "Patch 73 - Layered Scope Clarification" in status
    assert "Patch 73 - Layered Scope Clarification" in progress
    assert "No scoring formula change" in status + progress
