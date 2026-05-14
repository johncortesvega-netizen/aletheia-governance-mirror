import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_132_files_exist():
    required = [
        "docs/start_page_stabilization_checkpoint.md",
        "tests/test_patch_132_start_page_stabilization_checkpoint.py",
        "PATCH_132_MANIFEST.txt",
        "PATCH_132_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_start_gate_remains_session_state_only_and_stops_before_modules():
    app = read("app.py")
    has_start_page_gate = (
        "from ui.start_page import START_GATE_SESSION_KEY, render_start_page" in app
        and "st.session_state.get(START_GATE_SESSION_KEY, False)" in app
        and "render_start_page(st)" in app
        and "st.session_state[START_GATE_SESSION_KEY] = True" in app
    )
    has_unit_preview_gate = (
        "from ui.unit_preview import UNIT_PREVIEW_SESSION_KEY, render_unit_preview" in app
        and "st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False)" in app
        and "render_unit_preview(st)" in app
        and "st.session_state[UNIT_PREVIEW_SESSION_KEY] = True" in app
    )
    assert has_start_page_gate or has_unit_preview_gate
    assert "st.rerun()" in app
    assert "st.stop()" in app

    gate_markers = [
        marker
        for marker in [
            "if not st.session_state.get(START_GATE_SESSION_KEY, False):",
            "if not st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False):",
        ]
        if marker in app
    ]
    assert gate_markers
    gate_index = min(app.index(marker) for marker in gate_markers)
    tabs_index = app.index("st.tabs(APP_NAVIGATION_LABELS)")
    assert gate_index < tabs_index


def test_start_page_helper_has_single_proceed_button_and_no_persistence():
    helper = read("ui/start_page.py")
    tree = ast.parse(helper)
    button_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "button"
    ]
    assert len(button_calls) == 1
    assert "Proceed to ALETHEIA" in helper
    assert "aletheia_start_gate_passed" in helper

    forbidden = [
        "cookies",
        "cookie",
        "localStorage",
        "sessionStorage",
        "write_text",
        "open(",
        "requests.",
        "httpx",
        "urllib",
        "socket",
        "telemetry",
        "analytics",
        "tracking",
        "auth",
        "login",
        "database",
    ]
    lowered = helper.lower()
    for phrase in forbidden:
        assert phrase.lower() not in lowered


def test_normal_app_interface_still_renders_after_gate_passes():
    app = read("app.py")
    required_after_gate = [
        "render_app_header(mascot_logo_uri, APP_VERSION, st)",
        "render_how_to_use_note(st)",
        "render_try_this_first_guide(st, expanded=False)",
        "render_sidebar_brand(mascot_logo_uri, st)",
        "render_sidebar_context(st)",
        "st.tabs(APP_NAVIGATION_LABELS)",
        "with tab_chat:",
        "with tab_sim:",
        "with tab_boundary:",
        "with tab_ai_integrity:",
        "with tab_empirical:",
        "with tab_grid:",
        "with tab_doctrine:",
        "with tab_about:",
    ]
    for phrase in required_after_gate:
        assert phrase in app


def test_patch_132_docs_capture_stabilization_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "docs/start_page_stabilization_checkpoint.md",
            "PATCH_132_MANIFEST.txt",
            "PATCH_132_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
        ]
    ).lower()
    required = [
        "patch 132",
        "start page stabilization checkpoint",
        "session-state-only",
        "no cookies",
        "no persistent storage",
        "no telemetry",
        "no analytics",
        "no auth",
        "no tracking",
        "no scoring",
        "no routing",
        "no receipt schema",
        "no signal",
        "no privacy audit scan behavior change",
        "no ai integrity scan behavior change",
        "no world lens math",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in combined

    forbidden = [
        "privacy guaranteed",
        "guarantees privacy",
        "automatic enforcement",
        "final truth guaranteed",
        "certifies safety",
        "certifies compliance",
    ]
    for phrase in forbidden:
        assert phrase not in combined


def test_patch_132_python_files_parse():
    for rel in [
        "app.py",
        "ui/start_page.py",
        "tests/test_patch_132_start_page_stabilization_checkpoint.py",
    ]:
        ast.parse(read(rel))
