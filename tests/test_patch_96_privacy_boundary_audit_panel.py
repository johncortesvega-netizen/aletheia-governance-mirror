from pathlib import Path

from core.ai_integrity_mirror import (
    PRIVACY_BOUNDARY_SCAN_VERSION,
    audit_ai_integrity_artifact,
    scan_privacy_boundary_static,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def detection_names(scan: dict) -> set[str]:
    return {item.get("name") for item in scan.get("detections", [])}


def test_patch_96_privacy_boundary_scan_detects_core_categories():
    artifact = '''
import posthog
import sentry_sdk
fetch("https://collector.example.test/api/collect", {body: user_prompt})
requests.post("https://logs.example.test/api/telemetry", json={"usage_metrics": True})
telemetry_event = {"user_behavior": "session_replay"}
db.insert({"prompt": user_prompt})
backend_endpoint = "/api/upload"
# local-only: no built-in telemetry, no trackers, no analytics SDKs, no backend upload
'''
    scan = scan_privacy_boundary_static(artifact)
    names = detection_names(scan)

    assert scan["scan_mode"] == "Privacy Boundary Audit"
    assert scan["privacy_boundary_scan_version"] == PRIVACY_BOUNDARY_SCAN_VERSION
    assert "privacy_analytics_package_hint" in names
    assert "privacy_external_network_pattern" in names
    assert "privacy_telemetry_keyword" in names
    assert "privacy_database_write_hint" in names
    assert "privacy_backend_endpoint_hint" in names
    assert "privacy_local_only_statement" in names
    assert scan["active_signal_count"] >= 5
    assert scan["local_only_statement_present"] is True
    assert scan["privacy_boundary_tension"] is True


def test_patch_96_returns_local_statement_hosting_caveat_and_review_questions():
    scan = scan_privacy_boundary_static('local-only; no built-in telemetry; fetch("https://example.test/api/events")')
    questions = "\n".join(scan.get("review_questions", []))

    assert "no intended built-in telemetry" in scan["local_only_statement"]
    assert "Hosting providers" in scan["hosting_caveat"]
    assert "outside ALETHEIA" in scan["hosting_caveat"]
    assert "outbound calls" in questions or "local-only/no-data-collection" in questions
    assert "privacy guarantee" in scan["non_certification_note"]
    assert "no external calls" in scan["scope_note"]


def test_patch_96_integrates_privacy_audit_without_verdict_routing_change():
    result = audit_ai_integrity_artifact(
        'This tool is local-only and has no analytics SDKs. requests.post("https://example.test/api/telemetry", json=data)',
        artifact_kind="Code snippet",
    )
    audit = result.get("privacy_boundary_audit")

    assert result["scan"]["human_review_required"] is True
    assert result["sim"]["authority_claim"] is False
    assert audit["scan_mode"] == "Privacy Boundary Audit"
    assert audit["detection_count"] >= 2
    assert audit["privacy_boundary_tension"] is True
    assert result["scan"]["privacy_boundary_audit"]["detection_count"] == audit["detection_count"]
    assert result["report"]["privacy_boundary_audit"]["detection_count"] == audit["detection_count"]


def test_patch_96_ui_docs_manifest_and_status_include_boundaries():
    combined = "\n".join(
        read(path)
        for path in [
            "core/ai_integrity_mirror.py",
            "app.py",
            "README.md",
            "docs/ai_integrity_mirror.md",
            "docs/privacy_boundary_audit_panel.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_96_MANIFEST.txt",
            "PATCH_96_RECOVERY_NOTE.md",
        ]
    )

    for phrase in [
        "Patch 96",
        "Privacy Boundary Audit Panel",
        "analytics packages",
        "external network call patterns",
        "telemetry keywords",
        "database write hints",
        "backend endpoint hints",
        "local-only statement",
        "hosting caveat",
        "No analyzer scoring change",
        "No verdict-routing change",
        "No runtime monitoring",
        "No host-log inspection",
        "No dependency crawl",
        "No repository crawler",
        "No external calls",
        "No live model benchmarking",
        "No privacy guarantee",
        "No compliance approval",
        "No vendor audit",
        "No hosting audit",
        "No proof that no data is collected",
    ]:
        assert phrase in combined


def test_patch_96_does_not_introduce_privacy_or_authority_overclaims():
    patched_text = "\n".join(
        read(path)
        for path in [
            "core/ai_integrity_mirror.py",
            "app.py",
            "README.md",
            "docs/ai_integrity_mirror.md",
            "docs/privacy_boundary_audit_panel.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_96_MANIFEST.txt",
            "PATCH_96_RECOVERY_NOTE.md",
        ]
    ).lower()

    forbidden_claims = [
        "guarantees privacy",
        "privacy guaranteed",
        "certifies privacy",
        "proves no data is collected",
        "approved by aletheia",
        "will call external services",
        "monitors runtime behavior",
        "audits hosting providers",
    ]
    for phrase in forbidden_claims:
        assert phrase not in patched_text
