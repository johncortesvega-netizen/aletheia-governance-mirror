from pathlib import Path

from core.ai_integrity_mirror import (
    CODE_INTEGRITY_SCAN_VERSION,
    audit_ai_integrity_artifact,
    scan_code_integrity_static,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def detection_names(scan: dict) -> set[str]:
    return {item.get("name") for item in scan.get("detections", [])}


def test_patch_95_code_static_scan_detects_core_code_integrity_categories():
    code = '''
API_KEY = "sk_live_example_token_1234567890"
password = "super-secret-value"
if user.role == "admin": return True
subprocess.run(user_cmd, shell=True)
eval(user_input)
shutil.rmtree(target_path)
requests.post("https://example.test/collect", json={"prompt": user_prompt})
telemetry_event = {"usage_metrics": True}
central_identity_sync(user_id)
auto_deny(application)
'''
    scan = scan_code_integrity_static(code)
    names = detection_names(scan)

    assert scan["scan_mode"] == "Code Integrity Static Scan"
    assert scan["code_integrity_scan_version"] == CODE_INTEGRITY_SCAN_VERSION
    assert "code_exposed_secret" in names
    assert "code_dangerous_execution" in names
    assert "code_hardcoded_admin_bypass" in names
    assert "code_unsafe_deletion" in names
    assert "code_outbound_network_call" in names
    assert "code_telemetry_or_tracking_endpoint" in names
    assert "code_central_logging_or_identity_sync" in names
    assert "code_missing_human_review_gate" in names
    assert scan["missing_human_review_gate"] is True
    assert scan["severity_counts"]["High"] >= 3


def test_patch_95_redacts_secret_evidence_and_returns_review_questions():
    scan = scan_code_integrity_static('token = "abcdefghi123456789"\neval(user_input)')
    joined_evidence = "\n".join(
        snippet
        for item in scan.get("detections", [])
        for snippet in item.get("evidence_snippets", [])
    )
    questions = "\n".join(scan.get("review_questions", []))

    assert "abcdefghi123456789" not in joined_evidence
    assert "[REDACTED]" in joined_evidence
    assert "secrets or tokens" in questions
    assert "dynamic or shell execution" in questions


def test_patch_95_integrates_code_scan_without_changing_ai_integrity_routing_shape():
    result = audit_ai_integrity_artifact(
        'API_KEY = "sk_live_example_token_1234567890"\nrequests.post("https://example.test/telemetry", json=data)',
        artifact_kind="Code snippet",
    )
    code_scan = result.get("code_integrity_static_scan")

    assert result["scan"]["human_review_required"] is True
    assert result["sim"]["authority_claim"] is False
    assert code_scan["scan_mode"] == "Code Integrity Static Scan"
    assert code_scan["detection_count"] >= 2
    assert result["scan"]["code_integrity_static_scan"]["detection_count"] == code_scan["detection_count"]
    assert result["report"]["code_integrity_static_scan"]["detection_count"] == code_scan["detection_count"]


def test_patch_95_ui_docs_manifest_and_status_include_boundaries():
    combined = "\n".join(
        read(path)
        for path in [
            "app.py",
            "README.md",
            "docs/ai_integrity_mirror.md",
            "docs/code_integrity_static_scan.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_95_MANIFEST.txt",
            "PATCH_95_RECOVERY_NOTE.md",
        ]
    )

    for phrase in [
        "Patch 95",
        "Code Integrity Static Scan",
        "exposed secrets",
        "dangerous subprocess/eval usage",
        "hardcoded admin bypass",
        "unsafe deletion",
        "outbound network calls",
        "telemetry-like endpoints",
        "central logging / identity sync",
        "missing human-review gates",
        "No analyzer scoring change",
        "No verdict-routing change",
        "No code execution",
        "No repository crawler",
        "No external calls",
        "No live model benchmarking",
        "No penetration test",
        "No security guarantee",
        "No vulnerability certification",
    ]:
        assert phrase in combined


def test_patch_95_does_not_introduce_security_or_authority_claims():
    patched_text = "\n".join(
        read(path)
        for path in [
            "core/ai_integrity_mirror.py",
            "app.py",
            "README.md",
            "docs/ai_integrity_mirror.md",
            "docs/code_integrity_static_scan.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_95_MANIFEST.txt",
            "PATCH_95_RECOVERY_NOTE.md",
        ]
    ).lower()

    forbidden_claims = [
        "guarantees security",
        "security guaranteed",
        "certifies vulnerabilities",
        "certifies codebases",
        "approved by aletheia",
        "will call external services",
        "runs penetration tests",
    ]
    for phrase in forbidden_claims:
        assert phrase not in patched_text
