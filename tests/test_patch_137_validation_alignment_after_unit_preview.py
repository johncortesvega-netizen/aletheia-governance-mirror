import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def read_bytes(rel: str) -> bytes:
    return (ROOT / rel).read_bytes()


def test_patch_137_files_exist():
    required = [
        "docs/validation_alignment_after_unit_preview.md",
        "tests/test_patch_137_validation_alignment_after_unit_preview.py",
        "PATCH_137_MANIFEST.txt",
        "PATCH_137_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_current_front_door_is_unit_preview_session_gate_before_tabs():
    app = read("app.py")
    assert "from ui.unit_preview import UNIT_PREVIEW_SESSION_KEY, render_unit_preview" in app
    assert "st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False)" in app
    assert "render_unit_preview(st)" in app
    assert "st.session_state[UNIT_PREVIEW_SESSION_KEY] = True" in app
    assert "st.rerun()" in app
    assert "st.stop()" in app
    assert app.index("if not st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False):") < app.index("st.tabs(APP_NAVIGATION_LABELS)")


def test_older_start_page_tests_allow_successor_gate_instead_of_exact_old_import():
    patch_131_test = read("tests/test_patch_131_start_page_gate.py")
    patch_132_test = read("tests/test_patch_132_start_page_stabilization_checkpoint.py")
    assert "ui.unit_preview" in patch_131_test
    assert "UNIT_PREVIEW_SESSION_KEY" in patch_131_test
    assert "has_start_page_gate or has_unit_preview_gate" in patch_131_test
    assert "ui.unit_preview" in patch_132_test
    assert "UNIT_PREVIEW_SESSION_KEY" in patch_132_test
    assert "has_start_page_gate or has_unit_preview_gate" in patch_132_test


def test_manifest_is_utf8_without_bom_and_current_after_validation_alignment():
    raw = read_bytes("data/protocol_baseline_manifest.json")
    assert not raw.startswith(b"\xef\xbb\xbf")
    manifest = json.loads(raw.decode("utf-8"))
    assert str(manifest["created_for_patch"]) == "137"
    files = manifest["files"]
    required = [
        "tests/test_patch_131_start_page_gate.py",
        "tests/test_patch_131_test_check_hygiene.py",
        "tests/test_patch_132_start_page_stabilization_checkpoint.py",
        "tests/test_patch_137_validation_alignment_after_unit_preview.py",
        "docs/validation_alignment_after_unit_preview.md",
    ]
    for rel in required:
        assert rel in files


def test_patch_137_docs_are_boundary_safe():
    combined = "\n".join(
        read(rel)
        for rel in [
            "docs/validation_alignment_after_unit_preview.md",
            "PATCH_137_MANIFEST.txt",
            "PATCH_137_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
        ]
    ).lower()
    required = [
        "patch 137",
        "validation alignment",
        "unit preview",
        "test/check hygiene",
        "no runtime",
        "no scoring",
        "no verdict routing",
        "no receipt",
        "no signal",
        "no external calls",
        "no telemetry",
        "no certification",
        "no final-truth",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in combined

    # Negative boundary language such as "no telemetry" and "no privacy guarantee"
    # is allowed. The forbidden set below targets positive authority/guarantee claims.
    forbidden_positive_claims = [
        "is an automated approval",
        "provides automated approval",
        "is a privacy guarantee",
        "provides a privacy guarantee",
        "final truth system",
        "certifies integrity",
    ]
    for phrase in forbidden_positive_claims:
        assert phrase not in combined


def test_patch_137_python_files_parse():
    for rel in [
        "tests/test_patch_131_start_page_gate.py",
        "tests/test_patch_131_test_check_hygiene.py",
        "tests/test_patch_132_start_page_stabilization_checkpoint.py",
        "tests/test_patch_137_validation_alignment_after_unit_preview.py",
    ]:
        ast.parse(read(rel))
