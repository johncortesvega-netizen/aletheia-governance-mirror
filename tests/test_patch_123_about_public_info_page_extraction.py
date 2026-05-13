import ast
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_123_files_exist():
    required = [
        "pages_ui/__init__.py",
        "pages_ui/about_page.py",
        "docs/about_public_info_page_extraction.md",
        "tests/test_patch_123_about_public_info_page_extraction.py",
        "PATCH_123_MANIFEST.txt",
        "PATCH_123_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_about_page_helper_is_importable():
    helper = importlib.import_module("pages_ui.about_page")
    assert hasattr(helper, "render_about_public_info_page")
    assert callable(helper.render_about_public_info_page)


def test_app_imports_and_calls_about_page_helper():
    app = read("app.py")
    assert "from pages_ui.about_page import render_about_public_info_page" in app
    assert "with tab_about:" in app
    assert "render_about_public_info_page(st, header_image=resolve_about_header_image())" in app
    assert 'st.subheader("Why ALETHEIA")' not in app
    assert 'with st.expander("Positioning: not enterprise compliance, not fairness library"' not in app


def test_about_page_helper_keeps_public_copy():
    helper = read("pages_ui/about_page.py")
    required = [
        "Why ALETHEIA",
        "ALETHEIA helps review governance risk, evidence gaps, and safeguard needs. It reflects; people decide.",
        "validate spiritual authority, confirm extraordinary claims, or replace human judgment",
        "without assigning blame, issuing commands, or claiming final authority",
        "raw/internal taxonomy label",
        "Those labels are compatibility labels for review workflows.",
        "not legal, political, medical, religious, moral, or predictive verdicts",
        "World Lens is a **comparison and exposure model**",
        "not a real election, government, sovereign body, authority mechanism, political mandate, Global ID system, or real 9k body",
        "Humility / Z-axis boundary",
        "no code, receipt, metric, hash, tree, 9k structure, institution, person, or model reaches final authority",
        "Protocol integrity layer",
        "ALETHEIA is built for review, correction, and humility",
    ]
    for phrase in required:
        assert phrase in helper


def test_about_page_helper_remains_display_only():
    helper = read("pages_ui/about_page.py")
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
    ]
    for phrase in forbidden:
        assert phrase not in helper


def test_patch_123_docs_capture_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "docs/about_public_info_page_extraction.md",
            "PATCH_123_MANIFEST.txt",
            "PATCH_123_RECOVERY_NOTE.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "PATCH_STATUS.md",
        ]
    ).lower()
    required = [
        "patch 123",
        "about / public info page extraction",
        "pages_ui/about_page.py",
        "app.py",
        "orchestrator",
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


def test_patch_123_no_authority_claims_or_repair_notes():
    changed = "\n".join(
        read(rel)
        for rel in [
            "pages_ui/about_page.py",
            "docs/about_public_info_page_extraction.md",
            "PATCH_123_MANIFEST.txt",
            "PATCH_123_RECOVERY_NOTE.md",
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


def test_patch_123_python_files_parse():
    for rel in [
        "app.py",
        "pages_ui/about_page.py",
        "tests/test_patch_122_refactor_stabilization_checkpoint_2.py",
        "tests/test_patch_123_about_public_info_page_extraction.py",
    ]:
        ast.parse(read(rel))
