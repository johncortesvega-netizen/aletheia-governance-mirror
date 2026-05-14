from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_139_files_exist():
    required = [
        "PATCH_139_MANIFEST.txt",
        "PATCH_139_RECOVERY_NOTE.md",
        "docs/unit_preview_header_entry_hotfix.md",
        "tests/test_patch_139_unit_preview_header_entry_hotfix.py",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_unit_preview_renders_after_public_header_not_as_plain_first_screen():
    app = read("app.py")
    header = "render_app_header(mascot_logo_uri, APP_VERSION, st)"
    gate = "if not st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False):"
    preview_call = "render_unit_preview(st)"
    boundary = "render_app_boundary_notices(SUPPORTED_INPUT_LANGUAGE_NOTE, st)"
    tabs = "st.tabs(APP_NAVIGATION_LABELS)"

    assert header in app
    assert gate in app
    assert preview_call in app
    assert boundary in app
    assert tabs in app

    assert app.index(header) < app.index(gate) < app.index(boundary) < app.index(tabs)
    assert app.count(gate) == 1
    assert app.count(preview_call) == 1


def test_no_legacy_start_page_or_duplicate_entry_gate_is_active():
    app = read("app.py")
    assert "from ui.start_page" not in app
    assert "render_start_page(" not in app
    assert "aletheia_start_gate_passed" not in app
    assert "START_GATE_SESSION_KEY" not in app


def test_unit_preview_still_stops_before_full_modules_until_proceed():
    app = read("app.py")
    gate_block_start = app.index("if not st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False):")
    gate_block_end = app.index("render_app_boundary_notices(SUPPORTED_INPUT_LANGUAGE_NOTE, st)")
    gate_block = app[gate_block_start:gate_block_end]

    assert "if render_unit_preview(st):" in gate_block
    assert "st.session_state[UNIT_PREVIEW_SESSION_KEY] = True" in gate_block
    assert "st.rerun()" in gate_block
    assert "st.stop()" in gate_block


def test_unit_preview_helper_remains_non_authoritative():
    helper = read("ui/unit_preview.py")
    assert "Aletheia Unit Preview" in helper
    assert "Suggested path" in helper
    assert "does not score, certify" in helper
    assert "readings, not verdicts" in helper
    assert "Human judgment remains required" in helper
    forbidden = [
        "final truth",
        "privacy guarantee",
        "automated approval",
        "enforcement mechanism",
        "telemetry",
        "analytics",
        "external call",
        "requests.",
        "openai",
        "ollama",
        "embedding",
        "database",
    ]
    lowered = helper.lower()
    for phrase in forbidden:
        assert phrase not in lowered
