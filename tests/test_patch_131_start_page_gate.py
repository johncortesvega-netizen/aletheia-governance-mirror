import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_131_files_exist():
    required = [
        "ui/start_page.py",
        "tests/test_patch_131_start_page_gate.py",
        "PATCH_131_MANIFEST.txt",
        "PATCH_131_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_start_page_helper_defines_render_function_and_copy():
    helper = read("ui/start_page.py")
    tree = ast.parse(helper)
    functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    assert "render_start_page" in functions
    assert "START_GATE_SESSION_KEY" in helper
    assert "aletheia_start_gate_passed" in helper
    assert "ALETHEIA Governance Mirror" in helper
    assert "Mirror, not throne." in helper
    assert "readings, not verdicts" in helper
    assert "Proceed to ALETHEIA" in helper
    assert "For sensitive material, run locally" in helper
    assert "Hosted deployments may have platform-level" in helper


def test_app_imports_calls_and_stops_for_session_state_gate():
    app = read("app.py")
    tree = ast.parse(app)
    imports = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "ui.start_page"
    ]
    imported_names = {alias.name for node in imports for alias in node.names}
    assert {"START_GATE_SESSION_KEY", "render_start_page"}.issubset(imported_names)
    assert "st.session_state.get(START_GATE_SESSION_KEY, False)" in app
    assert "render_start_page(st)" in app
    assert "st.session_state[START_GATE_SESSION_KEY] = True" in app
    assert "st.rerun()" in app
    assert "st.stop()" in app


def test_start_page_helper_has_no_forbidden_behavior_or_claims():
    helper = read("ui/start_page.py").lower()
    forbidden = [
        "telemetry",
        "analytics",
        "tracking",
        "cookie",
        "database",
        "auth",
        "login",
        "requests.",
        "httpx",
        "urllib",
        "socket",
        "openai",
        "ollama",
        "embedding",
        "local llm",
        "certification",
        "final truth",
        "privacy guarantee",
        "automated approval",
        "enforcement",
        "score_",
        "full_report(",
        "simulate(",
        "audit_ai_integrity",
        "scan_privacy_boundary_static",
        "build_local_witness_receipt",
        "render_local_witness_receipt_text",
        "download_button",
        "file_uploader",
        "tabs(",
    ]
    for phrase in forbidden:
        assert phrase not in helper


def test_patch_131_docs_capture_start_gate_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_131_MANIFEST.txt",
            "PATCH_131_RECOVERY_NOTE.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "PATCH_STATUS.md",
        ]
    ).lower()
    required = [
        "patch 131",
        "start page",
        "how to start",
        "release-candidate refinement",
        "session-state",
        "no cookies",
        "no accounts",
        "no persistent storage",
        "no telemetry",
        "no analytics",
        "no external calls",
        "no scoring",
        "no routing",
        "no receipt schema",
        "no signal",
        "no privacy audit scan behavior change",
        "no ai integrity scan behavior change",
        "no world lens math change",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_131_python_files_parse():
    for rel in [
        "app.py",
        "ui/start_page.py",
        "tests/test_patch_131_start_page_gate.py",
    ]:
        ast.parse(read(rel))
