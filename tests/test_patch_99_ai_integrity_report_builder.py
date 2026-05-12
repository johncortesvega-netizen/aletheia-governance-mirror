from pathlib import Path

from core.ai_integrity_mirror import (
    AI_INTEGRITY_REPORT_VERSION,
    audit_ai_integrity_batch,
    build_ai_integrity_report,
    render_ai_integrity_report_text,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_patch_99_report_builder_returns_required_sections():
    batch = audit_ai_integrity_batch(
        "This is a bounded answer with human review, uncertainty, sources, and appeal.\n"
        "---\n"
        "This AI gives the final verdict and automatically denies access without appeal.\n"
        "---\n"
        "API_KEY = \"sk_live_example_secret_1234567890\"\nuser_prompt = input()\neval(user_prompt)",
        artifact_kind="AI output / code snippet",
    )
    report = build_ai_integrity_report(batch["results"])

    assert report["report_mode"] == "AI Integrity Report Builder"
    assert report["report_version"] == AI_INTEGRITY_REPORT_VERSION
    assert report["artifact_count"] == 3
    assert "executive_summary" in report
    assert "risk_distribution" in report
    assert "state_distribution" in report
    assert "top_triggered_categories" in report
    assert "highest_pressure_artifacts" in report
    assert "selected_evidence_snippets" in report
    assert "repair_questions" in report
    assert "non_certification_note" in report
    assert "privacy_note" in report
    assert report["repair_questions"]


def test_patch_99_report_text_contains_non_certification_and_privacy_notes():
    batch = audit_ai_integrity_batch(
        "The model is certified safe and the final authority. No human review is needed.\n"
        "---\n"
        "fetch('https://analytics.example/collect', {method: 'POST'}); local-only no built-in telemetry",
        artifact_kind="AI output",
    )
    report_text = render_ai_integrity_report_text(build_ai_integrity_report(batch["results"]))

    required = [
        "AI INTEGRITY REPORT BUILDER",
        "EXECUTIVE SUMMARY",
        "ARTIFACT COUNT",
        "RISK DISTRIBUTION",
        "TOP TRIGGERED CATEGORIES",
        "SELECTED REDACTED EVIDENCE SNIPPETS",
        "REPAIR QUESTIONS",
        "NON-CERTIFICATION NOTE",
        "PRIVACY NOTE",
        "not AI certification",
        "not model-wide certification",
        "no intended built-in telemetry",
    ]
    for phrase in required:
        assert phrase in report_text


def test_patch_99_docs_status_and_ui_are_wired():
    combined = "\n".join(
        read(path)
        for path in [
            ROOT / "app.py",
            ROOT / "core" / "ai_integrity_mirror.py",
            ROOT / "docs" / "ai_integrity_report_builder.md",
            ROOT / "docs" / "ai_integrity_mirror.md",
            ROOT / "README.md",
            ROOT / "PATCH_STATUS.md",
            ROOT / "docs" / "progress_database.md",
            ROOT / "PATCH_99_MANIFEST.txt",
            ROOT / "PATCH_99_RECOVERY_NOTE.md",
        ]
    )

    for phrase in [
        "Patch 99",
        "AI Integrity Report Builder",
        "build_ai_integrity_report",
        "render_ai_integrity_report_text",
        "executive summary",
        "artifact count",
        "risk distribution",
        "top triggered categories",
        "selected redacted evidence snippets",
        "repair questions",
        "non-certification note",
        "privacy note",
        "tools\\run_patch_checks.bat 99",
    ]:
        assert phrase in combined


def test_patch_99_preserves_boundaries_and_avoids_overclaiming():
    patched_text = "\n".join(
        read(path)
        for path in [
            ROOT / "core" / "ai_integrity_mirror.py",
            ROOT / "docs" / "ai_integrity_report_builder.md",
            ROOT / "docs" / "ai_integrity_mirror.md",
            ROOT / "README.md",
            ROOT / "PATCH_STATUS.md",
            ROOT / "docs" / "progress_database.md",
            ROOT / "PATCH_99_MANIFEST.txt",
            ROOT / "PATCH_99_RECOVERY_NOTE.md",
        ]
    ).lower()

    required_boundaries = [
        "no live model calls",
        "no external calls",
        "static pasted-artifact report only",
        "no vendor ranking",
        "no model-wide certification",
        "no safety guarantee",
        "no security guarantee",
        "no privacy guarantee",
        "no final truth claim",
    ]
    for phrase in required_boundaries:
        assert phrase in patched_text

    forbidden_claims = [
        "certifies models",
        "certifies vendors",
        "guarantees model safety",
        "guarantees security",
        "guarantees privacy",
        "proves model safety",
        "approved by aletheia",
        "calls live models",
        "benchmarks live models automatically",
        "ranks vendors",
    ]
    for phrase in forbidden_claims:
        assert phrase not in patched_text
