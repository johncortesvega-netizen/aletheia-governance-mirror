from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_failure_classification_docs_and_prompt_exist():
    doc = read("docs/failure_classification.md")
    prompt = read("prompts/failure_classification_prompt.md")

    for term in ["Actor Failure", "Policy Failure", "Implementation Failure", "Data Failure"]:
        assert term in doc
        assert term in prompt

    assert "Failure Classification" in doc
    assert "Failure Classification" in prompt
    assert "Classify the failure layer before recommending repair" in doc
    assert "Human review required before assigning responsibility" in prompt


def test_app_exposes_failure_classification_without_enforcement():
    app = read("app.py")

    assert "failure_mode_definitions" in app
    assert "Failure Classification output" in app
    assert "Primary failure type" in app
    assert "Secondary failure type" in app
    assert "Template-level calibration, not a final finding" in app
    assert "This layer helps humans repair the right part of a system" in app

    forbidden = [
        "This person is guilty.",
        "This leader must be removed.",
        "The AI has assigned responsibility.",
        "Human review is unnecessary.",
    ]
    for phrase in forbidden:
        assert phrase not in app


def test_readme_and_about_reference_failure_classification():
    readme = read("README.md")
    about = read("about_page.py")

    assert "docs/failure_classification.md" in readme
    assert "prompts/failure_classification_prompt.md" in readme
    assert "Failure Classification adds a repair-oriented diagnostic layer" in readme
    assert "Failure Classification separates governance-risk findings" in about
    assert "not blame, enforcement, or automated authority" in about


def test_recovery_note_declares_diagnostic_only():
    note = read("PATCH_35_RECOVERY_NOTE.md")

    assert "Patch 35" in note
    assert "Actor Failure" in note
    assert "Policy Failure" in note
    assert "Implementation Failure" in note
    assert "Data Failure" in note
    assert "diagnostic only" in note
    assert "does not assign final blame" in note
    assert "No core enforcement logic was added" in note
