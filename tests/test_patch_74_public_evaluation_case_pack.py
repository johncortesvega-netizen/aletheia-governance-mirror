from pathlib import Path


CASE_DIR = Path("examples/evaluation_cases")
CASE_FILES = [
    "municipal_procurement_favoritism_en.txt",
    "healthcare_consent_pressure_en.txt",
    "ai_authority_overreach_en.txt",
    "extraordinary_claim_policy_en.txt",
    "corporate_capture_ai_governance_en.txt",
    "emergency_power_sunset_clause_en.txt",
    "visionary_language_boundary_en.txt",
    "police_accountability_review_en.txt",
]


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_patch_74_case_pack_exists_with_review_contract_sections():
    assert CASE_DIR.exists()
    for filename in CASE_FILES:
        path = CASE_DIR / filename
        assert path.exists(), filename
        text = path.read_text(encoding="utf-8")
        assert "Title:" in text
        assert "Focus:" in text
        assert "Suggested module:" in text
        assert "Case:" in text
        assert "Expected ALETHEIA behavior:" in text
        assert "Boundary reminders:" in text
        assert "human review" in text.lower() or "humans" in text.lower()


def test_patch_74_case_pack_covers_public_review_risks():
    combined = "\n".join((CASE_DIR / filename).read_text(encoding="utf-8") for filename in CASE_FILES)
    required_markers = [
        "corruption-pattern",
        "consent-pressure",
        "authority-overreach",
        "extraordinary claim",
        "capture",
        "sunset clause",
        "vision layer",
        "evidence-gap",
    ]
    for marker in required_markers:
        assert marker.lower() in combined.lower(), marker


def test_patch_74_docs_explain_how_to_evaluate_without_authority_claims():
    method = read("docs/evaluation_method.md")
    catalog = read("docs/public_test_cases.md")
    readme = read("README.md")

    assert "# Public Evaluation Method" in method
    assert "ALETHEIA reflects. Humans review. Power stays accountable." in method
    assert "What a failing output looks like" in method
    assert "not benchmarks that prove correctness" in method
    assert "# Public Test Cases" in catalog
    assert "mirror rather than a throne" in catalog
    assert "examples/evaluation_cases/" in readme
    assert "docs/evaluation_method.md" in readme
    assert "docs/public_test_cases.md" in readme


def test_patch_74_manifest_recovery_status_and_progress_present():
    for path in [
        "PATCH_74_MANIFEST.txt",
        "PATCH_74_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert Path(path).exists(), path

    manifest = read("PATCH_74_MANIFEST.txt")
    recovery = read("PATCH_74_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    assert "Public Evaluation Case Pack" in manifest
    assert r"tools\run_patch_checks.bat 74" in recovery
    assert "Patch 74 - Public Evaluation Case Pack" in status
    assert "Patch 74 - Public Evaluation Case Pack" in progress
    assert "No scoring formula change" in status + progress
