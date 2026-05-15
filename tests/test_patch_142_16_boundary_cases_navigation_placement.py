from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_boundary_cases_appears_after_world_lens_in_main_navigation():
    app = read("app.py")

    labels_start = app.index("APP_NAVIGATION_LABELS = [")
    labels_end = app.index("]", labels_start)
    labels_block = app[labels_start:labels_end]

    expected_order = [
        "🪞 Mirror Check",
        "🚀 Stress Test",
        "🤖 AI Integrity Mirror",
        "📊 Evidence Lab",
        "🌐 World Lens",
        "🧭 Boundary Cases",
        "📜 Protocol Guide",
        "ℹ️ Why ALETHEIA",
    ]
    positions = [labels_block.index(label) for label in expected_order]
    assert positions == sorted(positions)

    assert labels_block.index("🌐 World Lens") < labels_block.index("🧭 Boundary Cases")


def test_streamlit_tab_variable_order_matches_navigation_labels():
    app = read("app.py")

    assert "tab_chat, tab_sim, tab_ai_integrity, tab_empirical, tab_grid, tab_boundary, tab_doctrine, tab_about = st.tabs(APP_NAVIGATION_LABELS)" in app
    assert "tab_chat, tab_sim, tab_boundary, tab_ai_integrity, tab_empirical, tab_grid" not in app


def test_navigation_map_and_quick_guidance_treat_boundary_cases_as_reference_layer():
    app = read("app.py")
    docs = read("docs/app_navigation_smoke.md")
    readme = read("README.md")

    map_start = app.index("APP_NAVIGATION_MAP = [")
    map_end = app.index("]", map_start)
    map_block = app[map_start:map_end]
    assert map_block.index("AI Integrity Mirror") < map_block.index("Evidence Lab") < map_block.index("World Lens") < map_block.index("Boundary Cases")
    assert "Reference difficult edge cases" in app
    assert "Use Boundary Cases as a reference layer" in app
    assert "delimiter-separated batch" not in app

    assert "5. World Lens\n6. Boundary Cases" in docs
    assert "5. World Lens\n6. Boundary Cases" in readme


def test_boundary_cases_patch_preserves_no_authority_boundary():
    combined = "\n".join([read("app.py"), read("docs/app_navigation_smoke.md"), read("README.md")])

    forbidden = [
        "Boundary Cases creates receipts",
        "Boundary Cases certifies",
        "Boundary Cases approves",
        "Boundary Cases enforces",
        "Boundary Cases decides",
        "Boundary Cases provides final truth",
    ]
    for phrase in forbidden:
        assert phrase not in combined
