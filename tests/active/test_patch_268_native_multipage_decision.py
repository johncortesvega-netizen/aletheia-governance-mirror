"""Patch 268 native multipage decision contract."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_patch_268_documents_keep_controlled_router_decision():
    doc = read("docs/native_multipage_decision_patch_268.md")
    summary = read("docs/native_multipage_decision_patch_268_summary.md")

    assert "Patch 268 — Native Multipage Decision" in doc
    assert "Keep the current controlled router for now." in doc
    assert "No Streamlit native multipage migration is performed." in doc
    assert "Receipt Reader under `Why ALETHEIA → Support utilities`" in doc
    assert "Patch 268 summary" in summary
    assert "Decision: keep the current controlled router for now." in summary
    assert "Runtime impact: none." in summary


def test_patch_268_preserves_controlled_router_owner_and_no_native_pages_directory():
    app = read("app.py")
    router = read("ui/main.py")

    assert "from ui.main import render_controlled_router" in app
    assert "render_controlled_router(" in app
    assert "def render_controlled_router(" in router
    assert "key=\"aletheia_active_module\"" in router
    assert "Receipt Reader: Why ALETHEIA → Support utilities → Receipt Reader — Standard View." in router
    assert not (ROOT / "pages").exists(), "Patch 268 must not create Streamlit native multipage entrypoints."


def test_patch_268_does_not_rename_or_move_navigation_labels():
    app = read("app.py")
    router = read("ui/main.py")

    expected_labels = [
        "🚀 Stress Test",
        "🧭 Boundary Cases",
        "📊 Evidence Lab",
        "🌐 World Lens",
        "🪞 Mirror Check",
        "📜 Protocol Guide",
        "ℹ️ Why ALETHEIA",
    ]
    for label in expected_labels:
        assert label in app
        assert f"selected_top_module == '{label}'" in router

    assert "APP_NAVIGATION_LABELS = [" in app
    assert "app_navigation_labels=APP_NAVIGATION_LABELS" in app


def test_patch_268_status_and_notes_are_current():
    status = read("PATCH_STATUS.md")
    notes = read("PATCH_NOTES.md")

    assert "Patch 268 — Native Multipage Decision" in status
    assert "Status: READY FOR LOCAL REVIEW" in status
    assert "Patch 268 — Native Multipage Decision" in notes
    assert "No root `pages/` directory is added." in notes
