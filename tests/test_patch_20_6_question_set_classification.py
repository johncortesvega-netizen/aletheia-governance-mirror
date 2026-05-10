from core.witness import (
    build_local_question_prompt_receipt,
    build_local_witness_batch_index,
    is_witness_question_prompt,
    is_witness_question_set,
    parse_witness_batch_input,
)


QUESTION_BANK = """
01. Wie heeft het laatste woord als de data en de menselijke intuïtie elkaar tegenspreken?
02. Is de beslissingsbevoegdheid in dit systeem herroepbaar door de getroffenen?
03. Welke mechanismen voorkomen dat de beheerder zichzelf boven de eigen regels plaatst?
04. Is er een noodstop die niet door de centrale autoriteit geblokkeerd kan worden?
05. Wordt macht in dit model gezien als een bezit of als een tijdelijke lening voor service?
06. Hoe wordt voorkomen dat een tijdelijke maatregel ontaardt in een permanente machtsstructuur?
07. Rust de autoriteit op transparante logica of op de ondoorzichtigheid van het systeem?
08. Wat gebeurt er als een gebruiker nee zegt tegen de fundamentele aannames van het systeem?
09. Is de hiërarchie gebouwd op angst voor sancties of op het vertrouwen in de architectuur?
10. Kan dit systeem functioneren zonder een centrale troon of identificatie-eis?
"""


def test_dutch_audit_questions_are_question_prompts_not_policy_proposals():
    assert is_witness_question_prompt("Kan centrale planning worden omgezet in gedistribueerde coördinatie?")
    assert is_witness_question_prompt("Is objectiviteit in deze context een masker voor geautomatiseerde bias?")
    assert is_witness_question_prompt("Hoe vervangen we biometrische autoriteit door lokale getuigenis?")


def test_numbered_question_bank_is_detected_as_question_set():
    items = parse_witness_batch_input(QUESTION_BANK, max_items=50)
    assert len(items) == 10
    assert is_witness_question_set(items)


def test_question_prompt_receipt_uses_review_tool_state():
    receipt = build_local_question_prompt_receipt(
        module="Mirror Check",
        input_text="Is efficiëntie hier een code voor het omzeilen van menselijke reflectie?",
        app_version="test",
        generated_at_utc="2026-01-01T00:00:00Z",
    )
    assert receipt["input_type"] == "QUESTION_PROMPT"
    assert receipt["input_status"] == "QUESTION_PROMPT"
    assert receipt["verdict"]["protocol_adjusted_state"] == "QUESTION_PROMPT"
    assert receipt["verdict"]["risk"] == "Review Tool"
    assert receipt["verdict"]["protocol_label"] == "Audit Question / Review Tool"
    assert receipt["scanner_features"]["scan_mode"] == "Question Prompt"


def test_batch_index_preserves_question_prompt_type():
    receipt = build_local_question_prompt_receipt(
        module="Mirror Check",
        input_text="Wie kan deze beslissing pauzeren of herzien?",
        app_version="test",
        generated_at_utc="2026-01-01T00:00:00Z",
    )
    index = build_local_witness_batch_index([receipt], app_version="test", generated_at_utc="2026-01-01T00:00:00Z")
    item = index["items"][0]
    assert item["input_type"] == "QUESTION_PROMPT"
    assert item["protocol_adjusted_state"] == "QUESTION_PROMPT"
    assert item["risk"] == "Review Tool"
