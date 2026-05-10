from core.witness import (
    build_local_witness_receipt,
    canonical_json,
    render_local_witness_receipt_text,
)


def sample_payload():
    scan = {
        "power_concentration": 0.8,
        "decision_transparency": 0.2,
        "regulatory_presence": 0.3,
        "anonymity_level": 0.4,
        "capital_scale": 0.5,
        "technical_complexity": 0.6,
        "scan_mode": "local",
    }
    sim = {
        "stability": 0.42,
        "trust_index": 0.35,
        "alignment": 0.31,
        "ego": 0.76,
        "collapse_risk": True,
    }
    report = {
        "integrity": 0.28,
        "friction": 0.71,
        "collapse_probability": 0.83,
        "trust_friction": 0.68,
        "repair_questions": ["Which appeal path is missing?"],
    }
    return scan, sim, report


def test_local_witness_receipt_is_deterministic_for_same_inputs():
    scan, sim, report = sample_payload()
    a = build_local_witness_receipt(
        module="Simulation",
        input_text="President Jane Doe creates irrevocable authority with no appeal.",
        processed_text="[ACTOR] creates irrevocable authority with no appeal.",
        input_status="USER_INPUT",
        scan=scan,
        sim=sim,
        report=report,
        verdict="ASYLUM",
        risk="High",
        protocol_label="ASYLUM",
        invisibility_applied=True,
        app_version="test",
        generated_at_utc="2026-05-09T00:00:00Z",
    )
    b = build_local_witness_receipt(
        module="Simulation",
        input_text="President Jane Doe creates irrevocable authority with no appeal.",
        processed_text="[ACTOR] creates irrevocable authority with no appeal.",
        input_status="USER_INPUT",
        scan=scan,
        sim=sim,
        report=report,
        verdict="ASYLUM",
        risk="High",
        protocol_label="ASYLUM",
        invisibility_applied=True,
        app_version="test",
        generated_at_utc="2026-05-09T00:00:00Z",
    )
    assert a["hashes"] == b["hashes"]
    assert a["hashes"]["scenario_sha256"] != a["hashes"]["processed_scenario_sha256"]
    assert len(a["hashes"]["audit_receipt_sha256"]) == 64


def test_local_witness_receipt_enforces_local_only_boundary_language():
    scan, sim, report = sample_payload()
    receipt = build_local_witness_receipt(
        module="Simulation",
        input_text="A local law removes appeals.",
        processed_text="A local law removes appeals.",
        scan=scan,
        sim=sim,
        report=report,
        verdict="THRESHOLD",
        risk="Medium",
        protocol_label="THRESHOLD",
        app_version="test",
        generated_at_utc="2026-05-09T00:00:00Z",
    )
    text = render_local_witness_receipt_text(receipt)
    assert "Local user-held receipt only" in receipt["notice"]
    assert "Power -> Mirror. Never Mirror -> Power." == receipt["dataflow"]
    assert "not published" not in canonical_json(receipt).lower()  # JSON stays compact and factual; UI caption carries that wording.
    assert "ALETHEIA LOCAL WITNESS RECEIPT" in text
    assert "MACHINE-READABLE RECEIPT JSON" in text
    assert "Which appeal path is missing?" in text


def test_receipt_hash_changes_when_verdict_signal_changes():
    scan, sim, report = sample_payload()
    base = dict(
        module="Simulation",
        input_text="A proposal removes public review.",
        processed_text="A proposal removes public review.",
        scan=scan,
        sim=sim,
        report=report,
        risk="Medium",
        protocol_label="THRESHOLD",
        app_version="test",
        generated_at_utc="2026-05-09T00:00:00Z",
    )
    sanctuary = build_local_witness_receipt(verdict="SANCTUARY", **base)
    threshold = build_local_witness_receipt(verdict="THRESHOLD", **base)
    assert sanctuary["hashes"]["scenario_sha256"] == threshold["hashes"]["scenario_sha256"]
    assert sanctuary["hashes"]["audit_receipt_sha256"] != threshold["hashes"]["audit_receipt_sha256"]


def test_receipt_numbers_are_rounded_for_readable_output():
    scan = {
        "power_concentration": 0.04999999999999993,
        "decision_transparency": 0.7200000000000001,
        "regulatory_presence": 0.5399999999999999,
        "anonymity_level": 0.12000000000000001,
        "capital_scale": 0.25,
        "technical_complexity": 0.38,
        "scan_mode": "Local Scan",
    }
    sim = {
        "stability": 0.7482800000000001,
        "trust_index": 0.9701599999999999,
        "alignment": 0.94316,
        "ego": 0.08130000000000001,
        "collapse_risk": False,
    }
    report = {
        "integrity": 0.8303,
        "friction": 0.0033,
        "collapse_probability": 0.088,
        "trust_friction": 0.017,
        "repair_questions": ["Which safeguard is reviewable?"],
    }
    receipt = build_local_witness_receipt(
        module="Mirror Check",
        input_text="Local review text.",
        processed_text="Local review text.",
        scan=scan,
        sim=sim,
        report=report,
        verdict="THRESHOLD",
        risk="Medium",
        protocol_label="Needs Safeguards",
        app_version="test",
        generated_at_utc="2026-05-09T00:00:00Z",
    )
    text = render_local_witness_receipt_text(receipt)

    assert "0.7482800000000001" not in text
    assert "0.9701599999999999" not in text
    assert "0.04999999999999993" not in text
    assert "Stability: 0.7483" in text
    assert "Trust index: 0.9702" in text
    assert "Power concentration: 0.0500" in text
    assert receipt["metrics"]["stability"] == 0.7483
    assert receipt["scanner_features"]["power_concentration"] == 0.05
