from pathlib import Path
import importlib

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_141_files_exist():
    for rel in [
        "tests/test_patch_141_v1_ui_receipt_upload_cleanup.py",
        "PATCH_141_MANIFEST.txt",
        "PATCH_141_RECOVERY_NOTE.md",
    ]:
        assert (ROOT / rel).exists(), rel


def test_receipt_reader_is_upload_only_and_uploaded_language():
    helper = read("ui/receipt_reader.py")
    assert "file_uploader" in helper
    assert "Upload an ALETHEIA receipt file" in helper
    assert '["txt", "md", "json"]' in helper
    assert "Paste an ALETHEIA receipt" not in helper
    assert "Paste a receipt" not in helper
    assert "pasted receipt" not in helper.lower()
    assert "uploaded ALETHEIA receipts" in helper
    assert "Not found in uploaded receipt" in helper


def test_receipt_reader_parser_does_not_infer_missing_values_or_rescore():
    reader = importlib.import_module("ui.receipt_reader")
    parsed = reader.parse_receipt_standard_view("Malformed uploaded file with no clear receipt fields")
    assert parsed["native_state"] == reader.MISSING_VALUE
    assert parsed["standard_band"] == reader.MISSING_VALUE
    assert all(value == reader.MISSING_VALUE for value in parsed["fields"].values())

    parsed_threshold = reader.parse_receipt_standard_view("Protocol-adjusted state: THRESHOLD\nIntegrity: 0.71")
    assert parsed_threshold["native_state"] == "THRESHOLD"
    assert parsed_threshold["fields"]["integrity"] == "0.71"

    forbidden = [
        "full_report(",
        "simulate(",
        "build_local_witness_receipt",
        "audit_ai_integrity",
        "scan_privacy_boundary_static",
        "requests.",
        "httpx.",
        "openai",
        "embedding",
        "database",
        "telemetry",
        "analytics",
        "download_button",
    ]
    helper = helper_lower = read("ui/receipt_reader.py").lower()
    for phrase in forbidden:
        assert phrase.lower() not in helper_lower


def test_receipt_reader_uses_compact_cards_not_large_table():
    helper = read("ui/receipt_reader.py")
    assert "Native state card" in helper
    assert "Values card" in helper
    assert "Plain-language explanation card" in helper
    assert "Standard View card" in helper
    assert ".table(" not in helper


def test_unit_preview_renders_packaged_html_and_ai_integrity_guidance():
    unit_preview = read("ui/unit_preview.py")
    assert "get_unit_preview_html_files" in unit_preview
    assert "render_unit_preview_html_reference" in unit_preview
    assert "Sydney_Protocol_v3.2.html" in unit_preview
    assert "GPA_v8.2.html" in unit_preview
    assert "container.columns(len(html_files))" in unit_preview
    assert "AI Integrity Mirror:" in unit_preview
    assert "Receipt Reader — Standard View" in unit_preview


def test_ai_integrity_remains_visible_as_main_module():
    app = read("app.py")
    labels_block = app.split("APP_NAVIGATION_LABELS = [", 1)[1].split("]", 1)[0]
    assert "AI Integrity Mirror" in labels_block
    assert "tab_ai_integrity" in app
    assert "st.subheader(\"AI Integrity Mirror" in app
    assert "tab_receipt_reader" not in app


def test_header_footer_v1_language_and_mirror_boundary():
    shell = read("ui/app_shell.py")
    assert "Aletheia V1 — Governance Mirror Final" in shell
    assert "Mirror, not throne." in shell
    forbidden = ["certification", "final truth", "legal authority", "official authority"]
    for phrase in forbidden:
        assert phrase not in shell.lower()


def test_why_aletheia_current_v1_positioning():
    about = read("pages_ui/about_page.py")
    required = [
        "restraint",
        "compliance as a floor, not the final measure of integrity",
        "Where is power moving?",
        "Who can appeal?",
        "What is hidden?",
        "Where is human review being weakened?",
        "ALETHEIA does not replace enterprise tools, legal review, security review, or",
        "human judgment",
        "AI Integrity Mirror",
        "ALETHEIA is a mirror",
    ]
    for phrase in required:
        assert phrase in about


def test_tree_canopy_adjustment_is_visual_only():
    app = read("app.py")
    assert "canopy_y_offset = 2 if state == \"SANCTUARY\" else (6 if state == \"THRESHOLD\" else 11)" in app
    snippet = app.split("def render_pulse_tree", 1)[1].split("components.html", 1)[0]
    forbidden_logic = ["protocol_adjusted_state", "full_report(", "simulate(", "build_local_witness_receipt"]
    for phrase in forbidden_logic:
        assert phrase not in snippet


def test_patch_141_docs_capture_boundaries():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_141_MANIFEST.txt",
            "PATCH_141_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
            "docs/architecture.md",
        ]
    ).lower()
    for phrase in [
        "patch 141",
        "upload-only",
        "no pasted receipt textbox",
        "does not rescore",
        "no scoring",
        "no verdict routing",
        "no receipt schema",
        "no receipt generation",
        "no external calls",
        "no telemetry",
        "no certification",
        "human review remains required",
    ]:
        assert phrase in combined
