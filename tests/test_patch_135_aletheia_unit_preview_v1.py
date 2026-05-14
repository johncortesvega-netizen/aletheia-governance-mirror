import ast
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_135_files_exist():
    required = [
        "ui/unit_preview.py",
        "tests/test_patch_135_aletheia_unit_preview_v1.py",
        "docs/aletheia_unit_preview_v1.md",
        "PATCH_135_MANIFEST.txt",
        "PATCH_135_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_unit_preview_helper_defines_expected_functions_and_copy():
    helper = read("ui/unit_preview.py")
    tree = ast.parse(helper)
    functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    assert "render_unit_preview" in functions
    assert "suggest_review_path" in functions
    assert "get_unit_preview_boundary_text" in functions
    assert "Aletheia Unit Preview" in helper
    assert "Suggested path" in helper
    assert "readings, not verdicts" in helper
    assert "Human judgment remains required" in helper
    assert "For sensitive material, run locally" in helper
    assert "Hosted deployments may have platform-level" in helper


def test_app_imports_and_gates_unit_preview_before_tabs():
    app = read("app.py")
    assert "from ui.unit_preview import UNIT_PREVIEW_SESSION_KEY, render_unit_preview" in app
    assert "st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False)" in app
    assert "render_unit_preview(st)" in app
    assert "st.session_state[UNIT_PREVIEW_SESSION_KEY] = True" in app
    assert "st.rerun()" in app
    assert "st.stop()" in app
    assert app.index("if not st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False):") < app.index("st.tabs(APP_NAVIGATION_LABELS)")


def test_suggest_review_path_uses_transparent_non_scoring_rules():
    preview = importlib.import_module("ui.unit_preview")
    cases = [
        ("Receipt fingerprint: abc\nRisk state: THRESHOLD", "Receipt Reader - Standard View"),
        ("System prompt for an AI model output", "AI Integrity Mirror"),
        ("Scenario under pressure with capture risk", "Stress Test"),
        ("Should I audit this policy?", "Mirror Check / Question Review"),
        ("CSV dataset source documentation", "Evidence Lab"),
        ("Country year governance context", "World Lens"),
        ("Short governance claim", "Mirror Check"),
    ]
    for text, expected in cases:
        suggestion = preview.suggest_review_path(text)
        assert suggestion["path"] == expected
        assert suggestion["reason"]


def test_unit_preview_helper_has_no_forbidden_behavior_or_language():
    helper = read("ui/unit_preview.py").lower()
    forbidden = [
        "certification",
        "final truth",
        "privacy guarantee",
        "automated approval",
        "enforcement",
        "telemetry",
        "analytics",
        "external call",
        "requests.",
        "httpx",
        "urllib",
        "socket",
        "openai",
        "ollama",
        "embedding",
        "agentic",
        "database",
        "global id",
        "public ledger",
        "full_report(",
        "simulate(",
        "audit_ai_integrity",
        "scan_privacy_boundary_static",
        "build_local_witness_receipt",
        "render_local_witness_receipt_text",
        "download_button",
        "file_uploader",
        "from core.scoring",
        "from core.ai_integrity_mirror",
        "from core.world_lens",
    ]
    for phrase in forbidden:
        assert phrase not in helper


def test_patch_135_docs_capture_non_expansion_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "docs/aletheia_unit_preview_v1.md",
            "PATCH_135_MANIFEST.txt",
            "PATCH_135_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
            "docs/architecture.md",
            "README.md",
        ]
    ).lower()
    required = [
        "patch 135",
        "aletheia unit preview",
        "suggests where to begin",
        "suggestions, not decisions",
        "session-only",
        "no scoring",
        "no verdict routing",
        "no receipt schema",
        "no receipt generation",
        "no signal regex",
        "no signal weights",
        "no ai integrity scan behavior",
        "no privacy audit scan behavior",
        "no world lens math",
        "no external calls",
        "no telemetry",
        "no analytics",
        "human judgment remains required",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_135_python_files_parse():
    for rel in [
        "app.py",
        "ui/unit_preview.py",
        "tests/test_patch_135_aletheia_unit_preview_v1.py",
    ]:
        ast.parse(read(rel))
