from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_156_mirror_check_uses_shared_module_template() -> None:
    source = read("app.py")

    assert "from ui.module_page_template import ModulePageTemplateCopy, render_module_page_template_intro" in source
    assert "render_module_page_template_intro(" in source
    assert 'module_name="Mirror Check"' in source
    assert "Plain-language purpose" not in source  # rendered by the shared helper, not duplicated manually


def test_patch_156_mirror_check_copy_keeps_module_specific_content() -> None:
    source = read("app.py")

    expected_phrases = (
        "Review one document, idea, proposal, policy text, or AI output",
        "ALETHEIA is English-first",
        "not as a general app-wide ",
        "language-compatibility claim",
        "Care alignment",
        "Power language",
        "Evidence and reviewability",
        "Appeal and repair",
        "Failure-mode pressure",
        "Witness receipt",
        "Use this module for one bounded text item",
        "not as approval, rejection, or truth certification",
        "local review artifacts held by the user",
    )
    for phrase in expected_phrases:
        assert phrase in source


def test_patch_156_mirror_check_page_polish_is_copy_layout_only() -> None:
    source = read("app.py")
    helper_source = read("ui/module_page_template.py")

    assert "full_report" not in helper_source
    assert "build_local_witness_receipt" not in helper_source
    assert "score_" not in helper_source
    assert "requests." not in helper_source
    assert "telemetry" not in helper_source
    assert "Global ID sync" not in helper_source
    assert "render_shared_protocol_state_notice(\"Mirror Check\")" in source
    assert "render_audit_module_integrity_panel()" in source


def test_patch_156_safe_first_path_and_batch_boundary_remain_visible() -> None:
    source = read("app.py")

    assert "Paste one short item, not a whole archive of mixed cases" in source
    assert "Use optional demos only for orientation" in source
    assert "Use the batch-testing panel only for deliberate test batches" in source
    assert "Mirror Check uses two separate side-by-side paths" in source
    assert "normal_review_col, batch_testing_col = st.columns" in source
