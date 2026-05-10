from pathlib import Path

from core.witness import (
    build_local_question_prompt_receipt,
    is_witness_question_prompt,
    is_witness_question_set,
)

ROOT = Path(__file__).resolve().parents[1]
APP_TEXT = (ROOT / "app.py").read_text(encoding="utf-8")
DOC_TEXT = (ROOT / "docs" / "stress_test_question_prompt_detection.md").read_text(encoding="utf-8")
BASELINE = ROOT / "examples" / "batch_questions" / "formal_doctrine_repair_questions_nl.txt"


def _load_questions():
    lines = BASELINE.read_text(encoding="utf-8").splitlines()
    return [line.split(".", 1)[1].strip() for line in lines if line.strip()]


def test_formal_doctrine_question_baseline_has_50_questions():
    questions = _load_questions()
    assert len(questions) == 50
    assert all(is_witness_question_prompt(q) for q in questions)
    assert is_witness_question_set(questions)


def test_simulation_question_prompt_receipt_contract():
    receipt = build_local_question_prompt_receipt(
        module="Simulation",
        input_text="Wie heeft het laatste woord als de data en de menselijke intuïtie elkaar tegenspreken?",
        processed_text="Wie heeft het laatste woord als de data en de menselijke intuïtie elkaar tegenspreken?",
        invisibility_applied=False,
        app_version="test",
    )
    assert receipt["input_status"] == "QUESTION_PROMPT"
    assert receipt["input_type"] == "QUESTION_PROMPT"
    assert receipt["verdict"]["protocol_adjusted_state"] == "QUESTION_PROMPT"
    assert receipt["verdict"]["risk"] == "Review Tool"
    assert receipt["verdict"]["protocol_label"] == "Audit Question / Review Tool"
    assert receipt["authority_boundary"]["authority_claim"] is False
    assert receipt["authority_boundary"]["human_review_required"] is True
    assert receipt["metrics"]["integrity"] is None


def test_stress_batch_uses_question_set_mode_before_scoring():
    assert "stress_question_set_mode = is_witness_question_set(stress_batch_items)" in APP_TEXT
    assert "if stress_question_set_mode and is_witness_question_prompt(raw_item):" in APP_TEXT
    assert "build_local_question_prompt_receipt(" in APP_TEXT
    assert 'module="Simulation"' in APP_TEXT
    assert "Question-prompt mode will keep audit/repair questions as review tools" in APP_TEXT


def test_docs_remind_user_of_exact_txt_file_name():
    assert "formal doctrine repair-question baseline.txt" in DOC_TEXT
    assert "QUESTION_PROMPT" in DOC_TEXT
    assert "Audit Question / Review Tool" in DOC_TEXT
    assert "not policy proposals" in DOC_TEXT
