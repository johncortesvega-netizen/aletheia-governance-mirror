from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_39_docs_and_prompt_exist():
    doc = ROOT / "docs" / "self_audit_mode.md"
    prompt = ROOT / "prompts" / "self_audit_prompt.md"
    assert doc.exists()
    assert prompt.exists()
    assert "No founder, architect, prompt, rubric, model, document, baseline, report, or output is above the mirror" in doc.read_text(encoding="utf-8")
    assert "Self-Audit Mode" in prompt.read_text(encoding="utf-8")


def test_self_audit_safe_language_rules():
    doc = read("docs/self_audit_mode.md")
    assert "ALETHEIA is objectively pure" in doc
    assert "The founder is validated" in doc
    assert "Human review is unnecessary" in doc
    assert "must not say" in doc
    assert "Self-audit is a credibility layer, not a certificate of purity" in doc


def test_app_exposes_self_audit_mode():
    app = read("app.py")
    assert "Self-Audit Mode" in app
    assert "Self-audit risk example" in app
    assert "founder capture" in app.lower()
    assert "not proof of correctness" in app
    assert "No founder, architect, prompt, rubric, model, document, or output is above the mirror" in app


def test_patch_status_and_progress_updated():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    assert "| 39 | Self-Audit Mode | Current |" in status
    assert "Patch 40 — Evidence Lab Hardening" in status
    assert "Patch 39 — Self-Audit Mode — current" in progress
    assert "Self-Audit Mode" in progress
