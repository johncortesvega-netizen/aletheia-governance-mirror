from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_158_receipt_reader_uses_shared_module_template() -> None:
    source = read("ui/receipt_reader.py")

    assert "from ui.module_page_template import ModulePageTemplateCopy, render_module_page_template_intro" in source
    assert "RECEIPT_READER_PAGE_COPY = ModulePageTemplateCopy" in source
    assert 'module_name="Receipt Reader - Standard View"' in source
    assert "render_module_page_template_intro(container, RECEIPT_READER_PAGE_COPY)" in source


def test_patch_158_receipt_reader_copy_keeps_reader_specific_content() -> None:
    source = read("ui/receipt_reader.py")

    expected_phrases = (
        "Read an existing local ALETHEIA receipt in plain language",
        "without rerunning, rescoring, editing, approving, rejecting, certifying, or overriding",
        "Native receipt state and review pressure exactly as recorded",
        "Module source and protocol label without inventing missing fields",
        "Metric observations copied from the receipt",
        "QUESTION_PROMPT metrics marked not applicable",
        "Failure-mode review signals such as authority drift",
        "Upload one ALETHEIA receipt file first",
        "Use batch ZIP reading as an index of receipts, not as a merged verdict",
        "Receipt Reader does not create or alter receipts",
    )
    for phrase in expected_phrases:
        assert phrase in source


def test_patch_158_receipt_reader_preserves_existing_upload_and_render_paths() -> None:
    source = read("ui/receipt_reader.py")

    assert "container.file_uploader(" in source
    assert 'type=["txt", "md", "json", "zip"]' in source
    assert "parse_uploaded_receipt_file(uploaded)" in source
    assert "_render_batch_zip(container, parsed)" in source
    assert "_render_single_view(container, parsed[\"view\"])" in source
    assert "_render_failure_mode_review_signals(container)" in source
    assert "_render_world_lens_bundle(container, parsed)" in source


def test_patch_158_receipt_reader_page_polish_is_copy_layout_only() -> None:
    helper_source = read("ui/module_page_template.py")
    source = read("ui/receipt_reader.py")

    assert "full_report" not in helper_source
    assert "simulate(" not in helper_source
    assert "score_" not in helper_source
    assert "requests." not in helper_source
    assert "telemetry" not in helper_source
    assert "Global ID sync" not in helper_source
    assert "It does not rescore, certify, approve, reject, enforce, or override" in source
