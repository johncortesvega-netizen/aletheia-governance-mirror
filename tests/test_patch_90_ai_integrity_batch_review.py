from pathlib import Path

from core.ai_integrity_mirror import (
    AI_INTEGRITY_BATCH_VERSION,
    audit_ai_integrity_batch,
    split_ai_integrity_batch_input,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_90_batch_splitter_uses_simple_static_delimiters():
    text = "bounded artifact\n---\nopaque artifact\n===\n###\ncode artifact"
    parts = split_ai_integrity_batch_input(text)
    assert parts == ["bounded artifact", "opaque artifact", "code artifact"]


def test_patch_90_batch_review_returns_per_item_readings_and_summary():
    batch = """
    This is a preliminary AI summary. Human review is required and users may appeal.
    ---
    This AI provides the final verdict. No human review is needed and users cannot appeal.
    ---
    API_KEY = "sk_live_example_token_1234567890"
    eval(user_prompt)
    """
    result = audit_ai_integrity_batch(batch, artifact_kind="AI output")

    assert result["batch_version"] == AI_INTEGRITY_BATCH_VERSION
    assert result["summary"]["artifact_count"] == 3
    assert len(result["results"]) == 3
    assert result["summary"]["risk_counts"]["Medium"] >= 1
    assert result["summary"]["highest_pressure_item"] in {2, 3}
    assert "certify systems" in result["summary"]["scope_note"].lower()
    assert "no built-in telemetry" in result["summary"]["privacy_note"].lower()
    assert all(item["batch_item_index"] for item in result["results"])
    assert "sk_live_example_token_1234567890" not in result["results"][2]["batch_item_excerpt"]


def test_patch_90_app_exposes_batch_review_without_benchmark_or_certification_claims():
    app = read("app.py")
    assert "Batch review mode: split pasted artifacts" in app
    assert "AI Integrity Batch Summary" in app
    assert "Batch item details" in app
    assert "audit_ai_integrity_batch" in app
    assert "not live model benchmarking or certification" in app
    assert "Batch comparison is artifact-level review support only" in app


def test_patch_90_docs_and_ledgers_capture_boundary():
    for path in [
        "docs/ai_integrity_mirror.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
        "PATCH_90_MANIFEST.txt",
        "PATCH_90_RECOVERY_NOTE.md",
    ]:
        assert (ROOT / path).exists(), path

    combined = "\n".join(
        read(path)
        for path in [
            "docs/ai_integrity_mirror.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_90_MANIFEST.txt",
            "PATCH_90_RECOVERY_NOTE.md",
        ]
    ).lower()
    for phrase in [
        "patch 90",
        "batch review",
        "pasted artifacts only",
        "no live model benchmarking",
        "no external calls",
        "no certification",
        r"tools\run_patch_checks.bat 90",
    ]:
        assert phrase.lower() in combined
