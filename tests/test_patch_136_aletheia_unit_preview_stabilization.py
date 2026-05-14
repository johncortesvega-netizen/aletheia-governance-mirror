import ast
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_136_files_exist():
    required = [
        "docs/aletheia_unit_preview_stabilization.md",
        "tests/test_patch_136_aletheia_unit_preview_stabilization.py",
        "PATCH_136_MANIFEST.txt",
        "PATCH_136_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_unit_preview_gate_still_stops_before_normal_tabs():
    app = read("app.py")
    gate = "if not st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False):"
    tabs = "st.tabs(APP_NAVIGATION_LABELS)"
    assert gate in app
    assert "render_unit_preview(st)" in app
    assert "st.session_state[UNIT_PREVIEW_SESSION_KEY] = True" in app
    assert "st.rerun()" in app
    assert "st.stop()" in app
    assert app.index(gate) < app.index(tabs)


def test_normal_app_surface_still_exists_after_gate():
    app = read("app.py")
    required = [
        "render_app_header(mascot_logo_uri, APP_VERSION, st)",
        "render_how_to_use_note(st)",
        "render_try_this_first_guide(st, expanded=False)",
        "render_sidebar_brand(mascot_logo_uri, st)",
        "render_sidebar_context(st)",
        "render_receipt_reader_standard_view(st)",
        "with tab_chat:",
        "with tab_sim:",
        "with tab_boundary:",
        "with tab_ai_integrity:",
        "with tab_empirical:",
        "with tab_grid:",
        "with tab_receipt_reader:",
        "with tab_doctrine:",
        "with tab_about:",
    ]
    for phrase in required:
        assert phrase in app


def test_suggest_review_path_is_pure_local_suggestion_logic():
    preview = importlib.import_module("ui.unit_preview")
    helper = read("ui/unit_preview.py")
    tree = ast.parse(helper)
    imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
    imported_text = "\n".join(ast.get_source_segment(helper, node) or "" for node in imports)
    assert "core." not in imported_text
    assert "requests" not in imported_text

    for sample in [
        "Receipt fingerprint: abc",
        "System prompt for model output",
        "Scenario under pressure",
        "CSV dataset source",
        "Country year governance context",
        "Should I review this?",
        "Short claim",
    ]:
        suggestion = preview.suggest_review_path(sample)
        assert set(suggestion) == {"path", "reason"}
        assert suggestion["path"]
        assert suggestion["reason"]


def test_unit_preview_does_not_mutate_receipts_or_call_engines():
    helper = read("ui/unit_preview.py").lower()
    forbidden = [
        "full_report(",
        "simulate(",
        "audit_ai_integrity",
        "scan_privacy_boundary_static",
        "build_local_witness_receipt",
        "render_local_witness_receipt_text",
        "download_button",
        "file_uploader",
        "pd.read_csv",
        "score_",
        "verdict routing",
        "receipt_schema",
        "requests.",
        "httpx",
        "urllib",
        "socket",
        "openai",
        "ollama",
        "embedding",
        "database",
        "telemetry",
        "analytics",
        "tracking",
        "global id",
        "public ledger",
    ]
    for phrase in forbidden:
        assert phrase not in helper


def test_patch_136_docs_capture_checkpoint_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "docs/aletheia_unit_preview_stabilization.md",
            "PATCH_136_MANIFEST.txt",
            "PATCH_136_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
            "docs/architecture.md",
        ]
    ).lower()
    required = [
        "patch 136",
        "aletheia unit preview stabilization",
        "front-door suggestion layer only",
        "session key",
        "aletheia_unit_preview_passed",
        "no scoring",
        "no verdict routing",
        "no receipt schema",
        "no receipt generation",
        "no signal regex",
        "no signal weights",
        "no ai integrity scan behavior",
        "no privacy audit scan behavior",
        "no world lens math",
        "no uploads/downloads",
        "no external calls",
        "no telemetry",
        "no analytics",
        "human judgment remains required",
    ]
    for phrase in required:
        assert phrase in combined

    forbidden_claims = [
        "privacy guaranteed",
        "guarantees privacy",
        "automatic enforcement",
        "final truth guaranteed",
        "certifies compliance",
        "compliance certified",
    ]
    for phrase in forbidden_claims:
        assert phrase not in combined


def test_patch_136_python_files_parse():
    for rel in [
        "app.py",
        "ui/unit_preview.py",
        "tests/test_patch_136_aletheia_unit_preview_stabilization.py",
    ]:
        ast.parse(read(rel))
