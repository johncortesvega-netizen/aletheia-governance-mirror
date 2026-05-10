"""
ALETHEIA RECOVERY NOTE
Patch 06: protocol repair-loop regression tests.

Purpose:
    Ensure the protocol-level repair loop introduced in Patch 01 remains a
    Silent Operator question layer rather than an instruction layer.

Rollback:
    Remove this test file. No production module should need rollback.
"""

import protocol


def test_protocol_repair_questions_exist_for_asylum_and_threshold():
    asylum_questions = protocol.protocol_repair_questions(
        "ASYLUM",
        stress_label="Throne Capture / Asylum",
        corruption_risk="High",
    )
    threshold_questions = protocol.protocol_repair_questions(
        "THRESHOLD",
        stress_label="Review Required",
        corruption_risk="Medium",
    )

    assert isinstance(asylum_questions, list)
    assert isinstance(threshold_questions, list)
    assert len(asylum_questions) >= 3
    assert len(threshold_questions) >= 3
    assert len(asylum_questions) == len(set(asylum_questions))
    assert len(threshold_questions) == len(set(threshold_questions))


def test_protocol_repair_questions_are_questions_not_commands():
    questions = protocol.protocol_repair_questions(
        "ASYLUM",
        stress_label="sovereignty capture global id",
        corruption_risk="High",
    )

    assert all(isinstance(question, str) and question.strip() for question in questions)
    assert all(question.strip().endswith("?") for question in questions)
    assert any("ALETHEIA" in question for question in questions)
    assert any("Throne" in question or "ownership" in question or "capture" in question for question in questions)
    assert any("appeal path" in question.lower() for question in questions)
    assert not any("Welke" in question or "Wat " in question for question in questions)
