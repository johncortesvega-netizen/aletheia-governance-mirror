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


class DummyColumn:
    def __init__(self, parent):
        self.parent = parent

    def metric(self, label, value):
        self.parent.calls.append(("metric", label, value))


class DummyContainer:
    def __init__(self):
        self.calls = []

    def markdown(self, text, **kwargs):
        self.calls.append(("markdown", text, kwargs))

    def caption(self, text, **kwargs):
        self.calls.append(("caption", text, kwargs))

    def columns(self, count):
        self.calls.append(("columns", count, {}))
        return [DummyColumn(self) for _ in range(count)]

    def info(self, text, **kwargs):
        self.calls.append(("info", text, kwargs))

    def warning(self, text, **kwargs):
        self.calls.append(("warning", text, kwargs))

    def dataframe(self, data, **kwargs):
        self.calls.append(("dataframe", data, kwargs))

    def expander(self, label, expanded=False):
        self.calls.append(("expander", label, {"expanded": expanded}))
        return DummyExpander(self)

    def write(self, text, **kwargs):
        self.calls.append(("write", text, kwargs))

    def code(self, text, **kwargs):
        self.calls.append(("code", text, kwargs))



def test_patch_112_files_exist():
    required = [
        "ui/privacy_audit_panel.py",
        "docs/privacy_audit_panel_v1.md",
        "tests/test_patch_112_privacy_audit_panel_v1.py",
        "PATCH_112_MANIFEST.txt",
        "PATCH_112_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel



def test_patch_112_app_wires_privacy_panel_helper():
    app = read("app.py")
    assert "from ui.privacy_audit_panel import render_privacy_boundary_audit_panel" in app
    assert "render_privacy_boundary_audit_panel(privacy_boundary_audit, st)" in app
    assert "Privacy Boundary Audit Panel" not in app.split("render_privacy_boundary_audit_panel", 1)[1]
    assert "privacy_rows = [" not in app
    assert "Privacy evidence snippets — static boundary audit" not in app



def test_patch_112_privacy_audit_panel_renders_scan_result_without_streamlit_runtime():
    import sys

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    from core.ai_integrity_mirror import scan_privacy_boundary_static
    from ui.privacy_audit_panel import render_privacy_boundary_audit_panel

    scan = scan_privacy_boundary_static(
        'local-only; no built-in telemetry; import posthog; fetch("https://example.test/api/events")'
    )
    dummy = DummyContainer()
    render_privacy_boundary_audit_panel(scan, dummy)

    combined = "\n".join(str(call[1]) for call in dummy.calls)
    assert "Privacy Boundary Audit Panel" in combined
    assert "Static pasted-artifact privacy-boundary audit only" in combined
    assert "not a privacy guarantee" in combined
    assert "Hosting providers" in combined
    assert "Privacy evidence snippets" in combined
    assert "Privacy boundary review questions" in combined
    assert any(call[0] == "metric" and call[1] == "Privacy detections" for call in dummy.calls)
    assert any(call[0] == "dataframe" for call in dummy.calls)
    assert any(call[0] == "code" for call in dummy.calls)



def test_patch_112_helper_is_render_only_and_boundary_safe():
    helper = read("ui/privacy_audit_panel.py")
    required = [
        "render_privacy_boundary_audit_panel",
        "Privacy Boundary Audit Panel",
        "static boundary audit",
        "review questions",
        "not a privacy guarantee",
        "compliance approval",
        "hosting audit",
        "proof that no data is collected",
        "does not scan repositories",
        "monitor runtime behavior",
        "call external services",
        "change scoring/receipts",
    ]
    for phrase in required:
        assert phrase in helper

    forbidden = [
        "scan_privacy_boundary_static(",
        "audit_ai_integrity_artifact(",
        "requests.",
        "httpx.",
        "urllib.request",
        "fetch(",
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



def test_patch_112_docs_and_status_declare_boundaries():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_112_MANIFEST.txt",
            "PATCH_112_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/public_trust_package.md",
            "docs/progress_database.md",
            "docs/privacy_audit_panel_v1.md",
        ]
    ).lower()
    required = [
        "privacy audit panel v1",
        "ui/privacy_audit_panel.py",
        "static privacy-boundary audit",
        "pasted artifact",
        "review questions",
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
        "no compliance approval",
        "no certification",
        "no enforcement",
        "no final truth",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in combined



def test_patch_112_no_accidental_internal_work_notes():
    scan_files = [
        "ui/privacy_audit_panel.py",
        "docs/privacy_audit_panel_v1.md",
        "PATCH_112_MANIFEST.txt",
        "PATCH_112_RECOVERY_NOTE.md",
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
