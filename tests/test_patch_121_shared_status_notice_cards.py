import ast
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def parsed_app() -> ast.AST:
    return ast.parse(read("app.py"))


def imports_name(tree: ast.AST, module_name: str, imported_name: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == module_name:
            if any(alias.name == imported_name for alias in node.names):
                return True
    return False


def calls_name(tree: ast.AST, function_name: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == function_name:
                return True
    return False


def test_patch_121_files_exist():
    required = [
        "ui/status_cards.py",
        "tests/test_patch_121_shared_status_notice_cards.py",
        "PATCH_121_MANIFEST.txt",
        "PATCH_121_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_status_cards_helper_exists_and_imports():
    helper = importlib.import_module("ui.status_cards")
    assert hasattr(helper, "render_ai_integrity_boundary_cards")
    assert callable(helper.render_ai_integrity_boundary_cards)


def test_app_imports_and_calls_status_card_helper():
    app = read("app.py")
    tree = parsed_app()
    assert imports_name(tree, "ui.status_cards", "render_ai_integrity_boundary_cards")
    assert calls_name(tree, "render_ai_integrity_boundary_cards")
    assert 'st.caption("Boundary extension: It does not certify models' not in app
    assert 'st.caption("Demo risk examples include phrases' not in app


def test_status_cards_are_copy_only():
    helper = read("ui/status_cards.py")
    forbidden = [
        "selectbox(",
        "slider(",
        "button(",
        "download_button(",
        "session_state",
        "full_report(",
        "simulate(",
        "audit_ai_integrity",
        "audit_ai_integrity_artifact",
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


def test_patch_121_docs_capture_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_121_MANIFEST.txt",
            "PATCH_121_RECOVERY_NOTE.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "PATCH_STATUS.md",
        ]
    ).lower()
    required = [
        "patch 121",
        "shared status",
        "notice cards",
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


def test_patch_121_no_forbidden_authority_claims_or_placeholders():
    changed = "\n".join(
        read(rel)
        for rel in [
            "ui/status_cards.py",
            "PATCH_121_MANIFEST.txt",
            "PATCH_121_RECOVERY_NOTE.md",
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


def test_patch_121_python_files_parse():
    ast.parse(read("ui/status_cards.py"))
    ast.parse(read("app.py"))
