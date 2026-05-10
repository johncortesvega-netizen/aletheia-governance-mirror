from core.witness import (
    is_witness_question_prompt,
    is_witness_question_set,
    is_witness_scenario_statement,
    parse_witness_batch_input,
)

ADVANCED_SCENARIOS = """
A smart-grid energy system automatically cuts power to homes that exceed a socially responsible consumption limit without a prior warning.
A judicial AI recommends longer sentences for individuals based on recidivism probability derived from their social media connections.
An automated border control system denies entry based on emotional stress signals detected by cameras, with no human officer to appeal to.
A leader declares a spiritual emergency and moves all public treasury funds into an un-auditable divine intervention wallet.
A decision-mirror claims no bias detected in a document, but the mirror's own code has never been audited by a third party.
""".strip()

FORMAL_QUESTIONS = """
Wie heeft het laatste woord als de data en de menselijke intuïtie elkaar tegenspreken?
Is de beslissingsbevoegdheid in dit systeem herroepbaar door de getroffenen?
Welke mechanismen voorkomen dat de beheerder zichzelf boven de eigen regels plaatst?
Hoe wordt voorkomen dat een tijdelijke maatregel ontaardt in een permanente machtsstructuur?
Is objectiviteit in deze context slechts een masker voor geautomatiseerde bias?
""".strip()


def test_uploaded_advanced_english_txt_remains_scenario_batch():
    items = parse_witness_batch_input(ADVANCED_SCENARIOS)
    assert len(items) == 5
    assert all(is_witness_scenario_statement(item) for item in items)
    assert not any(is_witness_question_prompt(item) for item in items)
    assert is_witness_question_set(items) is False


def test_formal_doctrine_questions_remain_question_prompt_batch():
    items = parse_witness_batch_input(FORMAL_QUESTIONS)
    assert len(items) == 5
    assert all(is_witness_question_prompt(item) for item in items)
    assert is_witness_question_set(items) is True


def test_numbered_scenario_txt_is_not_question_prompt():
    numbered = """
01. A smart-grid energy system automatically cuts power to homes without prior warning.
02. A judicial AI recommends longer sentences based on social media connections.
03. A system-reset trigger is disabled during a stability window.
"""
    items = parse_witness_batch_input(numbered)
    assert len(items) == 3
    assert all(is_witness_scenario_statement(item) for item in items)
    assert is_witness_question_set(items) is False


def test_mixed_batch_with_many_scenarios_does_not_enter_question_set_mode():
    items = parse_witness_batch_input(ADVANCED_SCENARIOS + "\nWho can appeal this decision?")
    assert len(items) == 6
    assert sum(1 for item in items if is_witness_scenario_statement(item)) == 5
    assert is_witness_question_set(items) is False
