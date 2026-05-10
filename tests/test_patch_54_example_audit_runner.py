from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_54_demo_input_files_exist_and_are_fictional():
    required = [
        "examples/demo_inputs/sample_ai_policy.txt",
        "examples/demo_inputs/sample_dao_governance.txt",
        "examples/demo_inputs/sample_public_policy.txt",
    ]
    for path in required:
        text = read(path).lower()
        assert "sample" in text
        assert len(text) > 100


def test_patch_54_documentation_preserves_opt_in_boundary():
    text = read("docs/example_audit_runner.md").lower()
    assert "patch 54" in text
    assert "opt-in" in text
    assert "never run automatically" in text
    assert "default state remains user input" in text
    assert "not legal advice" in text


def test_patch_54_app_exposes_demo_loader_without_auto_analysis():
    text = read("app.py")
    assert 'APP_VERSION = "v0.1-patch54-example-audit-runner"' in text
    assert "DEMO_INPUT_FILES" in text
    assert "load_demo_input" in text
    assert "Optional demo inputs" in text
    assert "they never run by themselves" in text
    assert "Click Review idea if you want ALETHEIA to analyze it" in text
    assert 'audit_chat_input_source = "DEMO_INPUT"' in text


def test_patch_54_ledgers_and_about_reference_demo_inputs():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    about = read("about_page.py")
    readme = read("README.md")
    assert "Patch 54 — Example Audit Runner / Demo Inputs" in status
    assert "Patch 54 Notes" in progress
    assert "opt-in demo inputs" in about.lower()
    assert "run_patch_checks.bat 54" in readme
