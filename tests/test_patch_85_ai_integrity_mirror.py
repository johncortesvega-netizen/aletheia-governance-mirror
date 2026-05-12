from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "core" / "ai_integrity_mirror.py"
SPEC = importlib.util.spec_from_file_location("patch85_ai_integrity_mirror", MODULE_PATH)
ai_module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = ai_module
SPEC.loader.exec_module(ai_module)

AI_INTEGRITY_NOTICE = ai_module.AI_INTEGRITY_NOTICE
AI_INTEGRITY_RUBRIC_VERSION = ai_module.AI_INTEGRITY_RUBRIC_VERSION
audit_ai_integrity_artifact = ai_module.audit_ai_integrity_artifact


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_85_static_analyzer_routes_overclaiming_ai_to_asylum_or_threshold():
    text = (
        "This AI provides the final verdict. No human review is needed. "
        "The system can automatically deny access and blacklist users without appeal "
        "because the model is certified safe and compliant."
    )
    result = audit_ai_integrity_artifact(text, artifact_kind="AI output")

    assert result["state"] in {"ASYLUM", "THRESHOLD"}
    assert result["risk"] in {"High", "Medium"}
    assert result["scan"]["human_review_required"] is True
    assert result["scan"]["authority_claim"] is True
    assert result["sim"]["authority_claim"] is False
    assert result["sim"]["human_review_required"] is True
    assert any("final_authority_claim" == item["name"] for item in result["findings"])
    assert any("automated_enforcement" == item["name"] for item in result["findings"])
    assert "certification" in result["notice"].lower()


def test_patch_85_static_analyzer_detects_code_secret_and_unsafe_execution():
    code = 'API_KEY = "sk_live_example_token_1234567890"\nuser_prompt = input()\neval(user_prompt)'
    result = audit_ai_integrity_artifact(code, artifact_kind="Code snippet")

    names = {item["name"] for item in result["findings"]}
    assert "secret_or_token_exposure" in names
    assert "unsafe_execution_or_network" in names
    assert result["state"] in {"ASYLUM", "THRESHOLD"}
    assert any("secrets" in question.lower() for question in result["report"]["repair_questions"])


def test_patch_85_bounded_ai_output_can_remain_low_risk_internal_reading():
    text = (
        "This is a preliminary AI summary, not legal, medical, political, religious, "
        "or official advice. Human review is required before reliance. Evidence is incomplete, "
        "affected people should have an appeal path, and an independent reviewer can challenge the output."
    )
    result = audit_ai_integrity_artifact(text, artifact_kind="AI output")

    assert result["state"] == "SANCTUARY"
    assert result["risk"] == "Low"
    assert result["report"]["integrity"] >= 0.80
    assert result["scan"]["positive_review_signal_count"] >= 3
    assert result["report"]["authority_claim"] is False
    assert result["report"]["human_review_required"] is True


def test_patch_85_app_wires_ai_integrity_tab_and_copy_without_certification_claim():
    app = read("app.py")

    assert "🤖 AI Integrity Mirror" in app
    assert "tab_ai_integrity" in app
    assert "audit_ai_integrity_artifact" in app
    assert "Run AI Integrity Mirror" in app
    assert "Static review only: no live model benchmarking" in app
    assert "It does not certify models, vendors, codebases, or outputs as safe." in app
    assert "AI Integrity Mirror for AI/code artifacts" in app
    assert "local witness receipt" in app.lower()
    assert "certify models" in app.lower()
    assert "certifies models" not in app.lower()
    assert "certified safe" in app  # demo risk text only


def test_patch_85_documentation_and_ledgers_present():
    for path in [
        "docs/ai_integrity_mirror.md",
        "PATCH_85_MANIFEST.txt",
        "PATCH_85_RECOVERY_NOTE.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert (ROOT / path).exists(), path

    doc = read("docs/ai_integrity_mirror.md")
    manifest = read("PATCH_85_MANIFEST.txt")
    recovery = read("PATCH_85_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    for text in (doc, manifest, recovery):
        assert "AI Integrity Mirror" in text
        assert "not certify" in text.lower() or "not certification" in text.lower()
        assert "live model benchmarking" in text.lower()

    assert "Patch 85" in status
    assert "AI Integrity Mirror Scaffold" in status
    assert "Patch 85" in progress
    assert "AI Integrity Mirror Scaffold" in progress
    assert r"tools\run_patch_checks.bat 85" in manifest + recovery + status


def test_patch_85_notice_and_rubric_are_explicitly_static_and_non_authoritative():
    assert AI_INTEGRITY_RUBRIC_VERSION == "ai-integrity-v0.1-static"
    lowered = AI_INTEGRITY_NOTICE.lower()
    for phrase in [
        "static review aid",
        "internal governance-integrity risk reading",
        "not certification",
        "final truth",
        "enforcement decision",
    ]:
        assert phrase in lowered
