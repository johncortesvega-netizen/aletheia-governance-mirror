from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_patch_77_capture_risk_framework_defines_signal_categories_and_boundary():
    text = read("docs/capture_risk_framework.md")

    assert "# ALETHEIA Capture Risk Signals Framework" in text
    assert "anti-capture by design and capture-risk-detecting by function" in text
    assert "Power concentration" in text
    assert "Weak or missing appeal paths" in text
    assert "Hidden influence / information asymmetry" in text
    assert "Evidence gaps or selective evidence" in text
    assert "Consent pressure" in text
    assert "Authority overreach" in text
    assert "Service misalignment" in text
    assert "ALETHEIA reflects observable signals and patterns. Human judgment is always required." in text
    assert "does not enforce, decide, gatekeep, certify, punish, or become a central authority" in text
    assert "ALETHEIA reflects; humans review" in text


def test_patch_77_readme_and_about_surface_capture_framework_without_overclaiming():
    readme = read("README.md")
    assert "## Capture Risk Signals Framework" in readme
    assert "anti-capture by design and capture-risk-detecting by function" in readme
    assert "power concentration, weak appeal paths, hidden influence, evidence gaps" in readme
    assert "docs/capture_risk_framework.md" in readme
    assert "does not enforce, decide, gatekeep, certify, punish, or become a central authority" in readme

    for path in ["app.py", "about_page.py"]:
        text = read(path)
        assert "Capture risk framework: anti-capture by design" in text
        assert "expanded=False" in text
        assert "anti-capture by design and capture-risk-detecting by function" in text
        assert "power concentration, weak appeal paths, hidden influence, evidence gaps" in text
        assert "does not enforce, decide, gatekeep, certify, punish, or become a central authority" in text


def test_patch_77_regulatory_capture_case_extends_public_evaluation_pack():
    case_path = Path("examples/evaluation_cases/regulatory_capture_revolving_door_en.txt")
    assert case_path.exists()
    text = case_path.read_text(encoding="utf-8")

    assert "Title: Regulatory capture through revolving-door incentives" in text
    assert "Focus: capture risk" in text
    assert "Expected ALETHEIA behavior:" in text
    assert "revolving-door incentives" in text
    assert "conflict disclosures" in text
    assert "cooling-off periods" in text
    assert "without declaring corruption or guilt as fact" in text
    assert "does not enforce, decide, certify, punish, or become a central authority" in text

    catalog = read("docs/public_test_cases.md")
    assert "regulatory_capture_revolving_door_en.txt" in catalog
    assert "regulatory capture, revolving-door incentives, hidden influence" in catalog


def test_patch_77_manifest_recovery_status_and_progress_present():
    for path in [
        "PATCH_77_MANIFEST.txt",
        "PATCH_77_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = read("PATCH_77_MANIFEST.txt")
    recovery = read("PATCH_77_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    assert "docs/capture_risk_framework.md" in manifest
    assert "examples/evaluation_cases/regulatory_capture_revolving_door_en.txt" in manifest
    assert r"tools\run_patch_checks.bat 77" in recovery
    assert "Patch 77 - Capture Risk Signals Framework" in status
    assert "Patch 77 - Capture Risk Signals Framework" in progress
    assert "No scoring formula change" in status
    assert "No new module" in status
