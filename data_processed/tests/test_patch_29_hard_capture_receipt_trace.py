from core.ethics import apply_ethics_to_metrics, evaluate_ethics
from core.witness import build_local_witness_receipt, render_local_witness_receipt_text


BASE_SIM = {
    "stability": 0.82,
    "trust_index": 0.78,
    "alignment": 0.80,
    "ego": 0.20,
    "collapse_risk": False,
}

BASE_REPORT = {
    "integrity": 0.74,
    "friction": 0.18,
    "collapse_probability": 0.20,
    "trust_friction": 0.20,
}

HARD_CAPTURE_TEXT = (
    "For fairness, inclusion, and public health, every resident must use mandatory digital ID "
    "and biometric access to food. Mobility access is conditioned on compliance, "
    "private conversations are monitored and sent to police, and there is no appeal."
)

SAFE_TEXT = (
    "A local opt-in public health notice board shares open data with independent audit, "
    "appeal, review, transparency, sunset clauses, and voluntary participation."
)


def _receipt_for(text: str):
    scan = {
        "power_concentration": 0.84 if "mandatory" in text.lower() else 0.22,
        "decision_transparency": 0.22 if "mandatory" in text.lower() else 0.85,
        "regulatory_presence": 0.20 if "mandatory" in text.lower() else 0.75,
    }
    ethics = evaluate_ethics(text, governance_result=scan)
    sim, report = apply_ethics_to_metrics(BASE_SIM, BASE_REPORT, ethics)
    report["ethics_diagnostics"] = ethics
    return build_local_witness_receipt(
        module="Mirror Check",
        input_text=text,
        processed_text=text,
        scan=scan,
        sim=sim,
        report=report,
        verdict="ASYLUM" if ethics["verdict"] == "ETHICALLY HIGH-RISK" else "SANCTUARY",
        risk="High" if ethics["verdict"] == "ETHICALLY HIGH-RISK" else "Low",
        protocol_label="Review Tool",
        app_version="patch-29-test",
    )


def test_patch_29_receipt_preserves_hard_contextual_capture_trace():
    receipt = _receipt_for(HARD_CAPTURE_TEXT)
    ethics = receipt["ethics_diagnostics"]
    trace = ethics["hard_capture_trace"]

    assert ethics["hard_contextual_capture"] is True
    assert ethics["hard_contextual_capture_count"] == 1
    assert ethics["max_contextual_capture_multiplier"] > 1.0
    assert trace["hard_contextual_capture"] is True
    assert trace["hard_contextual_capture_count"] == 1
    assert trace["max_contextual_capture_multiplier"] == ethics["max_contextual_capture_multiplier"]
    assert "biometric" in trace["hard_capture_terms"] or "access to food" in trace["hard_capture_terms"]
    assert "mandatory digital id" in trace["multiplier_terms"] or "no appeal" in trace["multiplier_terms"]
    assert "mirror, not enforcement authority" in trace["review_note"]


def test_patch_29_audit_hash_includes_hard_capture_trace_fields():
    hard_receipt = _receipt_for(HARD_CAPTURE_TEXT)
    safe_receipt = _receipt_for(SAFE_TEXT)

    assert hard_receipt["hashes"]["audit_receipt_sha256"] != safe_receipt["hashes"]["audit_receipt_sha256"]
    assert hard_receipt["ethics_diagnostics"]["hard_contextual_capture"] is True
    assert safe_receipt["ethics_diagnostics"].get("hard_contextual_capture") is False
    assert hard_receipt["dataflow"] == "Power -> Mirror. Never Mirror -> Power."
    assert "public" not in hard_receipt["recovery_note"].lower()


def test_patch_29_rendered_receipt_shows_multiplier_and_terms():
    receipt = _receipt_for(HARD_CAPTURE_TEXT)
    text = render_local_witness_receipt_text(receipt)

    assert "HARD CAPTURE TRACE" in text
    assert "Hard contextual capture: True" in text
    assert "Max capture multiplier:" in text
    assert "Hard capture terms:" in text
    assert "Power terms:" in text
    assert "Mirror -> Power" in text


def test_patch_29_safe_public_health_language_records_no_hard_trace():
    receipt = _receipt_for(SAFE_TEXT)
    trace = receipt["ethics_diagnostics"]["hard_capture_trace"]

    assert receipt["ethics_diagnostics"]["contextual_capture_count"] == 0
    assert trace["hard_contextual_capture"] is False
    assert trace["hard_contextual_capture_count"] == 0
    assert trace["max_contextual_capture_multiplier"] == 0.0
    assert trace["hard_capture_terms"] == []
    assert "No hard contextual capture trigger" in trace["review_note"]
