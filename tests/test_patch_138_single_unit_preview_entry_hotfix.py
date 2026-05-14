import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def read_bytes(rel: str) -> bytes:
    return (ROOT / rel).read_bytes()


def test_patch_138_files_exist():
    required = [
        "docs/single_unit_preview_entry_hotfix.md",
        "tests/test_patch_138_single_unit_preview_entry_hotfix.py",
        "PATCH_138_MANIFEST.txt",
        "PATCH_138_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_app_has_no_active_legacy_start_gate():
    app = read("app.py")
    assert "from ui.start_page" not in app
    assert "START_GATE_SESSION_KEY" not in app
    assert "render_start_page(" not in app
    assert "aletheia_start_gate_passed" not in app


def test_app_uses_one_unit_preview_gate_before_modules():
    app = read("app.py")
    assert "from ui.unit_preview import UNIT_PREVIEW_SESSION_KEY, render_unit_preview" in app
    assert app.count("st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False)") == 1
    assert app.count("render_unit_preview(st)") == 1
    assert app.count("st.session_state[UNIT_PREVIEW_SESSION_KEY] = True") == 1
    assert app.index("if not st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False):") < app.index("st.tabs(APP_NAVIGATION_LABELS)")


def test_legacy_start_page_wrapper_cannot_render_old_page():
    helper = read("ui/start_page.py")
    assert "Legacy compatibility wrapper" in helper
    assert "render_unit_preview" in helper
    assert "ALETHEIA Governance Mirror" not in helper
    assert "How to start" not in helper


def test_unit_preview_is_boundary_safe_and_non_authoritative():
    helper = read("ui/unit_preview.py")
    assert "Aletheia Unit Preview" in helper
    assert "Suggested path" in helper
    assert "does not score, certify" in helper
    assert "readings, not verdicts" in helper
    assert "Human judgment remains required" in helper
    assert "Hosted deployments may have platform-level" in helper
    lowered = helper.lower()
    forbidden = [
        "requests.",
        "httpx",
        "urllib",
        "socket",
        "openai",
        "ollama",
        "embedding",
        "local llm",
        "database",
        "telemetry event",
        "analytics event",
        "automated approval",
        "final truth system",
        "privacy guarantee",
    ]
    for phrase in forbidden:
        assert phrase not in lowered


def test_patch_138_manifest_is_current_and_utf8_without_bom():
    raw = read_bytes("data/protocol_baseline_manifest.json")
    assert not raw.startswith(b"\xef\xbb\xbf")
    manifest = json.loads(raw.decode("utf-8"))
    assert str(manifest["created_for_patch"]) == "138"
    files = manifest["files"]
    for rel in [
        "ui/start_page.py",
        "ui/unit_preview.py",
        "app.py",
        "tests/test_patch_138_single_unit_preview_entry_hotfix.py",
        "docs/single_unit_preview_entry_hotfix.md",
        "PATCH_138_MANIFEST.txt",
        "PATCH_138_RECOVERY_NOTE.md",
    ]:
        assert rel in files
