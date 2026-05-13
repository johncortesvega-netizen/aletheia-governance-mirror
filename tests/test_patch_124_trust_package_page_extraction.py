import ast
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_124_files_exist():
    required = [
        "pages_ui/trust_package_page.py",
        "docs/trust_package_page_extraction.md",
        "tests/test_patch_124_trust_package_page_extraction.py",
        "PATCH_124_MANIFEST.txt",
        "PATCH_124_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_trust_package_helper_is_importable():
    helper = importlib.import_module("pages_ui.trust_package_page")
    assert hasattr(helper, "render_public_trust_package_page")
    assert callable(helper.render_public_trust_package_page)
    assert hasattr(helper, "TRUST_PACKAGE_REVIEW_PATH")
    assert len(helper.TRUST_PACKAGE_REVIEW_PATH) >= 7


def test_app_imports_and_calls_trust_package_helper():
    app = read("app.py")
    assert "from pages_ui.trust_package_page import render_public_trust_package_page" in app
    assert "render_public_trust_package_page(st)" in app
    protocol_section = app.split("with tab_doctrine:", 1)[1].split("with tab_about:", 1)[0]
    assert "render_public_trust_package_page(st)" in protocol_section


def test_trust_package_helper_points_to_docs_as_source_of_truth():
    helper = read("pages_ui/trust_package_page.py")
    required = [
        "docs/public_trust_package.md",
        "docs/public_review_checklist.md",
        "docs/BOUNDARY.md",
        "docs/privacy_boundary.md",
        "docs/hosting_limits.md",
        "docs/signal_detection.md",
        "docs/SIGNAL_DICTIONARY.md",
        "docs/patch_index.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
        "source of truth remains the documentation",
        "review route, not a certification package",
        "ALETHEIA surfaces signals. Humans keep the judgment.",
    ]
    for phrase in required:
        assert phrase in helper


def test_trust_package_helper_is_display_only():
    helper = read("pages_ui/trust_package_page.py")
    forbidden = [
        "st.selectbox(",
        "st.slider(",
        "st.button(",
        "st.download_button(",
        "session_state",
        "full_report(",
        "simulate(",
        "audit_ai_integrity(",
        "audit_ai_integrity_artifact(",
        "scan_privacy_boundary_static(",
        "build_local_witness_receipt(",
        "render_local_witness_receipt_text(",
        "requests.",
        "httpx",
        "urllib",
        "socket",
        "openai",
        "read_text(",
        "write_text(",
        "open(",
    ]
    for phrase in forbidden:
        assert phrase not in helper


def test_patch_124_docs_capture_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "docs/trust_package_page_extraction.md",
            "PATCH_124_MANIFEST.txt",
            "PATCH_124_RECOVERY_NOTE.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "PATCH_STATUS.md",
        ]
    ).lower()
    required = [
        "patch 124",
        "trust package page extraction",
        "pages_ui/trust_package_page.py",
        "app.py",
        "orchestrator",
        "docs/public_trust_package.md",
        "docs/public_review_checklist.md",
        "no scoring",
        "no verdict-routing",
        "no signal-pattern",
        "no signal-weight",
        "no receipt schema",
        "no module-routing",
        "no session-state",
        "no external calls",
        "no telemetry",
        "no analytics",
        "no privacy guarantee",
        "no certification",
        "no enforcement",
        "no final truth",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_124_no_authority_claims_or_repair_notes():
    changed = "\n".join(
        read(rel)
        for rel in [
            "pages_ui/trust_package_page.py",
            "docs/trust_package_page_extraction.md",
            "PATCH_124_MANIFEST.txt",
            "PATCH_124_RECOVERY_NOTE.md",
        ]
    ).lower()
    forbidden = [
        "guarantees privacy",
        "privacy guaranteed",
        "certifies privacy",
        "certifies safety",
        "final truth guaranteed",
        "automatic enforcement",
        "placeholder",
        "todo",
        "fixme",
        "ajustando",
        "afirma",
        "preciso",
        "verwijderen",
        "overmatige",
    ]
    for phrase in forbidden:
        assert phrase not in changed


def test_patch_124_python_files_parse():
    for rel in [
        "app.py",
        "pages_ui/trust_package_page.py",
        "tests/test_patch_124_trust_package_page_extraction.py",
    ]:
        ast.parse(read(rel))
