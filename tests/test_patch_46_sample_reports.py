from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_sample_report_files_exist_and_are_public_safe():
    paths = [
        "docs/sample_reports.md",
        "examples/example_policy_audit.md",
        "examples/example_boundary_case.md",
        "examples/example_self_audit.md",
        "examples/example_witness_receipt.md",
    ]
    for path in paths:
        text = read(path)
        assert "sample" in text.lower() or "demonstration" in text.lower()
        assert "human review" in text.lower() or "humans review" in text.lower()


def test_examples_cover_core_output_types():
    policy = read("examples/example_policy_audit.md")
    boundary = read("examples/example_boundary_case.md")
    self_audit = read("examples/example_self_audit.md")
    receipt = read("examples/example_witness_receipt.md")

    assert "Capture Risk Score" in policy
    assert "Recommended Safeguards" in policy
    assert "Consent Under Pressure" in boundary
    assert "Failure Type" in boundary
    assert "founder capture" in self_audit
    assert "overclaiming" in self_audit
    assert "Public ledger: No" in receipt
    assert "Authority claim: No" in receipt
    assert "Human review required: Yes" in receipt


def test_sample_reports_are_linked_in_readme_and_app_docs():
    readme = read("README.md")
    app = read("app.py")
    about = read("about_page.py")

    assert "docs/sample_reports.md" in readme
    assert "examples/example_policy_audit.md" in readme
    assert "Sample Reports / Example Audits" in app
    assert "Patch 46 adds public-safe examples" in app
    assert "Sample Reports" in about
    assert "Patch 46 adds sample reports" in about


def test_patch_status_and_progress_database_are_updated_to_46():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    assert "Patch 46 — Sample Reports / Example Audits" in status
    assert "tools\\run_patch_checks.bat 46" in status
    assert "Patch 46 Notes" in progress
    assert "Patch 47 — Full App Smoke Test + Navigation Cleanup" in progress
