import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_131_files_exist_after_unit_preview_successor():
    required = [
        "ui/start_page.py",
        "ui/unit_preview.py",
        "tests/test_patch_131_start_page_gate.py",
        "PATCH_131_MANIFEST.txt",
        "PATCH_131_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_legacy_start_page_delegates_to_unit_preview_not_old_ui():
    helper = read("ui/start_page.py")
    tree = ast.parse(helper)
    functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    assert "render_start_page" in functions
    assert "render_unit_preview" in helper
    assert "Legacy compatibility wrapper" in helper
    assert "ALETHEIA Governance Mirror" not in helper
    assert "How to start" not in helper


def test_app_uses_single_unit_preview_gate_before_modules():
    app = read("app.py")
    assert "from ui.unit_preview import UNIT_PREVIEW_SESSION_KEY, render_unit_preview" in app
    assert "from ui.start_page" not in app
    assert "START_GATE_SESSION_KEY" not in app
    assert "render_start_page(" not in app
    assert "st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False)" in app
    assert "render_unit_preview(st)" in app
    assert "st.session_state[UNIT_PREVIEW_SESSION_KEY] = True" in app
    assert "st.rerun()" in app
    assert "st.stop()" in app
    assert app.index("if not st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False):") < app.index("st.tabs(APP_NAVIGATION_LABELS)")


def test_unit_preview_copy_has_boundary_and_proceed_button():
    helper = read("ui/unit_preview.py")
    assert "Aletheia Unit Preview" in helper
    assert "Suggested path" in helper
    assert "readings, not verdicts" in helper
    assert "Human judgment remains required" in helper
    assert "For sensitive material, run locally" in helper
    assert "Hosted deployments may have platform-level" in helper
    assert "Proceed to ALETHEIA" in helper


def test_start_gate_helpers_have_no_forbidden_behavior_or_claims():
    combined = (read("ui/start_page.py") + "\n" + read("ui/unit_preview.py")).lower()
    forbidden = [
        "requests.",
        "httpx",
        "urllib",
        "socket",
        "openai",
        "ollama",
        "embedding",
        "local llm",
        "is a certification",
        "final truth system",
        "privacy guarantee",
        "automated approval",
        "enforcement mechanism",
        "analytics event",
        "telemetry event",
        "database write",
    ]
    for phrase in forbidden:
        assert phrase not in combined
