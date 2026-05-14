from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class DummyExpander:
    def __init__(self, parent):
        self.parent = parent

    def __enter__(self):
        return self.parent

    def __exit__(self, exc_type, exc, tb):
        return False


class DummyContainer:
    def __init__(self):
        self.calls = []

    def expander(self, label, expanded=False):
        self.calls.append(("expander", label, {"expanded": expanded}))
        return DummyExpander(self)

    def markdown(self, text, **kwargs):
        self.calls.append(("markdown", text, kwargs))



def test_patch_111_files_exist():
    required = [
        "ui/beginner_guide.py",
        "docs/beginner_ux.md",
        "tests/test_patch_111_beginner_try_this_first_ux.py",
        "PATCH_111_MANIFEST.txt",
        "PATCH_111_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel



def test_patch_111_beginner_guide_moved_to_unit_preview_front_door():
    app = read("app.py")
    unit_preview = read("ui/unit_preview.py")
    assert "render_try_this_first_guide(st, expanded=False)" not in app
    assert "Start here: try this first" in unit_preview
    assert "get_unit_preview_start_here_markdown" in unit_preview

    header_region = app.split("# Header", 1)[1].split("# Sidebar controls", 1)[0]
    assert "render_app_header(mascot_logo_uri, APP_VERSION, st)" in header_region
    assert "render_unit_preview(st)" in header_region
    assert "render_app_boundary_notices(SUPPORTED_INPUT_LANGUAGE_NOTE, st)" in header_region



def test_patch_111_beginner_guide_renders_without_streamlit_runtime():
    import sys

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    from ui.beginner_guide import render_try_this_first_guide

    dummy = DummyContainer()
    render_try_this_first_guide(dummy, expanded=True)

    combined = "\n".join(str(call[1]) for call in dummy.calls)
    assert "Start here: try this first" in combined
    assert "A safe first path" in combined
    assert "Open **Mirror Check**" in combined
    assert "risk reading" in combined
    assert "observed reasons" in combined
    assert "repair questions" in combined
    assert "Download the receipt" in combined
    assert "not a verdict" in combined
    assert "certification" in combined
    assert "run ALETHEIA locally" in combined
    assert any(call[2].get("expanded") is True for call in dummy.calls if call[0] == "expander")



def test_patch_111_beginner_helper_stays_copy_only_and_boundary_safe():
    helper = read("ui/beginner_guide.py")
    required = [
        "render_try_this_first_guide",
        "Start here: try this first",
        "Mirror Check",
        "risk reading",
        "repair questions",
        "not a verdict",
        "run ALETHEIA locally",
        "application-code boundary",
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



def test_patch_111_docs_and_status_declare_boundaries():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_111_MANIFEST.txt",
            "PATCH_111_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "docs/beginner_ux.md",
        ]
    ).lower()
    required = [
        "beginner try this first ux",
        "ui/beginner_guide.py",
        "mirror check",
        "risk reading",
        "repair questions",
        "app.py remains the orchestrator",
        "no scoring",
        "no verdict-routing",
        "no signal-pattern",
        "no signal-weight",
        "no receipt schema",
        "no module-routing",
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
        "no final truth",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in combined



def test_patch_111_no_accidental_internal_work_notes():
    scan_files = [
        "ui/beginner_guide.py",
        "docs/beginner_ux.md",
        "PATCH_111_MANIFEST.txt",
        "PATCH_111_RECOVERY_NOTE.md",
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
