from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_consent_docs_and_prompt_exist_with_core_rule():
    doc = read("docs/consent_audit_engine.md")
    prompt = read("prompts/consent_audit_prompt.md")
    assert "Consent is only valid when refusal is realistically possible" in doc
    assert "Green — refusal is realistic" in doc
    assert "Yellow — pressure or ambiguity exists" in doc
    assert "Red — consent appears coerced or structurally forced" in doc
    assert "Consent-Audit Report" in prompt
    assert "Can the person realistically say no?" in prompt


def test_app_exposes_consent_audit_engine_without_authority_language():
    app = read("app.py")
    assert "### Consent-Audit Engine" in app
    assert "Consent-Audit Report" in app
    assert "Refusal reality" in app
    assert "Basic-rights dependency check" in app
    assert "This is a mirror output for human review" in app
    assert "The AI has voided the agreement" not in app
    assert "This consent is legally invalid" not in app


def test_about_and_readme_document_consent_layer():
    about = read("about_page.py")
    readme = read("README.md")
    assert "Consent-Audit Engine" in about
    assert "refusal is realistically possible" in about
    assert "docs/consent_audit_engine.md" in readme
    assert "prompts/consent_audit_prompt.md" in readme
    assert "Consent-Audit Engine" in readme


def test_patch_status_and_manifest_track_patch_37():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    manifest = read("PATCH_37_MANIFEST.txt")
    recovery = read("PATCH_37_RECOVERY_NOTE.md")
    assert "| 37 | Consent-Audit Engine | Current |" in status
    assert "Patch 38 — Mechanism-vs-Claim Scanner" in status
    assert "Patch 37 — Consent-Audit Engine — current" in progress
    assert "docs/consent_audit_engine.md" in manifest
    assert "tests/test_patch_37_consent_audit.py" in manifest
    assert "tools\\run_patch_checks.bat 37" in recovery
