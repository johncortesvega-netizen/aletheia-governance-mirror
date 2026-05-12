from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "core" / "ai_integrity_mirror.py"
SPEC = importlib.util.spec_from_file_location("patch87_ai_integrity_mirror", MODULE_PATH)
ai_module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = ai_module
SPEC.loader.exec_module(ai_module)

AI_INTEGRITY_DEMO_EXAMPLES = ai_module.AI_INTEGRITY_DEMO_EXAMPLES
audit_ai_integrity_artifact = ai_module.audit_ai_integrity_artifact


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_87_demo_examples_are_centralized_and_cover_core_ai_integrity_cases():
    assert len(AI_INTEGRITY_DEMO_EXAMPLES) >= 5

    titles = {item["title"] for item in AI_INTEGRITY_DEMO_EXAMPLES}
    kinds = {item["artifact_kind"] for item in AI_INTEGRITY_DEMO_EXAMPLES}
    joined = "\n".join(item["text"] + "\n" + item["review_focus"] for item in AI_INTEGRITY_DEMO_EXAMPLES)

    assert "Bounded AI answer with review path" in titles
    assert "Overclaiming automated decision" in titles
    assert "Opaque agent workflow" in titles
    assert "Central identity capture claim" in titles
    assert "Code snippet with exposed secret" in titles
    assert {"AI output", "Agent workflow / spec", "Code snippet", "Model card / safety claim"}.issubset(kinds)
    for phrase in ["human review", "final verdict", "hidden criteria", "global ID", "API_KEY"]:
        assert phrase in joined


def test_patch_87_all_demo_examples_are_auditable_without_external_calls():
    states = set()
    signal_names = set()
    for item in AI_INTEGRITY_DEMO_EXAMPLES:
        result = audit_ai_integrity_artifact(item["text"], artifact_kind=item["artifact_kind"])
        states.add(result["state"])
        signal_names.update(signal["name"] for signal in result["findings"])
        assert result["scan"]["ai_integrity_static_review"] is True
        assert result["scan"]["human_review_required"] is True
        assert "not certification" in result["notice"].lower()
        assert result["artifact_kind"] == item["artifact_kind"]

    assert "SANCTUARY" in states
    assert "ASYLUM" in states or "THRESHOLD" in states
    for expected in [
        "final_authority_claim",
        "automated_enforcement",
        "opacity_or_hidden_logic",
        "surveillance_or_identity_capture",
        "secret_or_token_exposure",
    ]:
        assert expected in signal_names


def test_patch_87_app_uses_shared_demo_examples_and_removes_duplicate_certification_sentence():
    app = read("app.py")
    assert "AI_INTEGRITY_DEMO_EXAMPLES" in app
    assert "Demo focus:" in app
    assert "Suggested type:" in app
    assert "selected_demo[\"text\"]" in app
    assert app.count("It does not certify models, vendors, codebases, prompts, agents, or outputs as safe.") == 1
    assert "It does not certify models, vendors, codebases, prompts, agents, or outputs as safe. It does not certify" not in app


def test_patch_87_documentation_ledgers_and_recovery_are_present():
    for path in [
        "PATCH_87_MANIFEST.txt",
        "PATCH_87_RECOVERY_NOTE.md",
        "docs/ai_integrity_mirror.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]:
        assert (ROOT / path).exists(), path

    doc = read("docs/ai_integrity_mirror.md")
    manifest = read("PATCH_87_MANIFEST.txt")
    recovery = read("PATCH_87_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    for text in [doc, manifest, recovery, status, progress]:
        assert "Patch 87" in text
        assert "AI Integrity Mirror" in text
        assert "demo" in text.lower() or "example" in text.lower()
        assert "not certification" in text.lower() or "does not certify" in text.lower()

    assert r"tools\run_patch_checks.bat 87" in manifest + recovery + status
