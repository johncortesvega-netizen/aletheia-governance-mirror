import ast
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_120_files_exist():
    required = [
        "ui/module_intro.py",
        "tests/test_patch_120_module_intro_extraction_step_2.py",
        "PATCH_120_MANIFEST.txt",
        "PATCH_120_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_module_intro_step_2_helpers_exist_and_import():
    helper = importlib.import_module("ui.module_intro")
    for name in [
        "render_stress_test_scan_intro",
        "render_boundary_cases_intro",
        "render_consent_audit_intro",
    ]:
        assert hasattr(helper, name)
        assert callable(getattr(helper, name))


def test_app_imports_and_calls_step_2_helpers():
    app = read("app.py")
    required = [
        "render_boundary_cases_intro",
        "render_consent_audit_intro",
        "render_boundary_cases_intro(st)",
        "render_consent_audit_intro(st)",
    ]
    for phrase in required:
        assert phrase in app

    assert 'st.info("Boundary cases calibrate the review model.' not in app
    assert 'st.markdown("### Consent-Audit Engine")' not in app


def test_module_intro_step_2_is_copy_only():
    helper = read("ui/module_intro.py")
    forbidden = [
        "selectbox(",
        "slider(",
        "button(",
        "download_button(",
        "session_state",
        "full_report(",
        "simulate(",
        "audit_ai_integrity",
        "scan_privacy_boundary_static",
        "score_",
        "receipt",
        "routing",
        "requests.",
        "urllib",
        "socket",
        "open(",
        "Path(",
    ]
    for phrase in forbidden:
        assert phrase not in helper


def test_patch_120_docs_capture_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_120_MANIFEST.txt",
            "PATCH_120_RECOVERY_NOTE.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "PATCH_STATUS.md",
        ]
    ).lower()
    required = [
        "patch 120",
        "module intro extraction step 2",
        "copy-only",
        "app.py",
        "orchestrator",
        "no scoring",
        "no verdict-routing",
        "no signal-pattern",
        "no signal-weight",
        "no receipt schema",
        "no external calls",
        "no telemetry",
        "no analytics",
        "no storage",
        "no privacy guarantee",
        "no certification",
        "no enforcement",
        "no final truth",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_120_no_forbidden_authority_claims_or_placeholders():
    changed = "\n".join(
        read(rel)
        for rel in [
            "ui/module_intro.py",
            "PATCH_120_MANIFEST.txt",
            "PATCH_120_RECOVERY_NOTE.md",
        ]
    ).lower()
    forbidden = [
        "guarantees privacy",
        "privacy guaranteed",
        "certifies privacy",
        "certifies safety",
        "final truth guaranteed",
        "claims final truth",
        "automatic enforcement",
        "ajustando",
        "afirma",
        "preciso",
        "verwijderen",
        "overmatige",
        "placeholder",
        "todo",
        "fixme",
    ]
    for phrase in forbidden:
        assert phrase not in changed


def test_patch_120_python_files_parse():
    ast.parse(read("ui/module_intro.py"))
    ast.parse(read("app.py"))
