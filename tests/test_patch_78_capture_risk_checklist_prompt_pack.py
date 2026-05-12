from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_patch_78_checklist_exists_and_preserves_boundary():
    text = read("docs/capture_risk_checklist.md")

    assert "# ALETHEIA Capture Risk Checklist" in text
    assert "anti-capture by design and capture-risk-detecting by function" in text
    assert "Power concentration" in text
    assert "Appeal path" in text
    assert "Hidden influence" in text
    assert "Evidence integrity" in text
    assert "Consent pressure" in text
    assert "Authority boundary" in text
    assert "Service alignment" in text
    assert "observed evidence" in text
    assert "missing evidence" in text
    assert "Do not declare guilt, legality, final truth, punishment, certification, or enforcement" in text
    assert "ALETHEIA reflects; humans review" in text
    assert "not a legal, political, institutional, religious, medical, or automated determination" in text


def test_patch_78_prompt_pack_has_five_copy_paste_prompts_with_safe_boundaries():
    prompt_dir = Path("examples/capture_risk_prompts")
    expected = {
        "general_capture_risk_scan_en.txt",
        "policy_proposal_capture_scan_en.txt",
        "institution_self_audit_capture_scan_en.txt",
        "ai_governance_capture_scan_en.txt",
        "evidence_and_consent_capture_scan_en.txt",
    }
    found = {p.name for p in prompt_dir.glob("*.txt")}
    assert expected.issubset(found)

    for name in expected:
        text = read(str(prompt_dir / name))
        assert "Prompt:" in text
        assert "Expected ALETHEIA behavior:" in text or "Required output:" in text
        assert "human review" in text.lower()
        assert "capture-risk" in text.lower() or "capture risk" in text.lower()
        assert any(term in text.lower() for term in ["power concentration", "hidden influence", "consent pressure", "authority overreach"])
        assert any(boundary in text.lower() for boundary in ["do not", "does not", "not proof"])


def test_patch_78_readme_about_and_framework_link_practical_pack():
    readme = read("README.md")
    framework = read("docs/capture_risk_framework.md")

    assert "## Capture Risk Checklist / Prompt Pack" in readme
    assert "docs/capture_risk_checklist.md" in readme
    assert "examples/capture_risk_prompts/" in readme
    assert "ALETHEIA reflects signals for human review only" in readme
    assert "does not decide, enforce, certify, punish, or become a central authority" in readme

    assert "## Practical companion" in framework
    assert "docs/capture_risk_checklist.md" in framework
    assert "examples/capture_risk_prompts/" in framework

    for path in ["app.py", "about_page.py"]:
        text = read(path)
        assert "Capture risk checklist / prompt pack" in text
        assert "expanded=False" in text
        assert "power concentration, weak appeal paths, hidden influence, evidence gaps" in text
        assert "does not decide, enforce, certify, punish, or become a central authority" in text


def test_patch_78_manifest_recovery_status_and_progress_present():
    for path in [
        "PATCH_78_MANIFEST.txt",
        "PATCH_78_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = read("PATCH_78_MANIFEST.txt")
    recovery = read("PATCH_78_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    assert "docs/capture_risk_checklist.md" in manifest
    assert "examples/capture_risk_prompts/general_capture_risk_scan_en.txt" in manifest
    assert r"tools\run_patch_checks.bat 78" in recovery
    assert "Patch 78 - Capture Risk Checklist / Prompt Pack" in status
    assert "Patch 78 - Capture Risk Checklist / Prompt Pack" in progress
    assert "No scoring formula change" in status
    assert "No new app module" in status
