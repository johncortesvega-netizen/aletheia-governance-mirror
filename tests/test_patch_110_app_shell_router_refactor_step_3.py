from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class DummyContainer:
    def __init__(self):
        self.calls = []

    def markdown(self, text, **kwargs):
        self.calls.append(("markdown", text, kwargs))

    def header(self, text):
        self.calls.append(("header", text, {}))

    def caption(self, text):
        self.calls.append(("caption", text, {}))



def test_patch_110_files_exist():
    required = [
        "ui/app_shell.py",
        "tests/test_patch_110_app_shell_router_refactor_step_3.py",
        "PATCH_110_MANIFEST.txt",
        "PATCH_110_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel



def test_patch_110_app_imports_and_calls_header_shell_helpers():
    app = read("app.py")
    assert "render_app_header" in app
    assert "render_how_to_use_note" in app
    assert "render_app_header(mascot_logo_uri, APP_VERSION, st)" in app
    assert "render_how_to_use_note(st)" in app
    assert "render_app_boundary_notices(SUPPORTED_INPUT_LANGUAGE_NOTE, st)" in app

    header_region = app.split("# Header", 1)[1].split("# Sidebar controls", 1)[0]
    assert "botanical-frame hero" not in header_region
    assert "How to use this:" not in header_region
    assert "render_app_header" in header_region
    assert "render_how_to_use_note" in header_region



def test_patch_110_app_shell_renders_header_copy_without_streamlit_runtime():
    import sys

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    from ui.app_shell import render_app_header, render_how_to_use_note

    dummy = DummyContainer()
    render_app_header("data:image/png;base64,example", "ALETHEIA test version", dummy)
    render_how_to_use_note(dummy)

    combined = "\n".join(str(call[1]) for call in dummy.calls)
    assert "botanical-frame hero" in combined
    assert "ALETHEIA" in combined
    assert "A mirror, not a throne." in combined
    assert "People first. Scores second." in combined
    assert "ALETHEIA asks. People decide." in combined
    assert "It never rules, votes, commands, or replaces people." in combined
    assert "How to use this:" in combined
    assert "You keep the final say." in combined
    assert "not legal, medical, political, religious, or official advice" in combined



def test_patch_110_shell_helper_stays_copy_only_and_boundary_safe():
    helper = read("ui/app_shell.py")
    required = [
        "render_app_header",
        "render_how_to_use_note",
        "render_app_boundary_notices",
        "A mirror, not a throne.",
        "ALETHEIA asks. People decide.",
        "You keep the final say.",
        "not legal, medical, political, religious, or official advice",
    ]
    for phrase in required:
        assert phrase in helper

    forbidden = [
        "simulate(",
        "full_report(",
        "audit_ai_integrity_artifact(",
        "requests.",
        "httpx.",
        "urllib.request",
        "st.session_state",
        "download_button",
        "file_uploader",
        "text_area",
        "selectbox",
        "slider",
        "button(",
    ]
    for phrase in forbidden:
        assert phrase not in helper



def test_patch_110_status_declares_router_shell_refactor_boundaries():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_110_MANIFEST.txt",
            "PATCH_110_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
        ]
    ).lower()
    required = [
        "app shell router refactor step 3",
        "public header",
        "first-use note",
        "ui/app_shell.py",
        "app.py remains the orchestrator",
        "no scoring change",
        "no verdict-routing change",
        "no signal-pattern change",
        "no signal-weight change",
        "no receipt schema change",
        "no module routing change",
        "no external calls",
        "no live model calls",
        "no telemetry",
        "no analytics",
        "no central storage",
        "no global id sync",
        "no public ledger sync",
        "no privacy guarantee",
        "no certification",
        "no enforcement",
        "no final truth claim",
    ]
    for phrase in required:
        assert phrase in combined



def test_patch_110_no_accidental_internal_work_notes():
    scan_files = [
        "ui/app_shell.py",
        "PATCH_110_MANIFEST.txt",
        "PATCH_110_RECOVERY_NOTE.md",
        "README.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
        "docs/architecture.md",
        "docs/patch_index.md",
    ]
    forbidden = [
        "internal repair note",
        "temporary work note",
        "placeholder button",
        "downloaded (placeholder)",
        "ajustando",
        "afirmação",
        "preciso",
        "verwijderen",
        "overmatige",
    ]
    text = "\n".join(read(rel) for rel in scan_files).lower()
    for fragment in forbidden:
        assert fragment not in text
