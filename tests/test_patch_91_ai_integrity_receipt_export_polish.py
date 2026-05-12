from pathlib import Path

from core.ai_integrity_mirror import (
    AI_INTEGRITY_RECEIPT_VERSION,
    audit_ai_integrity_artifact,
    audit_ai_integrity_batch,
    build_ai_integrity_receipt_context,
    render_ai_integrity_receipt_context_text,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_91_receipt_context_contains_scope_privacy_and_non_certification_notes():
    result = audit_ai_integrity_artifact(
        'API_KEY = "sk_live_example_token_1234567890"\nThis AI gives the final verdict. No human review is needed.',
        artifact_kind="Code snippet",
    )
    context = build_ai_integrity_receipt_context(result)
    text = render_ai_integrity_receipt_context_text(context)

    assert context["receipt_version"] == AI_INTEGRITY_RECEIPT_VERSION
    assert context["receipt_header"] == "AI Integrity Mirror — Static Artifact Review Receipt"
    assert context["artifact_type"] == "Code snippet"
    assert "pasted artifact only" in context["static_review_scope"].lower()
    assert "no built-in telemetry" in context["privacy_boundary"].lower()
    assert "not ai certification" in context["non_certification_note"].lower()
    assert "GENERIC LOCAL WITNESS RECEIPT FOLLOWS" in text
    assert "sk_live_example_token_1234567890" not in text
    assert "[REDACTED]" in text


def test_patch_91_receipt_context_can_include_batch_summary_without_ranking_claim():
    batch = """
    This is a preliminary AI summary. Human review is required and users may appeal.
    ---
    This AI provides the final verdict. No human review is needed and users cannot appeal.
    """
    batch_result = audit_ai_integrity_batch(batch, artifact_kind="AI output")
    result = batch_result["results"][1]
    context = build_ai_integrity_receipt_context(
        result,
        review_mode="batch static artifact",
        batch_summary=batch_result["summary"],
    )
    text = render_ai_integrity_receipt_context_text(context)

    assert "Review mode: batch static artifact" in text
    assert "BATCH SUMMARY" in text
    assert "Artifact count: 2" in text
    assert "not AI certification" in context["non_certification_note"]
    assert "benchmark proof" in context["non_certification_note"]


def test_patch_91_app_download_receipt_uses_ai_integrity_context_prefix():
    app = read("app.py")
    assert "build_ai_integrity_receipt_context" in app
    assert "render_ai_integrity_receipt_context_text" in app
    assert "AI_INTEGRITY_RECEIPT_VERSION" in app
    assert "Receipt export includes AI Integrity scope" in app
    assert "redacted evidence" in app
    assert "prompt_version=AI_INTEGRITY_RECEIPT_VERSION" in app


def test_patch_91_docs_ledgers_and_manifest_capture_receipt_boundary():
    for path in [
        "docs/ai_integrity_mirror.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
        "PATCH_91_MANIFEST.txt",
        "PATCH_91_RECOVERY_NOTE.md",
    ]:
        assert (ROOT / path).exists(), path

    combined = "\n".join(
        read(path)
        for path in [
            "docs/ai_integrity_mirror.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_91_MANIFEST.txt",
            "PATCH_91_RECOVERY_NOTE.md",
        ]
    ).lower()
    for phrase in [
        "patch 91",
        "receipt export polish",
        "static review scope",
        "privacy boundary",
        "non-certification",
        "redacted evidence",
        "no live model benchmarking",
        "no external calls",
        r"tools\run_patch_checks.bat 91",
    ]:
        assert phrase.lower() in combined
