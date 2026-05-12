from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_patch_76_comparison_doc_defines_distinct_niche_without_replacement_claims():
    text = read("docs/comparison_positioning.md")

    assert "# ALETHEIA Comparison Positioning" in text
    assert "qualitative governance-risk reflection for human review" in text
    assert "not an enterprise AI governance platform" in text
    assert "not replace model governance" in text
    assert "technical fairness" in text
    assert "ALETHEIA reflects. Humans review. Power stays accountable." in text
    assert "must not claim to govern, enforce, certify, adjudicate, punish, approve" in text


def test_patch_76_readme_links_positioning_and_free_open_source_commitment():
    text = read("README.md")

    assert "## Differentiation from other governance tools" in text
    assert "qualitative governance-risk reflection" in text
    assert "enterprise AI governance platform" in text
    assert "Technical fairness libraries" in text
    assert "ALETHEIA is free/open-source code and is intended to remain free" in text
    assert "docs/comparison_positioning.md" in text


def test_patch_76_about_surfaces_collapsed_positioning_without_ui_overload():
    for path in ["app.py", "about_page.py"]:
        text = read(path)
        assert "Positioning: not enterprise compliance, not fairness library" in text
        assert "expanded=False" in text
        assert "qualitative governance-risk reflection" in text
        assert "ALETHEIA is free/open-source code and is intended to remain free" in text
        assert "access to the mirror should not become a gatekeeping mechanism" in text


def test_patch_76_manifest_recovery_status_and_progress_present():
    for path in [
        "PATCH_76_MANIFEST.txt",
        "PATCH_76_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = read("PATCH_76_MANIFEST.txt")
    recovery = read("PATCH_76_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    assert "Differentiation / Comparison Framing" in manifest
    assert r"tools\run_patch_checks.bat 76" in recovery
    assert "Patch 76 - Differentiation / Comparison Framing" in status
    assert "Patch 76 - Differentiation / Comparison Framing" in progress
    assert "No scoring formula change" in status
