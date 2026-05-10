from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_38_docs_and_prompt_exist():
    doc = ROOT / "docs" / "mechanism_vs_claim_scanner.md"
    prompt = ROOT / "prompts" / "mechanism_vs_claim_prompt.md"
    assert doc.exists()
    assert prompt.exists()
    assert "Mechanisms outweigh adjectives" in doc.read_text(encoding="utf-8")
    assert "Mechanism-vs-Claim Scan" in prompt.read_text(encoding="utf-8")


def test_mechanism_vs_claim_safe_language_rules():
    doc = read("docs/mechanism_vs_claim_scanner.md")
    assert "The author is lying" in doc
    assert "The AI has proven bad faith" in doc
    assert "must not" in doc
    assert "human review" in doc.lower()


def test_app_exposes_mechanism_vs_claim_scanner():
    app = read("app.py")
    assert "Mechanism-vs-Claim Scanner" in app
    assert "Ethical language integrity example" in app
    assert "Mechanisms outweigh adjectives" in app
    assert "appeal, audit trail, time limits, correction" in app


def test_patch_status_and_progress_updated():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    assert "| 38 | Mechanism-vs-Claim Scanner | Current |" in status
    assert "Patch 39 — Self-Audit Mode" in status
    assert "Patch 38 — Mechanism-vs-Claim Scanner — current" in progress
    assert "Mechanism-vs-Claim Scanner" in progress
