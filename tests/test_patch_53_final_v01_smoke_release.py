from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_53_release_docs_exist():
    required = [
        "README.md",
        "docs/baseline_v01.md",
        "docs/eternal_baseline.md",
        "docs/protocol_guide.md",
        "docs/limitations.md",
        "docs/ethics.md",
        "docs/public_release_notes.md",
        "docs/v01_release_package.md",
        "docs/release_candidate_checklist.md",
        "docs/sample_reports.md",
        "docs/final_v01_smoke_release.md",
        "PATCH_STATUS.md",
    ]
    missing = [path for path in required if not (ROOT / path).exists()]
    assert not missing, f"Missing release docs: {missing}"


def test_patch_53_examples_and_workflow_exist():
    required = [
        "examples/example_policy_audit.md",
        "examples/example_boundary_case.md",
        "examples/example_self_audit.md",
        "examples/example_witness_receipt.md",
        "tools/run_checks.bat",
        "tools/run_patch_checks.bat",
        "tools/run_patch_checks.py",
        "tools/run_current_suite.py",
    ]
    missing = [path for path in required if not (ROOT / path).exists()]
    assert not missing, f"Missing examples/workflow files: {missing}"


def test_patch_53_final_smoke_doc_preserves_non_authority_boundary():
    text = read("docs/final_v01_smoke_release.md").lower()
    required = [
        "mirror",
        "humans review",
        "power stays accountable",
        "not add new doctrine",
        "no governance authority",
        "no global id sync",
        "no real 9k selection",
        "no automatic reset",
        "no public ledger",
        "no neural validation",
        "no religious validation",
        "no automated enforcement",
    ]
    for phrase in required:
        assert phrase in text


def test_patch_53_app_and_about_reference_final_smoke_release():
    app = read("app.py")
    about = read("about_page.py")
    readme = read("README.md")
    status = read("PATCH_STATUS.md")
    assert "v0.1-patch53-final-smoke-release" in app
    assert "Patch 53" in about
    assert "Final v0.1 Smoke Release" in readme
    assert "Patch 53" in status
