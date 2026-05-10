from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_boundary_cases_docs_and_prompt_exist():
    matrix = read("docs/boundary_cases_matrix.md")
    prompt = read("prompts/boundary_case_prompt.md")

    required_cases = [
        "Prediction vs Free Agency",
        "Voluntary Protection Mode",
        "Consent Under Pressure",
        "Basic Rights Scarcity",
        "Ambient Capture",
        "Performative Ethics",
        "ALETHEIA Audits Itself",
    ]
    for case in required_cases:
        assert case in matrix

    assert "Boundary Case Report" in matrix
    assert "Boundary Case Report" in prompt
    assert "No prediction may replace human agency" in prompt
    assert "Mechanisms outweigh adjectives" in prompt


def test_app_exposes_boundary_cases_tab_without_authority_language():
    app = read("app.py")

    assert "🧭 Boundary Cases" in app
    assert "Boundary Cases — Calibration Center" in app
    assert "Boundary cases calibrate the mirror" in app
    assert "This is a mirror output, not an instruction or enforcement decision." in app

    forbidden_authority_phrases = [
        "The leader must be deactivated",
        "The AI has decided.",
        "Guardrails no longer apply.",
        "This claim is divinely verified.",
    ]
    for phrase in forbidden_authority_phrases:
        assert phrase not in app


def test_readme_and_about_reference_boundary_cases():
    readme = read("README.md")
    about = read("about_page.py")

    assert "docs/boundary_cases_matrix.md" in readme
    assert "prompts/boundary_case_prompt.md" in readme
    assert "Boundary Cases Matrix adds a calibration layer" in readme
    assert "The Boundary Cases layer stress-tests difficult edge cases" in about
    assert "they do not create automated authority" in about


def test_recovery_note_declares_no_enforcement_added():
    note = read("PATCH_34_RECOVERY_NOTE.md")

    assert "Patch 34" in note
    assert "Boundary Cases are calibration tools" in note
    assert "no automatic reset" in note.lower()
    assert "no leader deactivation" in note.lower()
    assert "no spiritual validation" in note.lower()
