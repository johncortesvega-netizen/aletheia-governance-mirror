import json
import shutil
from pathlib import Path

from core.protocol_baseline_self_audit import (
    PROTOCOL_BASELINE_AUDIT_VERSION,
    audit_protocol_baseline,
    render_protocol_baseline_audit_text,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_patch_101_manifest_and_current_baseline_match():
    report = audit_protocol_baseline(ROOT)

    assert report["audit_mode"] == "Human-Auditable Protocol Baseline Self-Audit"
    assert report["audit_version"] == PROTOCOL_BASELINE_AUDIT_VERSION
    assert report["watched_file_count"] >= 10
    assert report["difference_count"] == 0
    assert report["status_counts"]["MATCHES_BASELINE"] == report["watched_file_count"]
    assert report["release_requires_human_review"] is True
    assert "Only humans can audit" in report["human_review_required_note"]


def test_patch_101_detects_modified_missing_and_unknown_files(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    (project / "watched.txt").write_text("base", encoding="utf-8")
    manifest = {
        "manifest_version": "test",
        "baseline_id": "test-baseline",
        "scope_note": "test scope",
        "files": {
            "watched.txt": "cae662172fd450bb0cd710a769079c05bfc5d8e35efa6576edc7d0377afdd4a2",
            "missing.txt": "0" * 64,
        },
    }
    manifest_path = project / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    (project / "watched.txt").write_text("changed", encoding="utf-8")
    (project / "unknown.txt").write_text("new", encoding="utf-8")
    report = audit_protocol_baseline(project, manifest_path, include_unknown=True)
    statuses = {row["path"]: row["status"] for row in report["rows"]}

    assert statuses["watched.txt"] == "MODIFIED_REQUIRES_HUMAN_REVIEW"
    assert statuses["missing.txt"] == "MISSING_REQUIRES_HUMAN_REVIEW"
    assert statuses["unknown.txt"] == "UNKNOWN_FILE_REQUIRES_HUMAN_REVIEW"
    assert report["difference_requires_human_review"] is True


def test_patch_101_text_report_and_docs_preserve_human_audit_boundary():
    report_text = render_protocol_baseline_audit_text(audit_protocol_baseline(ROOT))
    combined = "\n".join(
        read(path)
        for path in [
            ROOT / "docs" / "protocol_baseline_self_audit.md",
            ROOT / "docs" / "go_live_privacy_review_statement.md",
            ROOT / "README.md",
            ROOT / "PATCH_STATUS.md",
            ROOT / "docs" / "progress_database.md",
            ROOT / "PATCH_101_MANIFEST.txt",
            ROOT / "PATCH_101_RECOVERY_NOTE.md",
            ROOT / "core" / "protocol_baseline_self_audit.py",
        ]
    )

    for phrase in [
        "Human-Auditable Protocol Baseline Self-Audit",
        "MATCHES_BASELINE",
        "MODIFIED_REQUIRES_HUMAN_REVIEW",
        "MISSING_REQUIRES_HUMAN_REVIEW",
        "UNKNOWN_FILE_REQUIRES_HUMAN_REVIEW",
        "Only humans can audit",
        "not tamper-proof",
        "not automated approval",
        "not a security guarantee",
        "not a privacy guarantee",
        "not certification",
        "No built-in analytics SDK import",
        "hosting",
    ]:
        assert phrase in combined or phrase in report_text


def test_patch_101_does_not_add_live_calls_or_active_telemetry_dependencies():
    python_source = "\n".join(
        read(path)
        for path in [
            ROOT / "app.py",
            ROOT / "about_page.py",
            ROOT / "protocol.py",
            ROOT / "core" / "ai_integrity_mirror.py",
            ROOT / "core" / "protocol_baseline_self_audit.py",
        ]
        if path.exists()
    ).lower()
    package_config = "\n".join(
        read(path)
        for path in [ROOT / "package.json", ROOT / "capacitor.config.json"]
        if path.exists()
    ).lower()

    # Pattern strings inside the static scanner are allowed; active imports/dependencies are not.
    for phrase in ["import requests", "import httpx", "import posthog", "import sentry_sdk"]:
        assert phrase not in python_source
    for phrase in ["google-analytics", "segment.com", "mixpanel", "amplitude", "hotjar", "fullstory", "logrocket", "posthog", "sentry"]:
        assert phrase not in package_config

    boundary_text = "\n".join(
        read(path)
        for path in [
            ROOT / "docs" / "go_live_privacy_review_statement.md",
            ROOT / "docs" / "protocol_baseline_self_audit.md",
            ROOT / "PATCH_STATUS.md",
        ]
    ).lower()
    assert "static repository review only" in boundary_text
    assert "human review remains required" in boundary_text
