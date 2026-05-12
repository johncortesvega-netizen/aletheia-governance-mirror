from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "core" / "ai_integrity_mirror.py"
SPEC = importlib.util.spec_from_file_location("patch88_ai_integrity_mirror", MODULE_PATH)
ai_module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = ai_module
SPEC.loader.exec_module(ai_module)

audit_ai_integrity_artifact = ai_module.audit_ai_integrity_artifact


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_88_findings_include_categories_and_evidence_snippets():
    result = audit_ai_integrity_artifact(
        "The agent gives the final verdict with hidden criteria. "
        "Users cannot appeal, and the score can automatically deny access without review.",
        artifact_kind="Agent workflow / spec",
    )

    findings = result["findings"]
    assert findings
    assert {"category", "evidence_snippets", "description", "hit_count"}.issubset(findings[0])
    categories = {item["category"] for item in findings}
    assert "Authority boundary" in categories
    assert "Transparency" in categories or "Reviewability" in categories
    assert any("final verdict" in " ".join(item["evidence_snippets"]).lower() for item in findings)


def test_patch_88_secret_evidence_is_redacted_before_display_or_receipt_metadata():
    result = audit_ai_integrity_artifact(
        'API_KEY = "sk_live_example_token_1234567890"\nuser_prompt = input()\neval(user_prompt)',
        artifact_kind="Code snippet",
    )

    secret_finding = next(item for item in result["findings"] if item["name"] == "secret_or_token_exposure")
    joined = "\n".join(secret_finding["evidence_snippets"])
    assert "[REDACTED]" in joined
    assert "sk_live_example_token_1234567890" not in joined
    assert secret_finding["category"] == "Code / credential hygiene"


def test_patch_88_app_displays_category_and_redacted_evidence_column():
    app = read("app.py")
    assert '"Category": item.get("category", "General")' in app
    assert '"Evidence snippet": " | ".join(item.get("evidence_snippets", []))' in app
    assert "Credential-like values are redacted" in app


def test_patch_88_documentation_ledgers_and_recovery_are_present():
    for path in [
        "PATCH_88_MANIFEST.txt",
        "PATCH_88_RECOVERY_NOTE.md",
        "docs/ai_integrity_mirror.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert (ROOT / path).exists(), path

    combined = "\n".join(
        read(path)
        for path in [
            "PATCH_88_MANIFEST.txt",
            "PATCH_88_RECOVERY_NOTE.md",
            "docs/ai_integrity_mirror.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
        ]
    )
    for phrase in [
        "Patch 88",
        "AI Integrity Mirror",
        "evidence snippet",
        "redacted",
        "not certification",
        r"tools\run_patch_checks.bat 88",
    ]:
        assert phrase.lower() in combined.lower()
