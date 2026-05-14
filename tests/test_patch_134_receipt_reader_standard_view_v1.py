import ast
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_134_files_exist():
    required = [
        "ui/receipt_reader.py",
        "docs/receipt_reader_standard_view_v1.md",
        "tests/test_patch_134_receipt_reader_standard_view_v1.py",
        "PATCH_134_MANIFEST.txt",
        "PATCH_134_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_receipt_reader_parser_maps_native_values_without_rescoring():
    reader = importlib.import_module("ui.receipt_reader")
    parsed = reader.parse_receipt_standard_view(
        """
Module: Mirror Check
Risk state: THRESHOLD
Integrity: 72
Friction: Medium
Collapse probability: 0.21
Trust: 64
Alignment: 58
Ego: Low
Repair questions:
- What appeal path is available?
        """
    )
    assert parsed["native_state"] == "THRESHOLD"
    assert parsed["standard_band"] == "Elevated review pressure"
    fields = parsed["fields"]
    assert fields["module_source"] == "Mirror Check"
    assert fields["integrity"] == "72"
    assert "What appeal path" in fields["repair_questions"]


def test_receipt_reader_missing_fields_are_not_inferred():
    reader = importlib.import_module("ui.receipt_reader")
    parsed = reader.parse_receipt_standard_view("Malformed receipt without known values")
    assert parsed["native_state"] == reader.MISSING_VALUE
    assert parsed["standard_band"] == reader.MISSING_VALUE
    assert all(value == reader.MISSING_VALUE for value in parsed["fields"].values())


def test_receipt_reader_helper_is_local_explanatory_only():
    helper = read("ui/receipt_reader.py")
    tree = ast.parse(helper)
    functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    assert "parse_receipt_standard_view" in functions
    assert "render_receipt_reader_standard_view" in functions
    assert "Receipt Reader - Standard View explains pasted ALETHEIA receipts" in helper
    assert "It does not rescore, certify, approve, reject, or override the original receipt." in helper
    assert "STANDARD_BANDS" in helper
    assert "Not found in pasted receipt" in helper

    forbidden = [
        "requests.",
        "httpx",
        "urllib",
        "socket",
        "openai",
        "ollama",
        "embedding",
        "database",
        "telemetry",
        "analytics",
        "write_text",
        "download_button",
        "file_uploader",
        "full_report(",
        "simulate(",
        "audit_ai_integrity",
        "scan_privacy_boundary_static",
        "build_local_witness_receipt",
    ]
    lowered = helper.lower()
    for phrase in forbidden:
        assert phrase.lower() not in lowered


def test_app_exposes_receipt_reader_without_changing_existing_tabs():
    app = read("app.py")
    assert "from ui.receipt_reader import render_receipt_reader_standard_view" in app
    assert '"Receipt Reader"' in app
    assert "tab_receipt_reader" in app
    assert "render_receipt_reader_standard_view(st)" in app
    for existing in [
        "Mirror Check",
        "Stress Test",
        "Boundary Cases",
        "AI Integrity Mirror",
        "Evidence Lab",
        "World Lens",
        "Protocol Guide",
        "Why ALETHEIA",
    ]:
        assert existing in app


def test_patch_134_docs_capture_runtime_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "docs/receipt_reader_standard_view_v1.md",
            "PATCH_134_MANIFEST.txt",
            "PATCH_134_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
            "docs/architecture.md",
        ]
    ).lower()
    required = [
        "patch 134",
        "receipt reader",
        "standard view v1",
        "native receipt values remain the source of truth",
        "not found in pasted receipt",
        "does not rescore",
        "no scoring",
        "no receipt schema",
        "no external calls",
        "no llm calls",
        "no embeddings",
        "no database",
        "no telemetry",
        "no final truth",
        "human review remains required",
    ]
    for phrase in required:
        assert phrase in combined
