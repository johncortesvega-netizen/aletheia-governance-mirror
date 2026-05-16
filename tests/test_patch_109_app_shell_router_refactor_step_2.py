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


def test_patch_109_files_exist():
    required = [
        "ui/app_shell.py",
        "tests/test_patch_109_app_shell_router_refactor_step_2.py",
        "PATCH_109_MANIFEST.txt",
        "PATCH_109_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_patch_109_app_imports_and_calls_sidebar_shell_helpers():
    app = read("app.py")
    assert "from ui.app_shell import render_app_boundary_notices, render_sidebar_brand, render_sidebar_context" in app
    assert "render_sidebar_brand(mascot_logo_uri, st)" in app
    assert "render_sidebar_context(st)" in app
    assert "render_privacy_panel(st, expanded=False)" in app
    assert "render_boundary_statement(\"footer\", st)" in app

    # Static sidebar shell copy should now live in the helper, not inline inside
    # the app.py sidebar block.
    sidebar_block = app.split("# Sidebar controls", 1)[1].split("MIN_FULL_GRID_COUNTRIES", 1)[0]
    assert "sidebar-emblem-card" not in sidebar_block
    assert "Privacy boundary: no built-in telemetry" not in sidebar_block


def test_patch_109_app_shell_renders_sidebar_copy_without_streamlit_runtime():
    import sys

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    from ui.app_shell import render_sidebar_brand, render_sidebar_context

    dummy = DummyContainer()
    render_sidebar_brand("data:image/png;base64,example", dummy)
    render_sidebar_context(dummy)

    combined = "\n".join(str(call[1]) for call in dummy.calls)
    assert "ALETHEIA" in combined
    assert "A mirror, not a throne." in combined
    assert "Reading controls" in combined
    assert "English-first" in combined
    assert "Dutch/Nederlands examples may be used for batch testing" in combined
    assert "Privacy boundary" in combined
    assert "no built-in telemetry" in combined


def test_patch_109_shell_helper_stays_copy_only_and_boundary_safe():
    helper = read("ui/app_shell.py")
    required = [
        "render_app_boundary_notices",
        "render_sidebar_brand",
        "render_sidebar_context",
        "A mirror, not a throne.",
        "Privacy boundary",
        "no built-in telemetry",
        "central user-input database",
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


def test_patch_109_status_declares_router_shell_refactor_boundaries():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_109_MANIFEST.txt",
            "PATCH_109_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "README.md",
            "docs/architecture.md",
        ]
    ).lower()
    required = [
        "app shell router refactor step 2",
        "sidebar identity card",
        "sidebar context",
        "ui/app_shell.py",
        "app.py remains the orchestrator",
        "no scoring change",
        "no verdict-routing change",
        "no signal-pattern change",
        "no signal-weight change",
        "no receipt schema change",
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


def test_patch_109_no_accidental_internal_work_notes():
    scan_files = [
        "ui/app_shell.py",
        "PATCH_109_MANIFEST.txt",
        "PATCH_109_RECOVERY_NOTE.md",
        "README.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
        "docs/architecture.md",
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
