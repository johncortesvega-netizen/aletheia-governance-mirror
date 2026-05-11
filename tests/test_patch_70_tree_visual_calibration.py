from pathlib import Path

APP = Path("app.py").read_text(encoding="utf-8")
DOC = Path("docs/tree_visual_calibration.md").read_text(encoding="utf-8")


def test_patch_70_tree_helpers_exist_and_distinguish_visual_from_receipt_metrics():
    assert "def tree_copy_for_state" in APP
    assert "Visual tree score" in APP
    assert "protocol-adjusted integrity" in APP
    assert "receipt integrity remains the protocol metric" in APP.lower()


def test_patch_70_question_prompt_is_review_tool_not_risk_state():
    assert "QUESTION_PROMPT" in APP
    assert "Review Tool Mode" in APP
    assert "not a scored governance scenario" in APP
    assert "QUESTION_PROMPT" in DOC
    assert "not render as Sanctuary, Threshold, or Asylum" in DOC


def test_patch_70_mirror_and_stress_tree_copy_are_separate():
    assert "mode=\"Stress Test\"" in APP
    assert "mode=\"Mirror Check\"" in APP
    assert "Power under stress" in APP
    assert "Evidence + accountability" in APP
    assert "Human dignity" in DOC
    assert "Human review" in DOC


def test_patch_70_manifest_recovery_and_docs_are_present():
    assert Path("PATCH_70_MANIFEST.txt").exists()
    assert Path("PATCH_70_RECOVERY_NOTE.md").exists()
    assert Path("docs/tree_visual_calibration.md").exists()
    assert "Patch 70" in Path("PATCH_STATUS.md").read_text(encoding="utf-8")
    assert "Patch 70" in Path("docs/progress_database.md").read_text(encoding="utf-8")
