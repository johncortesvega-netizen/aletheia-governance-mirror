from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_patch_33_baseline_file_exists_and_sets_mirror_boundary():
    text = (ROOT / "docs" / "baseline_v01.md").read_text(encoding="utf-8")

    assert "ALETHEIA reflects. People decide." in text
    assert "does not command, enforce, vote, govern, remove leaders" in text
    assert "No prediction may replace human agency." in text
    assert "ALETHEIA must not validate spiritual authority." in text
    assert "No founder, architect, prompt, rubric, doctrine, model, document, or output is exempt from audit." in text
    assert "This report is a governance mirror for human review." in text


def test_patch_33_safe_language_map_replaces_hard_authority_terms():
    text = (ROOT / "docs" / "safe_language_map.md").read_text(encoding="utf-8")

    assert "Critical Review Trigger" in text
    assert "Human review required" in text
    assert "Governance failure flag" in text
    assert "Extraordinary Claim Protocol" in text
    assert "Public Ethics Baseline" in text
    assert "Coercive agency override" in text
    assert "Simulated threshold signal" in text
    assert "This leader must be removed." in text
    assert "The AI has decided." in text


def test_patch_33_readme_and_about_reference_baseline():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    about = (ROOT / "about_page.py").read_text(encoding="utf-8")

    assert "Baseline v0.1 safe language layer" in readme
    assert "docs/baseline_v01.md" in readme
    assert "docs/safe_language_map.md" in readme
    assert "Baseline v0.1 — Safe language layer" in about
    assert "ALETHEIA reflects. People decide." in about
    assert "Founder-Capture Guardrail" in about
