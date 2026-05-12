from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "core" / "ai_integrity_mirror.py"
SPEC = importlib.util.spec_from_file_location("patch86_ai_integrity_mirror", MODULE_PATH)
ai_module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = ai_module
SPEC.loader.exec_module(ai_module)

audit_ai_integrity_artifact = ai_module.audit_ai_integrity_artifact
AI_INTEGRITY_RUBRIC_VERSION = ai_module.AI_INTEGRITY_RUBRIC_VERSION
AI_INTEGRITY_COPY_VERSION = ai_module.AI_INTEGRITY_COPY_VERSION
AI_INTEGRITY_SCOPE_NOTE = ai_module.AI_INTEGRITY_SCOPE_NOTE
AI_INTEGRITY_RECEIPT_NOTE = ai_module.AI_INTEGRITY_RECEIPT_NOTE
AI_INTEGRITY_RELIANCE_NOTE = ai_module.AI_INTEGRITY_RELIANCE_NOTE


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_86_core_exposes_static_scope_receipt_and_reliance_notes():
    assert AI_INTEGRITY_RUBRIC_VERSION == "ai-integrity-v0.1-static"
    assert AI_INTEGRITY_COPY_VERSION == "static-receipt-polish-v0.2"
    assert "pasted artifact only" in AI_INTEGRITY_SCOPE_NOTE.lower()
    assert "does not test a live model" in AI_INTEGRITY_SCOPE_NOTE.lower()
    assert "review evidence" in AI_INTEGRITY_RECEIPT_NOTE.lower()
    assert "not certification" in AI_INTEGRITY_RECEIPT_NOTE.lower()
    assert "human review" in AI_INTEGRITY_RELIANCE_NOTE.lower()
    assert "outside ALETHEIA" in AI_INTEGRITY_RELIANCE_NOTE


def test_patch_86_analyzer_carries_copy_polish_into_scan_report_and_receipt_context():
    text = "This AI answer is uncertain. Human review is required before reliance, and sources should be checked."
    result = audit_ai_integrity_artifact(text, artifact_kind="AI output")

    for container in [result, result["scan"], result["report"]]:
        joined = " ".join(str(value) for value in container.values())
        assert "pasted artifact" in joined.lower()
        assert "not certification" in joined.lower() or "not certify" in joined.lower()
        assert "human review" in joined.lower()

    assert result["scan"]["ai_integrity_scope_note"] == AI_INTEGRITY_SCOPE_NOTE
    assert result["report"]["ai_integrity_receipt_note"] == AI_INTEGRITY_RECEIPT_NOTE
    assert result["receipt_note"] == AI_INTEGRITY_RECEIPT_NOTE
    assert result["scope_note"] == AI_INTEGRITY_SCOPE_NOTE
    assert result["reliance_note"] == AI_INTEGRITY_RELIANCE_NOTE


def test_patch_86_app_copy_uses_reading_and_scope_language_not_certification_language():
    app = read("app.py")

    assert "AI Integrity Mirror — Static Review, Not Certification" in app
    assert "pasted artifact only" in app
    assert "Pasted artifact in, local risk reading out" in app
    assert "How to read this result" in app
    assert "Risk reading" in app
    assert "Integrity reading" in app
    assert "Capture pressure" in app
    assert "not a public certification grade" in app
    assert "It does not certify models, vendors, codebases, prompts, agents, or outputs as safe." in app
    assert "Local AI Integrity receipt" in app
    assert "receipt_note" in app
    assert "certifies models" not in app.lower()


def test_patch_86_documentation_ledgers_and_recovery_are_present():
    for path in [
        "PATCH_86_MANIFEST.txt",
        "PATCH_86_RECOVERY_NOTE.md",
        "docs/ai_integrity_mirror.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert (ROOT / path).exists(), path

    doc = read("docs/ai_integrity_mirror.md")
    manifest = read("PATCH_86_MANIFEST.txt")
    recovery = read("PATCH_86_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    for text in [doc, manifest, recovery, status, progress]:
        assert "Patch 86" in text
        assert "AI Integrity Mirror" in text
        assert "not certification" in text.lower() or "does not certify" in text.lower()

    assert r"tools\run_patch_checks.bat 86" in manifest + recovery + status
    assert "static-receipt-polish" in doc + manifest + recovery
    assert "copy_version" in read("core/ai_integrity_mirror.py")
