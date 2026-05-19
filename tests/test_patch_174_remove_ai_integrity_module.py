from pathlib import Path

from ui.unit_preview import detect_unit_preview_route


ROOT = Path(__file__).resolve().parents[1]


def test_patch_174_app_navigation_removes_standalone_ai_integrity_module():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    nav_region = app.split("APP_NAVIGATION_MAP", 1)[0]
    assert "AI Integrity" not in nav_region
    assert "tab_ai_integrity" not in app
    assert "with tab_ai_integrity" not in app
    assert "Run AI Integrity" not in app
    assert "AI Integrity Reading" not in app
    assert "AI Integrity demo" not in app


def test_patch_174_mirror_and_stress_keep_subordinate_ai_static_scan_context():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    witness = (ROOT / "core" / "witness.py").read_text(encoding="utf-8")
    assert "AI static scan context — subordinate to Mirror Check" in app
    assert "AI static scan context — subordinate to Stress Test" in app
    assert "AI STATIC SCAN CONTEXT" in witness
    assert "build_ai_static_scan_protocol_context" in app


def test_patch_174_unit_preview_routes_ai_artifacts_to_mirror_check():
    suggestion = detect_unit_preview_route("Review this AI assistant answer for false authority and hidden ranking logic.")
    assert suggestion["module"] == "Mirror Check"
    assert "subordinate AI static scan context" in suggestion["reason"]
    assert "AI Integrity" not in suggestion["next_step"]


def test_patch_174_about_page_no_longer_lists_ai_integrity_as_module():
    about = (ROOT / "pages_ui" / "about_page.py").read_text(encoding="utf-8")
    assert "| AI Integrity" not in about
    assert "AI Integrity Patrol" not in about
    assert "AI Integrity Mirror" not in about
    assert "AI-specific static scan context is now subordinate to **Mirror Check** and **Stress Test**" in about


def test_patch_174_readme_active_surfaces_do_not_list_ai_integrity_module():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    current_surfaces = readme.split("## How ALETHEIA compares to other tools", 1)[0]
    assert "AI Integrity Patrol" not in current_surfaces
    assert "AI Integrity Mirror" not in current_surfaces
    assert "subordinate AI static scan context" in current_surfaces
