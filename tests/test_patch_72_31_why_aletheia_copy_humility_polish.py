from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def about_page_text() -> str:
    return Path("about_page.py").read_text(encoding="utf-8")


def why_aletheia_block() -> str:
    text = app_text()
    start = text.index("with tab_about:")
    return text[start:]


def test_patch_72_31_why_aletheia_intro_is_review_oriented():
    block = why_aletheia_block()

    assert "ALETHEIA helps review governance risk, evidence gaps, and safeguard needs. It reflects; people decide." in block
    assert "validate spiritual authority, confirm extraordinary claims, or replace human judgment" in block
    assert "without assigning blame, issuing commands, or claiming final authority" in block
    assert "It reflects; people decide." in block


def test_patch_72_31_why_aletheia_navigation_and_modules_are_humbled():
    block = why_aletheia_block()

    assert "raw/internal taxonomy label" in block
    assert "Those labels are compatibility labels for review workflows." in block
    assert "not legal, political, medical, religious, moral, or predictive verdicts" in block
    assert "World Lens is a **comparison and exposure model**" in block
    assert "not a real election, government, sovereign body, authority mechanism, political mandate, Global ID system, or real 9k body" in block


def test_patch_72_31_why_aletheia_protocol_guide_copy_uses_humility_language():
    block = why_aletheia_block()

    assert "Humility / Z-axis boundary" in block
    assert "no code, receipt, metric, hash, tree, 9k structure, institution, person, or model reaches final authority" in block
    assert "Protocol Guide preserves the operating boundaries behind the mirror" in block
    assert "Protocol integrity layer" in block
    assert "World Lens" in block


def test_patch_72_31_why_aletheia_research_caution_uses_internal_reading_language():
    block = why_aletheia_block()

    assert "does not prove legal, political, medical, religious, moral, predictive, or final truth" in block
    assert "Its outputs are internal review readings." in block
    assert "ALETHEIA is built for review, correction, and humility — not final authority." in block
    assert "Its classifications are internal model outputs" not in block
    assert "Global Grid" not in block
    assert "V-Axis Compass" not in block


def test_patch_72_31_standalone_about_page_receives_same_treatment():
    text = about_page_text()

    assert "Why ALETHEIA" in text
    assert "It reflects; people decide." in text
    assert "World Lens" in text
    assert "raw/internal taxonomy label" in text
    assert "Humility / Z-axis boundary" in text
    assert "final safety claims, or authority claims" in text
    assert "Global Grid" not in text
    assert "V-Axis Compass" not in text
    assert "real 9k selection" not in text
    assert "Its classifications are internal model outputs" not in text


def test_patch_72_31_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_31_MANIFEST.txt",
        "PATCH_72_31_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_31_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_31_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Why ALETHEIA Copy Humility Polish" in manifest
    assert r"tools\run_patch_checks.bat 72_31" in recovery
    assert "Patch 72.31" in status
    assert "Patch 72.31" in progress
    assert "Why ALETHEIA Copy Humility Polish" in status + progress
