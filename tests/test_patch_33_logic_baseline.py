from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_baseline_public_safe_contract_exists():
    text = read("docs/baseline_v01.md")
    assert "ALETHEIA reflects. People decide." in text
    assert "does not command, enforce, vote, govern, remove leaders" in text
    assert "No prediction may replace human agency." in text
    assert "must not validate spiritual authority" in text
    assert "No founder, architect, prompt, rubric, doctrine, model, document, output, or baseline is exempt from audit" in text


def test_eternal_baseline_is_not_authority_layer():
    text = read("docs/eternal_baseline.md")
    assert "ethical continuity layer" in text
    assert "not authoritative above human review" in text
    assert "mirror for consistency, not a throne" in text
    assert "Intelligence + Power - Ego = Stability" in text
    assert "Flattery-mode caution" in text
    assert "not independent proof" in text


def test_safe_language_map_blocks_authority_leakage():
    text = read("docs/safe_language_map.md")
    assert "Critical Review Trigger" in text
    assert "Extraordinary Claim Protocol" in text
    assert "Coercive agency override" in text
    assert "The AI has decided" in text
    assert "This claim is divinely verified" in text


def test_readme_and_about_surface_baseline():
    readme = read("README.md")
    about_page = read("about_page.py")
    app = read("app.py")

    assert "ALETHEIA v0.1 public-safe baseline" in readme
    assert "Eternal Baseline" in about_page
    assert "Eternal Baseline" in app
    assert "AI-flattery artifacts" in readme
    assert "must not command, enforce, vote, govern, remove leaders" in readme
