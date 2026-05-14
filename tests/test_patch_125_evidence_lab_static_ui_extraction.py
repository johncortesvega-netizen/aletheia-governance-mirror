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


def test_patch_125_files_exist():
    required = [
        "pages_ui/evidence_lab_page.py",
        "docs/evidence_lab_static_ui_extraction.md",
        "tests/test_patch_125_evidence_lab_static_ui_extraction.py",
        "PATCH_125_MANIFEST.txt",
        "PATCH_125_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_evidence_lab_helper_is_importable():
    helper = importlib.import_module("pages_ui.evidence_lab_page")
    assert hasattr(helper, "render_evidence_lab_intro")
    assert hasattr(helper, "render_evidence_lab_public_data_build_intro")
    assert callable(helper.render_evidence_lab_intro)
    assert callable(helper.render_evidence_lab_public_data_build_intro)


def test_app_imports_and_calls_evidence_lab_helpers():
    app = read("app.py")
    tree = parsed_app()
    for function_name in [
        "render_evidence_lab_intro",
        "render_evidence_lab_public_data_build_intro",
    ]:
        assert imports_name(tree, "pages_ui.evidence_lab_page", function_name)
        assert calls_name(tree, function_name)

    evidence_section = app.split("with tab_empirical:", 1)[1].split("with tab_grid:", 1)[0]
    assert "render_evidence_lab_intro(st)" in evidence_section
    assert "render_evidence_lab_public_data_build_intro(st)" in evidence_section
    assert 'st.subheader("Evidence Lab' not in evidence_section
    assert 'st.markdown("### Build a country-year table from public data")' not in evidence_section


def test_evidence_lab_helper_contains_static_copy():
    helper = read("pages_ui/evidence_lab_page.py")
    required = [
        "Evidence Lab",
        "Data Check",
        "Build or upload a country-year evidence table from public sources",
        "symbolic doctrine meets public evidence",
        "Evidence does not come from ALETHEIA",
        "World Bank WGI",
        "population for country-level allocation",
        "V-Dem and trust",
        "modern era from 1996 onward",
    ]
    for phrase in required:
        assert phrase in helper


def test_evidence_lab_helper_is_copy_only():
    helper = read("pages_ui/evidence_lab_page.py")
    forbidden = [
        "file_uploader(",
        "button(",
        "download_button(",
        "selectbox(",
        "checkbox(",
        "session_state",
        "read_public_data_upload",
        "build_master_from_public_uploads",
        "public_upload_diagnostics",
        "prepare_empirical_frame",
        "score_empirical_frame",
        "validation_summary",
        "build_local_witness",
        "render_local_witness_receipt_text",
        "pd.",
        "go.",
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


def test_evidence_processing_stays_in_app_py():
    app = read("app.py")
    required = [
        "st.file_uploader(",
        "Build master CSV from uploads",
        "read_public_data_upload",
        "build_master_from_public_uploads",
        "public_upload_diagnostics",
        "prepare_empirical_frame",
        "score_empirical_frame",
        "validation_summary",
        "st.download_button(",
        "st.session_state",
    ]
    for phrase in required:
        assert phrase in app


def test_patch_125_docs_capture_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "docs/evidence_lab_static_ui_extraction.md",
            "PATCH_125_MANIFEST.txt",
            "PATCH_125_RECOVERY_NOTE.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "PATCH_STATUS.md",
        ]
    ).lower()
    required = [
        "patch 125",
        "evidence lab static ui extraction",
        "pages_ui/evidence_lab_page.py",
        "app.py",
        "orchestrator",
        "no evidence processing",
        "no upload handling",
        "no dataframe logic",
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


def test_patch_125_no_authority_claims_or_repair_notes():
    changed = "\n".join(
        read(rel)
        for rel in [
            "pages_ui/evidence_lab_page.py",
            "docs/evidence_lab_static_ui_extraction.md",
            "PATCH_125_MANIFEST.txt",
            "PATCH_125_RECOVERY_NOTE.md",
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


def test_patch_125_python_files_parse():
    for rel in [
        "app.py",
        "pages_ui/evidence_lab_page.py",
        "tests/test_patch_125_evidence_lab_static_ui_extraction.py",
    ]:
        ast.parse(read(rel))
