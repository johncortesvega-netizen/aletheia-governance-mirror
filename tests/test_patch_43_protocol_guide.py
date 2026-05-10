from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_protocol_guide_document_exists_and_consolidates_modules():
    text = read("docs/protocol_guide.md")
    required = [
        "ALETHEIA reflects. People decide.",
        "Baseline v0.1",
        "Safe Language Layer",
        "Eternal Baseline",
        "Boundary Cases Matrix",
        "Failure Classification",
        "Consent-Audit Engine",
        "Mechanism-vs-Claim Scanner",
        "Self-Audit Mode",
        "Evidence Lab",
        "World Lens Simulation",
        "Local Witness Receipt v2",
    ]
    for phrase in required:
        assert phrase in text


def test_protocol_guide_keeps_safe_authority_boundaries():
    text = read("docs/protocol_guide.md")
    required = [
        "does not command, enforce, vote, govern, remove leaders",
        "must not validate spiritual authority",
        "Do not use:",
        "The AI has decided.",
        "automatic reset",
        "Human review Disclaimer".replace("Human review", "Human Review"),
    ]
    for phrase in required:
        assert phrase in text


def test_app_and_about_surface_protocol_guide_consolidation():
    app = read("app.py")
    about = read("about_page.py")
    assert "Protocol Guide Consolidation" in app
    assert "ALETHEIA reflects. Humans review. Power stays accountable." in app
    assert "Protocol Guide Consolidation" in about
    assert "Baseline, Safe Language Layer, Eternal Baseline" in about


def test_patch_tracking_and_manifest_include_protocol_guide_items():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    manifest = read("PATCH_43_MANIFEST.txt")
    assert "Patch 43" in status and "Protocol Guide Consolidation" in status
    assert "Patch 43 Notes" in progress
    assert "docs/protocol_guide.md" in manifest
    assert "tests/test_patch_43_protocol_guide.py" in manifest
