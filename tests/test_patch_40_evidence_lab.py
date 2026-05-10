from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_evidence_lab_doc_defines_status_levels_and_guardrails():
    text = read("docs/evidence_lab.md")
    for phrase in [
        "Strong evidence",
        "Partial evidence",
        "Weak evidence",
        "No evidence supplied",
        "Extraordinary Claim Protocol",
        "public, testable, non-coercive evidence",
        "must not validate spiritual authority",
        "must not say",
        "This proves divine authority",
    ]:
        assert phrase in text


def test_evidence_lab_prompt_is_safe_and_review_oriented():
    text = read("prompts/evidence_lab_prompt.md")
    for phrase in [
        "Evidence Lab mode",
        "You reflect risks for human review",
        "Treat spiritual, divine, prophetic, alien, neural, metaphysical",
        "unverified unless supported by public, testable, non-coercive evidence",
        "Policy Consequence Audit",
        "You must not say",
        "Guardrails can be removed",
    ]:
        assert phrase in text


def test_app_surfaces_evidence_lab_protocol_without_authority_claims():
    text = read("app.py")
    for phrase in [
        "Evidence status + extraordinary claim protocol",
        "Evidence Lab Review",
        "Unverified extraordinary claim",
        "policy consequences of a claim",
        "must not validate spiritual authority",
        "Audit the consequences. Do not crown the claim.",
    ]:
        assert phrase in text

    forbidden = [
        "This proves divine authority.",
        "Guardrails can be removed.",
        "Human review is unnecessary.",
    ]
    # Forbidden phrases may appear only inside explicit "must not" safe-output contexts.
    for phrase in forbidden:
        assert phrase not in text or "must not" in text[text.find(phrase)-250:text.find(phrase)+50].lower()


def test_patch_status_and_readme_track_patch_40():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    readme = read("README.md")
    for text in [status, progress, readme]:
        assert "Patch 40" in text
    assert "Evidence Lab + Extraordinary Claim Protocol" in status
    assert "tools\\run_patch_checks.bat 40" in progress
    assert "docs/evidence_lab.md" in readme
    assert "prompts/evidence_lab_prompt.md" in readme
