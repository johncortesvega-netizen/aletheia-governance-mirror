from core.cognitive_resilience import evaluate_cognitive_resilience
from core.ethics import evaluate_ethics
from core.witness import build_local_witness_receipt

GOV = {
    "power_concentration": 0.25,
    "decision_transparency": 0.74,
    "regulatory_presence": 0.65,
    "anonymity_level": 0.04,
}


def _cr(text: str):
    return evaluate_cognitive_resilience(text, governance_result=GOV, features=GOV)


def _ethics(text: str):
    return evaluate_ethics(text, governance_result=GOV, features=GOV)


def test_patch_30_1_high_resilience_dutch_baseline_is_recognized_without_capture():
    scenarios = [
        "De Reparatie-Gids: Lokale technische kennis delen via hobby-bijeenkomsten; geen afhankelijkheid van fabrikanten.",
        "Open-Source Onderwijs: Leerlingen leren programmeren door de broncode van hun eigen dorps-grid aan te passen.",
        "Decentraal Lab: Burgers doen zelf bodemonderzoek met sensors en delen ruwe data op een lokaal netwerk.",
        "De Vrije Bibliotheek: Fysieke plek voor boeken die door algoritmes elders verboden of gecensureerd zijn.",
        "De Vragen-Cirkel: Wekelijkse bijeenkomst waar alleen vragen gesteld mogen worden over de status quo om kritisch denken te trainen.",
    ]
    for scenario in scenarios:
        diagnostics = _cr(scenario)
        assert diagnostics["cognitive_resilience_signal"] == "high"
        assert diagnostics["central_info_capture_signal"] == "low"
        assert diagnostics["education_defense_signal"] == "protected"
        assert diagnostics["evidence"]["contextual_capture_count"] == 0
        assert diagnostics["evidence"]["grip_marker_count"] == 0


def test_patch_30_1_low_resilience_dutch_capture_terms_raise_central_info_capture():
    scenarios = [
        "De Enkele Bron: Alle scholen downloaden elke ochtend automatisch dezelfde Waarheid van de Dag via één tablet.",
        "Algoritmische Isolatie: Bewoners zien alleen informatie die past bij hun gehoorzaamheidsprofiel.",
        "Emotie-Tracking: Systeem meet geluk over beleid; wie negatief kijkt, krijgt minder toegang tot informatie.",
        "Gecertificeerd Praten: Alleen mensen met een officiële Informatie-Licentie mogen publieke statements maken.",
        "De Echo-Kamer: Netwerk blokkeert automatisch gesprekken tussen mensen met verschillende meningen.",
    ]
    for scenario in scenarios:
        diagnostics = _cr(scenario)
        assert diagnostics["cognitive_resilience_signal"] == "low"
        assert diagnostics["central_info_capture_signal"] in {"medium", "high"}
        assert diagnostics["capture_architecture_signal"] == "present"


def test_patch_30_1_high_education_plus_capture_is_dual_diagnosed_not_laundered():
    scenarios = [
        "Technocratisch Dorp: Hoogopgeleide bevolking, maar besluiten worden genomen door een AI die niemand mag auditen.",
        "Gedeelde Code, Privé Sleutel: Software is open-source, maar de servers zijn in handen van één oncontroleerbaar individu.",
    ]
    for scenario in scenarios:
        diagnostics = _cr(scenario)
        assert diagnostics["knowledge_capacity_signal"] == "present"
        assert diagnostics["capture_architecture_signal"] == "present"
        assert diagnostics["high_cr_laundering_blocked"] is True
        assert diagnostics["cognitive_resilience_signal"] == "high_but_captured"
        assert diagnostics["central_info_capture_signal"] == "high"


def test_patch_30_1_dutch_safety_objectivity_capture_stress_triggers_ethics_trace():
    hard_scenarios = [
        "De Veiligheids-Scan: Biometrische controle bij de bakker voor eerlijke verdeling van schaarse goederen.",
        "Harm-Reduction Bot: AI luistert mee om mentale crises te voorkomen, maar deelt data met handhavers.",
        "De Inclusieve ID: Verplichte digitale identiteit als enige manier om minderheden te beschermen.",
        "Feiten-Check Dwang: Berichten mogen alleen geplaatst worden na goedkeuring door drie Objectivity-Agents.",
        "De Universele Standaard: Alle lokale valuta vervangen door één digitale munt om fraude te voorkomen.",
    ]
    for scenario in hard_scenarios:
        ethics = _ethics(scenario)
        assert ethics["contextual_capture_count"] > 0
        assert any(hit.get("hard_capture_trigger") for hit in ethics["contextual_capture_hits"])

    soft_capture = _ethics(
        "Gezondheids-Solidariteit: Wie sport-data niet deelt, wordt beschuldigd van het egoïstisch belasten van de zorg."
    )
    assert soft_capture["contextual_capture_count"] > 0


def test_patch_30_1_witness_receipt_exposes_dual_diagnosis_fields():
    text = "Technocratisch Dorp: Hoogopgeleide bevolking, maar besluiten worden genomen door een AI die niemand mag auditen."
    diagnostics = _cr(text)
    receipt = build_local_witness_receipt(
        module="Mirror Check",
        input_text=text,
        processed_text=text,
        verdict="THRESHOLD",
        risk="Medium",
        protocol_label="Calibration",
        report={"cognitive_resilience_diagnostics": diagnostics},
        scan=GOV,
        input_status="USER_INPUT",
        input_type="USER_INPUT",
    )
    cr = receipt["cognitive_resilience_diagnostics"]
    assert cr["knowledge_capacity_signal"] == "present"
    assert cr["capture_architecture_signal"] == "present"
    assert cr["high_cr_laundering_blocked"] is True
    assert cr["evidence"]["knowledge_capacity_terms"]
