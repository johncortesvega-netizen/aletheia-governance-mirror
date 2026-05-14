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


def test_single_unit_preview_gate_is_session_state_only_and_before_modules():
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


def test_unit_preview_helper_has_proceed_button_and_no_persistence():
    helper = read("ui/unit_preview.py")
    tree = ast.parse(helper)
    button_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "button"
    ]
    labels = []
    for call in button_calls:
        if call.args and isinstance(call.args[0], ast.Constant):
            labels.append(str(call.args[0].value))
    assert "Preview review path" in labels
    assert "Proceed to ALETHEIA" in labels
    assert "aletheia_unit_preview_passed" in helper

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
        "auth/login",
        "login",
        "database",
    ]
    lowered = helper.lower()
    for phrase in forbidden:
        assert phrase.lower() not in lowered


def test_stabilization_docs_acknowledge_successor_unit_preview():
    combined = "\n".join(
        read(rel)
        for rel in [
            "docs/start_page_stabilization_checkpoint.md",
            "docs/aletheia_unit_preview_v1.md",
            "docs/aletheia_unit_preview_stabilization.md",
        ]
        if (ROOT / rel).exists()
    ).lower()
    assert "session" in combined
    assert "unit preview" in combined
    assert "human judgment" in combined
