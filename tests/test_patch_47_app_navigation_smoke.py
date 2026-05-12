from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_app_navigation_labels_are_centralized_and_ordered():
    app = read("app.py")
    assert "APP_NAVIGATION_LABELS" in app
    expected = [
        "💬 Mirror Check",
        "🚀 Stress Test",
        "🧭 Boundary Cases",
        "🤖 AI Integrity Mirror",
        "📊 Evidence Lab",
        "🌐 World Lens",
        "📜 Protocol Guide",
        "ℹ️ Why ALETHEIA",
    ]
    positions = [app.index(label) for label in expected]
    assert positions == sorted(positions)
    assert "st.tabs(APP_NAVIGATION_LABELS)" in app


def test_navigation_document_lists_public_safe_module_map():
    doc = read("docs/app_navigation_smoke.md")
    for phrase in [
        "Mirror Check",
        "Stress Test",
        "Boundary Cases",
        "AI Integrity Mirror",
        "Evidence Lab",
        "World Lens",
        "Protocol Guide",
        "Why ALETHEIA",
        "No tab may command",
        "tools\\run_patch_checks.bat 47",
    ]:
        assert phrase in doc


def test_app_and_about_include_navigation_cleanup_language():
    app = read("app.py")
    about = read("about_page.py")
    for text in (app, about):
        assert "App Navigation" in text or "Navigation map" in text
        assert "no tab" in text.lower()
        assert "human" in text.lower() and "review" in text.lower()


def test_patch_status_points_to_current_navigation_history():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    navigation_doc = read("docs/app_navigation_smoke.md")
    assert "Patch 47" in navigation_doc
    assert "App Navigation + Smoke Test Cleanup" in navigation_doc
    assert "tools\\run_patch_checks.bat 47" in navigation_doc
    assert "Patch 85" in status
    assert "AI Integrity Mirror Scaffold" in status
    assert "Patch 85" in progress
    assert "navigation" in navigation_doc.lower()
