from pathlib import Path


def app_text() -> str:
    return Path("app.py").read_text(encoding="utf-8")


def boundary_cases_section() -> str:
    text = app_text()
    start = text.index("with tab_boundary:")
    end = text.index("with tab_empirical:", start)
    return text[start:end]


def test_patch_72_5_boundary_intro_is_neutral_and_current():
    section = boundary_cases_section()

    assert "Boundary cases calibrate the review model. They do not create authority, enforcement, or final decisions." in section
    assert "turn the mirror into a throne" not in section
    assert "ALETHEIA reflects risk patterns for human review" in section


def test_patch_72_5_sanctuary_related_boundary_copy_is_neutralized():
    section = boundary_cases_section()

    assert "before any Sanctuary reading" not in section
    assert "approach Sanctuary" not in section
    assert "allowing missing safeguards to score as Sanctuary" not in section
    assert "before any low-risk internal reading" in section
    assert "approach the review boundary" in section
    assert "not a low-risk internal reading" in section


def test_patch_72_5_extraordinary_claim_and_self_audit_copy_is_neutralized():
    section = boundary_cases_section()

    assert "Treating an unverified extraordinary claim as authority" in section
    assert "Validating spiritual authority" not in section
    assert "spiritual validation" not in section
    assert "spiritual authority leakage" not in section.lower()
    assert "extraordinary-claim validation" in section
    assert "unverified authority leakage" in section
    assert "does not certify ALETHEIA as correct, complete, or beyond review" in section


def test_patch_72_5_receipt_disclaimer_uses_extraordinary_claim_validation():
    section = boundary_cases_section()

    assert "extraordinary-claim validation, public ledger proof" in section
    assert "spiritual validation, public ledger proof" not in section


def test_patch_72_5_manifest_recovery_and_status_present():
    for path in [
        "PATCH_72_5_MANIFEST.txt",
        "PATCH_72_5_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = Path("PATCH_72_5_MANIFEST.txt").read_text(encoding="utf-8")
    recovery = Path("PATCH_72_5_RECOVERY_NOTE.md").read_text(encoding="utf-8")
    status = Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = Path("docs/progress_database.md").read_text(encoding="utf-8")

    assert "Boundary Cases Neutral Text Refresh" in manifest
    assert "tools\\run_patch_checks.bat 72_5" in recovery
    assert "Patch 72.5" in status
    assert "Patch 72.5" in progress
    assert "Boundary Cases Neutral Text Refresh" in status + progress
