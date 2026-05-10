from core.witness import build_local_witness_receipt, render_local_witness_receipt_text


def _demo_receipt():
    return build_local_witness_receipt(
        module="Mirror Check",
        input_text="This bundled sample shows a local transparency council with appeal and review.",
        processed_text="This bundled sample shows a local transparency council with appeal and review.",
        input_status="DEMO_INPUT",
        input_type="DEMO_INPUT",
        scan={"power_concentration": 0.25, "decision_transparency": 0.74, "scan_mode": "Local Scan"},
        sim={"stability": 0.79, "trust_index": 0.98, "alignment": 0.95, "ego": 0.0009, "collapse_risk": False},
        report={"integrity": 0.7451, "friction": 0.0, "collapse_probability": 0.073, "trust_friction": 0.0},
        verdict="SANCTUARY",
        risk="Low",
        protocol_label="Generic Local Scan",
        generated_at_utc="2026-05-09T15:04:50Z",
        app_version="patch-29.1-test",
    )


def test_patch_29_1_demo_input_receipt_is_visibly_marked_as_demo_mode():
    receipt = _demo_receipt()

    assert receipt["input_status"] == "DEMO_INPUT"
    assert receipt["input_type"] == "DEMO_INPUT"
    assert receipt["demo_mode"] is True
    assert "sample input" in receipt["demo_warning"].lower()
    assert "not be treated as a real scenario assessment" in receipt["demo_warning"].lower()


def test_patch_29_1_rendered_demo_receipt_shows_non_evaluative_warning():
    text = render_local_witness_receipt_text(_demo_receipt())

    assert "Input status: DEMO_INPUT" in text
    assert "Input type: DEMO_INPUT" in text
    assert "Demo mode: True" in text
    assert "Demo warning: Demo/sample input" in text
    assert "should not be treated as a real scenario assessment" in text
    assert "Power -> Mirror. Never Mirror -> Power." in text


def test_patch_29_1_regular_user_receipt_does_not_show_demo_warning():
    receipt = build_local_witness_receipt(
        module="Mirror Check",
        input_text="A real local scenario with opt-in repair review.",
        processed_text="A real local scenario with opt-in repair review.",
        input_status="USER_INPUT",
        input_type="USER_INPUT",
        report={"integrity": 0.8, "friction": 0.1, "collapse_probability": 0.1, "trust_friction": 0.1},
        verdict="SANCTUARY",
        risk="Low",
        protocol_label="Local Scan",
        generated_at_utc="2026-05-09T15:04:50Z",
    )
    text = render_local_witness_receipt_text(receipt)

    assert receipt["demo_mode"] is False
    assert receipt["demo_warning"] is None
    assert "Demo mode: True" not in text
    assert "Demo warning:" not in text


def test_patch_29_1_demo_guard_changes_audit_hash_against_regular_receipt():
    demo = _demo_receipt()
    regular = build_local_witness_receipt(
        module="Mirror Check",
        input_text="This bundled sample shows a local transparency council with appeal and review.",
        processed_text="This bundled sample shows a local transparency council with appeal and review.",
        input_status="USER_INPUT",
        input_type="USER_INPUT",
        scan={"power_concentration": 0.25, "decision_transparency": 0.74, "scan_mode": "Local Scan"},
        sim={"stability": 0.79, "trust_index": 0.98, "alignment": 0.95, "ego": 0.0009, "collapse_risk": False},
        report={"integrity": 0.7451, "friction": 0.0, "collapse_probability": 0.073, "trust_friction": 0.0},
        verdict="SANCTUARY",
        risk="Low",
        protocol_label="Generic Local Scan",
        generated_at_utc="2026-05-09T15:04:50Z",
        app_version="patch-29.1-test",
    )

    assert demo["hashes"]["audit_receipt_sha256"] != regular["hashes"]["audit_receipt_sha256"]
