"""Patch 262/263 controlled-router contracts.

Patch 262 froze the current app.py routing behavior before extraction.
Patch 263 moves selected-page resolution and dispatch into ui/main.py while
keeping app.py as the Streamlit entrypoint and preserving labels, state key,
Receipt Reader placement, and dispatch targets.
"""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EXPECTED_NAVIGATION_LABELS = [
    "🪞 Mirror Check",
    "🚀 Stress Test",
    "📊 Evidence Lab",
    "🌐 World Lens",
    "🧭 Boundary Cases",
    "📜 Protocol Guide",
    "ℹ️ Why ALETHEIA",
]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _literal_assignment(source: str, name: str):
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise AssertionError(f"{name} assignment not found")


def test_patch_262_documents_routing_extraction_prep():
    doc = read("docs/routing_extraction_prep_patch_262.md")

    assert "Patch 262 — Routing Extraction Prep" in doc
    assert "key=\"aletheia_active_module\"" in doc
    assert "Why ALETHEIA → Support utilities → Receipt Reader — Standard View" in doc
    assert "Patch 263 may create `ui/main.py`" in doc


def test_patch_263_documents_controlled_router_extraction():
    doc = read("docs/controlled_router_extraction_patch_263.md")

    assert "Patch 263 — Controlled Router Extraction" in doc
    assert "ui/main.py" in doc
    assert "render_controlled_router" in doc
    assert "No Streamlit native multipage migration" in doc
    assert "No session-state extraction" in doc


def test_top_level_navigation_labels_order_is_preserved_in_app_entrypoint():
    app = read("app.py")

    assert _literal_assignment(app, "APP_NAVIGATION_LABELS") == EXPECTED_NAVIGATION_LABELS
    assert "Receipt Reader" not in _literal_assignment(app, "APP_NAVIGATION_LABELS")


def test_app_delegates_to_controlled_router_without_inline_dispatch():
    app = read("app.py")

    assert "from ui.main import render_controlled_router" in app
    assert "render_controlled_router(" in app
    assert "app_navigation_labels=APP_NAVIGATION_LABELS" in app
    assert "module_globals=globals()" in app
    assert "key=\"aletheia_active_module\"" not in app
    assert "selected_top_module = st.radio(" not in app
    assert "if selected_top_module ==" not in app


def test_ui_main_owns_top_level_radio_state_key_and_shape():
    main = read("ui/main.py")

    assert 'selected_top_module = st.radio(' in main
    assert '"ALETHEIA module"' in main
    assert "app_navigation_labels" in main
    assert "horizontal=True" in main
    assert 'label_visibility="collapsed"' in main
    assert 'key="aletheia_active_module"' in main
    assert (
        "Receipt Reader: Why ALETHEIA → Support utilities → Receipt Reader — Standard View."
        in main
    )


def test_ui_main_preserves_dispatch_targets_after_router_move():
    main = read("ui/main.py")

    expected_dispatch_tokens = [
        "if selected_top_module == '🚀 Stress Test':",
        "render_stress_test_page(stress_test_dependency_map(module_globals))",
        "if selected_top_module == '🧭 Boundary Cases':",
        "render_boundary_cases_page(",
        "if selected_top_module == '📊 Evidence Lab':",
        "render_evidence_lab_page(evidence_lab_dependency_map(module_globals))",
        "if selected_top_module == '🌐 World Lens':",
        "render_world_lens_page(world_lens_dependency_map(module_globals))",
        "if selected_top_module == '🪞 Mirror Check':",
        "render_mirror_check_page(mirror_check_dependency_map(module_globals))",
        "if selected_top_module == '📜 Protocol Guide':",
        "render_protocol_guide_page()",
        "if selected_top_module == 'ℹ️ Why ALETHEIA':",
        "render_about_public_info_page(st, header_image=resolve_about_header_image())",
        "render_receipt_reader_standard_view(st)",
        "render_app_footer_banner(app_version, st)",
    ]

    for token in expected_dispatch_tokens:
        assert token in main, f"Missing dispatch token: {token}"
