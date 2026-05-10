from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app.py"
TEXT = APP.read_text(encoding="utf-8")


def test_patch32_1_updates_version():
    assert 'APP_VERSION = "v9.6.13-patch32-1-repair-question-routing"' in TEXT


def test_patch32_1_embeds_plain_question_bank():
    assert "PLAIN_REPAIR_QUESTION_BANK" in TEXT
    assert TEXT.count('"question":') >= 50
    assert "Wie beslist er als data en menselijk gevoel elkaar tegenspreken?" in TEXT
    assert "Is 'objectiviteit' hier een mooi woord voor vooroordelen die in een algoritme zijn verstopt?" in TEXT


def test_patch32_1_adds_relevant_routing_function():
    assert "def select_plain_repair_questions" in TEXT
    assert "Pick 3–7 simple repair questions" in TEXT
    assert "RISK_FAMILY_TAGS" in TEXT
    assert "RISK_TO_QUESTION_TAGS" in TEXT


def test_patch32_1_routes_mirror_judgment_questions():
    assert 'judgment["questions"] = select_plain_repair_questions(text_value, judgment, report, limit=5)' in TEXT
    assert "Small question set before trusting this model" in TEXT


def test_patch32_1_preserves_question_bank_boundary():
    assert "QUESTION_PROMPT / Review Tool" in TEXT
    assert "uploaded question banks still stay QUESTION_PROMPT / Review Tool" in TEXT
    assert "is_witness_question_set" in TEXT


def test_patch32_1_keeps_mirror_not_throne_language():
    assert "These questions are deliberately reflective. They do not command, enforce, or decide." in TEXT
    assert "It gives no orders and no final judgment." in TEXT
