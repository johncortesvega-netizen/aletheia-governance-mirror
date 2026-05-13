import ast
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_119_files_exist():
    required = [
        "ui/module_intro.py",
        "tests/test_patch_119_app_shell_router_refactor_step_6.py",
        "PATCH_119_MANIFEST.txt",
        "PATCH_119_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_module_intro_helper_exists_and_imports():
    helper = importlib.import_module("ui.module_intro")
    assert hasattr(helper, "render_stress_test_scan_intro")
    assert callable(helper.render_stress_test_scan_intro)


def test_app_imports_and_calls_module_intro_helper():
    app = read("app.py")
    assert "from ui.module_intro import render_stress_test_scan_intro" in app
    assert "render_stress_test_scan_intro(st)" in app
    assert 'st.info("Scan my idea is for your own text.' not in app


def test_module_intro_helper_is_copy_only():
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
        "privacy_boundary",
        "World Lens",
        "score_",
        "receipt",
        "signal",
        "routing",
        "requests.",
        "urllib",
        "socket",
        "open(",
        "Path(",
    ]
    for phrase in forbidden:
        assert phrase not in helper


def test_patch_119_boundary_language_remains_non_authoritative():
    combined = "\n".join(
        read(rel)
        for rel in [
            "ui/module_intro.py",
            "PATCH_119_MANIFEST.txt",
            "PATCH_119_RECOVERY_NOTE.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "PATCH_STATUS.md",
        ]
    ).lower()
    required = [
        "patch 119",
        "app shell router refactor step 6",
        "module intro",
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


def test_patch_119_no_forbidden_authority_claims_or_placeholders():
    changed = "\n".join(
        read(rel)
        for rel in [
            "ui/module_intro.py",
            "PATCH_119_MANIFEST.txt",
            "PATCH_119_RECOVERY_NOTE.md",
        ]
    ).lower()
    forbidden = [
        "guarantees privacy",
        "privacy guaranteed",
        "certifies privacy",
        "certified safe",
        "certifies safety",
        "final truth guaranteed",
        "claims final truth",
        "proves final truth",
        "final verdict",
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


def test_patch_119_python_files_parse():
    ast.parse(read("ui/module_intro.py"))
    ast.parse(read("app.py"))
